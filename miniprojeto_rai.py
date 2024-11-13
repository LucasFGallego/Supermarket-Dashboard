# python3 -m venv venv
# source venv/bin/activate
# pip install pandas numpy matplotlib seaborn scikit-learn plotly openpyxl

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
import plotly.express as px
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

# Leitura do dataframe já tratado
data = pd.read_excel('Dados.xlsx')
data = data.drop("Unnamed: 0", axis = 'columns')
print(data.head(3))

# Leitura do tipo de produto que será analisado
print(f"Tipos de produtos: {data['Product line'].unique()}")
produto_escolhido = input("Você deseja analisar as vendas de qual produto? ")

# Filtragem do dataframe pelo produto escolhido
data_por_produto = data.loc[data['Product line'] == produto_escolhido]

# Laço para gerar um gráfico por mês
for mes in sorted(data['Date'].dt.month.unique()):
  # Filtragem do dataframe pelo mês atual
  data_mes = data_por_produto.loc[data_por_produto['Date'].dt.month == mes]

  # Agrupamento das vendas por mês
  produto_por_mes = data_mes.groupby(data_mes['Date'].dt.day).size()

  # Plotagem do gráfico
  fig = px.line(produto_por_mes, x = produto_por_mes.index, y = produto_por_mes.values,
                title = f'Vendas de {produto_escolhido} no mês {mes} de 2019')

  # Customização do layout
  fig.update_traces(line_color='purple', fill='tozeroy', mode='lines+markers')
  fig.update_layout(
      xaxis_title=f'Dias do mês {mes}',
      yaxis_title='Quantidade vendida',
      showlegend=True,
      xaxis=dict(showgrid=True),
      yaxis=dict(showgrid=True)
  )

  fig.show()

# Leitura do tipo de produto que será analisado
print(f"Tipos de produtos: {data['Product line'].unique()}")
produto_escolhido2 = input("Você deseja analisar o lucro de qual tipo de produto? ")

# Selecionar os dados do dataframe que correspondem ao produto escolhido
data_produto = data.loc[(data['Product line'] == produto_escolhido2)]

# Laço para gerar um gráfico por mês
for mes in sorted(data['Date'].dt.month.unique()):
  # Filtragem do dataframe pelo mês atual
  produto_meses = data.loc[data['Date'].dt.month == mes]

  # Agrupamento do dataframe entre os meses e o lucro
  lucro_produto_mes = produto_meses.groupby(produto_meses['Date'].dt.day)['gross income'].sum()

  # PLotagem do gráfico
  fig = px.line(lucro_produto_mes, x = lucro_produto_mes.index, y = lucro_produto_mes.values,
           title = f'Lucro de {produto_escolhido} por dia do mês {mes} de 2019')

  # Customização do layout e sombra
  fig.update_traces(line_color='Orange', fill='tozeroy', mode='lines+markers')
  fig.update_layout(
    xaxis_title=f'Dias do mês {mes}',
    yaxis_title='Lucro',
    showlegend=True,
    xaxis=dict(showgrid=True),  # Habilita grid no eixo X
    yaxis=dict(showgrid=True)   # Habilita grid no eixo Y
  )

  fig.show()

# Filtragem do gráfico pela forma de pagamento por cidades
data_cidade_pagamento = data.groupby(['City', 'Payment']).size().unstack()

# Laço para plotagem dos gráficos por cidade
for cidade in data_cidade_pagamento.index:
  # Filtragem dos dados pela cidade atual
  cidade_pagamento = data_cidade_pagamento.loc[cidade]

  # Plotagem do gráfico de rosca
  fig = px.pie(cidade_pagamento, values=cidade_pagamento.values, names=cidade_pagamento.index,
                title=f"Formas de pagamento em {cidade}",
                hole=0.5,
               color_discrete_sequence=px.colors.qualitative.T10)

  # Exibe o gráfico
  fig.show()

# Clusterização
data_num = data
print(data_num.head(3))

# Label encoding
data_num['City'] = LabelEncoder().fit_transform(data_num['City'])
data_num['Customer type'] = LabelEncoder().fit_transform(data_num['Customer type'])
data_num['Gender'] = LabelEncoder().fit_transform(data_num['Gender'])
data_num['Product line'] = LabelEncoder().fit_transform(data_num['Product line'])
data_num['Payment'] = LabelEncoder().fit_transform(data_num['Payment'])
print(data_num.head(3))

# Tratamento das colunas de tempo
data_num['Day'] = data_num['Datetime'].dt.day
data_num['Month'] = data_num['Datetime'].dt.month
data_num = data_num.drop(['Date', 'Datetime'], axis = 1)
print(data_num.head(3))

# Identificar o número de clusters com o método do cotovelo
sse = []
for i in range(1, 11):
  kmeans = KMeans(n_clusters = i, random_state = 42)
  kmeans.fit(data_num)
  sse.append(kmeans.inertia_)
fig = px.line(x = range(1, 11), y = sse, title = 'Método do Cotovelo')
fig.update_traces(line_color='deeppink', fill='tozeroy', mode='lines+markers')
fig.update_layout(
    xaxis_title='Número de clusters',
    yaxis_title='Somas dos erros quadráticos (inércia)',
    showlegend=True,
    xaxis=dict(showgrid=True),
    yaxis=dict(showgrid=True)
)
fig.show()

# Aplicar o K-Means
kmeans = KMeans(n_clusters = 4, random_state = 42)
kmeans.fit(data_num)
labels = kmeans.labels_
data_num['Clusters'] = labels
print(data_num.head(3))

# Analisar a distribuição dos clusters
data_num['Clusters'].value_counts()
cluster_analysis = data_num.groupby('Clusters').mean()
print(cluster_analysis)
# Plotar os dados clusterizados
fig = px.scatter(data_num, x = data_num['Unit price'], y = data_num['Quantity'],
                 color='Clusters',
                 title='Clusters de K-Means',
                 color_discrete_sequence=px.colors.qualitative.Set1)

fig.update_layout(
    xaxis_title='Preço unitário',
    yaxis_title='Quantidade comprada'
)

# Exibir o gráfico
fig.show()