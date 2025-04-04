import dash
import dash_bootstrap_components as dbc
import dash_bootstrap_templates

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
dash_bootstrap_templates.load_figure_template('sandstone')


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    external_stylesheets=[dbc.themes.SANDSTONE, dbc.icons.FONT_AWESOME, dbc_css],
    use_pages=True
)
app.title = "Data Jobs in Israel 2024-2025"
server = app.server


# Layout of Dash App
app.layout = dbc.Container(
    children=[
        dbc.NavbarSimple([
            dbc.NavItem(dbc.NavLink("Comparisons", href="/compare", style = {"alignment": "left"})),
            dbc.NavItem(dbc.NavLink("About", href="/about", style = {"alignment": "right"}))
            ],
            sticky="top",
            color="primary",
            brand="Data Jobs in Israel 2024-2025",
            brand_href="/",
            links_left=False,
            dark=True,
            brand_style ={"font-size": 24},
        ),
        dash.page_container,
    ]
, fluid=True)

if __name__ == '__main__':
    app.run_server()