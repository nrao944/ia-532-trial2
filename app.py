import altair as alt
from gapminder import gapminder
import pandas as pd
from dash import Dash, html, dcc, Input, Output, State
    
gapminder1 = gapminder

grouped_df = gapminder1.groupby(["year", "continent"])
mean_df = grouped_df.mean()
mean_df = mean_df.reset_index()
mean_df

def plot_altair(ycol):
    chart = alt.Chart(mean_df).mark_point().encode(
        alt.X('year', scale=alt.Scale(zero=False)),
        y = ycol,
        color = 'continent',
        tooltip='lifeExp').interactive()
    return chart.to_html()

app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server

app.layout = html.Div([
        dcc.Dropdown(
            id='ycol', value='lifeExp',
            options=[{'label': i, 'value': i} for i in mean_df[['pop','gdpPercap', 'lifeExp']]]),
        html.Iframe(
            id='scatter',
            style={'border-width': '0', 'width': '100%', 'height': '400px'},
            srcDoc=plot_altair(ycol='lifeExp'))])

@app.callback(
    Output('scatter', 'srcDoc'),
    Input('ycol', 'value'))
def update_output(ycol):
    return plot_altair(ycol)

if __name__ == '__main__':
    app.run_server(debug=True)