import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

from data_analysis_nontemporal import *
from data_clean import data
from quarto_quartil_graficos import *

# Dados Consolidados

# 0 - Título

def set_title(cidade, produto, total):
    if not total:
        return f"{cidade} - {produto}"
    else:
        return "Total"

# 1 - Quanto Vendeu no total

def sales_amount(df, cidade, produto, total):
    df_filtered = df[df['City'] == cidade]
    df_filtered_2 = df_filtered[df_filtered['Product line'] == produto]

    if not total:
        return df_filtered_2['Quantity'].sum()
    
    else:
        return df['Quantity'].sum()

# 2 - Gross income

def gross_income(df, cidade, produto, total):
    df_filtered = df[df['City'] == cidade]
    df_filtered_2 = df_filtered[df_filtered['Product line'] == produto]

    if not total:
        return f"$ {round(df_filtered_2['gross income'].sum()/1000,2)} K"
    
    else:
        return f"$ {round(df['gross income'].sum()/1000,2)} K"


# 3 - Total de vendas

def returns(df, cidade, produto, total):
    df_filtered = df[df['City'] == cidade]
    df_filtered_2 = df_filtered[df_filtered['Product line'] == produto]

    if not total:
        return f"$ {round(df_filtered_2['Total'].sum()/1000,2)} K"
    
    else:
        return f"$ {round(df['Total'].sum()/1000,2)} K"

# 4 - Ranking de venda dos produtos

def ranking(df, cidade, total):
    df_filtered = df[df['City'] == cidade]
    #df_filtered_2 = df_filtered[df_filtered['Product line'] == produto]

    if total:

        df_income = data.groupby('Product line')['Total'].sum()
        df_income.sort_values(ascending = False, inplace  = True)
        df_income = pd.DataFrame(df_income)
        df_income['% Change'] = df_income['Total'].pct_change()
        df_income['% Change']['Food and beverages'] = 0
        df_income['% Change'] = df_income['% Change'].apply(lambda x: str(round(x*100,3)) + '%')
    
    else:
        df_income = df_filtered.groupby('Product line')['Total'].sum()
        df_income.sort_values(ascending = False, inplace  = True)
        df_income = pd.DataFrame(df_income)
        df_income['% Change'] = df_income['Total'].pct_change()
        df_income['% Change']['Food and beverages'] = 0
        df_income['% Change'] = df_income['% Change'].apply(lambda x: str(round(x*100,3)) + '%')


    return df_income


# 5 - Rating por cidade

def city_rating(df, produto, total):

    if not total:

        df_filtered = df[df['Product line'] == produto]

        rating_cidade = df_filtered.groupby('City')['Rating'].mean().reset_index()
        fig_rating = px.bar(rating_cidade, x='City', y='Rating', template='plotly_dark')
        fig_rating.update_layout(
            title=f'Rating por Cidade produto {produto}',
            xaxis_title='Cidade',
            template = 'plotly_dark',
            yaxis_title='Rating'
        )
    
    else:
        rating_cidade = df.groupby('City')['Rating'].mean().reset_index()   
        fig_rating = px.bar(rating_cidade, x='City', y='Rating', template = 'plotly_dark')
        fig_rating.update_layout(
            title='Rating por Cidade total',
            template = 'plotly_dark',
            xaxis_title='Cidade',
            yaxis_title='Rating'
            )
    
    return fig_rating

def rosca(df, produto, cidade, total):
    if not total:
        data_filtrada = df[df['Product line'] == produto]
        data_cidade_pagamento = data_filtrada[data_filtrada['City'] == cidade].groupby(['Payment']).size()
        fig = px.pie(data_cidade_pagamento, values=data_cidade_pagamento.values, names=data_cidade_pagamento.index,
                title=f"Formas de pagamento em {cidade} ({produto})",
                hole=0.5)
        
        fig.update_layout(template = 'plotly_dark')
        return fig
    else:
        data_cidade_pagamento = df.groupby(['Payment']).size()
        fig = px.pie(data_cidade_pagamento, values=data_cidade_pagamento.values,    
                     names = data_cidade_pagamento.index,
                     title="Formas de pagamento total",
                     hole=0.5)
        fig.update_layout(template = 'plotly_dark')
        #fig.update_layout(width = 600, height = 400)
        return fig

def timeseries_month(df, produto, cidade, total):   
    gallego_data_temporal1 = df.copy()
    gallego_data_temporal2 = df.copy()
    # Criar uma nova coluna com o mês e ano no formato string para os dois datasets
    gallego_data_temporal1['Month'] = gallego_data_temporal1['Date'].dt.to_period('M').astype(str)
    gallego_data_temporal2['Month'] = gallego_data_temporal2['Date'].dt.to_period('M').astype(str)

    if not total:
              df_filtered1 = gallego_data_temporal1[gallego_data_temporal1['Product line'] == produto]
              df_filtered_aux1 = df_filtered1[df_filtered1['City'] == cidade]

              # Agrupar por mês e somar a coluna 'Quantity' para o primeiro gráfico
              monthly_quantity = df_filtered_aux1.groupby('Month')['Quantity'].sum()

              # Agrupar por mês e somar a coluna 'gross income' para o segundo gráfico
              monthly_income = df_filtered_aux1.groupby('Month')['gross income'].sum()

              # Criar a figura
              fig = go.Figure()

              # Adicionar o primeiro traço (Quantidade vendida) como barras
              fig.add_trace(go.Bar(x=monthly_quantity.index, y=monthly_quantity.values, name='Quantidade vendida'))

              # Adicionar o segundo traço (Lucro), utilizando o segundo eixo y como linhas
              fig.add_trace(go.Scatter(x=monthly_income.index, y=monthly_income.values, mode='markers+lines', marker=dict(size=20),
                                        line=dict(dash='dash'), yaxis='y2', name='Lucro'))

              # Atualizar o layout com dois eixos y
              fig.update_layout(
                  title="Vendas Totais e Lucro ao longo do Ano",
                  xaxis=dict(title="Mês"),
                  yaxis=dict(title="Quantidade", showgrid=False),
                  yaxis2=dict(title="Lucro", overlaying="y", side="right"),
                  template="plotly_dark",
                  legend=dict(x=1, y=1.1)
              )
               # Exibir o gráfico
              return fig
    if total:
              monthly_quantity = gallego_data_temporal1.groupby('Month')['Quantity'].sum()

              # Agrupar por mês e somar a coluna 'gross income' para o segundo gráfico
              monthly_income = gallego_data_temporal2.groupby('Month')['gross income'].sum()

              # Criar a figura
              fig = go.Figure()

              # Adicionar o primeiro traço (Quantidade vendida) como barras
              fig.add_trace(go.Bar(x=monthly_quantity.index, y=monthly_quantity.values, name='Quantidade vendida'))

              # Adicionar o segundo traço (Lucro), utilizando o segundo eixo y como linhas
              fig.add_trace(go.Scatter(x=monthly_income.index, y=monthly_income.values, mode='markers+lines', marker=dict(size=20),
                                        line=dict(dash='dash'), yaxis='y2', name='Lucro'))
              fig.update_layout(
                  title="Vendas Totais e Lucro ao longo do Ano",
                  xaxis=dict(title="Mês"),
                  yaxis=dict(title="Quantidade", showgrid=False),
                  yaxis2=dict(title="Lucro", overlaying="y", side="right"),
                  template="plotly_dark",
                  legend=dict(x=1, y=1.1)
              )
              return fig

def vendas_e_lucro_por_mes(df, produto_escolhido, mes, cidade, total):

    if not total:
        # Filtragem do dataframe pelo produto escolhido
        data_produto = df.loc[df['Product line'] == produto_escolhido]
        # Filtragem do dataframe pelo mês atual
        produto_meses = data_produto.loc[data_produto['Date'].dt.month == mes]

        # Filtragem por cidade

        produto_cidade = produto_meses[produto_meses['City'] == cidade]
        # Agrupamento por dia do mês e contagem de vendas
        vendas_por_mes = produto_cidade.groupby(produto_cidade['Date'].dt.day).size()
        # Agrupamento por dia do mês e soma do lucro
        lucro_por_mes = produto_cidade.groupby(produto_cidade['Date'].dt.day)['gross income'].sum()
        # Criação do gráfico com duas linhas (vendas e lucro)
        fig = go.Figure()
        # Linha para vendas
        fig.add_trace(go.Scatter(
            x=vendas_por_mes.index, y=vendas_por_mes.values, mode='lines+markers', name='Vendas',
            line=dict()))
        # Linha para lucro
        fig.add_trace(go.Scatter(
            x=lucro_por_mes.index, y=lucro_por_mes.values, mode='lines+markers', name='Lucro',
            line=dict(), yaxis='y2'))
        # Customização do layout
        fig.update_layout(
            title=f'Vendas e Lucro de {produto_escolhido} por dia do mês {mes} de 2019',
            xaxis_title=f'Dias do mês {mes}',
            yaxis_title='Quantidade',
            yaxis2=dict(title="Lucro", overlaying="y", side="right"),
            showlegend=True,
            template = 'plotly_dark',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False)
        )
        return fig
    else:
                # Agrupamento por dia do mês e contagem de vendas
        vendas_por_mes = df.groupby(df['Date'].dt.day).size()
        # Agrupamento por dia do mês e soma do lucro
        lucro_por_mes = df.groupby(df['Date'].dt.day)['gross income'].sum()
        # Criação do gráfico com duas linhas (vendas e lucro)
        fig = go.Figure()
        # Linha para vendas
        fig.add_trace(go.Scatter(
            x=vendas_por_mes.index, y=vendas_por_mes.values, mode='lines+markers', name='Vendas',
            line=dict()))
        # Linha para lucro
        fig.add_trace(go.Scatter(
            x=lucro_por_mes.index, y=lucro_por_mes.values, mode='lines+markers', name='Lucro',
            line=dict(), yaxis='y2'))
        # Customização do layout
        fig.update_layout(
            title=f'Vendas e Lucro Totais por dia do mês {mes} de 2019',
            xaxis_title=f'Dias do mês {mes}',
            yaxis_title='Quantidade',
            yaxis2=dict(title="Lucro", overlaying="y", side="right"),
            showlegend=True,
            template = 'plotly_dark',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False)
        )
        return fig

                

def timeseries_year(df, produto, cidade, total):
        
        if not total:
            df_filtered = df[df['Product line'] == produto]
            df_filtered_aux = df_filtered[df_filtered['City'] == cidade]
            df_filtered_aux.sort_values(by = 'Date', inplace = True)
            df_filtered_aux_quantity = df_filtered_aux.groupby('Date')['Quantity'].sum()
            df_filtered_aux_profit = df_filtered_aux.groupby('Date')['gross income'].sum()

            # Construindo o gráfico

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_filtered_aux_quantity.index, y=df_filtered_aux_quantity.values, mode='lines',
                                     name = 'Quantidade vendida'))
            fig.add_trace(go.Scatter(x = df_filtered_aux_profit.index, y = df_filtered_aux_profit.values, mode = 'lines', 
                                    name = 'Lucro',
                                    line = dict(),
                                    yaxis='y2'))
            
            fig.update_layout(
            title = f"Vendas de {produto} em {cidade} ao longo do Ano",
            #xaxis = dict(title="Date"),
            yaxis = dict(title="Quantidade", showgrid = False),
            yaxis2 = dict(title="Lucro", overlaying = "y", side = "right"),
            template = "plotly_dark",
            legend = dict(x=1,y=1.1))

            fig.update_layout(
            legend=dict(
                orientation="h",  # Define a orientação como horizontal
                yanchor="bottom",  # Alinha a legenda ao fundo
                y=-0.2,           # Ajusta a posição vertical da legenda
                xanchor="center",  # Alinha a legenda ao centro horizontalmente
                x=0.5             # Coloca a legenda no centro horizontal
                        )
)

            return fig
        
        else:
            df.sort_values(by = 'Date', inplace = True)
            df_quantity = df.groupby('Date')['Quantity'].sum()
            df_profit = df.groupby('Date')['gross income'].sum()

            fig = go.Figure()
            fig.add_trace(go.Scatter(x= df_quantity.index, y=df_quantity.values, mode='lines', name = 'Quantidade vendida'))
            fig.add_trace(go.Scatter(x = df_profit.index, y = df_profit.values, mode = 'lines', line = dict(), yaxis = 'y2',
                                     name = 'Lucro'))

            fig.update_layout(
            title = f"Vendas Totais ao longo do Ano",
            #xaxis = dict(title="Date"),
            yaxis = dict(title="Quantidade", showgrid = False),
            yaxis2 = dict(title="Lucro", overlaying = "y", side = "right"),
            template = "plotly_dark",
            legend = dict(x=1,y=1.1))

            fig.update_layout(
            legend=dict(
                orientation="h",  # Define a orientação como horizontal
                yanchor="bottom",  # Alinha a legenda ao fundo
                y=-0.2,           # Ajusta a posição vertical da legenda
                xanchor="center",  # Alinha a legenda ao centro horizontalmente
                x=0.5             # Coloca a legenda no centro horizontal
                        )
)

            return fig
        

def timeseries_day(df, produto, cidade, total):
    if not total:
        df_filtered = df[df['Product line'] == produto]
        df_filtered_aux = df_filtered[df_filtered['City'] == cidade]
        df_filtered_aux.loc[:, 'Hour'] = df_filtered_aux['Datetime'].dt.hour

        quantidade = df_filtered_aux.groupby('Hour')['Quantity'].sum()
        lucro = df_filtered_aux.groupby('Hour')['gross income'].sum()

        figure = px.bar(quantidade, x=quantidade.index, y=quantidade.values, title= f'Vendas de {produto} em {cidade} durante dia', 
            labels={'Hour': 'Horas'})
        figure.add_trace(go.Scatter(x = lucro.index, y = lucro.values, mode = 'lines+markers', 
                                    name = 'Lucro',
                                    line = dict(),
                                    yaxis='y2'))
        figure.update_layout(
            title = f"Vendas de {produto} em {cidade} durante dia",
            #xaxis = dict(title="Date"),
            yaxis = dict(title="Quantidade", showgrid = False),
            yaxis2 = dict(title="Lucro", overlaying = "y", side = "right"),
            template = "plotly_dark",
            legend = dict(x=1,y=1.1))
        
        figure.update_layout(template = 'plotly_dark')
        return figure
    if total:
        df_filtered_aux = df.copy()
        quantidade = df_filtered_aux.groupby('Hour')['Quantity'].sum()
        lucro = df_filtered_aux.groupby('Hour')['gross income'].sum()

        figure = px.bar(quantidade, x=quantidade.index, y=quantidade.values, title= f'Vendas de {produto} em {cidade} durante dia', 
            labels={'Hour': 'Horas'})
        figure.add_trace(go.Scatter(x = lucro.index, y = lucro.values, mode = 'lines+markers', 
                                    name = 'Lucro',
                                    line = dict(),
                                    yaxis='y2'))
        figure.update_layout(
            title = f"Vendas em {cidade} durante dia",
            #xaxis = dict(title="Date"),
            yaxis = dict(title="Quantidade", showgrid = False),
            yaxis2 = dict(title="Lucro", overlaying = "y", side = "right"),
            template = "plotly_dark",
            legend = dict(x=1,y=1.1))
        figure.update_layout(template = 'plotly_dark')
        return figure
        

def timeseries_week(df, produto, cidade, total):
    if not total:
        df_filtered = df[df['Product line'] == produto]
        df_filtered_aux = df_filtered[df_filtered['City'] == cidade]
        quantidade = df_filtered_aux.groupby(df_filtered_aux['Datetime'].dt.to_period('W'))['Quantity'].size()
        lucro = df_filtered_aux.groupby(df_filtered_aux['Datetime'].dt.to_period('W'))['gross income'].sum()

        quantidade_semanal = quantidade.reset_index(name='Count')
        quantidade_semanal['Week of Month'] = (quantidade_semanal.index % 4) + 1
        quantidade_semanal = quantidade_semanal.rename(columns={'Datetime': 'Week'})
        quantidade_semanal['Week'] = quantidade_semanal['Week'].astype(str)
        quantidade_semanal['Week of Month'] = quantidade_semanal['Week of Month'].astype(str)

        lucro_semanal = lucro.reset_index(name='Count')
        lucro_semanal['Week of Month'] = (lucro_semanal.index % 4) + 1
        lucro_semanal = lucro_semanal.rename(columns={'Datetime': 'Week'})
        lucro_semanal['Week'] = lucro_semanal['Week'].astype(str)

        figure = px.bar(quantidade_semanal, x=(quantidade_semanal.index+1), y='Count', title=f'Vendas de {produto} em {cidade} na semana', 
            labels={'x': 'Semana', 'Count': 'Quantidade'}, color='Week of Month')
        figure.add_trace(go.Scatter(x = (lucro_semanal.index+1), y = lucro_semanal['Count'], mode = 'lines+markers', 
                                    name = 'Lucro',
                                    line = dict(),
                                    yaxis='y2'))
        
        figure.update_layout(
            title = f"Vendas de {produto} em {cidade} pelas semanas",
            #xaxis = dict(title="Date"),
            yaxis = dict(title="Quantidade", showgrid = False),
            yaxis2 = dict(title="Lucro", overlaying = "y", side = "right"),
            template = "plotly_dark",
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5) # Legend at bottom)
        )

        figure.update_layout(template = 'plotly_dark')
        return figure
    else:
        df_filtered_aux = df.copy()
        quantidade = df_filtered_aux.groupby(df_filtered_aux['Datetime'].dt.to_period('W'))['Quantity'].size()
        lucro = df_filtered_aux.groupby(df_filtered_aux['Datetime'].dt.to_period('W'))['gross income'].sum()

        quantidade_semanal = quantidade.reset_index(name='Count')
        quantidade_semanal['Week of Month'] = (quantidade_semanal.index % 4) + 1
        quantidade_semanal = quantidade_semanal.rename(columns={'Datetime': 'Week'})
        quantidade_semanal['Week'] = quantidade_semanal['Week'].astype(str)
        quantidade_semanal['Week of Month'] = quantidade_semanal['Week of Month'].astype(str)

        lucro_semanal = lucro.reset_index(name='Count')
        lucro_semanal['Week of Month'] = (lucro_semanal.index % 4) + 1
        lucro_semanal = lucro_semanal.rename(columns={'Datetime': 'Week'})
        lucro_semanal['Week'] = lucro_semanal['Week'].astype(str)

        figure = px.bar(quantidade_semanal, x=(quantidade_semanal.index+1), y='Count', title=f'Vendas de {produto} em {cidade} na semana', 
            labels={'x': 'Semana', 'Count': 'Quantidade'}, color='Week of Month')
        figure.add_trace(go.Scatter(x = (lucro_semanal.index+1), y = lucro_semanal['Count'], mode = 'lines+markers', 
                                    name = 'Lucro',
                                    line = dict(),
                                    yaxis='y2'))
        
        figure.update_layout(
            title = f"Vendas em {cidade} pelas semanas",
            #xaxis = dict(title="Date"),
            yaxis = dict(title="Quantidade", showgrid = False),
            yaxis2 = dict(title="Lucro", overlaying = "y", side = "right"),
            template = "plotly_dark",
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5) # Legend at bottom))
        )

        figure.update_layout(template = 'plotly_dark')
        return figure


def rosca_clientes(df):
    data_gender = df.groupby(['Gender', 'Customer type']).agg({'gross income': 'sum'}).reset_index()
    data_gender.rename(columns={'gross income': 'Total Gross Income'}, inplace=True)

    data_gender['Gender_Status'] = data_gender['Gender'] + ' - ' + data_gender['Customer type']
    figure = px.pie(data_gender, values='Total Gross Income', names='Gender_Status', width=600, title='Lucro bruto por gênero e customer type',
                    hole = 0.5)
    figure.update_layout(template = 'plotly_dark')
    return figure













