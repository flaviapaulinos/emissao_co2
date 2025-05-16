
import numpy as np
import pandas as pd

import plotly.express as px #para mostrar os dados da analise exploratória de forma interativa
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import streamlit as st

from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,

)
from joblib import load

from notebooks.src.config import DADOS_TRATADOS, DADOS_TRAD, MODELO_FINAL, IMAGEM_1

#para o arquivo não ficar sendo recarregado o tempo inteiro
@st.cache_data
def carregar_dados(arquivo):
    return pd.read_parquet(arquivo)

#para carregar o modelo
@st.cache_resource
def carregar_modelo(arquivo):
    return load(arquivo)

    

df_tratado = carregar_dados(DADOS_TRATADOS)
df_traduzido = carregar_dados(DADOS_TRAD)

modelo=carregar_modelo(MODELO_FINAL)


df_traduzido = df_traduzido[
    [
        'ano do modelo', 
        'marca', 
        'modelo', 
        'emissões co2 g/km',
        'classe', 
        'tamanho do motor /l',
        'cilindros', 
        'transmissão', 
        'combustível', 
        'consumo urbano l/100km',
        'consumo estrada l/100km', 
        'consumo combinado l/100km',      
    ]
]


 #dicionário para valores mais amigáveis

mapa_transmissao = {
    'A': 'automática',
    'M': 'manual',
    'AS': 'automática com troca seletiva',
    'AV': 'variável Contínua',
    'AM': 'manual automatizada'
}
#para inserir no dataframe
mapa_transmissao_inverso = {v: k for k, v in mapa_transmissao.items()}

mapa_combustivel = {
    'reg_gasoline': 'gasolina',
    'premium_gasoline': 'gasolina preium',
    'ethanol': 'ethanol',
    'diesel': 'diesel',
}
mapa_combustivel_inverso = {v: k for k, v in mapa_combustivel.items()}

mapa_veiculo = {
     'car': 'carro',
     'suv': 'suv/ utiltário esportivo',
     'station_wagon': 'station-wagon/ perua',
     'van': 'van',
     'pickup_truck': 'caminhonete',
     'special_purpose': 'Veículo de uso especial ',
}
mapa_veiculo_inverso = {v: k for k, v in mapa_veiculo.items()}

mapa_motor = {
    'up_to_1.9': 'até 1,9 litros',
    'up_to_3':  'até 3 litros',
    'up_to_5':  'até 5 litros',
    'more_than_5': 'mais de 5 litros',  
}
mapa_motor_inverso = {v: k for k, v in mapa_motor.items()}

mapa_cilindros = {
    'up_to_4': 'até 4 cilindros',
    'up_to_6': 'até 6 cilindros',
    'up_to_8': 'até 8 cilindros',
    'more_than_8': 'mais de 8 cilindros',
   
}
mapa_cilindros_inverso = {v: k for k, v in mapa_cilindros.items()}
st.image(IMAGEM_1, "imagem de freepik.com")


#criar abas no streamlit
aba1, aba2, aba3 = st.tabs(['Dados', 'Faça uma estimativa', 'Informações'])

with aba1:

    #informações sobre os gráficos
    st.info("""
    Análise de emissão de dióxido de carbono por veículos entre 2005 e 2024 
                  (dados retirados do site governo canadense).  
                  
    **Fique à vontade para explorar!**  
    
    Você pode interagir com os gráficos e tabelas:  
    - Adicione filtros  
    - Amplie áreas específicas  
    - Clique nas legendas para ativar/desativar itens  
    """)

    
    #passar nosso dataframe para que as pessoas possam interagir com ele e fazer pesquisas inclusive
    df_filter = df_traduzido
    st.dataframe(
        df_filter.style.background_gradient(
            subset=['emissões co2 g/km', 'consumo combinado l/100km'],
            cmap='RdYlGn_r',
        )
    )
    cmin, cmax=(
    df_filter['emissões co2 g/km'].min(),
    df_filter['emissões co2 g/km'].max(),
    )

    #criar a contagem de veívulos
    df_filter['contagem']=1

  

    #grafico de barras plotly
    #posso fazer um gráfico independente da seleção aplicadas acima (usando o data frame df_traduzido)
    #mas vou fazer em formato de dashboard, vinculando as informações e por isso vou usar o df_filter
    fig2 = px.bar(
        df_filter[['marca', 'emissões co2 g/km']].groupby('marca').mean().reset_index(),
        x='marca',
        y='emissões co2 g/km',
        title='Média de emissão de CO<sub>2</sub> por fabricante(g/km)', #2 subescrito usando html
        color='emissões co2 g/km',
        color_continuous_scale="RdYlGn_r",
        hover_data= {'emissões co2 g/km': ":.2f"},
        
    )
    fig2.update_xaxes(categoryorder="total descending")
    fig2.data[0].update(marker_cmin=cmin, marker_cmax=cmax)
    fig2.add_hline(
        y = df_filter['emissões co2 g/km'].mean(),
        line_dash='dot',
        line_color='grey',
    )
    fig2.add_annotation(
        xref='paper',
        x=0.95,
        y=df_filter['emissões co2 g/km'].mean(),
        text=f'Média: {df_filter['emissões co2 g/km'].mean():.2f}g/km',
        showarrow=False,
        yshift=10
    )
        
    
    st.plotly_chart(fig2)

     #grafico de barras plotly
    #posso fazer um gráfico independente da seleção aplicadas acima (usando o data frame df_traduzido)
    #mas vou fazer em formato de dashboard, vinculando as informações e por isso vou usar o df_filter
    fig3 = px.bar(
        df_filter[['classe', 'emissões co2 g/km']].groupby('classe').mean().reset_index(),
        x='classe',
        y='emissões co2 g/km',
        title='Média de emissão de CO<sub>2</sub> por classe de veículo(g/km)', #2 subescrito usando html
        color='emissões co2 g/km',
        color_continuous_scale="RdYlGn_r",
        hover_data= {'emissões co2 g/km': ":.2f"},
        range_color=[cmin, cmax]
        
    )
    fig3.update_xaxes(categoryorder="total descending")
    fig3.data[0].update(marker_cmin=cmin, marker_cmax=cmax)
    fig3.add_hline(
        y = df_filter['emissões co2 g/km'].mean(),
        line_dash='dot',
        line_color='grey',
    )
    fig3.add_annotation(
        xref='paper',
        x=0.95,
        y=df_filter['emissões co2 g/km'].mean(),
        text=f'Média: {df_filter['emissões co2 g/km'].mean():.2f}g/km',
        showarrow=False,
        yshift=10
    )
        
    
    st.plotly_chart(fig3)

  
    fig4= px.scatter(
        df_filter,
        x= 'consumo combinado l/100km',
        y='emissões co2 g/km',
        title='Emissão de CO<sub>2</sub> x Consumo Combinado x Tipo de Combustível', #2 subescrito usando html
        color='combustível',
        color_discrete_sequence=px.colors.qualitative.Light24,
        #hover_data= {'emissões co2 g/km': ":.2f"},
        labels = {'consumo combinado l/100km': 'consumo combinado (l/ 100 km)',
                  'emissões co2 g/km': 'emissão de CO<sub>2</sub> (g/km)'
                 }
    )
    st.plotly_chart(fig4)

 
    fig5= px.scatter(
        df_filter,
        x= 'consumo combinado l/100km',
        y='emissões co2 g/km',
        title='Emissão de CO<sub>2</sub> x Consumo Combinado x Tipo de Classe de Veículo', #2 subescrito usando html
        color='classe',
        color_discrete_sequence=px.colors.qualitative.Light24,
        #hover_data= {'emissões co2 g/km': ":.2f"},
        labels = {'consumo combinado l/100km': 'consumo combinado (l/ 100 km)',
                  'emissões co2 g/km': 'emissão de CO<sub>2</sub> (g/km)'
                 }
    )
    st.plotly_chart(fig5)
    
    fig6 = px.bar(
        df_filter[[ 'ano do modelo', 'emissões co2 g/km']].groupby('ano do modelo').mean().reset_index(),
        x= 'ano do modelo',
        y='emissões co2 g/km',
        title='Média de emissão de CO<sub>2</sub> por ano do modelo(g/km)', #2 subescrito usando html
        color='emissões co2 g/km',
        color_continuous_scale="RdYlGn_r",
        hover_data= {'emissões co2 g/km': ":.2f"},
        range_color=[cmin, cmax]
        
    )
    fig6.update_xaxes(categoryorder="total descending")
    fig6.data[0].update(marker_cmin=cmin, marker_cmax=cmax)
    fig6.add_hline(
        y = df_filter['emissões co2 g/km'].mean(),
        line_dash='dot',
        line_color='grey',
    )
    fig6.add_annotation(
        xref='paper',
        x=0.95,
        y=df_filter['emissões co2 g/km'].mean(),
        text=f'Média: {df_filter['emissões co2 g/km'].mean():.2f}g/km',
        showarrow=False,
        yshift=10
    )
             
    st.plotly_chart(fig6)

 

    
with aba2:
    #modelo regressão 
    #primeiro passar as entradas necessárias
    #pegar elementos de entrada, colocar em forma de dataframe, passar para o modelo
    #para pegar os elementos de entrada, vamos buscar os Dados_tratados

    #colunas selectbox
    anos = sorted(df_tratado['model_year'].unique())
    transmissao = sorted(df_tratado['transmission'].unique())
    combustivel = sorted(df_tratado['fuel_type'].unique())
    tipo_veiculo = sorted(df_tratado['vehicle_class'].unique())
    tamanho_motor = sorted(df_tratado['engine_size_l'].unique())
    cilindros = sorted(df_tratado['cylinders'].unique())   
    

    #colunas slider
    colunas_slider = (
        'city_l_100_km',
        'highway_l_100_km',
        'combined_l_100_km',
    )

    colunas_slider_min_max = {
        coluna: {
            'min_value': df_tratado[coluna].min(),
            'max_value': df_tratado[coluna].max(),
        }
        for coluna in colunas_slider
    }
    #para evitar da página ficar recarregando o tempo inteiro vou colocar os widgets dentro de um formulário. Assim todas as caixas só serão recarregadas quando eu clicar em submeter

    with st.form(key='formulario'):

        #criar colunas
        coluna_esquerda, coluna_direita = st.columns(2)

        with coluna_esquerda:

            #widgets selectbox
            widget_ano=st.selectbox("Ano", anos)

            lista_transmissao = [mapa_transmissao[val] for val in transmissao]
            widget_transmissao = st.selectbox("Transmissão", lista_transmissao)

            lista_combustivel = [mapa_combustivel[val] for val in combustivel]
            widget_combustivel= st.selectbox("Combustível", lista_combustivel)
            
            
        with coluna_direita:
            
             #widgets selectbox

            lista_veiculo = [mapa_veiculo[val] for val in tipo_veiculo]
            widget_tipo_veiculo= st.selectbox("Tipo de veículo",  lista_veiculo)

            lista_motor = [mapa_motor[val] for val in tamanho_motor]
            widget_tamanho_motor=st.selectbox("Tamanho do motor em litros", lista_motor)

            lista_cilindros = [mapa_cilindros[val] for val in cilindros]
            widget_cilindros =st.selectbox("Quantidade de cilindros", lista_cilindros) 
            
            
         #widgets slider
        widget_city = st.slider(
            "Consumo urbano (litros/100 km)",
            **colunas_slider_min_max["city_l_100_km"]
        )
            
        widget_highway = st.slider(
            "Consumo na estrada (litros/100 km)",
            **colunas_slider_min_max["highway_l_100_km"]
        )
            
        widget_combined = st.slider(
            "Consumo combinado (estrada e urbano - litros/100 km)",
            **colunas_slider_min_max["combined_l_100_km"]
        )

        #botao previsao (fechar formulário)
        botao_previsao = st.form_submit_button("Prever emissão")

    #criar o data frame para abastecer o modelo
    entrada_modelo = {
        'model_year': widget_ano,
        'engine_size_l':  mapa_motor_inverso[widget_tamanho_motor],
        'cylinders': mapa_cilindros_inverso[widget_cilindros],
        'transmission': mapa_transmissao_inverso[widget_transmissao],
        'fuel_type': mapa_combustivel_inverso[widget_combustivel],
        'city_l_100_km': widget_city,
        'highway_l_100_km' :widget_highway, 
        'combined_l_100_km': widget_combined ,
        'vehicle_class': mapa_veiculo_inverso[widget_tipo_veiculo],
    }
    df_entrada_modelo = pd.DataFrame([entrada_modelo])

    #enviar dados para o modelo

    if botao_previsao:
        emissao =  modelo.predict(df_entrada_modelo)
        st.metric(label="Emissão prevista (g/km)", value=f"{emissao[0][0]:.2f}")

    with aba3:
        #definir urls
        url1 = "https://open.canada.ca/data/en/dataset/98f1a129-f628-4ce4-b24d-6f16bf24dd64"
        url2 = "https://natural-resources.canada.ca/energy-efficiency/transportation-alternative-fuels/personal-vehicles/choosing-right-vehicle/buying-electric-vehicle/understanding-the-tables/21383"
        
        st.info("""
        
        Os conjuntos de dados fornecem classificações de consumo de combustível específicas do modelo e emissões estimadas de dióxido de carbono para novos veículos leves para venda no varejo no Canadá.
        
         """)
        st.markdown(f'Base retirada do site do governo canadense: [{url1}]')

        st.markdown(f'Detalhes sobre as terminologias estão disponíveis aqui: [{url2}] e resumidos a seguir.')
         
        st.markdown("""
        
        ### **Dados**

        | Dado                        | Descrição                                                                                 
        |-----------------------------|--------------------------------------------------------------------------------------------
        | `ano do Modelo`             | ano do modelo                                                                              
        | `marca`                     | fabricante                                                                                 
        | `modelo`                    | modelo (ver abaixo)                                                                       
        | `classe`                    | classe do veículo (ver abaixo)                                                            
        |  `tamanho do motor /l`     | tamanho do motor em litros                                                               
        | `cilindros`                 | número de cilindros                                                                      
        | `transmissão`               | tipo de transmissão (ver abaixo)                                                          
        | `combustível`               | tipo de combustível (ver abaixo)                                                           
        | `consumo urbano l/100km`   | consumo de combustível em L/100 km em perímetro urbano                                    
        | `consumo estrada l/100km`   | consumo de combustível em L/100 km em estradas                                            
        | `consumo combinado l/100km `| consumo de combustível em L/100 km considerando 55% em perímetro urbano e 45 % em estradas                                
        | `emissões co2 g/km`         | emissão de CO2 em g/km de percurso combinado                                              
  
        ---

        
        ### **Detalhes para a coluna `Modelo`**
        - **AWD**: Tração nas quatro rodas (veículo projetado para operar com todas as rodas acionadas).
        - **4WD / 4X4**: Tração nas quatro rodas (duas ou quatro rodas acionadas).
        - **FFV**: Veículo flexível a combustível (opera com gasolina e até 85% de etanol - E85).
        - **CNG**: Gás natural comprimido; **NGV**: Veículo a gás natural.
        - **SWB**: Distância entre eixos curta; **LWB**: Distância entre eixos longa; **EWB**: Distância entre eixos estendida; **#**: Motor de alta potência.
        
        ---
        
        ### **Detalhes para a coluna `Classe`**
        #### 🚗 **Carros**
        | Classe do veículo               | Volume interno               |
        |---------------------------------|-------------------------------|
        | Dois lugares (T)                | n/a                           |
        | Minicompacto (I)                | < 2.405 L (85 cu. ft.)        |
        | Subcompacto (S)                 | 2.405–2.830 L (85–99 cu. ft.) |
        | Compacto (C)                    | 2.830–3.115 L (100–109 cu. ft.) |
        | **Médio (M)**                   | 3.115–3.400 L (110–119 cu. ft.) |
        | **Grande (L)**                  | ≥ 3.400 L (120 cu. ft.)       |
        
        #### 🚙 **Caminhonetes, Caminhões e Vans**
        | Classe do veículo               | Peso bruto do veículo         |
        |---------------------------------|-------------------------------|
        | Caminhonetes - Pequena (PS)     | < 2.722 kg (6.000 lb)         |
        | Caminhonetes - Padrão (PL)      | 2.722–3.856 kg (6.000–8.500 lb) |
        | Utilitário esportivo - Pequeno (US) | < 2.722 kg (6.000 lb)      |
        
        *L = litros; cu. ft. = pés cúbicos; kg = quilogramas; lb = libras.*
        
        ---
        
        ### **Detalhes para a coluna `Transmissão`**
        - **A**: Automático
        - **AM**: Manual automatizado
        - **AS**: Automático com troca seletiva
        - **AV**: Variável contínua
        - **M**: Manual
        - **Nº de marchas**: (1–10 velocidades)
    """)

        

    
   


