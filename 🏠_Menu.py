import streamlit as st
from pages import * 
import webbrowser

from data_clean import data

st.set_page_config(
    page_title = 'Home',
    page_icon= '🏠',
    layout = 'wide',
)

st.title(
    '🏠 Menu Principal'
)


st.markdown(
    """
    <style>
    .stButton > button {
        display: block;
        margin: 0 auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .stDownloadButton > button {
        display: block;
        margin: 0 auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.sidebar.markdown("<h1 style='text-align: center;'> Desenvolvedores ", unsafe_allow_html=True)

st.sidebar.write('')

btn = st.sidebar.button('Liga de Data Science', type = 'primary')

if btn:
    webbrowser.open_new_tab('https://linktr.ee/ligadsunicamp?utm_source=linktree_profile_share&ltsid=bcdbacaf-d0b6-48f7-9aa3-897fac981740')


@st.cache_data # Previne que a operação seja executada sempre que o programa for re-executado
def convert_df(df):
    return df.to_csv().encode('utf-8')
st.sidebar.markdown("<h1 style='text-align: center;'> Base de dados", unsafe_allow_html=True)
download = st.sidebar.download_button('Download data as CSV', data = convert_df(data), file_name='Adidas.csv', mime = 'text/csv')



st.markdown(
    """
    <p style = "text-align:justify;">
    Este projeto é uma aplicação prática de conceitos de <b>análise de dados</b> e <b>Machine Learning</b> em um dataset de vendas de supermercado,
    que pode ser acessado, já tratado, por meio do botão da <em>sidebar</em>. Com ele, foram gerados diversos gráficos e filtros, que permitem
    um controle por parte dos gerentes dessa rede de varejo acerca das vendas dentro do escopo temporal, conforme mostra a aba <b><i>Dashboard</i></b>. 
    Além disso, foram criados diferentes modelos de clusterização, que permitem a geração de insights valiosos acerca de possíveis estratégias de
    agrupamento dos diferentes produtos, vide a aba <b><i>Clusterização</i></b>.

    Acesse as páginas na <em>sidebar</em> para verificar os resultados da nossa análise!

    </p>


    """, unsafe_allow_html= True
)