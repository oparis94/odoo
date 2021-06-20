# -*- coding: utf-8 -*-
{
    'name': 'Leave Request Management',
    'version': '14.0.1.0.0',
    'sequence': '',
    'author': 'OpParis94',
    'website': 'https://liveoninternetvn.wixsite.com/thanhtuan',
    'depends': ['mail', ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/request_sequence.xml',
        'data/email_template.xml',
        'views/types_of_leaves_views.xml',
        'views/request_views.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}