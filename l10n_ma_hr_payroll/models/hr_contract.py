from odoo import fields, models, api


class HrContract(models.Model):
    _inherit = 'hr.contract'

    # "Important: Les indemnités qui dépassent le plafond admis en exoneration remplissent automatiquement les champs des Indemnité taxable avec le reste supérieur"
    int1 = fields.Float(digits='Account', string="Indemnité de Transport")
    indm_transport_select = fields.Selection([
        ('urban', '500 DH (Pérmiètre urbain)'),
        ('not_urban', '750 DH (Dehors périmètre urbain)'),
        ('other', 'Autre..'), ], string="Conditions/Plafond Transport", default='other')

    int2 = fields.Float(digits='Account', string="Indemnité de Panier")
    indm_panier_select = fields.Selection([
        ('x2_smig', 'Deux fois le SMIG Horaire'),
        ('other', 'Autre..')], string="Conditions/Plafond Panier", default='other')

    int3 = fields.Float(digits='Account', string="Indemnité de Représentation")
    int4 = fields.Float(digits='Account', string="Indemnité Non taxable 4")
    int5 = fields.Float(digits='Account', string="Indemnité Non taxable 5")

    it1 = fields.Float(digits='Account', string="Indemnité Transport Taxable", compute='get_taxed_transport', )
    it2 = fields.Float(digits='Account', string="Indemnité Panier Taxable", compute='get_taxed_panier', )
    it3 = fields.Float(digits='Account', string="Indemnité Représentation Taxable",
                       compute='get_taxed_representation', )
    it4 = fields.Float(digits='Account', string="Indemnité taxable 4")
    it5 = fields.Float(digits='Account', string="Indemnité taxable 5")

    @api.onchange('indm_transport_select')
    def onchange_indm_transport_select(self):
        for rec in self:
            if rec.indm_transport_select == 'urban':
                rec.int1 = 500
            elif rec.indm_transport_select == 'not_urban':
                rec.int1 = 750

    @api.depends('indm_transport_select', 'int1')
    def get_taxed_transport(self):
        for rec in self:
            if rec.int1 and rec.indm_transport_select == 'other':
                result = rec.int1 - 500
                if result > 0:
                    rec.it1 = result
                else:
                    rec.it1 = 0
            else:
                rec.it1 = 0

    @api.depends('int3')
    def get_taxed_representation(self):
        for rec in self:
            if rec.int3 and rec.int3 > rec.wage * 0.10:
                rec.it3 = rec.int3 - (rec.wage * 0.10)
            else:
                rec.it3 = 0

    @api.depends('int2')
    def get_taxed_panier(self):
        for rec in self:
            if rec.int2 and rec.int2 > ((15.55 * 2) * 26):
                rec.it2 = rec.int2 - ((15.55 * 2) * 26)
            else:
                rec.it2 = 0



