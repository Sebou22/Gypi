# -*- encoding: utf-8 -*-

from odoo import models,fields, api,tools
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    id_fisc = fields.Char(string=u'IF (Identifiant Fiscal)')
    rc = fields.Char(string=u'RC (Registre de Commerce)')
    cnss = fields.Char(string=u'Numéro de la sécurité sociale')
    capital_social = fields.Char(string=u'Capital social')
    ice = fields.Char(string=u'ICE (Identifiant Commun d Entreprise)')
    itp = fields.Char(string=u'ITP (Identifiant Taxe Professionnelle)')
    activites = fields.Char(string=u"Profession ou activités exercées")
    # nationalite = fields.Char(string=u"Nationalité")
    # fax = fields.Char(string=u"Fax")

    @api.constrains('ice')
    def _check_ice(self):
        for rec in self:
            if rec.ice and (len(rec.ice) != 15 or not rec.ice.isdigit()):
                    raise ValidationError(u"L'ICE doit être constitué de 15 chiffres")

