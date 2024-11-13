import pandas as pd
import numpy as np
from math import sqrt
import seaborn as sns
import plotly.express as px

# importando a base de dados limpa
from data_clean import data

# Customer Type e Gênero

data_customer_1 = data.groupby('Customer type').size().reset_index(name='Sales')
figure_1 = px.pie(data_customer_1, values='Sales', names='Customer type', width=600, title='Porcentagem de vendas absolutas por tipo de consumidor')

data_customer_2 = data.groupby('Customer type')['gross income'].sum().reset_index(name='Gross Income')
figure_2 = px.pie(data_customer_2, values='Gross Income', names='Customer type', width=600, title='Porcentagem de lucro bruto por tipo de consumidor')

data_gender_1 = data.groupby('Gender').size().reset_index(name='Sales')
figure_3 = px.pie(data_gender_1, values='Sales', names='Gender', width=600, title='Porcentagem de vendas absolutas por tipo de gênero')

data_gender_2 = data.groupby('Gender')['gross income'].sum().reset_index(name='Gross Income')
figure_4 = px.pie(data_gender_2, values='Gross Income', names='Gender', width=600, title='Porcentagem de lucro bruto por gênero')

data_gender_3 = data.groupby(['Gender', 'Customer type']).size().reset_index(name='Quantity')
data_gender_3['Gender_Status'] = data_gender_3['Gender'] + ' - ' + data_gender_3['Customer type']
figure_4 = px.pie(data_gender_3, values='Quantity', names='Gender_Status', width=600, title='Distribuição de gênero por customer type')

data_gender_4 = data.groupby(['Gender', 'Customer type']).agg({'gross income': 'sum'}).reset_index()
data_gender_4.rename(columns={'gross income': 'Total Gross Income'}, inplace=True)

data_gender_4['Gender_Status'] = data_gender_4['Gender'] + ' - ' + data_gender_4['Customer type']
figure_5 = px.pie(data_gender_4, values='Total Gross Income', names='Gender_Status', width=600, title='Lucro bruto por gênero e customer type')

data_customer_3= pd.DataFrame(columns=['Hour', 'Customer type', 'Sales'])
hourly_customer_sales_count = data.groupby(['Hour', 'Customer type']).size().reset_index(name='Sales')
data_customer_3= pd.concat([data_customer_3, hourly_customer_sales_count], ignore_index=True)
figure_6 = px.bar(data_customer_3, x="Hour", y="Sales", color='Customer type', barmode="group", width=800, title="Vendas absolutas por hora e customer type")

data_gender_5 = pd.DataFrame(columns=['Hour', 'Gender', 'Sales'])
hourly_gender_sales_count = data.groupby(['Hour', 'Gender']).size().reset_index(name='Sales')
data_gender_5 = pd.concat([data_gender_5, hourly_gender_sales_count], ignore_index=True)
figure_7 = px.bar(data_gender_5, x="Hour", y="Sales", color='Gender', barmode="group", width=800, title="Vendas absolutas por hora e gênero")

data_gender_6 = data.groupby(['Hour', 'Gender', 'Customer type']).size().reset_index(name='Quantity')
data_gender_6['Gender_Status'] = data_gender_6['Gender'] + ' - ' + data_gender_6['Customer type']
figure = px.bar(data_gender_6, x='Hour', y='Quantity', color="Gender_Status", width=1000, title='Vendas absolutas por hora por gênero e customer type')


# Medidas Consolidadas: Lucro Bruto Total, quantidade vendida total e receita total 

# Gross income total

gross_total = data['gross income'].sum()

# Quantidade total comprada

quantity_total = data['Quantity'].sum()

# Total de vendas

sales_total = data['Total'].sum()

# Ranking de vendas do produto com maior lucro

df_income = data.groupby('Product line')['Total'].sum()
df_income.sort_values(ascending = False, inplace  = True)
df_income = pd.DataFrame(df_income)
df_income['% Change'] = df_income['Total'].pct_change()
df_income['% Change']['Food and beverages'] = 0
df_income['% Change'] = df_income['% Change'].apply(lambda x: str(round(x*100,3)) + '%')

graph_2 = px.bar(
    df_income,
    x = 'Total',
    y = df_income.index,
    title = 'Ranking de vendas do produto com maior lucro',
    hover_data=['% Change'],
    color_discrete_sequence = ['red']
)

# Indicador para a média do Rating por cidade

rating_cidade = data.groupby('City')['Rating'].mean().reset_index()


fig_rating = px.bar(rating_cidade, x='City', y='Rating', color_discrete_sequence=['blue'])
fig_rating.update_layout(
    title='Rating por Cidade',
    xaxis_title='Cidade',
    yaxis_title='Rating'
)

# Análise dos 25% clientes que mais gastam

gallego_q3 = data['Total'].quantile(0.75)
gallego_quartil_quatro = data[data['Total'] > gallego_q3]
gallego_media_q4 = gallego_quartil_quatro['Total'].mean()
gallego_grouped1 = gallego_quartil_quatro.groupby('Customer type')['Total'].sum()

gallego_grouped1 = gallego_quartil_quatro.groupby('Customer type')['Total'].sum().reset_index()

# Criar o gráfico de barras
fig = px.bar(gallego_grouped1, x='Customer type', y='Total', color_discrete_sequence=['blue'])

# Adicionar título e rótulos aos eixos
fig.update_layout(
    title='Quantidade por Tipo de Cliente (4º Quartil)',
    xaxis_title='Tipo de Cliente',
    yaxis_title='Total'
)

# Filtrando os dados
gallego_customer_normal_quartil = gallego_quartil_quatro[gallego_quartil_quatro['Customer type'] == 'Normal']

# Agrupando e somando os totais
gallego_grouped2 = gallego_customer_normal_quartil.groupby(['City', 'Gender'])['Total'].sum().reset_index()

#Cores
color_discrete_map = {'Male': 'blue', 'Female': 'red'}
# Criando o gráfico de barras empilhadas
fig = px.bar(gallego_grouped2, x='City', y='Total', color='Gender', title='Quantidade por Gênero e Cidade (4º Quartil)', labels={'City': 'Cidade', 'Total': 'Total'}, color_discrete_map=color_discrete_map)




