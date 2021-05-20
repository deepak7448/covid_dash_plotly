import dash
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta,date
from datetime import datetime
from dash.dependencies import Input,Output,State
from dateutil.relativedelta import *
from dash_extensions import Lottie 

scripts = "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML" 
app = dash.Dash(__name__,title='Covid Dash',external_stylesheets=[dbc.themes.BOOTSTRAP],external_scripts=[scripts],
     meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}])    
server = app.server

covid_active = 'https://assets6.lottiefiles.com/packages/lf20_nKCnOy.json'
covid_confirm = 'https://assets1.lottiefiles.com/packages/lf20_u41SFE.json'
covid_recovered = 'https://assets5.lottiefiles.com/packages/lf20_nmx1GJ.json'
covid_death  = 'https://assets9.lottiefiles.com/packages/lf20_AQ3M8U.json'
options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))

#All_state_cases_table_header
table_url='https://api.covid19india.org/csv/latest/state_wise.csv'
table_df=pd.read_csv(table_url)

table_df['Last_Updated_Time'] = pd.to_datetime(table_df.Last_Updated_Time)
table_df['Last_Updated_Time'] = table_df['Last_Updated_Time'].dt.strftime('%d %b,%I:%M %p')
tablle_date=table_df['Last_Updated_Time'].iloc[0]
table_df['Delta_Active'] = table_df['Delta_Confirmed']-table_df['Delta_Recovered']-table_df['Delta_Deaths']

# confirmed = table_df['Confirmed'].iloc[0]
# recovered = table_df['Recovered'].iloc[0]
# active = table_df['Active'].iloc[0]
# deaths = table_df['Deaths'].iloc[0]
# todayconfirmed = table_df['Delta_Confirmed'].iloc[0]
# todayrecovered	 = table_df['Delta_Recovered'].iloc[0]
# todaydeaths = table_df['Delta_Deaths'].iloc[0]
# todayactive = table_df['Delta_Active'].iloc[0]
table_df = table_df[['State','Confirmed','Recovered','Deaths','Active','Delta_Confirmed','Delta_Recovered','Delta_Deaths']]
#table_df = table_df.rename(columns = {'Delta_Confirmed':'Total Confirmed','Delta_Recovered':'Today Recovered','Delta_Deaths':'Today Deaths'}, inplace = True)
table_covid_data = table_df.groupby(['State'],as_index=False)[['Confirmed','Recovered','Deaths','Active']].sum()
table_covid =table_covid_data.sort_values(by=["Confirmed"],ascending=[False])
table_covid['State'][0:1]='India'
table_covid['Confirmed'] =table_covid.apply(lambda confirmed:"{:,}".format(confirmed['Confirmed']),axis=1)
table_covid['Recovered'] =table_covid.apply(lambda recovered:"{:,}".format(recovered['Recovered']),axis=1)
table_covid['Deaths'] =table_covid.apply(lambda deaths:"{:,}".format(deaths['Deaths']),axis=1)
table_covid['Active'] =table_covid.apply(lambda active:"{:,}".format(active['Active']),axis=1)
table_covid_All = table_covid.head(37)

#Cumulative_heading
date=datetime.today()
today=date.strftime("%Y-%m-%d")
premonth = date.today() + relativedelta(months=-1,days=-2)
Cumulative_url="https://api.covid19india.org/csv/latest/states.csv"
Cumulative=pd.read_csv(Cumulative_url)
Cumulative_date = Cumulative[(Cumulative['Date']>str(premonth))]
Cumulative_date['Active'] = Cumulative_date['Confirmed'] - Cumulative_date['Deceased'] - Cumulative_date['Recovered']
Cumulative_data = Cumulative_date[['Date','State','Confirmed','Recovered','Deceased','Active',]]
Cumulative_data_graph = Cumulative_data.groupby(['Date', 'State'],as_index=False)[['Confirmed','Recovered','Deceased','Active']].sum()


#Cumulative_bar_graph_char
today = date.strftime("%Y-%m-%d")
todays = date.today() - timedelta(1)
premonths = date.today() + relativedelta(months=-1,days=-2,)
Cumulative_graph = Cumulative[(Cumulative['Date']>str(premonths)) & (Cumulative['Date'] < str(todays))]
Cumulative_graph['Active'] = Cumulative_graph['Confirmed'] - Cumulative_graph['Deceased'] - Cumulative_graph['Recovered']
Cumulative_graph = Cumulative_graph[['Date','State','Confirmed','Recovered','Deceased','Active',]]
Cumulative_graph = Cumulative_graph.groupby(['Date', 'State'],as_index=False)[['Confirmed','Recovered','Deceased','Active']].sum()

#total_vaccine_doses
url="http://api.covid19india.org/csv/latest/vaccine_doses_statewise.csv"
vaccine_data = pd.read_csv(url)
vaccine  = vaccine_data.iloc[-1]
total_vaccine=vaccine[-1:]
total_vaccine_dose = total_vaccine[-1]

#dialy_corona_cases
today = date.today()
premn = today + relativedelta(months=-1,days=-2,)
url='https://api.covid19india.org/csv/latest/state_wise_daily.csv'
dialy_cases=pd.read_csv(url)
dates = dialy_cases[(dialy_cases['Date_YMD']>str(premn))]
all_state = dates.loc[:, dialy_cases.columns != 'DD']
all_states = all_state.rename(columns = {
    'TT':'India','AN':'Andaman and Nicobar Islands','AP':'Andhra Pradesh','AR':'Arunachal Pradesh','AS':'Assam','BR':'Bihar','CH':'Chandigarh','CT':'Chhattisgarh','DN':'Dadra and Nagar Haveli and Daman and Diu',
    'DL':'Delhi','GA':'Goa','GJ':'Gujarat','HR':'Haryana','HP':'Himachal Pradesh','JK':'Jammu and Kashmir','JH':'Jharkhand','KA':'Karnataka','KL':'Kerala','LA':'Ladakh','LD':'Lakshadweep','MP':'Madhya Pradesh',
    'MH':'Maharashtra','MN':'Manipur','ML':'Meghalaya','MZ':'Mizoram','NL':'Nagaland','OR':'Odisha','PY':'Puducherry','PB':'Punjab','RJ':'Rajasthan','SK':'Sikkim','TN':'Tamil Nadu','TG':'Telangana','TR':'Tripura',
    'UP':'Uttar Pradesh','UT':'Uttarakhand','WB':'West Bengal',}, inplace = True)

Confirmed = (all_state['Status'] == 'Confirmed')
Recovered = (all_state['Status'] == 'Recovered')
Deceased = (all_state['Status'] == 'Deceased')
Confirmed = all_state[Confirmed]
Recovered = all_state[Recovered]
Deceased = all_state[Deceased]




app.layout = dcc.Loading(
    children=[
    html.Div([
    html.H3(["Covid19"],id='covid-19-india',className="text-center mt-4"),
    html.H3(id='covid19state',className="text-center mb-3"),
    html.Div([
         html.Div(html.P(f"Last update on {tablle_date}")),
    ],className="text-center"),
     dbc.Row([
          dbc.Col([
             dbc.Card([
                 dbc.CardBody([html.H4(["Confirmed"],className="text-center"),
                              html.H5(id='covidconfirmed',className="card-subtitle mt-2 text-center"),
                              html.H5(id='covidtotalconfirmed', className="card-text mt-2 text-center"),
                              html.H6(Lottie(options=options, width="50%", height="80%", url=covid_confirm)),]),],
                 id='covid-confirmed',)],lg=3,md=3,sm=6,className='mb-3'),
           dbc.Col([
             dbc.Card([
                dbc.CardBody([html.H4(["Active"],className="text-center"),
                              html.H5(id='covidActive',className="card-subtitle mt-2 text-center"),
                              html.H5(id='covidtotalActive', className="card-text mt-2 text-center"),
                             html.H6(Lottie(options=options, width="55%", height="80%", url=covid_active),className='mt-1'),]),],
                 id='covid-active',)],lg=3,md=3,sm=6,className='mb-3'),
         dbc.Col([
             dbc.Card([
                 dbc.CardBody([html.H4(["Recovered"],className="text-center"),
                             html.H5(id='covidRecovered',className="card-subtitle mt-2 text-center"),
                              html.H5(id='covidtotalRecovered', className="card-text mt-2 text-center"),
                              html.H6(Lottie(options=options, width="55%", height="80%", url=covid_recovered),className='mt-4'),]),],
                 id='covid-recovered')],lg=3,md=3,sm=6,className='mb-3'),
           dbc.Col([
             dbc.Card([
                 dbc.CardBody([html.H4(["Death"],className="text-center"),
                              html.H5(id='covidDeath',className="card-subtitle mt-2 text-center"),
                              html.H5(id='covidtotalDeath', className="card-text mt-2 text-center"),
                              html.H6(Lottie(options=options, width="55%", height="80%%", url=covid_death)),]),],
                 id='covid-death',)],lg=3,md=3,sm=6)
     ],className='pl-3 pr-3 mt-2',id="total-corona-cases"),
    html.Div([
    dbc.Button("Show/Hide All States",id="collapse-button",color="primary",),],className="mt-1 text-center"),
    html.Div([
   
    #table_chart
    dbc.Collapse(
        dbc.Col([dbc.Table([
       html.Table(
        # Header
        [html.Tr([html.Th(col) for col in table_covid_All.columns])] +
        # Body
        [html.Tr([
            html.Td(table_covid_All.iloc[i][col]) 
            for col in table_covid_All.columns]) 
            for i in range(min(len(table_covid_All), 37) )] ) 
             ],className='mt-5',bordered=True,hover=True,responsive=True,)
            ],lg=12,sm=12,md=12,id='all-state-table',),id="collapse",),
        #bar_chat_cases
        dbc.Col([html.Div([
                dcc.Dropdown(
                    id='totalcases',
                    options=[{'label':x,'value':x}for x in table_covid_All['State']],
                    value = 'India',
                    multi = False,
                    persistence=True,
                    persistence_type='session',
                clearable=False,)],className='mt-4'), ]),
        html.Div([
        dbc.Badge(f"{total_vaccine_dose:,.0f} vaccine doses administered", color="danger", ),],className="mt-3 text-center"),
        html.Div([
        dcc.RadioItems(
                id='show-table',
                options=[{'label': 'Cumulative', 'value': 'cumulative'},
                         {'label': 'Daily', 'value': 'Daily'}],
                value='cumulative',
            )],className='text-center mt-3'),
        
        #Cumulative_corona_cases         
        #pie_chat
        html.Div([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='pie_chart',config={'displayModeBar':False},className='mt-5')
                ],lg=5,md=12,sm=12),
        dbc.Col([
         dbc.Row([
            dbc.Col([
            dcc.Graph(id='Confirmed',config={'displayModeBar': False})
        ],lg=6,md=6,sm=12,className='layout_chart'),
        dbc.Col([
            dcc.Graph(id='Active', config={'displayModeBar': False})
        ],lg=6,md=6,sm=12,className='layout_chart'),
           dbc.Col([
            dcc.Graph(id='Recovered', config={'displayModeBar': False}),
        ],lg=6,md=6,sm=12,className='layout_chart'),
        dbc.Col([
            dcc.Graph(id='Deceased', config={'displayModeBar': False})
        ],lg=6,md=6,sm=12,className='layout_chart'),])],lg=7,md=12,sm=12,id="total-case-chart"),])],id='Cumulative_cases'),
        
        #daily_corona_cases
        html.Div([
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='pie_chart_daily',config={'displayModeBar':False},className='mt-5')
            ],lg=5,md=12,sm=12),
         dbc.Col([
        dbc.Row([
            dbc.Col([
            dcc.Graph(id='daily-confirmed',config={'displayModeBar': False})
        ],lg=6,md=6,sm=12,className='layout_chart'),
#         dbc.Col([
#             dcc.Graph(id='daily-active', config={'displayModeBar': False})
#         ],lg=6,md=6,sm=12,className='layout_chart'),
           dbc.Col([
            dcc.Graph(id='daily-recovered', config={'displayModeBar': False}),
        ],lg=6,md=6,sm=12,className='layout_chart'),
        dbc.Col([
            dcc.Graph(id='daily-deceased', config={'displayModeBar': False})
        ],lg=12,md=12,sm=12,className='layout_chart'),])],lg=7,md=12,sm=12,id="today-case-chart",)])],id='Daily_cases')
    ])
])

],type="circle", fullscreen=True,)

#table_show_hide
@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        time.sleep(1)
        return not is_open
    time.sleep(1)
    return is_open

@app.callback(
    Output('covid19state','children'),
    [Input('totalcases', 'value')])
def statecases(totalcases):
    state_cases = []
    State = Cumulative_data_graph[Cumulative_data_graph['State'] == totalcases]['State']
    for i in State:
        if i not in state_cases:
            state_cases.append(i)
    return state_cases

#totoal_corona_cases
@app.callback(
    Output('covidconfirmed','children'),
    [Input('totalcases', 'value')])
def confirmed(totalcases):
    confirmed = Cumulative_data_graph[Cumulative_data_graph['State'] == totalcases]['Confirmed']
    confirm = list(confirmed)
    today_confirm = confirm[-1]
    yesterday_confirm = confirm[-2]
    today_incre = today_confirm - yesterday_confirm
    return f"{today_confirm:,.0f}"


@app.callback(
    Output('covidRecovered','children'),
    [Input('totalcases', 'value')])
def recovered(totalcases):
    Recovered = Cumulative_data_graph[Cumulative_data_graph['State'] == totalcases]['Recovered']
    Recovered = list(Recovered)
    today_Recovered = Recovered[-1]
    today_Recovered = Recovered[-2]
    today_incre = today_Recovered - today_Recovered
    return f"{today_Recovered:,.0f}"

@app.callback(
    Output('covidActive','children'),
    [Input('totalcases', 'value')])
def active(totalcases):
    Active = Cumulative_data_graph[Cumulative_data_graph['State'] == totalcases]['Active']
    Active = list(Active)
    today_Active = Active[-1]
    yesterday_Active = Active[-2]
    today_incre = today_Active  - yesterday_Active
    return f"{today_Active:,.0f}"

@app.callback(
    Output('covidDeath','children'),
    [Input('totalcases', 'value')])
def death(totalcases):
    Death = Cumulative_data_graph[Cumulative_data_graph['State'] == totalcases]['Deceased']
    Death = list(Death)
    today_Death = Death[-1]
    yesterday_Death = Death[-2]
    today_incre = today_Death - yesterday_Death
    return f"{today_Death:,.0f}"

#today_corona_cases
@app.callback(
    Output('covidtotalconfirmed','children'),
    [Input('totalcases', 'value')])
def confirmed(totalcases):
    confirmed = Cumulative_data_graph[Cumulative_data_graph['State'] == totalcases]['Confirmed']
    confirm = list(confirmed)
    today_confirm = confirm[-1]
    yesterday_confirm = confirm[-2]
    today_confirmed = today_confirm - yesterday_confirm
    return f"+{today_confirmed:,.0f}"

@app.callback(
    Output('covidtotalRecovered','children'),
    [Input('totalcases', 'value')])
def confirmed(totalcases):
    Recovered = Cumulative_data_graph[Cumulative_data_graph['State'] == totalcases]['Recovered']
    Recovered = list(Recovered)
    today_Recovered = Recovered[-1]
    yesterday_Recovered = Recovered[-2]
    today_recovered = today_Recovered - yesterday_Recovered
    return f"+{today_recovered:,.0f}"

@app.callback(
    Output('covidtotalActive','children'),
    [Input('totalcases', 'value')])
def confirmed(totalcases):
    Active = Cumulative_data_graph[Cumulative_data_graph['State'] == totalcases]['Active']
    Active = list(Active)
    today_Active = Active[-1]
    yesterday_Active = Active[-2]
    today_active = today_Active  - yesterday_Active
    if today_active>=0:
        return f"+{today_active:,.0f}"
    else:
        return f"{today_active:,.0f}"

@app.callback(
    Output('covidtotalDeath','children'),
    [Input('totalcases', 'value')])
def confirmed(totalcases):
    Death = Cumulative_data_graph[Cumulative_data_graph['State'] == totalcases]['Deceased']
    Death = list(Death)
    today_Death = Death[-1]
    yesterday_Death = Death[-2]
    today_deceased = today_Death - yesterday_Death
    return f"+{today_deceased:,.0f}"

#pie_chat
@app.callback(
    Output('pie_chart','figure'),
    [Input('totalcases', 'value')])
def pie_chat_output(totalcases):
    confirmed = Cumulative_graph[Cumulative_graph['State'] == totalcases]['Confirmed'].iloc[-1]
    active = Cumulative_graph[Cumulative_graph['State'] == totalcases]['Active'].iloc[-1]
    recovered = Cumulative_graph[Cumulative_data_graph['State'] == totalcases]['Recovered'].iloc[-1]
    deceased = Cumulative_graph[Cumulative_data_graph['State'] == totalcases]['Deceased'].iloc[-1]
    colors = ['#ef5b60','#237bfa','#53a844','#798189']
    fig = go.Figure(go.Pie(labels=['Confirmed','Active','Recovered','Deceased'],
                          values=[confirmed,active,recovered,deceased],
                          marker=dict(colors=colors),
                          hoverinfo='label+percent',
                          textinfo='label+percent',
                          textfont=dict(size=13),
                          hole=.5,
                          rotation=45))
    fig.update_layout(hoverlabel_font_color='#ffffff',legend={'orientation': 'h','xanchor': 'center', 'x': 0.5, 'y': -0.07},
                     font=dict(family="Ubuntu",size=14,),margin = dict(t=20,b=15))
    return fig

#Cumulative_bar_graph_char
@app.callback(
    Output('Confirmed', 'figure'),
    [Input('totalcases', 'value')])
def confirmed_output(totalcases):
    date = Cumulative_graph[Cumulative_graph['State'] == totalcases]['Date']
    confirmed = Cumulative_graph[Cumulative_graph['State'] == totalcases]['Confirmed']
    fig = go.Figure(go.Line(x=date, y=confirmed,marker=dict(color='#ef5b60'),line = dict(width=3),mode='lines+markers',
    text='<b>Date</b>: ' + date.astype(str) + '<br>' + '<b>Confirmed</b>: ' + [f'{x:,.0f}' for x in confirmed] + '<br>',
    hoverinfo='text'))
    fig.update_xaxes(title=None,showgrid = False,fixedrange=True,linecolor='#ef5b60',
    linewidth=2,ticks='outside',tickfont=dict(family='Arial',size=12,color='#ef5b60'))
    fig.update_yaxes(side="right",showgrid = False,fixedrange=True,linecolor='#ef5b60',
    linewidth=2,ticks='outside',tickfont=dict(family='Arial',size=12,color='#ef5b60'))
    fig.update_layout(hoverlabel_font_color='#ffffff',plot_bgcolor='#f9e0e5',hovermode='x',margin = dict(t=15,b=15,r=15,l=15),paper_bgcolor='#f9e0e5')
    fig.update_traces(fill="tonexty", selector=dict(type='scatter'))
    fig.add_annotation(text="Confirmed",xref="paper", yref="paper",x=0.01,y=0.99 ,showarrow=False,font=dict(size=13,))
    return fig


@app.callback(
    Output('Active', 'figure'),
    [Input('totalcases', 'value')])
def active_output(totalcases):
    date = Cumulative_graph[Cumulative_graph['State'] == totalcases]['Date']
    active = Cumulative_graph[Cumulative_graph['State'] == totalcases]['Active']
    fig = go.Figure(go.Line(x=date, y=active,marker=dict(color='#237bfa'),line = dict(width=3),mode='lines+markers',
    text='<b>Date</b>: ' + date.astype(str) + '<br>' + '<b>Active</b>: ' + [f'{x:,.0f}' for x in active] + '<br>',
    hoverinfo='text'))
    fig.update_xaxes(title=None,showgrid = False,fixedrange=True,linecolor='#237bfa',
    linewidth=2,ticks='outside',tickfont=dict(family='Arial',size=12,color='#237bfa'))
    fig.update_yaxes(side="right",showgrid = False,fixedrange=True,linecolor='#237bfa',
    linewidth=2,ticks='outside',tickfont=dict(family='Arial',size=12,color='#237bfa'))
    fig.update_layout(hoverlabel_font_color='#ffffff',plot_bgcolor='#f0f6fe',hovermode='x',margin = dict(t=15,b=15,r=15,l=15),paper_bgcolor='#f0f6fe')
    fig.update_traces(fill="tonexty", selector=dict(type='scatter'))
    fig.add_annotation(text="Active",xref="paper", yref="paper",x=0.01,y=0.99 ,showarrow=False,font=dict(size=13,))
    return fig

@app.callback(
    Output('Recovered', 'figure'),
    [Input('totalcases', 'value')])
def recovered_output(totalcases):
    date = Cumulative_graph[Cumulative_graph['State'] == totalcases]['Date']
    recovered = Cumulative_graph[Cumulative_graph['State'] == totalcases]['Recovered']
    fig = go.Figure(go.Line(x=date, y=recovered,marker=dict(color='#53a844'),line = dict(width=3),mode='lines+markers',
    text='<b>Date</b>: ' + date.astype(str) + '<br>' + '<b>Recovered</b>: ' +  [f'{x:,.0f}' for x in recovered] + '<br>',
    hoverinfo='text'))
    fig.update_xaxes(title=None,showgrid = False,fixedrange=True,linecolor='#53a844',
    linewidth=2,ticks='outside',tickfont=dict(family='Arial',size=12,color='#53a844'))
    fig.update_yaxes(side="right",showgrid = False,fixedrange=True,linecolor='#53a844',
    linewidth=2,ticks='outside',tickfont=dict(family='Arial',size=12,color='#53a844'))
    fig.update_layout(hoverlabel_font_color='#ffffff',plot_bgcolor='#e4f4e7',hovermode='x',margin = dict(t=15,b=15,r=15,l=15),paper_bgcolor='#e4f4e7',)
    fig.update_traces(fill="tonexty", selector=dict(type='scatter'))
    fig.add_annotation(text="Recovered",xref="paper", yref="paper",x=0.01,y=0.99 ,showarrow=False,font=dict(size=13,))
    return fig

@app.callback(
    Output('Deceased', 'figure'),
    [Input('totalcases', 'value')])
def deceased_output(totalcases):
    date = Cumulative_graph[Cumulative_graph['State'] == totalcases]['Date']
    deceased = Cumulative_graph[Cumulative_graph['State'] == totalcases]['Deceased']
    fig = go.Figure(go.Line(x=date, y=deceased,marker=dict(color='#798189'),line = dict(width=3),mode='lines+markers',
    text='<b>Date</b>: ' + date.astype(str) + '<br>' + '<b>Deceased</b>: ' + [f'{x:,.0f}' for x in deceased] + '<br>',
    hoverinfo='text'))
    fig.update_xaxes(title=None,showgrid = False,fixedrange=True,linecolor='#798189',title_font_color='#798189',
    linewidth=2,ticks='outside',tickfont=dict(family='Arial',size=12,color='#798189'))
    fig.update_yaxes(side="right",showgrid = False,fixedrange=True,linecolor='#798189',
    linewidth=2,ticks='outside',tickfont=dict(family='Arial',size=12,color='#798189'))
    fig.update_layout(hoverlabel_font_color='#ffffff',plot_bgcolor='#f6f6f7',hovermode='x',margin = dict(t=15,b=15,r=15,l=15),paper_bgcolor='#f6f6f7',)
    fig.update_traces(fill="tonexty", selector=dict(type='scatter'))
    fig.add_annotation(text="Death",xref="paper", yref="paper",x=0.01,y=0.99 ,showarrow=False,font=dict(size=13,))
    return fig


#pie_chat
@app.callback(
    Output('pie_chart_daily','figure'),
    [Input('totalcases', 'value')])
def pie_chat_daily_output(totalcases):
    confirmed = Cumulative_data_graph[Cumulative_data_graph['State'] == totalcases]['Confirmed']
    Confirmed = list(confirmed)
    recovered = Cumulative_data_graph[Cumulative_data_graph['State'] == totalcases]['Recovered']
    Recovered = list(recovered)
    deceased = Cumulative_data_graph[Cumulative_data_graph['State'] == totalcases]['Deceased']
    Deceased = list(deceased)
    dialy_confirmed = Confirmed[-2] - Confirmed[-3]
    dialy_recovered = Recovered[-2] - Recovered[-3]
    dialy_deceased = Deceased[-2] - Deceased[-3]
    colors = ['#ef5b60','#53a844','#798189']
    fig = go.Figure(go.Pie(labels=['Confirmed','Recovered','Deceased'],
                          values=[dialy_confirmed,dialy_recovered,dialy_deceased],
                          marker=dict(colors=colors),
                          hoverinfo='label+percent',
                          textinfo='label+percent',
                          textfont=dict(size=13),
                          hole=.5,
                          rotation=45))
    fig.update_layout(hoverlabel_font_color='#ffffff',legend={'orientation': 'h','xanchor': 'center', 'x': 0.5, 'y': -0.07},
                     font=dict(family="Ubuntu",size=14,),margin = dict(t=20,b=15))
    return fig

#daily_bar_graph_char
@app.callback(
    Output('daily-confirmed', 'figure'),
    [Input('totalcases', 'value')])
def Confirmed_update_output(totalcases):
    fig = px.bar(Confirmed,x='Date_YMD', y=totalcases)
    fig.update_traces(marker_color='#ef5b60',hovertemplate='<b>Date</b>: ' + Confirmed['Date_YMD'].astype(str) + '<br>' +  '<b>Confirmed</b>: %{y:,.0f}' + '<br>',)
    fig.update_xaxes(title=None,showgrid = False,fixedrange=True,linecolor='#ef5b60',
    linewidth=2,ticks='outside',tickfont=dict(size=12,color='#ef5b60'))
    fig.update_yaxes(title=None,side="right",showgrid = False,fixedrange=True,linecolor='#ef5b60',
    linewidth=2,ticks='outside',tickfont=dict(size=12,color='#ef5b60'))
    fig.update_layout(hoverlabel_font_color='#ffffff',plot_bgcolor='#f9e0e5',hovermode='x',margin = dict(t=15,b=15,r=15,l=15),paper_bgcolor='#f9e0e5')
    fig.add_annotation(text="Confirmed",xref="paper", yref="paper",x=0.01,y=0.99 ,showarrow=False,font=dict(size=13,))
    return fig
             
@app.callback(
    Output('daily-recovered', 'figure'),
    [Input('totalcases', 'value')])
def Recovered_update_output(totalcases):
    fig = px.bar(Recovered,x='Date_YMD', y=totalcases)
    fig.update_traces(marker_color='#53a844',hovertemplate='<b>Date</b>: ' + Confirmed['Date_YMD'].astype(str) + '<br>' +  '<b>Confirmed</b>: %{y:,.0f}' + '<br>',)
    fig.update_xaxes(title=None,showgrid = False,fixedrange=True,linecolor='#53a844',
    linewidth=2,ticks='outside',tickfont=dict(size=12,color='#53a844'))
    fig.update_yaxes(title=None,side="right",showgrid = False,fixedrange=True,linecolor='#53a844',
    linewidth=2,ticks='outside',tickfont=dict(size=12,color='#53a844'))
    fig.update_layout(hoverlabel_font_color='#ffffff',plot_bgcolor='#e4f4e7',hovermode='x',margin = dict(t=15,b=15,r=15,l=15),paper_bgcolor='#e4f4e7',)
    fig.add_annotation(text="Recovered",xref="paper", yref="paper",x=0.01,y=0.99 ,showarrow=False,font=dict(size=13,))
    return fig
             
@app.callback(
    Output('daily-deceased', 'figure'),
    [Input('totalcases', 'value')])
def Death_update_output(totalcases):
    fig = px.bar(Deceased,x='Date_YMD', y=totalcases)
    fig.update_traces(marker_color='#798189',hovertemplate='<b>Date</b>: ' + Confirmed['Date_YMD'].astype(str) + '<br>' +  '<b>Confirmed</b>: %{y:,.0f}' + '<br>',)
    fig.update_xaxes(title=None,showgrid = False,fixedrange=True,linecolor='#798189',title_font_color='#798189',
    linewidth=2,ticks='outside',tickfont=dict(size=12,color='#798189'))
    fig.update_yaxes(title=None,side="right",showgrid = False,fixedrange=True,linecolor='#798189',
    linewidth=2,ticks='outside',tickfont=dict(size=12,color='#798189'))
    fig.update_layout(hoverlabel_font_color='#ffffff',plot_bgcolor='#f6f6f7',hovermode='x',margin = dict(t=15,b=15,r=15,l=15),paper_bgcolor='#f6f6f7',)
    fig.add_annotation(text="Death",xref="paper", yref="paper",x=0.01,y=0.99 ,showarrow=False,font=dict(size=13,))
    return fig

#options_button
@app.callback(
    Output('Daily_cases', 'style'),
    Output('Cumulative_cases', 'style'),
    [Input('show-table', 'value')])
def toggle_container(toggle_value):
    #print(toggle_value, flush=True)
    if toggle_value == 'Daily':
        dialy_cases =[{'display': 'block'},{'display': 'none'}]
        time.sleep(2)
        return dialy_cases
    else:
        cumulative_cases =[{'display': 'none'},{'display': 'block'}]
        time.sleep(2)
        return cumulative_cases
    
if __name__ == '__main__':
    app.run_server(debug=True)
