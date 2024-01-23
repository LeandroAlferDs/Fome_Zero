#===================================
#Libraries
#===================================

import streamlit as st
import numpy as np
import csv
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from folium.plugins import MarkerCluster


import inflection
import folium
from haversine import haversine

from PIL import Image
from streamlit_folium import folium_static

#--------------------------------------------
st.set_page_config(page_title="Cidades",page_icon='', layout='wide')




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

df1 = df.copy()
#=====================================================
#Barra Lateral
#=====================================================

st.sidebar.title('_----Fome Zero----_')


image = Image.open( 'logo1.png' )
st.sidebar.image(image, width=180)

st.sidebar.markdown("""___""")


options = st.sidebar.multiselect (
        'Selecione os Países desejados',
    ['India','Australia', 'Brazil', 'Canada', 'Indonesia',
    'New Zeland', 'Philippines','Qatar', 'Singapure','South Africa', 'Sri Lanka','Turkey', 'United Arab Emirates','England', 'United States of America'],

    ['Brazil','Canada','England','Australia','Qatar','India'] )


#filtro de Países
linhas_selecionadas = df['country_code'].isin( options )
df = df.loc[linhas_selecionadas,:]

st.sidebar.markdown ("""___""")
st.sidebar.markdown ("Criado por LeandroAlfer")
st.sidebar.markdown ("""___""")



#=====================================================
#Layout no Streamlit
#=====================================================

st.header ('_Visão Cidades_')
with st.container():
        
        col1,col2,col3 = st.columns(3,gap='large')
        


        with col1:
            st.markdown('Cidades com Restaurantes Avaliados Maior que 4.0')
            df1= df[ df['aggregate_rating'] >=4]
            df1 = df1.loc[:,['city','restaurant_id']].groupby('city').count().sort_values('restaurant_id',ascending=False).reset_index().head(15)
            fig=px.bar(df1,x='city',y='restaurant_id')
            fig .update_layout(yaxis_title='Quantidade de Restaurantes')
            fig .update_layout(xaxis_title='Cidades')
            st.plotly_chart(fig, use_container_width=True)



        with col2:
            st.markdown('Cidades com Restaurantes Avaliados Menor que 2.5')
            df1= df[df['aggregate_rating'] <= 2.5]
            df1 = df1.loc[:,['city','restaurant_id']].groupby('city').count().sort_values('restaurant_id',ascending=False).reset_index().head(15)
            fig = px.bar(df1,x='city',y='restaurant_id')
            fig .update_layout(yaxis_title='Quantidade de Restaurantes')
            fig .update_layout(xaxis_title='Cidades')
            st.plotly_chart(fig, use_container_width=True)
        
        with col3:
            st.markdown('Quantidade de Cidades registradas por País')
            df1 = df.loc[:,['country_code','city']].groupby('country_code').nunique().sort_values('city',ascending=False).reset_index().head(15)
            fig=px.bar(df1,x='country_code',y='city')
            fig .update_layout(xaxis_title='Países')
            fig .update_layout(yaxis_title='Quantidade de Cidades')
            st.plotly_chart(fig, use_container_width=True)

        

with st.container():
        
    
    col1 = st.columns(1,gap='large')

    st.subheader('_Culinárias distintas por Cidades_')
    df = (df.loc[:,['cuisines','city']].groupby('city').nunique()
                                    .sort_values('cuisines',ascending=False)
                                    .reset_index())
    fig = px.line(df,y='cuisines',x='city')
    fig .update_layout(xaxis_title='Cidades')
    fig .update_layout(yaxis_title='Quantidade de Culinárias')
    st.plotly_chart(fig, use_container_width=True)



