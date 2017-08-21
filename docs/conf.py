import sphinx_materialdesign_theme

html_theme = 'sphinx_materialdesign_theme'
html_theme_path = [sphinx_materialdesign_theme.get_path()]

html_logo = 'http://i.imgur.com/kyMfmAk.png'

html_theme_options = {
    'header_links': [
        ('Home', 'index', False, 'home'),
        ("Website", "https://auroraproject.xyz/#/sigma", True, 'link'),
        ("GitHub", "https://github.com/aurora-pro", True, 'link')
    ],
    'primary_color': 'teal',
    'accent_color': 'grey',
    'fixed_drawer': True,
    'fixed_header': True,
    'header_waterfall': True,
    'header_scroll': False,
    'show_header_title': False,
    'show_drawer_title': True,
    'show_footer': False
}
