# -*- coding: utf-8 -*-


import pandas as pd
import plotly.express as px
import streamlit as st

from data_clean import data

#Importando o dataset

#data = pd.read_csv('Data.csv')
gallego_data = data.copy()

#Tratando o dataset

#gallego_data.drop(['Invoice ID','Branch','Tax 5%','cogs','gross margin percentage'], axis = 1, inplace = True)
#gallego_data['Datetime'] = gallego_data['Date'] + ' ' + gallego_data['Time']
#gallego_data['Date'] = pd.to_datetime(gallego_data['Date'])
#gallego_data['Datetime'] = pd.to_datetime(gallego_data['Datetime'])
#gallego_data.drop('Time', axis =1, inplace = True)

#Criando a copia do data para quarto quartil

gallego_data_clientes = gallego_data.copy()

#Gerando o data exclusivo para quarto quartil

gallego_q3 = gallego_data_clientes['Total'].quantile(0.75)
gallego_quartil_quatro = gallego_data_clientes[gallego_data_clientes['Total'] > gallego_q3]

#Grafico customer type quarto quartil

def customer_type_q4(cidade, produto, total):
    if not total:
        # Filtragem por cidade e produto
        df_filtered = gallego_quartil_quatro[gallego_quartil_quatro['City'] == cidade]
        df_filtered_2 = df_filtered[df_filtered['Product line'] == produto]

        # Agrupar por tipo de cliente e somar o total de vendas
        grouped_data = df_filtered_2.groupby('Customer type')['Total'].sum().reset_index()

        title = f'Receita por Tipo de Cliente (4° Quartil) de {produto} em {cidade}'

    else:
        # Agrupar por tipo de cliente e somar o total de vendas sem filtros
        grouped_data = gallego_quartil_quatro.groupby('Customer type')['Total'].sum().reset_index()

        title = 'Receita por Tipo de Cliente (4º Quartil) Total'

    # Criar o gráfico de barras usando Plotly
    fig = px.bar(grouped_data, x='Customer type', y='Total')

    # Adicionar título e rótulos aos eixos
    fig.update_layout(
        title=title,
        xaxis_title='Tipo de Cliente',
        yaxis_title='Receita',
        template = 'plotly_dark'
    )

    # Mostrar o gráfico
    return fig

#Grafico genero quarto quartil


def gender_q4(cidade, produto, total):
    if not total:
        # Filtragem por cidade e produto
        df_filtered = gallego_quartil_quatro[gallego_quartil_quatro['City'] == cidade]
        df_filtered_2 = df_filtered[df_filtered['Product line'] == produto]

        # Agrupar por gênero e somar o total de vendas
        grouped_data = df_filtered_2.groupby('Gender')['Total'].sum().reset_index()

        title = f'Receita por Gênero (4° Quartil) de {produto} em {cidade}'
    else:
        # Agrupar por gênero e e somar o total de vendas sem filtros
        grouped_data = gallego_quartil_quatro.groupby('Gender')['Total'].sum().reset_index()

        title = 'Receita por Gênero (4º Quartil) Total'

    # Criar o gráfico de barras usando Plotly
    color_map = {'Female': 'red', 'Male': 'blue'}  # Mapeamento de cores
    fig = px.bar(grouped_data, x='Gender', y='Total', color='Gender')




    # Adicionar título e rótulos aos eixos
    fig.update_layout(
        title=title,
        xaxis_title='Gênero',
        yaxis_title='Receita',
        template = 'plotly_dark'
    )
    # Mostrar o gráfico
    return fig