# Account Payment Alerts

Este módulo extiende la funcionalidad de contabilidad de Odoo 18, proporcionando un tablero Kanban y un motor de reglas para identificar facturas de clientes con alto riesgo de atraso en el cobro.

## Características Principales

- **Motor de Reglas Dinámico:** Permite crear múltiples perfiles de riesgo (`account.collection.alert.rule`) basados en una matriz de "Días de Atraso" (Days Overdue) y "Monto Mínimo Pendiente" (Minimum Amount).
- **Jerarquía de Riesgos:** Clasifica automáticamente las facturas en nivel de riesgo Alto, Medio o Bajo. Si una factura cumple con múltiples reglas, el sistema es lo suficientemente inteligente para asignar y preservar el nivel de riesgo más alto.
- **Dashboard Kanban:** Un tablero integrado bajo `Contabilidad > Clientes > Payment Alerts`, pre-agrupado por nivel de riesgo, permitiendo a los gestores de cobranza atacar visualmente la deuda más crítica.

## Arquitectura y Rendimiento (Technical Notes)

A diferencia de aproximaciones estándar (donde los desarrolladores suelen usar campos computados `compute` al vuelo, destruyendo el rendimiento del servidor), este módulo está diseñado bajo el patrón de **Batch Processing**.

El campo `risk_level` está almacenado de forma nativa en la tabla `account_move`. Las reglas no se evalúan cada vez que el usuario abre la pantalla; en su lugar, existe un Cron Job (Acción Planificada) llamado _Account: Evaluate Collection Risks_ que se ejecuta diariamente en segundo plano. Este método utiliza búsquedas nativas del ORM (`search` con operadores lógicos matemáticos) y actualizaciones masivas (`write`), garantizando **Cero N+1 Queries**, de forma que el módulo escala perfectamente independientemente de si tienes 100 facturas o 1 millón en tu base de datos.
