# Stock Priority Replenishment 📦

## Descripción

Este módulo ha sido diseñado bajo estándares de arquitectura avanzada de Odoo. Su propósito es automatizar la gestión de inventarios críticos, identificando cuándo un producto cae por debajo de su umbral de "Stock Objetivo" y generando proactivamente notificaciones (`mail.activity`) a los responsables de almacén.

## Funcionalidades Principales

- **Priorización de Productos:** Agrega un nivel de criticidad (Baja, Media, Alta) en la ficha del producto.
- **Control de Stock Objetivo:** Define el umbral mínimo deseado en almacén.
- **Acción Automatizada (Cron Job):** Evalúa eficientemente grandes volúmenes de datos usando _Batch Processing_ y genera actividades si el inventario actual (`qty_available`) es menor al esperado.
- **Prevención de Duplicidad:** Verifica la existencia de actividades previas (estado _To-do_) para evitar inundar a los encargados con notificaciones redundantes.
- **Vista de Tablero Dedicada:** Lista los productos con necesidad de reabastecimiento priorizados mediante colores y pre-agrupados por criticidad en el menú de inventario.

## Notas de Arquitectura

- Se ha utilizado un campo `needs_replenishment` indexable por el Cron para evitar que las vistas de lista tengan que calcular `qty_available` _On-the-fly_ para miles de productos, previniendo caídas del rendimiento y consultas recursivas a la base de datos PostgreSQL.
- Validado bajo TDD (Test Driven Development) para garantizar la integridad.

## Uso

1. Instalar el módulo `stock_priority`.
2. Ir a **Inventario > Productos > Productos** y definir _Target Stock_ y _Replenishment Priority_.
3. Esperar la ejecución del cron "Inventory: Evaluate Stock Priorities" o ejecutarlo manualmente desde Ajustes > Técnico.
4. Revisar la bandeja de actividades y el nuevo menú **Inventario > Operaciones > Reabastecimientos Pendientes**.
