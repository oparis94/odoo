{
    'name': 'Hospital Management',
    'version': '14.0.1',
    'category': '',
    'sequence': '',
    'depends': [
        'sale',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/patient_sequence.xml',
        'data/appointment_sequence.xml',
        'data/data_default.xml',
        'data/mail_template.xml',
        'wizards/create_appointment.xml',
        'views/patient.xml',
        'views/appointment.xml',
        'views/appointment.xml',
        'views/doctor.xml',
        'reports/patient_card.xml',
        'reports/report.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,

}