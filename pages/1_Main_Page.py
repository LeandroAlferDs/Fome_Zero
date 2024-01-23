#===================================
#Libraries
#===================================
import numpy as np
import csv
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from folium.plugins import MarkerCluster



import folium
from haversine import haversine
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config(page_title="Main Page")

#--------------------------------------------




COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",}

def country_name(country_id):
      return COUNTRIES[country_id] 

def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"
    
    
COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}
def color_name(color_code):
    return COLORS[color_code]


def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

def data_clean( df ):
    
    ''' Esta função faz o tratamento e a limpeza do dataframe.
    
        Ações:
            -Elimina as linhas com células vazias ('NaN');
            -Renomeia as colunas;
            -Elimina linhas duplicadas;
            -Categoriza nome dos países;
            -Categoriza range de preços;
            -Categoriza cor das avaliações;
            -Categoriza tipo de culinária;
            -Reseta os indices do dataframe.

            Input: Dataframe
            Output: Dataframe '''
    
    
    #df.rename(columns={"country_name"}, inplace=True)

    
    #Renomeando as colunas do dataframe
    df = rename_columns(df)

    #Eliminando linhas com dados vazios NaN
    df = df.dropna()

    #Eliminando linhas duplicadas
    df = df.drop_duplicates(keep='first')

    
    #Categorizando tipo de culinária por sua especialidade, considerada como sendo a da primeira posição
    #df['cuisines'] = df.loc[:, 'cuisines'].apply(lambda x: x.split(',')[0])
    df["cuisines"] = df.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])
    df['country_code'] = df['country_code'].apply(country_name) 
    #Resetando indices das linhas
    df = df.reset_index(drop = True)
    
    return df

    #=============================================================
    #Import dataset
    #=============================================================

df_raw = pd.read_csv('zomato.csv')

df = data_clean( df_raw )



@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(df_raw)







#visao main page


#=====================================================
#Barra Lateral
#=====================================================

st.sidebar.title('_----Fome Zero----_')
#image_path = '/home/leandro/Documentos/repos_zomato/logo1.png'

image = Image.open( 'logo1.png' )
st.sidebar.image(image, width=180)
st.sidebar.markdown("""___""")



options = st.sidebar.multiselect (
        'Selecione os Países desejados',
    ['India','Australia', 'Brazil', 'Canada', 'Indonesia',
    'New Zeland', 'Philippines','Qatar', 'Singapure','South Africa', 'Sri Lanka','Turkey', 'United Arab Emirates','England', 'United States of America'],

    ['Brazil','Canada','England','Australia','Qatar','India'] )


#filtro de trânsito
linhas_selecionadas = df['country_code'].isin( options )
df = df.loc[linhas_selecionadas,:]

st.sidebar.markdown ("""___""")
st.sidebar.header('Dados Analisados')
st.sidebar.download_button(
    label="Download",
    data=csv,
    file_name='zomato.csv',
    mime='text/csv',
)


st.sidebar.markdown ("""___""")

st.sidebar.markdown ("Criado por LeandroAlfer")
st.sidebar.markdown ("""___""")

#=====================================================
#Layout no Streamlit
#=====================================================

st.title ('_Fome Zero_')
st.subheader('Visão dos Restaurantes e Tipos Culinários')


with st.container():
    col1, col2 ,col3, col4, col5 = st.columns(5,gap='large')

    with col1:
        qtd_rest = df.loc[:,'restaurant_id'].nunique()
        col1.metric("Total de Restaurantes", qtd_rest)



    with col2:
        qtd_pais = df.loc[:,'country_code'].nunique()
        col2.metric('Total de Países', qtd_pais)

    with col3: 
                
        qtd_cidades = df.loc[:, 'city'].nunique()
        col3.metric('Total de Cidades', qtd_cidades)

    with col4: 
                
        qtd_votos = df.loc[:, 'votes'].sum()      
        col4.metric('Total de Avaliações', qtd_votos)

    with col5: 
                
        qtd_culinarias =df.loc[:,'cuisines'].nunique()
        col5.metric('Tipos de Culinária', qtd_culinarias)


    with st.container():
        map = folium.Map()
        marker_cluster = MarkerCluster().add_to(map)

        for index, location_info in df.iterrows():
            popup_content = f"""
                    <h4>{location_info['restaurant_name']}</h4>
                    <p><strong>Culinaria:</strong> {location_info['cuisines']}</p>
                    <p><strong>Avaliação:</strong> {location_info['aggregate_rating']}/5.0</p>
                    <p><strong>Preço para dois:</strong> {location_info['average_cost_for_two']}</p>
                    <p><strong>Moeda País:</strong> {location_info['currency']}</p>

        """
            folium.Marker([location_info['latitude'],
                    location_info['longitude']],
                    popup=popup_content,
                    icon=folium.Icon(color=color_name(location_info['rating_color']))).add_to(marker_cluster)
        folium_static(map, width=1024, height=600)


    







    



