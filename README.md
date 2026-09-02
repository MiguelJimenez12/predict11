# Predict11

Aplicación full-stack que analiza estadísticas de Liga MX y genera probabilidades de victoria, empate y derrota con una explicación legible.

## MVP terminado

- Catálogo de equipos, partidos, tabla, estadísticas e historial directo desde API-Football.
- Predicción con probabilidades normalizadas, marcador estimado y nivel de confianza.
- Interfaz React adaptable a móvil y escritorio.
- API documentada automáticamente con FastAPI.
- PostgreSQL, SQLAlchemy y migraciones Alembic preparadas para persistencia futura.

## Ejecutar en local

Requisitos: Python 3.11 o superior, Node.js 20 o superior y una clave de [API-Football](https://www.api-football.com/).

### Backend

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item ..\.env.example .\.env
# Agrega tu FOOTBALL_API_KEY en .env
uvicorn app.main:app --reload
```

La API queda en `http://localhost:8000` y su documentación en `http://localhost:8000/docs`.

### Frontend

En otra terminal:

```powershell
cd frontend
npm install
npm run dev
```

Abre `http://localhost:5173`.

## Cómo funciona la predicción

El modelo heurístico combina puntos por partido, diferencia de goles, porterías en cero, ventaja de local e historial entre los equipos. Una función logística transforma la diferencia de fuerza en probabilidades válidas que suman 100%. Es una estimación demostrativa y no una recomendación de apuestas.

## Arquitectura

```text
React + Vite  →  FastAPI  →  API-Football
                       ↘  motor de predicción
                        ↘ PostgreSQL / Alembic
```

## Verificación

```powershell
cd backend
python -m unittest discover -s tests -v

cd ..\frontend
npm run lint
npm run build
```

## Autor

Miguel Ángel Jiménez Ramírez — [GitHub](https://github.com/MiguelJimenez12)
