import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
from helpers import revenue_forecaster, movie_tags
from dash.dependencies import Input, Output

# Format the dashboard
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Read dummy data
data_revenue = pd.read_excel('data/Dummy Data.xlsx', engine='openpyxl', sheet_name='Sheet1')
data_movie = pd.read_excel('data/Dummy Data.xlsx', engine='openpyxl', sheet_name='Sheet2')

# Configure the dashboard layout
app.layout = html.Div(children=[
    html.H1(children='Dashboard Demo'),

    html.Div(children='''
        Dash: Below is a rough dashboard demo based on my previous project with a movie distributor.
        I have not had enough time to polish it but it should support pretty much all the types of viz.
    '''),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='country',
                options=[{'label': i, 'value': i} for i in data_revenue['Country'].unique()],
                multi=False,
                value='France',
            ),
            dcc.Dropdown(
                id='movie',
                options=[{'label': i, 'value': i} for i in data_revenue['Movie'].unique()],
                multi=False,
                value='Title A',
            )], style={'display': 'inline-block', 'width': '20%'}),

        dbc.Row(
            [dcc.Graph(
                id='revenue_forecast',
                figure=revenue_forecaster(data_revenue, 'France', 'Title B'), style={'display': 'inline-block'}),
            dcc.Graph(
                id='revenue_forecast_country',
                figure=revenue_forecaster(data_revenue, 'France', 'Title A'), style={'display': 'inline-block'})
            ], style={'display': 'inline-block'})

    ], style={'display': 'inline-block'}),

    html.Div(id='tags',
             children='Tags'),
])


@app.callback(
    Output(component_id='revenue_forecast', component_property='figure'),
    Input(component_id='country', component_property='value'),
    Input(component_id='movie', component_property='value')
)
def update_output_forecast(country, movie):
    """Whenever a movie is selected, update the forecast plot"""
    return revenue_forecaster(data_revenue, country, movie)


@app.callback(
    Output(component_id='tags', component_property='children'),
    Input(component_id='movie', component_property='value')
)
def update_output_tags(movie):
    """Whenever a movie is selected, update its tag"""
    return movie_tags(data_movie, movie)


@app.callback(
    Output(component_id='movie', component_property='options'),
    Output(component_id='movie', component_property='value'),
    Output(component_id='revenue_forecast_country', component_property='figure'),
    Input(component_id='country', component_property='value')
)
def update_movie_list_and_country_revenue(country):
    """Whenever a country is selected, update the movie list and country revenue forecast"""
    movie_list = data_revenue[data_revenue['Country'] == country]['Movie'].unique()
    return [{'label': i, 'value': i} for i in movie_list], \
           movie_list[0], \
           revenue_forecaster(data_revenue, country, "")


if __name__ == '__main__':
    app.run_server(debug=True)