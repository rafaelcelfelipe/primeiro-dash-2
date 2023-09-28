from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import dash
from app import *
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

 
import plotly.express as px
import plotly.graph_objects as go

load_figure_template("minty")


app = dash.Dash(external_stylesheets=[dbc.themes.MINTY])
server = app.server


df_data = pd.read_csv('supermarket_sales.csv')
df_data['Date'] = pd.to_datetime(df_data['Date'])


app.layout = dbc.Container(children=[
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        [
                            html.H2('Análise de Vendas', style={'font-family': 'Voltaire', 'font-size': '50px', 'text-align': 'center'}),

                            html.Hr(),

                            html.H5('Cidades:', style={'font-size': '30px', 'text-align': 'center', 'padding-top': '20px'}),

                            dcc.Checklist(df_data['City'].value_counts().index, df_data['City'].value_counts().index, id= 'check_city', 
                            inputStyle={'font-size': '20px', 'text-align': 'center', "margin-right": "5px", "margin-left": "20px"},
                            labelStyle={'display': 'block', 'verticalAlign': 'middle'}, className='checklist'),
                            
                            html.Hr(),

                            html.H5('Variável de análise:', style={'font-size': '30px', 'margin-top': '20px', 'text-align': 'center'}),

                            dcc.RadioItems(['gross income', 'Rating'], 'gross income', id='main_variable', 
                            inputStyle={'font-size': '20px', 'text-align': 'center', "margin-right": "5px", "margin-left": "20px"},
                            labelStyle={'display': 'inline-block'})

                        ], style={'padding': '40px', 'height': '100vh', 'align-itens': 'center'})
                    
                        ], md= 3),

                dbc.Col(
                    [
                        dbc.Row([
                            dbc.Col([dcc.Graph(id='city_fig')], md= 4),
                            dbc.Col([dcc.Graph(id='gender_fig')], md= 4),
                            dbc.Col([dcc.Graph(id='pay_fig')], md= 4)
                        ], style={'padding-top': '20px'}),
                        html.Hr(),
                        dbc.Row([dcc.Graph(id='income_per_date_fig')]),
                        html.Hr(),
                        dbc.Row([dcc.Graph(id='income_per_product_fig')])
                ])
            ])  
        ])


@app.callback([
    Output('city_fig', 'figure'),
    Output('gender_fig', 'figure'),
    Output('pay_fig', 'figure'),
    Output('income_per_date_fig', 'figure'),
    Output('income_per_product_fig', 'figure')
],
               [
    Input('check_city', 'value'),
    Input('main_variable', 'value')
               ])
                  
def render_page_content(cities, main_variable):
    operation = np.sum if main_variable == 'gross income' else np.mean
    df_filtered = df_data[df_data['City'].isin(cities)]

    df_city = df_filtered.groupby('City')[main_variable].apply(operation).to_frame().reset_index()
    df_gender = df_filtered.groupby(['Gender', 'City'])[main_variable].apply(operation).to_frame().reset_index()
    df_payment = df_filtered.groupby('Payment')[main_variable].apply(operation).to_frame().reset_index()
    df_product_income_date = df_filtered.groupby('Date')[main_variable].apply(operation).to_frame().reset_index()
    df_product_income = df_filtered.groupby(['Product line','City'])[main_variable].apply(operation).to_frame().reset_index()

    fig_city = px.bar(df_city, x='City', y=main_variable)
    fig_gender = px.bar(df_gender, x='Gender', y=main_variable, barmode= 'group', color='City')
    fig_payment = px.bar(df_payment, y='Payment', x=main_variable, orientation='h')
    fig_product_income_date = px.bar(df_product_income_date, x='Date', y=main_variable)
    fig_product_income = px.bar(df_product_income, x=main_variable, y='Product line', color='City', orientation='h', barmode= 'group')
   
    for fig in [fig_city, fig_gender, fig_payment,fig_product_income_date]:
        fig.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=200)

    fig_product_income.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=300)

    return fig_city, fig_gender, fig_payment, fig_product_income_date, fig_product_income



if __name__ == '__main__':
    app.run_server(port=8052, debug=False)

