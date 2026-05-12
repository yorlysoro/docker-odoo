# Account Withholdings Partner 📉

## Descripción

Módulo contable para automatizar la aplicación de impuestos de retención en facturas de clientes o proveedores basándose en "Perfiles Fiscales" asignados. Evita el trabajo manual y asegura que las normativas fiscales se apliquen en el momento exacto de la validación del documento.

## Arquitectura

Este módulo intercepta el método `_post()` de `account.move`. Aplica un patrón de **Batch Processing** (procesamiento por lotes) para garantizar que la recolección de las reglas fiscales y la asignación de impuestos se realicen sin caer en consultas SQL redundantes (N+1 queries).

## Configuración y Uso

1. Navega a **Contabilidad > Configuración > Perfiles Fiscales** y crea los perfiles necesarios (Ej. Agente de Retención, Contribuyente Especial, Exento).
2. Ve a **Contabilidad > Configuración > Reglas de Retención** y mapea cada perfil a sus respectivos impuestos de retención (generalmente impuestos con porcentaje negativo en Odoo) por compañía.
3. Asigna el Perfil Fiscal a tus clientes/proveedores en su ficha `res.partner`.
4. Al generar una factura, no es necesario agregar la retención manualmente. Al hacer clic en **Confirmar**, el sistema inyectará la línea de impuesto de manera silenciosa y recalculará los totales antes de generar el apunte contable.

## Manejo de Errores (Fail-Fast)

Si un contacto posee un Perfil Fiscal pero el sistema no encuentra una Regla de Retención en la compañía emisora, se detendrá el proceso de validación arrojando un error en pantalla. Esto fuerza una configuración contable íntegra y evita evasiones de lógica de negocio.
