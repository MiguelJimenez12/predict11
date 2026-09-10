# Decisiones técnicas y de producto

Fecha de revisión: 9 de septiembre de 2026.

## Datos

| Fuente | Coste inicial | Cobertura útil | Frecuencia / límites | Decisión |
|---|---:|---|---|---|
| football-data.org | €0 | Cinco grandes ligas + Champions | 10 llamadas/min; marcadores con retraso | Principal para datos actuales europeos |
| football-data.co.uk | €0 | CSV históricos de las cinco grandes | Actualización anunciada dos veces por semana | Principal para entrenamiento |
| footballcsv GitHub | €0, CC0 | Espejo histórico y Liga MX parcial | No garantiza actualidad | Respaldo reproducible |
| StatsBomb Open Data | €0 con condiciones | Eventos, alineaciones y xG en muestras selectas | Actualización irregular; atribución obligatoria | Fase posterior de investigación/xG |
| API-Football | Plan gratuito limitado | Liga MX y endpoints ya integrados | Temporadas gratuitas 2022–2024 en la cuenta actual | Compatibilidad Liga MX |

No existe una única fuente gratuita que entregue simultáneamente datos en vivo, xG, históricos extensos y las siete competiciones. La arquitectura por adaptadores evita acoplar el producto a un proveedor.

## Persistencia y autenticación

Supabase Free es la opción recomendada porque combina Postgres y Auth: 500 MB de base, 50,000 MAU y dos proyectos activos. Su principal limitación es la pausa tras una semana sin actividad. SQLite queda para desarrollo local; no sirve como almacenamiento persistente en Render Free.

El backend debe verificar el JWT de Supabase, localizar al usuario por `auth_subject`, bloquear su fila, refrescar créditos y descontar uno dentro de la misma transacción. Nunca debe aceptar saldo, plan o estado de suscripción enviados por el frontend.

## Créditos

- Alta: 20 créditos.
- Recarga: 3 por día transcurrido.
- Tope gratuito: 20.
- Premium activo: consumo ilimitado.
- Operación: transacción atómica con bloqueo de fila.
- Pagos futuros: webhook firmado e idempotente actualiza `subscription_status`; la pantalla de éxito no activa premium.

El modelo es técnicamente viable. Económicamente, el caché y los modelos locales hacen que el coste marginal por predicción sea casi cero; el límite protege el proveedor gratuito y permite medir intención de pago.

## Hosting

Render es la ruta más sencilla para el MVP porque admite FastAPI y sitios estáticos desde el mismo repositorio. El plan gratuito ofrece 750 horas por workspace, duerme servicios tras 15 minutos y usa disco efímero. Supabase aloja datos persistentes. Coste mensual inicial estimado: $0 MXN mientras se respeten cuotas.

Cloudflare Pages es una alternativa excelente para el frontend; sus activos estáticos son gratuitos y sus Functions comparten el límite de Workers Free. No se eligió para FastAPI porque obligaría a adaptar el backend Python a otra arquitectura.

## Dominio

La consulta RDAP oficial de Verisign confirmó que `predict11.com` está registrado. Un subdominio `onrender.com` es gratuito, pero no equivale a poseer un dominio. Los `.com` requieren registro y renovación anual.

## Pagos

| Proveedor | Cuota mensual | Tarifa pública relevante | Suscripciones | Observación |
|---|---:|---|---|---|
| Stripe México | $0 | 3.6% + MXN 3; Billing 0.7% | Sí | Recomendado por API, sandbox y coste local |
| PayPal México | $0 | 3.95% + tarifa fija | Sí | Reconocido, algo más caro |
| Mercado Pago | $0 para integrar | Depende de plazo y medio | Sí | Buena alternativa local |
| Paddle | $0 | 5% + USD 0.50 | Sí | Merchant of record; impuestos incluidos |
| Lemon Squeezy | $0 | 5% + USD 0.50 | Sí | Merchant of record; impuestos incluidos |

No se implementaron pagos. La integración debe comenzar sólo en sandbox y guardar secretos en el proveedor de hosting.

## Fuentes verificadas

- https://www.football-data.org/pricing
- https://www.football-data.org/coverage
- https://docs.football-data.org/general/v4/policies.html
- https://www.football-data.co.uk/data.php
- https://github.com/footballcsv/cache.footballdata
- https://github.com/hudl/open-data
- https://render.com/docs/free
- https://render.com/docs/static-sites
- https://supabase.com/pricing
- https://stripe.com/mx/pricing
- https://www.paypal.com/mx/business/paypal-business-fees
- https://www.paddle.com/pricing
- https://www.lemonsqueezy.com/pricing
- https://www.namecheap.com/domains/registration/gtld/com/
