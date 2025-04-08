from odoo import fields, models  # type:ignore


class SupportIncident(models.Model):
    _name = "support.incident"
    _description = "Soporte de incidentes "
    _inherit = ['mail.thread', 'mail.activity.mixin']  # <-- integración aquí

    name = fields.Char(required=True)
    description = fields.Text()
    category = fields.Selection([
        ("servicio_cliente", "Servicio Cliente"),
        ("soporte", "Soporte"),
        ("recursos_humanos", "Recursos Humanos")
    ], required=True, string="Categoria")
    email = fields.Text(string="Email", required=True)
    priority = fields.Selection([
        ("baja", "Baja"),
        ("media", "Media"),
        ("alta", "Alta")], required=True, string="Prioridad"
    )

    state = fields.Selection([
        ("ingresado", "Ingresado"),
        ("proceso", "Proceso"),
        ("resuelto", "Resuelto")], default="ingresado", required=True, string="Estado"
    )

    user_id = fields.Many2one("res.partner")
    deadline = fields.Date(required=True, string="Fecha limite")

    # def send_notification(self):

    # return self.env.ref('Soporte_Expr-s_odoo.cambio_estado').send_mail(self.id, force_send=True)

# def write(self, vals):
    # Guardamos los estados actuales de cada registro antes de la actualización
    # old_states = {record.id: record.state for record in self}
    # Super realiza cambios en la base de datos
    #  result = super(SupportIncident, self).write(vals)
    # Recorremos los registros y verificamos si el estado cambió
# for record in self:
    # if 'state' in vals and old_states.get(record.id) != record.state:
    # record.send_notification()
    # return result

    def cambiar_estado(self):
        for record in self:
            siguiente_estado = {
                'ingresado': 'proceso',
                'proceso': 'resuelto',
                'resuelto': 'cerrado',
            }.get(record.state)

            if siguiente_estado:
                record.state = siguiente_estado

                # Mensaje al chatter
                record.message_post(
                    body=f"📢 Estado cambiado a <b>{siguiente_estado.capitalize()}</b>"
                )

                # Enviar correo usando plantilla
                template = self.env.ref('soporte_expr_s_odoo.cambio_estado')
                if template:
                    template.send_mail(record.id, force_send=True)
