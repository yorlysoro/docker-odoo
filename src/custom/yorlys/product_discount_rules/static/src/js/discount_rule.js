/** @odoo-module */
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";

patch(PosStore.prototype, {
    
    async addLineToCurrentOrder(vals, options) {
        // 1. Ejecución nativa para agregar el producto a la orden
        await super.addLineToCurrentOrder(...arguments);

        const order = this.get_order();
        if (!order) return;

        const selectedLine = order.get_selected_orderline();
        if (!selectedLine) return;

        // 2. LLAMADA RPC (Búsqueda directa a la base de datos)
        // Usamos una caché (this._discountRulesCache) para no saturar el servidor en cada escaneo
        if (!this._discountRulesCache) {
            try {
                // this.env.services.orm es el puente oficial en Odoo 18 para llamadas asíncronas
                this._discountRulesCache = await this.env.services.orm.searchRead(
                    'pos.discount.rule',
                    [['active', '=', true]],
                    ['name', 'hour_from', 'hour_to', 'discount_percentage']
                );
                console.log("📡 [RPC EXITO] Reglas descargadas directamente de la DB:", this._discountRulesCache);
            } catch (error) {
                console.error("🔴 [RPC ERROR] Falló la conexión con el servidor al buscar reglas:", error);
                this._discountRulesCache = []; // Evitamos que el POS crashee si no hay red
            }
        }

        const rules = this._discountRulesCache;
        const now = new Date();
        const currentHour = now.getHours() + (now.getMinutes() / 60.0);

        // 3. Filtrado de las reglas activas
        const activeRules = rules.filter(rule => {
            const from = parseFloat(rule.hour_from);
            const to = parseFloat(rule.hour_to);
            return currentHour >= from && currentHour < to;
        });

        // 4. Lógica de asignación (Multiregla)
        if (activeRules.length > 0) {
            const totalDiscount = activeRules.reduce((sum, r) => sum + r.discount_percentage, 0);
            const ruleNames = activeRules.map(r => r.name).join(' + ');
            
            const finalDiscount = Math.min(totalDiscount, 100); // Límite de seguridad
            
            if (selectedLine.get_discount() !== finalDiscount) {
                selectedLine.set_discount(finalDiscount);
                selectedLine.set_customer_note(`🏷️ Descuento agregados: ${ruleNames}`);
            }
        } else {
            // Limpieza si no aplican reglas
            selectedLine.set_discount(0);
            selectedLine.set_customer_note('');
        }
    }
});