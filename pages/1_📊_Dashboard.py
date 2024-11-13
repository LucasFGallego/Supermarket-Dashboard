import streamlit as st
from pages import *

from data_clean import data
from functions import *

#from exportar_vendas_de_supermercado_gallego import *
#from miniprojeto_rai import *

st.set_page_config(
        page_title = "Dashboard",
        page_icon = '📊',
        layout="wide",
    )

# Sidebar 
st.sidebar.markdown('### Filtros')

cidade = st.sidebar.selectbox(
    "Cidade",
    data['City'].unique()
)

produto = st.sidebar.selectbox(
    "Produto",
    data['Product line'].unique()
)

total = st.sidebar.checkbox(
    "Total"
)

# Sidebar - Séries Temporais
st.sidebar.divider()

tempo = st.sidebar.select_slider('Escala Temporal', ['Dia','Semana', 'Mês', 'Ano'])

st.title(
    f"📊Dashboard: {set_title(cidade, produto, total)}"
)


# Dashboard

st.divider()

# Divisão das colunas:

col1, col2 = st.columns([0.45, 0.55])

with col1.container(border = True):
    subcol1, subcol2, subcol3 = st.columns([0.3, 0.33, 0.36])
    subcol1.metric(
    label="Unidades vendidas",
    value = sales_amount(data, cidade, produto, total)
)
    subcol2.metric(
        label="Lucro Bruto",
        value = gross_income(data, cidade, produto, total)
    )

    subcol3.metric(
        label = 'Receita',
        value = returns(data, cidade, produto, total)
    )
    
    st.markdown(f"#### Ranking de produtos em {cidade if not total else 'Total'}")

    st.table(
        data = ranking(data, cidade, total)
    )

    st.text("* Coluna 'Total': Receita")

    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")


with col2.container(border = True):
    if tempo == "Mês":
        aux_col1, aux_col2 = st.columns([0.5,0.5])
        consol = aux_col1.radio("Dados Consolidados?", options = ['Sim', 'Não'], horizontal=True)
        if consol == 'Sim':
            st.plotly_chart(timeseries_month(data, produto, cidade, total), use_container_width=True, config = {'displayModeBar': False})
            st.markdown('')
        if consol == 'Não':
            mes = aux_col2.radio("Mês:", options = [1,2,3], horizontal = True)
            st.plotly_chart(vendas_e_lucro_por_mes(data, produto, mes, cidade,total), use_container_width=True, config = {'displayModeBar': False})


    elif tempo == "Ano":
        st.plotly_chart(timeseries_year(data, produto, cidade, total), use_container_width= True, config = {'displayModeBar':False})
        st.markdown('')
        st.markdown('')
        st.markdown('')
        st.markdown('')
        st.markdown('')
    
    elif tempo == 'Dia':
        st.plotly_chart(timeseries_day(data, produto, cidade, total), use_container_width=True, config = {'displayModeBar':False})
        st.markdown('')
        st.markdown('')
        st.markdown('')
        st.markdown('')
        st.markdown('')

    elif tempo == 'Semana':
        st.plotly_chart(timeseries_week(data, produto, cidade, total), use_container_width= True, config = {'displayModeBar':False})
        st.markdown('')
        st.markdown('')
        st.markdown('')
        st.markdown('')
        st.markdown('')


with st.container(border = True):
    col1, col2 = st.columns([0.5, 0.5])
    col3, col4 = st.columns([1/2, 1/2])
    col1.plotly_chart(city_rating(data, produto, total), use_container_width=True, config = {'displayModeBar': False})
    col2.plotly_chart(rosca(data, produto, cidade, total), use_container_width=True, config = {'displayModeBar': False})
    col3.plotly_chart(customer_type_q4(cidade, produto, total), use_container_width=True, config = {'displayModeBar': False})
    col4.plotly_chart(gender_q4(cidade, produto, total),use_container_width=True, config = {'displayModeBar': False})
    st.plotly_chart(rosca_clientes(data), use_container_width= True, config = {'displayModeBar':False})
    








