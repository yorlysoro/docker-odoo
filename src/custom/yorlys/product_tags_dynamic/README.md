# Product Tags Dynamic

Este módulo extiende la funcionalidad de inventario de Odoo 18, permitiendo clasificar productos mediante etiquetas logísticas y operativas (`stock.operation.tag`).

## Características

- **Modelo Independiente:** Separa las etiquetas comerciales (eCommerce/Ventas) de las operativas (Almacén).
- **Tipos de Operación:** Permite categorizar la etiqueta por tipo de movimiento (Recepción, Entrega, Transferencia Interna, Fabricación).
- **Optimización Visual:** Integración limpia en las vistas Kanban usando `many2many_tags` con índices de color nativos, permitiendo agrupar y visualizar propiedades críticas (ej. _Frágil_, _Cadena de Frío_) de un vistazo.
- **Acción Rápida:** Posibilidad de asignar de forma masiva desde la vista de lista (`<list>`) gracias a la estructura nativa de edición de Odoo 18, apoyado por una acción de servidor.

## Arquitectura y Rendimiento

Se ha diseñado el módulo minimizando llamadas a la base de datos (N+1 queries) apoyándonos en el método `read_group` del ORM en lugar de búsquedas iterativas para agrupar campos `Many2many`. Se implementó TDD para asegurar la robustez de las relaciones entre `product.template` y el nuevo modelo.

## Configuración

1. **Crear Etiquetas Operativas:**
   Vaya a `Inventario -> Configuración -> Etiquetas Operativas`.
   - Cree etiquetas como "Frágil", "Cadena de Frío", etc.
   - **Importante:** Seleccione el "Tipo de Operación" correspondiente (Recepción, Entrega, etc.). Esto determina en qué flujos de trabajo se usarán.

2. **Asignar Etiquetas a Productos:**
   - Vaya a `Inventario -> Productos`.
   - Abra un producto y busque el campo Etiquetas Operativas en la vista de formulario.
   - Asigne las etiquetas correspondientes.
