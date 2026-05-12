# -*- coding: utf-8 -*-
from odoo import models
from odoo.exceptions import UserError
from odoo.tools.translate import _

class AccountMove(models.Model):
    _inherit = 'account.move'

    def _post(self, soft=True):
        """
        Intercepts the posting process to inject withholding taxes 
        dynamically based on the partner's fiscal profile.
        We apply batch processing to guarantee $O(1)$ DB queries per batch.
        """
        # 1. Filter out non-invoices or invoices without a partner fiscal profile
        invoices = self.filtered(lambda m: m.is_invoice() and m.partner_id.fiscal_profile_id)
        
        if invoices:
            # 2. Extract unique profiles and companies
            profile_ids = invoices.mapped('partner_id.fiscal_profile_id').ids
            company_ids = invoices.mapped('company_id').ids
            
            # 3. Fetch rules in a single query
            rules = self.env['account.withholding.rule'].search([
                ('profile_id', 'in', profile_ids),
                ('company_id', 'in', company_ids)
            ])
            
            # 4. Map rules in memory: {(profile_id, company_id): recordset(account.tax)}
            rule_map = {(r.profile_id.id, r.company_id.id): r.tax_ids for r in rules}
            
            for invoice in invoices:
                profile = invoice.partner_id.fiscal_profile_id
                taxes_to_apply = rule_map.get((profile.id, invoice.company_id.id))
                
                if taxes_to_apply is None:
                    # Fail-fast mechanism: Prevent posting if configuration is missing
                    raise UserError(_(
                        "The partner %(partner)s has a fiscal profile '%(profile)s' but there is no withholding rule configured for company %(company)s.",
                        partner=invoice.partner_id.name,
                        profile=profile.name,
                        company=invoice.company_id.name
                    ))
                
                if taxes_to_apply:
                    for line in invoice.invoice_line_ids.filtered(lambda l: l.display_type == 'product'):
                        # Apply set difference to avoid duplicating existing taxes
                        new_taxes = taxes_to_apply - line.tax_ids
                        if new_taxes:
                            # Use Odoo's Command syntax (4 = link)
                            line.tax_ids = [(4, tax.id) for tax in new_taxes]

        # 5. Delegate to super() to finalize the accounting entries with the new taxes
        return super()._post(soft)
