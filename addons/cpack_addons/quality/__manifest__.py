{
    'name': "Quality",
    'version': '1.0.0.0',
    'depends': ['base','web','mail'],
    'installable': True,
    'aplication': True,
    'author': "Victor Oliveira Morais de Vasconcelos",
    'description': """
    A module to insert and visualize process forms, as well as solicit changes to the forms.
    """,
    
    'assets' : {
        'web.assets_backend' :[
            'quality/static/src/css/style.css',
        ]
    },

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/manage_arquives.xml',
        'views/manage_solicitations.xml',
        'views/solicit_changes.xml',
        'views/visualize_arquives.xml',
        'wizards/wizard_dismissed.xml',
        'wizards/wizard_solicit.xml',
        'views/menus_and_actions.xml',
    ],
    
    'demo': [
        
    ],
}