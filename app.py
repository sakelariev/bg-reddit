from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import locale
import re
import pandas as pd
import random

# External stylesheets and scripts
FA = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"
external_stylesheets = [dbc.themes.FLATLY, FA]
external_scripts = ["https://cdn.plot.ly/plotly-locale-bg-latest.js"]

monthly_unigram = pd.read_csv("data/monthly_unigram.csv", index_col=0, parse_dates=['date'])
# monthly_unigram = monthly_unigram.sort_values(by=['date'])
monthly_bigram = pd.read_csv("data/monthly_bigram.csv", index_col=0, parse_dates=['date'])
# monthly_bigram = monthly_bigram.sort_values(by=['date'])
# monthly_trigram = pd.read_csv("data/monthly_trigram.csv", index_col=0, parse_dates=['date'])

# Try to normalize dates to begining of month
monthly_unigram['date'] = monthly_unigram['date'] - pd.offsets.MonthBegin(1, normalize=True)
monthly_bigram['date'] = monthly_bigram['date'] - pd.offsets.MonthBegin(1, normalize=True)




app = Dash(__name__, external_stylesheets=external_stylesheets, external_scripts=external_scripts)

fig = go.Figure()
fig.update_xaxes(showgrid=False, ticks="inside")
fig.update_yaxes(tickformat = '%')
fig.update_layout(hovermode="x unified", template = "plotly_white", xaxis=dict(tickformat="%B-%Y"), hoverlabel_namelength=-1)

def data_missing(df):
    if len(df) <= 1:
        missing_data = True
    else:
        missing_data = False
    return missing_data

def check_string(string):
    ngram = len(string.split())
    string = string.lower()
    string = string.rstrip()
    string = string.lstrip()
    if ngram == 1:
        df = monthly_unigram[monthly_unigram['unigram'] == string]
        missing_state = data_missing(df)
        forbidden_state = False
    elif ngram == 2:
        df = monthly_bigram[monthly_bigram['bigram'] == string]
        missing_state = data_missing(df)
        forbidden_state = False
    elif ngram == 3:
        df = 0
        print("За момента не се поддържат фрази с повече от 2 думи.")
        forbidden_state = True
        # df = monthly_trigram[monthly_trigram['trigram'] == string]
        # forbidden_state = False
    elif ngram == 0:
        df = 0
        forbidden_state = False
        raise PreventUpdate
    else:
        df = 0
        print("За момента не се поддържат фрази с повече от 2 думи.")
        forbidden_state = True
    return df, forbidden_state, missing_state

app.layout = dbc.Container([
        
        dbc.Navbar(
            dbc.Container(
                [
                    html.H2("За какво/кого говори българският Reddit?", className="text_gradient"),
                ]
            ), 
        ),
        html.Hr(className="line_gradient"),
        dbc.Row([
        dbc.Col([
        ], md=2),     
        dbc.Col([
        dbc.Button('Случайни идеи',id='random_shuffle', color="dark", outline=True, style={'font-size' : '13px'}),
        ], md=1), 
        dbc.Col([
        html.Div([
        html.Div(dbc.Button('🔍',id='search', color='light', outline=True, style={'padding':'7px', 'color': '#fff','border-color': '#fff'}), style={'display' : 'inline-block', 'vertical-align': 'middle'}),
        html.Div(
            dbc.Input(
            id="input",
            type="text",
            debounce=True,
            minLength=3,
            # maxLength=100
            placeholder="Търси думи, имена, фрази...",
            style = {'width' : '100%'}
        ), style={'display' : 'inline-block', 'vertical-align': 'middle', 'width' : '90%'}),
        ])], md=6),
        
        dbc.Col([
        html.P("Интерполация", style={'font-size' : '13px', 'text-align' :'center', 'padding' : '0px', 'margin' : '0px'}),
        dcc.Slider(min=0, max=12, value=0, step=1, id='smoothing', drag_value=1, marks=None,
        tooltip={"placement": "bottom", "always_visible": True},
        className="smoothing_slider")
        ], md=1),
        
        dbc.Col([
        ], md=2) 
        ], align="center", style={'margin-top' : '50px', 'padding-bottom' : '15px'}, className="g-0",
        ),
        
        dbc.Row([
            
        dbc.Col([
        ], md=3),
        dbc.Col([
        dbc.Alert(
            children=[],
            id="alert-missing",
            dismissable=True,
            is_open=False,
            color="danger",
            style={'font-size' : '13px'}
        ),
        dbc.Alert(
            "За момента не се поддържат фрази с повече от 2 думи.",
            id="alert-fade",
            dismissable=True,
            is_open=False,
            color="danger",
            style={'font-size' : '13px'}
        ),     
        ], md=6),    
        dbc.Col([
        ], md=3) 
        
        ], align="center", className="g-0"),
        
        dbc.Row([
        dbc.Col([
        ], md=1), 
        dbc.Col([
        dcc.Graph(figure=fig, config=dict({'scrollZoom': False, "displaylogo": False, 'displayModeBar': False, 'showAxisDragHandles': False, 'locale' : 'bg'}),
        id='main_graph')
        ], md=10),
        dbc.Col([
        ], md=1) 
        ], align="center", 
        ),
        
        dbc.Row([
            dbc.Col([], md=3),
            dbc.Col([
            # html.H4(children="Описание на данните от Facebook Movement Range Maps", id="description_data"),
            dcc.Markdown('''Българският Reddit (r/bulgaria) е относително малко кътче в Интернет пространството, но пък в него потребителите дискутират актуални събития за страната и би било интересно да се проследяват трендове за различните теми, хора и събития, които се обсъждани на платформата. Затова създадох този инструмент, вдъхновен от [Google Ngram Viewer](https://books.google.com/ngrams). Данните използвани за създаването му бяха взети от всички коментари (около 735 000) в българският subreddit – r/bulgaria от юли 2008 година до май 2022 година. Повече информация за това как бяха генерирани и обработени данни, и как беше създаден Ngram моделът може да прочете в този мой [блог пост](https://github.com/sakelariev/reddit-scraper). Отвореният код на приложението може да разгледате (и използвате както си пожелаете) в [Github](https://github.com/sakelariev/reddit-scraper).''')
            ],
            md=6),
        
            dbc.Col([], md=3)
        ], style={
                            "position":"relative",
                            "bottom":0,
                            "padding-bottom": "30px",
                            "margin-top": "30px",
                        }),
        
        ], fluid=True)

# For the callback I have two options - either with Input(n_submit) + State or with Input(value) and debounce=True,
@app.callback(
    Output(component_id='main_graph', component_property='figure'),
    # Input(component_id='input', component_property='n_submit'),
    # State(component_id='input', component_property='value'),
    Input(component_id='search', component_property='n_clicks'),
    Input(component_id='smoothing', component_property='value'),
    Input(component_id='input', component_property='value'),
    )
def update_figure(n_clicks, smoothing, string):
    # if n_submit is None:
    #     raise PreventUpdate
    # else:
    print(string)
    # smoothing = smoothing / 10
    print(smoothing)
    fig = go.Figure()
    for element in string.split(','):
        df = check_string(element)[0]
        double_check = check_string(element)[1]
        check_missing = check_string(element)[2]
        element = element.rstrip()
        element = element.lstrip()
        df['average'] = df.ratio.rolling(smoothing).mean()
        if double_check == False and check_missing == False:
            if smoothing <= 1:
                fig.add_trace(go.Scatter(x=df['date'], y=df['ratio'],
                                    mode='lines+markers',
                                    name=element,
                                    # line_shape='spline',
                                    # line={'smoothing' : 0.5}
                                    ))
            else:
                fig.add_trace(go.Scatter(x=df['date'], y=df['average'],
                mode='lines+markers',
                name=element,
                # line_shape='spline',
                # line={'smoothing' : 0.5}
                ))
        fig.update_traces(mode="lines", hovertemplate=None)
        fig.update_xaxes(showgrid=False, ticks="inside", tickangle=0, ticklabelstep=1)
        fig.update_yaxes(tickformat = '%')
        fig.update_layout(hovermode="x unified", template = "plotly_white", xaxis=dict(tickformat="%B<br>%Y"), hoverlabel_namelength=-1, legend=dict(orientation="h", yanchor="bottom", y=1.03, xanchor="center", x=0.5))
    return fig


# Second callback is for notifications
@app.callback(
    Output(component_id='alert-fade', component_property='is_open'),
    Input(component_id='input', component_property='value'),
    [State("alert-fade", "is_open")],
    )
def trigger_notification(string, is_open):
    for element in string.split(','):
        double_check = check_string(element)[1]
        if double_check:
            is_open = True
        else:
            is_open = False
    return is_open

# Alert for when some phrase is missing from the data
@app.callback(
   [Output(component_id='alert-missing', component_property='is_open'),
    Output(component_id='alert-missing', component_property='children')],
    Input(component_id='input', component_property='value'),
    [State("alert-missing", "is_open")],
    )
def trigger_notification(string, is_open):
    for element in string.split(','):
        check_missing = check_string(element)[2]
        if check_missing:
            is_open = True
            message = dcc.Markdown("**{}** липсва от данните.".format(element))
        else:
            is_open = False
            message = ''
    return is_open, message
    
# Shuffle random ideas to explore the tool
@app.callback(
    Output(component_id='input', component_property='value'),
    Input(component_id='random_shuffle', component_property='n_clicks'),
    )
def shuffle_random_ideas(n_clicks):
    random_ideas = ["Левски,ЦСКА,Лудогорец", "Копейкин,Костадин Костадинов", "Бойко Борисов,Кирил Петков", "Възраждане,ДПС", "Ковид,Ваксина", "България, Русия, САЩ", "Америка, САЩ", "Ванга, Дънов"]
    draw_random = random.choice(random_ideas)
    return draw_random


if __name__ == '__main__':
    app.run_server(debug=True)