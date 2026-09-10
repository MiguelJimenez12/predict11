# Predict11

Predict11 es una aplicación full-stack de análisis y predicción de fútbol. Combina datos actuales de competiciones con modelos entrenados sobre resultados históricos para estimar las probabilidades de victoria local, empate y victoria visitante.

> Las predicciones son estimaciones estadísticas para fines educativos. No garantizan resultados ni constituyen recomendaciones de apuestas.

## Características

- Siete competiciones configuradas mediante identificadores internos estables.
- Catálogo de equipos, calendario y resultados a través de proveedores intercambiables.
- Clasificador multiclase entrenado y evaluado cronológicamente.
- Features de Elo, últimos cinco partidos, goles recientes y rendimiento local/visitante.
- Métricas por liga: accuracy, log loss, Brier score, precision, recall y matriz de confusión.
- Interfaz React responsive con selector de liga y probabilidades explicadas.
- Caché de cinco minutos para respetar el límite del proveedor gratuito.
- Base para autenticación, créditos diarios y suscripciones futuras.
- Despliegue reproducible en Render y validación continua con GitHub Actions.

## Ligas soportadas

| Identificador | Competición | Datos actuales | Modelo histórico |
|---|---|---|---|
| `premier-league` | Premier League | football-data.org | Sí |
| `la-liga` | LaLiga | football-data.org | Sí |
| `serie-a` | Serie A | football-data.org | Sí |
| `bundesliga` | Bundesliga | football-data.org | Sí |
| `ligue-1` | Ligue 1 | football-data.org | Sí |
| `champions-league` | UEFA Champions League | football-data.org | Pendiente de histórico homogéneo |
| `liga-mx` | Liga MX | API-Football | Heurística estadística existente |

## Fuentes de datos

La fuente principal de fixtures, resultados y tablas europeas es [football-data.org](https://www.football-data.org/coverage). Su plan gratuito ofrece 12 competiciones y 10 solicitudes por minuto. Los modelos usan CSV de [Football-Data](https://www.football-data.co.uk/data.php) y su [espejo CC0 en GitHub](https://github.com/footballcsv/cache.footballdata). Liga MX conserva el adaptador de API-Football.

[StatsBomb Open Data](https://github.com/hudl/open-data) se evaluó para una fase posterior de xG y eventos. No es la fuente principal porque su cobertura abierta es selectiva e irregular y requiere atribución específica.

## Modelo predictivo

Cada liga histórica utiliza una regresión logística multinomial ligera implementada en Python. Antes de cada partido calcula exclusivamente información disponible hasta esa fecha:

1. diferencia Elo;
2. puntos de los últimos cinco partidos;
3. goles anotados y recibidos recientemente;
4. diferencia de goles del local en casa;
5. diferencia de goles del visitante fuera.

Los datos se ordenan por fecha. El 80% inicial se usa para entrenamiento y el 20% final para prueba, evitando mezclar partidos futuros en las features. Los artefactos versionados viven en `ml_models/`.

### Evaluación actual

| Liga | Partidos | Accuracy | Log loss |
|---|---:|---:|---:|
| Premier League | 1,900 | 54.74% | 0.9489 |
| LaLiga | 1,900 | 52.11% | 0.9716 |
| Serie A | 1,900 | 53.95% | 0.9863 |
| Bundesliga | 1,530 | 49.67% | 0.9627 |
| Ligue 1 | 1,725 | 46.38% | 1.0561 |

El empate sigue siendo la clase más difícil y con menor recall. Las métricas completas están disponibles en `GET /predictions/models/{league}/metrics`; no deben interpretarse como rentabilidad o certeza.

## Arquitectura

```text
React + Vite
      |
      v
FastAPI (routers / services / schemas)
      |----------------------|
      v                      v
Proveedores actuales     Modelos históricos JSON
      |
      v
PostgreSQL / Supabase Auth (usuarios y créditos)
```

## Instalación

Requisitos: Python 3.11+, Node.js 20+ y Git.

```powershell
git clone https://github.com/MiguelJimenez12/predict11.git
cd predict11\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item ..\.env.example .\.env
```

Edita `backend/.env` y configura al menos una fuente:

```dotenv
FOOTBALL_DATA_TOKEN=token_gratuito_de_football_data_org
FOOTBALL_API_KEY=clave_de_api_football_para_liga_mx
DATABASE_URL=postgresql://usuario:password@host:5432/predict11
ALLOWED_ORIGINS=http://localhost:5173
```

Nunca confirmes `.env` en Git.

## Ejecución local

Terminal 1:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

Terminal 2:

```powershell
cd frontend
npm install
npm run dev
```

- Aplicación: `http://localhost:5173`
- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`

## Endpoints principales

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/health` | Estado del backend |
| GET | `/leagues/` | Ligas configuradas |
| GET | `/leagues/{slug}/teams` | Equipos por liga |
| GET | `/leagues/{slug}/matches` | Partidos, con filtros de fecha/estado |
| GET | `/leagues/{slug}/standings` | Clasificación normalizada por liga |
| GET | `/matches/upcoming?league={slug}` | Próximos partidos |
| POST | `/predictions/` | Predicción ML europea por nombres de equipo |
| GET | `/predictions/{league}/{match_id}` | Predicción para un partido del proveedor |
| GET | `/predictions/models/{league}/metrics` | Evaluación histórica |
| POST | `/predict/` | Predicción Liga MX compatible con v1 |
| GET | `/teams/`, `/matches/`, `/standings/`, `/statistics/` | Endpoints heredados de Liga MX |

## Entrenamiento y actualización

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python scripts\train_models.py
```

El workflow `Update prediction models` se ejecuta semanalmente y también puede lanzarse manualmente desde GitHub Actions. Sólo confirma nuevos artefactos cuando los datos cambian.

## Usuarios, créditos y premium

La migración más reciente prepara estos campos en el backend:

- 20 créditos iniciales;
- recuperación de 3 créditos diarios;
- máximo gratuito de 20;
- tipo y estado de suscripción;
- identificador externo de autenticación.

La recarga y el descuento se calculan bajo bloqueo de fila en el backend. El frontend nunca decide el saldo. Los usuarios premium activos no consumen créditos.

La recomendación es usar [Supabase Auth y Postgres Free](https://supabase.com/pricing): incluye 50,000 usuarios activos mensuales y 500 MB de base de datos, aunque pausa proyectos tras una semana de inactividad. La ruta pública de predicción seguirá sin consumir créditos hasta conectar y verificar JWT de un proyecto Supabase real; no se simula autenticación insegura.

## Despliegue a $0 MXN/mes

El archivo `render.yaml` define:

- backend FastAPI como Render Free Web Service;
- frontend React como Render Static Site gratuito;
- secretos configurados únicamente en el panel de Render.

Render proporciona subdominios `onrender.com`, TLS y sitios estáticos gratuitos. El backend gratuito se duerme tras 15 minutos sin tráfico y puede tardar aproximadamente un minuto en despertar. Su disco es efímero, por lo que producción debe usar Supabase Postgres, no SQLite local. Consulta las [limitaciones oficiales de Render Free](https://render.com/docs/free).

## Dominio

`predict11.com` aparece registrado en RDAP de Verisign al 9 de septiembre de 2026 y no está disponible para registro normal. No se compró ningún dominio. El proyecto puede salir sin coste como `predict11-web.onrender.com`; otra opción es un nombre disponible como `predict11app.com` o un subdominio de un dominio que ya poseas.

Un `.com` no es gratuito: como referencia, Namecheap mostraba USD 10.98 de registro y USD 18.48 de renovación, más la tarifa ICANN, al consultar en septiembre de 2026. Render permite conectar dominios propios y administra TLS, pero no regala la propiedad del dominio.

## Monetización futura

No hay pagos reales ni claves privadas en el repositorio. Para México, la primera opción recomendada es Stripe Checkout/Billing en modo de prueba: no tiene mensualidad; la tarifa publicada para tarjetas nacionales es 3.6% + MXN 3 por transacción y Billing añade 0.7% del volumen. Mercado Pago es una alternativa local con suscripciones; PayPal publica 3.95% + tarifa fija para transacciones nacionales.

Paddle y Lemon Squeezy cobran 5% + USD 0.50 y actúan como merchant of record, incluyendo gestión fiscal internacional; resultan más simples para vender globalmente, pero el componente fijo es alto para una suscripción económica. Véase [Stripe México](https://stripe.com/mx/pricing), [PayPal México](https://www.paypal.com/mx/business/paypal-business-fees), [Paddle](https://www.paddle.com/pricing) y [Lemon Squeezy](https://www.lemonsqueezy.com/pricing).

Precio inicial sugerido para validar demanda: MXN 79–99 al mes. Primero deben medirse uso, coste por predicción y retención; no se debe activar el cobro hasta implementar JWT, webhooks idempotentes y una política legal/fiscal apropiada.

## Pruebas

```powershell
cd backend
python -m unittest discover -s tests -v

cd ..\frontend
npm run lint
npm run build
```

GitHub Actions ejecuta estas verificaciones en cada push y pull request.

## Estructura

```text
backend/
  app/
    config/       catálogo de ligas
    ml/           entrenamiento y predicción pura
    models/       entidades SQLAlchemy
    routers/      endpoints FastAPI
    schemas/      contratos Pydantic
    services/     proveedores y reglas de negocio
  scripts/        entrenamiento reproducible
  tests/
frontend/         React + Vite
ml_models/        artefactos y métricas versionados
.github/workflows/
render.yaml
```

## Autor

Miguel Ángel Jiménez Ramírez — [GitHub](https://github.com/MiguelJimenez12)
