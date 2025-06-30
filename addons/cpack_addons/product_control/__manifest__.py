{
    'name': "product_control",
    'version': '1.0.0.0',
    'depends': ['base','web','mail'],
    'installable': True,
    'aplication': True,
    'author': "Victor Oliveira Morais de Vasconcelos",
    'description': """
    A module for product and process control.
    """,
    
    'assets' : {
        'web.assets_backend' :[
            'product_control/static/src/js/form_controller_extend.js',
            'product_control/static/src/css/style.css',
        ]
    },

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/final_control.xml',
        'views/store_control.xml',
        'views/register_control.xml',
        'views/process_control.xml',
        'views/menus_and_actions.xml',
    ],

    
    'demo': [
        
    ],
}