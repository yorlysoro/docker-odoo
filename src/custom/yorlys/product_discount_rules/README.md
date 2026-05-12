# Product Discount Rules - POS 🕰️🏷️

## Descripción General

Este módulo implementa un sistema automatizado de "Happy Hour" para el Punto de Venta de Odoo. Permite a los administradores definir franjas horarias exactas durante las cuales se aplicará un porcentaje de descuento automático a las líneas de la orden, eliminando la necesidad de cálculos manuales por parte del cajero.

## Arquitectura y Lógica de Negocio

El módulo ha sido desarrollado bajo los estrictos estándares de rendimiento de Odoo.

1. **Frontend Reactivo (OWL):** En lugar de forzar recálculos pesados en el backend, la validación de tiempo se inyecta en el flujo de la aplicación POS. Cuando el cajero procede a seleccionar un producto, el sistema evalúa la hora local del navegador y aplica la regla activa correspondiente instantáneamente a cada producto, y deja una nota en cada producto con el nombre del descuento aplicado.
2. **Backend Sanity Checks:** El modelo `pos.order` contiene un método interceptor en la creación (`create`) que realiza un _Batch Processing_ para verificar que los descuentos enviados desde el cliente POS no violen las reglas configuradas.
3. **Restricción de Solapamientos:** La base de datos está protegida mediante `api.constrains` que utilizan búsquedas O(1) para garantizar que dos reglas activas jamás choquen en tiempo.

## Configuración y Uso

1. Ve al menú **Punto de Venta > Configuración > Reglas de Descuento**.
2. Crea una nueva regla, por ejemplo: "Desayuno Express".
3. Define la hora de inicio (ej. `07:00`), la hora de fin (ej. `09:30`), y el porcentaje de descuento (ej. `15%`).
4. Abre una nueva sesión del POS. Si realizas una venta dentro de esa franja horaria, el descuento se aplicará automáticamente al proceder al pago.
