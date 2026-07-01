**PROJECT ARGUS**

Sistema de monitoreo de seguridad en tiempo real, compuesto por dos componentes: ArgusCore, la consola que detecta y registra eventos de amenazas, y Argus Dashboard, la interfaz web que visualiza esos eventos (fuerza bruta, escaneo de puertos, abuso de API, escalación de privilegios, logins multi-IP y flood de tickets) con métricas en vivo, gráfico de volumen de amenazas y un registro de eventos recientes.

Versión actual: 1.1.0

--------------------------------------------------------------------------------------------------

**Características**

Tarjetas de métricas por tipo de amenaza, con severidad codificada por color (crítica, alta, media, baja) y porcentaje sobre el total.
Gráfico de volumen en tiempo real (área/montaña) que se actualiza cada 2 segundos consultando la API interna.
Tabla de eventos recientes con hora, fuente, IP, tipo de evento y severidad.
Panel de estado con versión del sistema, estado de conexión, cantidad de detectores activos y alertas activas.
7 detectores activos monitoreando distintos vectores de ataque.


**ArgusCore (Backend/API)**


Consola de detección y registro de eventos de seguridad. Escribe los eventos detectados en la tabla logs.


**Argus Dashboard (Front-end)**


Django — framework principal, vistas y enrutamiento.
PostgreSQL — base de datos compartida entre ArgusCore y Argus Dashboard.
HTML5 + CSS3 (sin framework de estilos, diseño custom).
JavaScript vanilla (fetch API, manipulación de DOM).
Chart.js — gráfico de volumen de amenazas en tiempo real.
chartjs-plugin-datalabels — soporte de etiquetas en el gráfico.
Tipografías Share Tech Mono y Rajdhani (Google Fonts).


## Arquitectura de Argus

```text
┌──────────────────┐
│  ArgusCore       │
│   (Consola)      │
└────────┬─────────┘
         │
         │ Escribe eventos
         ▼
┌──────────────────┐
│ PostgreSQL       │
│ Tabla: logs      │
└────────┬─────────┘
         │
         │ Consultas ORM
         ▼
┌──────────────────┐
│ Django API       │
│ /api/metrics/    │
└────────┬─────────┘
         │
         │ Fetch cada 2s
         ▼
┌──────────────────┐
│ Argus Dashboard  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   SOC Analyst    │
└──────────────────┘
```
ArgusCore (la consola) detecta y registra los eventos de seguridad directamente en la tabla logs. La vista metrics_api consulta esa misma tabla, calcula contadores por tipo de evento, arma los últimos 5 eventos para la tabla de "Recent Events" y devuelve todo como JSON. El frontend de Argus Dashboard consume ese JSON cada 2 segundos para refrescar tarjetas, gráfico y tabla sin recargar la página.

Endpoints (Argus Dashboard)

RutaDescripción/Renderiza el dashboard (dashboard.html)./api/metrics/Devuelve métricas en tiempo real en formato JSON: volumen reciente, contadores por tipo de amenaza y últimos eventos.

## Notas de la versión 1.1.0

- Corregida la duplicación de leyendas en el gráfico de amenazas.
- Corregido el gráfico de volumen que se mostraba plano en 0 (desajuste de zona horaria entre los timestamps de la tabla `logs` y las consultas de Django).
- Ampliada la ventana de cálculo de "volumen reciente" para reflejar mejor la actividad real.
- Corregido el campo de IP en la tabla de eventos recientes.
- Agregados valores visibles de versión (`1.1.0`) y cantidad de detectores activos (`7`) en el panel de estado.

Detalle técnico completo de estos cambios en [`FIXES.md`](./FIXES.md).

## Roadmap / posibles mejoras futuras

- Persistencia de configuración del dashboard (versión, detectores) en base de datos en lugar de valores por defecto en el template.
- Autenticación para el acceso al dashboard.
- Exportación de eventos a CSV/PDF.
- Alertas configurables por umbral de severidad.
