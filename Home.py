import streamlit as st
from PIL import Image

st.set_page_config(page_title="Home")




image= Image.open('logo1.png')
st.sidebar.image( image, width=220 )

st.sidebar.markdown ('# Fome Zero Dashboard')

st.sidebar.markdown ("""___""")
st.sidebar.write('Criado por Leandro Alfer')
st.sidebar.markdown ("""___""")

st.write( "# Fome Zero Dashboard" )

st.markdown(
    """
     ## Fome Zero Dashboard foi construído para acompanhar as métricas de crescimento de Restaurantes Parceiros.
     #### Como utilizar esse Dashboard?
    - Visão Main Page:
        - Nesta seção, é possivel observar as Quantidade de: Países, Cidades, Restaurantes e
        tipos de Culinárias cadastradas no Projeto Fome Zero.
        - Temos um Filtro de Países onde o *stakeholder* poderá visualizar apenas o País que desejar.
        - Existe um botão de download para baixar o arquivo utilizado neste projeto.

    - Visão Países: 
        - Acompanhamento dos indicadores de crescimento, onde existe um filtro para permitir
        a visualização somente dos Países desejados. 
        - Temos a visualização gráfica e em tabela, conforme
        a preferência do usuário.

    - Visão Cidades: 
        - Segue o mesmo padrão, com um filtro para apresentar as métricas de negócio por Cidades, 
        de acordo com a necessidade do usuário.

    - Visão Culinárias: 
        - Acompanhamento dos indicadores de crescimento dos restaurantes por Culinária.
    Nesta seção, tem dois filtros a mais que nas anteriores, onde abrange as informações
    das diferentes Culinárias, e um filtro de arraste onde o usuário controla através de um slider a
    quantidade de informações por gráfico ou tabela.
    

    """
    )