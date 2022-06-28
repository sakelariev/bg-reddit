# coding=utf8
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


# Read csv files
unigram_full_df = pd.read_csv("data/unigram_full_df.csv", index_col=0, parse_dates=['date'])
bigram_full_df = pd.read_csv("data/bigram_full_df.csv", index_col=0, parse_dates=['date'])

# Main app 
app = Dash(__name__, external_stylesheets=external_stylesheets, external_scripts=external_scripts)
app.title = 'За какво говори българският Reddit - Ngram приложение'
application = app.server

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
    if ngram == 1 :
        df = unigram_full_df[unigram_full_df['gram'] == string]
        missing_state = data_missing(df)
        forbidden_state = False
    elif ngram == 2:
        df = bigram_full_df[bigram_full_df['gram'] == string]
        missing_state = data_missing(df)
        forbidden_state = False
    elif ngram == 0:
        df = 0
        forbidden_state = False
        missing_state = True
        raise PreventUpdate
    else:
        df = 0
        print("За момента не се поддържат фрази с повече от 2 думи.")
        forbidden_state = True
        missing_state = True
    return df, forbidden_state, missing_state

app.layout = dbc.Container([
            
            dbc.Navbar(
                dbc.Container(
                    [
                        html.H2("За какво и кого говори българският Reddit?", className="text_gradient"),
                    ]
                ), 
            ),
            html.Hr(className="line_gradient"),
            dbc.Row([
            dbc.Col([
            ], md=1),     
            dbc.Col([
            dbc.Button('🎲 Случайни идеи', id='random_shuffle', color="dark", className='d-flex justify-content-center', outline=True, style={'font-size' : '12px',  'text-align' : 'center', 'margin-left': '25%'}),
            ], md=2), 
            dbc.Col([
            html.Div([
            html.Div(dbc.Button('🔍',id='search', color='light', outline=True, style={'padding':'7px', 'color': '#fff','border-color': '#fff'}), style={'display' : 'inline-block', 'vertical-align': 'middle'}),
            dbc.Tooltip(
                 "Търси",
                 target="search",
                 placement="bottom",
             ),
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
            html.P("Подвижна средна стойност", id="inter", style={'font-size' : '12px', 'text-align' :'center', 'padding' : '0px', 'margin' : '0px'}),
            dcc.Slider(min=1, max=12, value=1, step=1, id='smoothing', drag_value=1, marks=None,
            tooltip={"placement": "bottom", "always_visible": True},
            className="smoothing_slider"),
            dbc.Tooltip(
                  "Изравняване на данни с подвижна средна стойност. 1 са суровите данни, 2 е средната стойност за два месеца, 3 е средната стойност за месеца и т.н.",
                  target="inter",
                  placement="top"
              ),
            ], md=2, style={'padding-left': '2%'}),
            
            dbc.Col([
            ], md=1) 
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
            dcc.Loading(
            id="loading-graph",
            type="dot",
            color="#82888a",
            children=dcc.Graph(figure=fig, config=dict({'scrollZoom': False, "displaylogo": False, 'displayModeBar': False, 'showAxisDragHandles': False, 'locale' : 'bg'}),
            id='main_graph'))
            ], md=10),
            dbc.Col([
            ], md=1) 
            ], align="center", className="g-0",
            ),
            
            dbc.Row([
                dbc.Col([], md=3),
                dbc.Col([
                dcc.Markdown('''Българският Reddit (r/bulgaria) е относително малко кътче в Интернет пространството, но пък в него потребителите дискутират актуални събития за страната и би било интересно да се проследяват трендове за различните теми, хора и събития, които се обсъждат там. 
                За тази цел създадох този инструмент, вдъхновен от [Google Books Ngram Viewer](https://books.google.com/ngrams). 
                Въведете различни фрази в търсачката (с натискане на бутона или клавиш Enter) и ще получите графика, която визуализира колко често тези фрази са били споменати в [reddit.com/r/bulgaria](https://www.reddit.com/r/bulgaria/) през дадения период. 
                Данните бяха генерирани от всички коментари (около 735 000) в българският subreddit – r/bulgaria от началото на 2016 година до май 2022 година.  
                Повече информация за това как бяха свалени и обработени коментарите, и как беше създаден Ngram моделът може да прочете в този [блог пост](https://ivaylo.xyz/posts/2022-06-20-reddit-ngram-viewer/).\n Отвореният код на приложението може да разгледате (и използвате както си пожелаете) в [Github](https://github.com/sakelariev/bg-reddit).\n 
*\*Абсолютен брой има достъпен само при суровите данни (Подвижна средна стойност = 1).*
                ''')
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
  Input(component_id='search', component_property='n_clicks'),
  Input(component_id='smoothing', component_property='value'),
  Input(component_id='input', component_property='value'),
  )
def update_figure(n_clicks, smoothing, string):
  fig = go.Figure()
  colors_list = px.colors.qualitative.Plotly
  for count, element in enumerate(string.split(',')):
      df = check_string(element)[0]
      double_check = check_string(element)[1]
      check_missing = check_string(element)[2]
      element = element.rstrip()
      element = element.lstrip()
      # Fill in all missing monthly values with 0 - this makes the plot look correct now
      df = (df.set_index('date').reindex(pd.date_range('2016-01-01', '2022-05-01', freq='MS')).rename_axis(['date']).fillna(0).reset_index())
      df['average'] = df.ratio.rolling(smoothing).mean()
      df['average_count'] = df['count'].rolling(smoothing).mean().round(0)
      if double_check == False and check_missing == False:
          if smoothing <= 1:
              fig.add_trace(go.Scatter(x=df['date'], y=df['ratio'],
                                  mode='lines',
                                  name=element,
                                  customdata=df[['count']], 
                                  legendgroup=element,
                                  line_shape='spline',
                                  line={'smoothing' : 0.6, 'color' : colors_list[count]},
                                  hovertemplate='<b>%{y}</b> <br>Абсолютен брой<sup>*</sup>: %{customdata[0]}'
                                  ))
              # add traces for annotations and text for end of lines
              fig.add_scatter(x=df['date'].tail(1), y=df['ratio'].tail(1),
               mode='text',
               text=" " + element,
               hoverinfo='skip',
               hovertemplate=None,
               textfont=dict(color=colors_list[count]),
               textposition='middle right',
               cliponaxis=False,
               legendgroup=element,
               showlegend=False)
          else:
              fig.add_trace(go.Scatter(x=df['date'], y=df['average'],
              mode='lines',
              name=element,
              # customdata=df[['average_count']], 
              legendgroup=element,
              line_shape='spline',
              line={'smoothing' : 0.6, 'color' : colors_list[count]},
              # hovertemplate='<b>%{y}</b> <br>Абсолютен брой(подвижна средна стойност): %{customdata[0]}'
              ))
              # add traces for annotations and text for end of lines
              fig.add_scatter(x=df['date'].tail(1), y=df['average'].tail(1),
                mode='text',
                text=" " + element,
                hoverinfo='skip',
                hovertemplate=None,
                cliponaxis=False,
                textfont=dict(color=colors_list[count]),
                textposition='middle right',
                legendgroup=element,
                showlegend=False)

      # fig.update_traces(hovertemplate=None, connectgaps=True)
      fig.update_traces(connectgaps=True)
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
    State(component_id='input', component_property='value'),
    )
def shuffle_random_ideas(n_clicks, current_value):
    random_ideas = ["Левски,ЦСКА,Лудогорец", "Копейкин,Костя,Костадин Костадинов", "Бойко Борисов,Кирил Петков", "Възраждане,ДБ,ГЕРБ,БСП,ИТН", "Ковид,Ваксина", "Украйна,Русия,САЩ","Меркел,Орбан", "Путин,Ердоган", "Гешев,Борисов", "Слави,Бойко", "олио,зехтин", "инфлация,кредит", "НАТО,ЕС", "фалшиви новини,fake news", "орки"]
    draw_random = random.choice(random_ideas)
    if draw_random == current_value:
        random_ideas.remove(current_value)
        draw_random = random.choice(random_ideas)
    return draw_random


if __name__ == '__main__':
    app.run_server(debug=False)