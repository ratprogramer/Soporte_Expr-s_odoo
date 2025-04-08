{
    "name": "Soporte de incidentes",
    "depends": [
        "base", "mail"
    ],
    "data": [
        "views/support_incident_views.xml",
        "security/ir.model.access.csv",
        "data/mail_templates.xml"
    ],
    "assets": {
        "web.assets_backend": [
            "Soporte_Express_odoo/static/src/css/custom_view.css",
        ],
    },
    "application": True,
}
