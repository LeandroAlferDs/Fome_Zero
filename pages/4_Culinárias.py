#===================================
#Libraries
#===================================
import numpy as np
import csv
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from folium.plugins import MarkerCluster


import inflection 
import folium as folium
from haversine import haversine
from PIL import Image
import streamlit as st
from streamlit_folium import folium_static

st.set_page_config(page_title="Culinárias",page_icon='', layout='wide')

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




def extract_unique_cuisines(df):
  

  # Pega todas as culinarias da coluna cuisines
  cuisines = df['cuisines'].tolist()

  # elimina as culinarias duplicadas
  unique_cuisines = set(cuisines)

  return unique_cuisines
    



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

#visao main page


#=====================================================
#Barra Lateral
#=====================================================

st.sidebar.title('_----Fome Zero----_')



image = Image.open( 'logo1.png' )
st.sidebar.image(image, width=180)

st.sidebar.markdown("""___""")


options_country = st.sidebar.multiselect (
        'Selecione os Países desejados',
    ['India','Australia', 'Brazil', 'Canada', 'Indonesia',
    'New Zeland', 'Philippines','Qatar', 'Singapure','South Africa', 'Sri Lanka','Turkey', 'United Arab Emirates','England', 'United States of America'],

    default=['Brazil','Canada','England','Australia','Qatar','India'] )


def make_sidebar(df):
    value = st.sidebar.slider("__________", 0, 20, 10)
    return value
st.sidebar.markdown('Selecione a quantidade desejada de Restaurantes/Culinárias')
value = make_sidebar(df)


# Pegar todas as culinárias da coluna cuisines.
cuisines = extract_unique_cuisines(df)

# Criando um multiselect.
options_cuisines = st.sidebar.multiselect(
        "Escolha a Culinária desejada", cuisines,
    default=['Italian','American','Japanese','Arabian','Brazilian','BBQ','Pizza','Burger','Chinese',
             'Salad',] )


#filtro de paises
linhas_selecionadas = df['country_code'].isin( options_country )
df = df.loc[linhas_selecionadas,:]



linhas_selecionadas = df['cuisines'].isin( options_cuisines )
df = df.loc[linhas_selecionadas,:]

#filtro de culinarias
linhas_selecionadas = df['cuisines'].isin( options_cuisines )
df1 = df.loc[linhas_selecionadas,:]



st.sidebar.markdown ("""___""")
st.sidebar.markdown ("Criado por LeandroAlfer")
st.sidebar.markdown ("""___""")

#=====================================================
#Layout no Streamlit
#=====================================================
st.title ('_Visão dos Tipos de Culinária_')
st.subheader ('Restaurantes com melhores Avaliações em suas especialidades')

with st.container():
        
        col1,col2,col3,col4,col5 = st.columns(5,gap='large')
        


        with col1:

            #df1 = df[df['cuisines'] == 'Italian']
            
            #df1.loc[:,['aggregate_rating','restaurant_name']].groupby('restaurant_name').mean()
            #df1 = df1.sort_values(['aggregate_rating', 'restaurant_id'], ascending=[False, True])
            #df1 = df1.head(1)
            #st.col1.metric('Italiano',df1)
            #Italiana = (df1['restaurant_name'].values[0])
            #Nota_Italiana = (df1['aggregate_rating'].values[0])
            st.write(f'<h6 style=\'text-align: left; \'>Italiana: Darshan   \n',unsafe_allow_html=True)
            st.write(f'<h4 style=\'text-align: left; \'>{4.9}/5.0',unsafe_allow_html=True)
            
        with col2:
    
            #df1 = df[df['cuisines'] == 'Arabian']
            #df1.loc[:,['aggregate_rating','restaurant_name']].groupby('restaurant_name').mean()
            #df1 = df1.sort_values(['aggregate_rating', 'restaurant_id'], ascending=[False, True])
            #df1 = df1.head(1)
            #Árabe = (df1['restaurant_name'].values[0])
            #Nota_Árabe = (df1['aggregate_rating'].values[0])
            st.write(f'<h6 style=\'text-align: left; \'>Árabe: Mandi@36   \n',unsafe_allow_html=True)
            st.write(f'<h4 style=\'text-align: left;\'>{4.7}/5.0', unsafe_allow_html=True)
            
        with col3:

            #df1 = df[df['cuisines'] == 'Japanese']
            #df1.loc[:,['aggregate_rating','restaurant_name']].groupby('restaurant_name').mean()
            #df1 = df1.sort_values(['aggregate_rating', 'restaurant_id'], ascending=[False, True])
            #df1 = df1.head(1)
            #Japonesa = (df1['restaurant_name'].values[0])
            #Nota_Japonesa = (df1['aggregate_rating'].values[0])
            st.write(f'<h6 style=\'text-align: left; \'>Japonesa : Sushi Samba  \n',unsafe_allow_html=True)
            st.write(f'<h4 style=\'text-align: left; \'>{4.9}/5.0', unsafe_allow_html=True)

        with col4:

            #df1 = df[df['cuisines'] == 'American']
            #df1.loc[:,['aggregate_rating','restaurant_name']].groupby('restaurant_name').mean()
            #df1 = df1.sort_values(['aggregate_rating', 'restaurant_id'], ascending=[False, True])
            #df1 = df1.head(1)
            #Americana = (df1['restaurant_name'].values[0])
            #Nota_Americana = (df1['aggregate_rating'].values[0])
            st.write(f'<h6 style=\'text-align: left; \'>Americana: Burger & Lobster  \n',unsafe_allow_html=True)
            st.write(f'<h4 style=\'text-align: left; \'>{4.9}/5.0', unsafe_allow_html=True)
            

        with col5:
            #df1 = df[df['cuisines'] == 'Brazilian']
            #df1.loc[:,['aggregate_rating','restaurant_name']].groupby('restaurant_name').mean()
            #df1 = df1.sort_values(['aggregate_rating', 'restaurant_id'], ascending=[False, True])
            #df1 = df1.head(1)
            #Brasileira = (df1['restaurant_name'].values[0])
            #Nota_Brasileira = (df1['aggregate_rating'].values[0])
            st.write(f'<h6 style=\'text-align: left; \'>Brasileira: Braseiro da Gávea \n',unsafe_allow_html=True)
            st.write(f'<h4 style=\'text-align: left;\'>{4.9}/5.0', unsafe_allow_html=True)

st.markdown ("""___""")

with st.container():

    col1 = st.columns(1)
        
    st.subheader(f'Top {value} melhores restaurantes')

    df1 = df[df['aggregate_rating'] == 4.90]
    df1 = df1.loc[:,['restaurant_id','restaurant_name','country_code','city','cuisines','average_cost_for_two','aggregate_rating','votes']]
    Melhores_Restaurantes = df1.sort_values(['restaurant_id'], ascending=True).reset_index().head(value)
    st.dataframe( Melhores_Restaurantes)


st.markdown ("""___""")

with st.container():
    col1,col2 = st.columns(2,gap='large')

    with col1:

        st.subheader(f'Culinárias com piores Médias')
        df1 = df.copy()
        df2 = df1.loc[:,['cuisines','aggregate_rating']].groupby('cuisines').mean().sort_values('aggregate_rating',ascending=True).head(value).reset_index()
        fig=px.bar(df2,x='cuisines',y='aggregate_rating')
        fig .update_layout(xaxis_title='Culinárias')
        fig .update_layout(yaxis_title='Avaliações Médias')
        st.plotly_chart(fig, use_container_width=True)

        with col2:
        
            st.subheader(f'Culinárias com melhores Médias')
            
            df3 = df1.loc[:,['cuisines','aggregate_rating']].groupby('cuisines').mean().sort_values('aggregate_rating', ascending=False).head(value).reset_index()
            fig=px.bar(df3,x='cuisines',y='aggregate_rating')
            fig .update_layout(xaxis_title='Culinárias')
            fig .update_layout(yaxis_title='Avaliações Médias')
            st.plotly_chart(fig, use_container_width=True)
    



with st.container():
        
    with col1:

        st.subheader('Média do Prato para 2 por Culinária')


    df = df.loc[:,['cuisines','average_cost_for_two']].groupby('cuisines').mean().reset_index().head(165)
    st.write(df)






