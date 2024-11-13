# python3 -m venv venv
# source venv/bin/activate
# pip install openpyxl pandas matplotlib streamlit plotly

import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar o arquivo Excel para a variável 'data'
data = pd.read_excel('Dados.xlsx')

# Obter a lista de tipos de produtos únicos
#tipos_produto = data['Product line'].unique()

# Adicionar uma sidebar com a selectbox para o usuário escolher o tipo de produto
#tipo_selecionado = st.sidebar.selectbox('Selecione a linha de produto', tipos_produto)

# Filtrar os dados pelo tipo de produto selecionado
data_filtrada = data[data['Product line'] == tipo_selecionado]

# Obter a lista de cidades disponíveis com base nos dados filtrados
cidades_disponiveis = data_filtrada['City'].unique()

# Adicionar uma selectbox para o usuário escolher a cidade
cidade_selecionada = st.sidebar.selectbox('Selecione a cidade', cidades_disponiveis)

# Filtragem do gráfico pela forma de pagamento da cidade selecionada
data_cidade_pagamento = data_filtrada[data_filtrada['City'] == cidade_selecionada].groupby(['Payment']).size()

# Plotagem do gráfico de rosca para a cidade e produto selecionados
fig = px.pie(data_cidade_pagamento, values=data_cidade_pagamento.values, names=data_cidade_pagamento.index,
             title=f"Formas de pagamento em {cidade_selecionada} ({tipo_selecionado})",
             hole=0.5,
             color_discrete_sequence=px.colors.qualitative.T10)

# Ajuste das margens
fig.update_layout(margin=dict(t=20, b=20, l=20, r=20))

# Exibe o gráfico no Streamlit
st.plotly_chart(fig)
