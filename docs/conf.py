import sphinx_rtd_theme

extensions = [
    "sphinx_rtd_theme",
]

html_logo = "project_sigma_white.png"

html_theme = "sphinx_rtd_theme"

html_theme_options = {
    "gitlab_url": "https://gitlab.com/lu-ci/sigma/apex-sigma"
}

html_static_path = ['static']

html_css_files = [
    'custom.css'
]
