import streamlit as st

from clusterization_background import *


st.set_page_config(
        page_title = "Clusterização",
        page_icon = "🎯",
        layout="wide",
    )

st.title(
    "🎯 Clusterização"
)

# Gallego (G*)
st.markdown("## 1. Introdução ao Banco de Dados")
st.markdown(
    """
    <p style = "text-align:justify;">
    Este dataset contém um histórico de vendas de uma rede de supermercados, com registros de 3 filiais durante um período de 3 meses. A riqueza de detalhes fornecidos permite a aplicação de métodos analíticos preditivos, facilitando a extração de insights valiosos sobre o comportamento de compra dos clientes e o desempenho das vendas. Os dados incluem informações como o tipo de cliente (membros ou não-membros), localização das filiais, categorias de produtos comprados, formas de pagamento, além de detalhes financeiros como o preço por unidade, quantidade de itens comprados e o total gasto, incluindo impostos.
    
    Outros aspectos, como o custo dos produtos vendidos (COGS), margem de lucro, e uma avaliação da experiência de compra dos clientes, também estão presentes. Esse conjunto de dados é ideal para análises que buscam otimizar estratégias de marketing, melhorar a gestão de estoque e aumentar a satisfação dos clientes. Ao explorar padrões como sazonalidade, preferências de produto e influências de promoções, é possível desenvolver estratégias mais informadas para impulsionar o crescimento e a eficiência operacional do supermercado.
    </p>
    """,unsafe_allow_html= True
)

st.markdown("## 2. O método do cotovelo ")
st.markdown(
    """
    <p style = "text-align:justify;">
    A clusterização é um processo de agrupamento de dados de acordo com características que eles compartilham. No caso deste projeto, foi utilizado
    o K-means, um algoritmo de aprendizado não supervisionado que, definido um número de agrupamentos (fornecido como dado de entrada), agrupa os dados
    de acordo com os padrões intrínsecos ao conjunto de dados.
    </p>


    <p style = "text-align:justify;">
    Nesse sentido, para se determinar o número ótimo de <i>clusters</i>, foi aplicado o <b>Método do Cotovelo</b>, que, em sua essência, é uma iteração 
    do K-means para diferentes números de agrupamentos, de modo que o critério que define a otimalidade é a <b>inércia</b>, um resultado que pode ser extraído do 
    próprio modelo. É gerado, após a iteração, um conjunto de dados da inércia associada ao número de agrupamentos respectivo, que pode ser interpretado como pares ordenados em um plano cartesiano, 
    de modo que o ponto que indica o número ótimo de <i>clusters</i> é aquele que mais dista da reta que une o primeiro e o último pontos da série. Portanto, é possível utilizar
    equacionamentos da geometria analítica para determinar a distância dos pontos em relação a essa reta.

    </p>
    """, unsafe_allow_html= True
)

st.markdown(
    """
    <p style = "text-align:justify;">
    A Equação de uma reta é dada por
    </p>

    """, unsafe_allow_html= True
)

st.latex(r'''
\begin{equation}
0 = A\cdot{x}+B\cdot{y} + C  ,
\end{equation}

''')

st.markdown(
    """
    <p style = "text-align:justify;">
    Em que <i>A</i>, <i>B</i> e <i>C</i> são coeficientes a serem determinados.
    </p>

    """, unsafe_allow_html= True
)

st.markdown(
    """
    <p style = "text-align:justify;">
    Já a equação do coeficiente angular de uma reta é
    </p>

    """, unsafe_allow_html= True
)

st.latex(r'''
\begin{equation}
m = \frac{y_2-y_1}{x_2-x_1} ,
\end{equation}
''')

st.markdown(
    """
    <p style = "text-align:justify;">
    assumindo que a diferença no denominador é diferente de zero, ou seja, que os pontos são distintos e quaisquer.
    </p>

    """, unsafe_allow_html= True

)


st.markdown(
    """
    <p style = "text-align:justify;">
    Tem-se, então, que:
    </p>

    """, unsafe_allow_html= True
)

st.latex(r'''
\begin{equation}
A = -m,
\end{equation}
''')
st.latex(r'''
\begin{equation}
B = 1,
\end{equation}''')
st.latex(r'''
\begin{equation}
C = -y_0 + m\cdot{x_0} .
\end{equation} 
''')

st.markdown(
    """
    <p style = "text-align:justify;">
    Após encontrar os coeficientes associados à reta que passa pelos os pontos inicial e final do conjunto de pares ordenados previamente gerado 
    (por meio das equações 3 à 5), é possível aplicar a equação 
    </p>

    """, unsafe_allow_html= True

)

st.latex(r'''
\begin{equation}
d = \frac{|Ax_1 + By_1 + C|}{\sqrt{A^2 + B^2}}
\end{equation}
''')

st.markdown(
    """
    <p style = "text-align:justify;">
    para determinar a distância dos demais pontos da série em relação a ela e, então, selecionar o ponto cuja distância é a maior. 
    </p>

    """, unsafe_allow_html= True

)

st.markdown(
    """
    <p style = "text-align:justify;">
    Todo esse procedimento pode ser consolidado na seguinte função: 
    </p>

    """, unsafe_allow_html= True

)

st.code(
    """
    from sklearn.cluster import KMeans
    from math import sqrt
    import pandas as pd


    def elbow_method(df, criteria):
    '''
    Função que retorna o número ótimo de clusters para determinado dataframe.

    Input:
    - df: dataframe a ser utilizado na clusterização;
    - criteria: lista de critérios segundo a qual será feita a clusterização (e.g: ['Rating', 'Quantity'])

    Output: número ótimo de clusters
    '''
     # Calculando os valores de inércia numericamente, dado um critério de parada de 0.01
        n = [2]
        inertia_values = []  # valores de inércia
        inertia_diff = []    # valores de diferenças de inércia
    
        while True:   # loop para o cálculo de dos valores de inércia enquanto houver diferença maior que 1 entre as últimas duas inércias
            if n[-1] == 2:
            kmeans = KMeans(n_clusters = n[-1])
            kmeans.fit(df[criteria])
            inertia = kmeans.inertia_
            inertia_values.append(inertia)
            n.append(n[-1]+1)
            elif n[-1] > 2:
            kmeans = KMeans(n_clusters = n[-1])
            kmeans.fit(df[criteria])
            inertia = kmeans.inertia_
            inertia_values.append(inertia)
            inertia_diff.append(abs(inertia_values[-2] - inertia_values[-1]))
            if inertia_diff[-1] <= 1:
                break
            else:
                n.append(n[-1] + 1)
                continue
        # Encontrando a equação da reta associada ao primeiro e ao último pontos:
        x_0, y_0 = n[0], inertia_values[0]    # primeiro ponto do gráfico
        x_n, y_n = n[-1], inertia_values[-1]  # último ponto do gráfico

        m = (y_n - y_0)/(x_n-x_0)   # Coeficiente angular

        # Parâmetros da Reta
        C = -(y_0 + m*(-x_0))
        A = -m
        B = 1

        # Encontrando todos os pontos do gráfico
        points = list(zip(n, inertia_values))

        #Aplicando a fórmula da distância para TODOS os pontos de points:
        d = []
        for i in points:
            x_1, y_1 = i[0], i[1]
            d.append((abs(A*x_1 + B*y_1 + C)/(sqrt(A**2+B**2))))
        argmax = d.index(max(d))
        optimal_n = points[d.index(max(d))][0]
        return optimal_n
     
    """)
 
st.markdown("## 3. Faixa de gastos prioritária")

st.markdown(
    """
    <p style = "text-align:justify;">
    O objetivo dessa análise foi determinar a faixa de gastos que gera a maior receita para a franquia como um todo (aqui, não 
    foram aplicados filtros por cidade, produto ou tempo, como no caso do dashboard). Para tal, foi aplicado o método do cotovelo e o K-Means para gerar
    um gráfico que separa todas as transações em categorias, associadas ao total gasto e ao Rating. O resultado gerado foi o seguinte:
    </p>
    """, unsafe_allow_html= True
)

st.plotly_chart(fig_2, use_container_width=True, config = {'displayModeBar':False})

st.markdown(
    """
    <p style = "text-align:justify;">
    As informações sobre as <i>labels</i> foram, então, consolidadas em um dataframe mostra qual faixa é de gastos é a que mais gera retorno para o 
    supermercado:
    """, unsafe_allow_html= True
)

st.table(consolidatedinfo_label)

st.markdown(
    """
    <p style = "text-align:justify;">
    Portanto, pode-se concluir que a faixa de preços associada às maiores receitas <b>não</b> é aquela que se associa aos maiores gastos, porque estes não são
    mantidos por um elevado numero de clientes (vide tabela). Uma estratégia que pode ser desenvolvida com essa análise é a criação de um programa de benefícios para atrair
    para atrair mais clientes para essa zona de preços, por exemplo.
    </p>
    """, unsafe_allow_html= True
)

# Raissa (G*)

st.markdown("## 4. Preço unitário e quantidade comparada")

st.markdown(
    """
    <p style = "text-align:justify;">
    A clusterização realizada considera a distribuição dos dados ao longo de duas variáveis: "Preço Unitário" e "Quantidade Comprada". Através dela é possível correlacionar os tipos de clientes que frequentam o mercado em questão, considerando a escolha do produto comprado através do preço e da quantidade.

    O gráfico apresenta quatro clusters, ou seja, apresenta quatro principais tipos de clientes do supermercado. Ao comparar os grupos mais "extremos" apresentados, é possível perceber a divergência na relação preço-quantidade. O cluster 0, em tom claro, representa as pessoas que, se comprarem produtos com preços elevados, irão adquirir uma pequena quantidade de itens; ou, caso os produtos escolhidos possuam preços unitários menores, irão optar por levá-los em maior quantidade.

    Já o cluster 3, em tom azul escuro, representa os clientes que adquirem produtos de acordo com uma relação diretamente proporcional entre preço e quantidade, uma vez que, caso optem por adquirir produtos mais caros, a quantidade comprada será alta também; da mesma forma, caso o preço unitário do produto seja inferior, sua quantidade adquirida também será.

    Ainda, através da análise gráfica é possível realizar algumas conclusões mais pontuais. Por exemplo, os produtos que apresentam um preço intermediário distribuem-se em diferentes clusters, o que pode indicar que esses produtos podem atrair clientes com diferentes perfis de compra.
    </p>
    """, unsafe_allow_html= True
)

last_fig = consolidation_final()
st.plotly_chart(last_fig)

st.markdown("## 5. Conclusões")

st.markdown(
    """
    <p style = "text-align:justify;">
    Com base na primeira análise, concluímos que a faixa de preços que gera maior receita não é necessariamente associada aos maiores gastos individuais, pois clientes que gastam mais representam uma parcela menor do total. Uma estratégia sugerida seria a criação de programas de benefícios para atrair mais clientes para essa faixa de preços mais elevada, aumentando o volume de transações e, consequentemente, as receitas da franquia.
    
    Além disso, a análise dos comportamentos de compra revelou que os quatro clusters de clientes apresentam relações distintas entre preço e quantidade, com o Cluster 0 indicando uma preferência por comprar menos itens de produtos caros e mais itens de produtos baratos, enquanto o Cluster 3 demonstra uma disposição para gastar mais em produtos de maior valor. Assim, para maximizar os lucros, o supermercado deve implementar estratégias que incentivem um maior número de clientes a se envolverem com produtos em faixas de preço intermediárias, onde há diversidade de perfis. A combinação dessas análises sugere que programas de benefícios e promoções específicas podem aumentar a atratividade dessas faixas de preços, estimulando mais clientes a gastar, o que potencialmente otimiza as receitas globais da franquia.
    </p>
    """, unsafe_allow_html= True
)
