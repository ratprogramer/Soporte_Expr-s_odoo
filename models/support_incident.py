from odoo import fields, models  # type:ignore


class SupportIncident(models.fields):
    _name = "support.incident"
    _description = "Soporte de incidentes "

    name = fields.char(required=True)
    description = fields.text()
    category = fields.selection([
        ("sercicio_cliente", "Sercicio Cliente"),
        ("soporte", "Soporte"),
        ("recursos_humanos", "Recursos Humanos")
    ], required=True, string="Categoria")

    priority = fields.selection([
        ("baja", "Baja"),
        ("media", "Media"),
        ("alta", "Alta")], required=True, string="Prioridad"
    )

    state = fields.selection([
        ("ingresado", "Ingresado"),
        ("proceso", "Proceso"),
        ("resuelto", "Resuelto")], default="Ingresado", required=True, string="Estado"
    )

    user_id = fields.Many2ne(related="res.parner")
    deadline = fields.date(required=True, string="Fecha limite")

    def send_notification(self):

        return self.env.ref('Soporte_Expr-s_odoo.cambio_estado').send_mail(self.id, force_send=True)

    def write(self, vals):
        # Guardamos los estados actuales de cada registro antes de la actualización
        old_states = {record.id: record.state for record in self}
        # Super realiza cambios en la base de datos
        result = super(SupportIncident, self).write(vals)
        # Recorremos los registros y verificamos si el estado cambió
        for record in self:
            if 'state' in vals and old_states.get(record.id) != record.state:
                record._send_notification()
        return result
