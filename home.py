import pandas as pd
import streamlit as st

from joblib import load

from notebooks.src.config import DADOS_LIMPOS, MODELO_FINAL


@st.cache_data
def carregar_dados():
    return pd.read_parquet(DADOS_LIMPOS)


@st.cache_resource
def carregar_modelo():
    return load(MODELO_FINAL)


df = carregar_dados()
modelo = carregar_modelo()

niveis_educacionais_texto = {
    1: "Educação Básica",
    2: "Educação Superior",
    3: "Bacharelado",
    4: "Mestrado",
    5: "Doutorado",
}

niveis_satisfacao_texto = {
    1: "Insatisfeito",
    2: "Razoável",
    3: "Satisfeito",
    4: "Muito satisfeito",
}

niveis_vida_trabalho_texto = {
    1: "Ruim",
    2: "Razoável",
    3: "Bom",
    4: "Excelente",
}

generos = sorted(df["Gênero"].unique())
niveis_educacionais = sorted(df["Formação acad"].unique())
area_formacao = sorted(df["Área form"].unique())
departamentos = sorted(df["Departamento"].unique())
viagem_negocios = sorted(df["Viagens trab"].unique())
hora_extra = sorted(df["Hora extra"].unique())
satisfacao_trabalho = sorted(df["Satisf trab"].unique())
satisfacao_colegas = sorted(df["Satisf relac"].unique())
satisfacao_ambiente = sorted(df["Satisf amb"].unique())
vida_trabalho = sorted(df["Equil vida-trab"].unique())
opcao_acoes = sorted(df["Opc ações"].unique())
envolvimento_trabalho = sorted(df["Envolv trab"].unique())

colunas_slider = [
    "Distância casa",
    "Renda mensal",
    "Nº empresas trab",
    "% aumento sal",
    "Anos traba",
    "Treinam ultm ano",
    "Anos empresa",
    "Anos cargo atual",
    "Anos ult prom",
    "Anos gerente atual",
]

colunas_slider_min_max = {
    coluna: {"min_value": df[coluna].min(), "max_value": df[coluna].max()}
    for coluna in colunas_slider
}

colunas_ignoradas = (
    "Idade",
    "Tarifa diária",
    "Nível cargo",
    "Tarifa hora",
    "Tarifa mensal",
    "Avaliação desemp",
)

medianas_colunas_ignoradas = {
    coluna: df[coluna].median() for coluna in colunas_ignoradas
}

st.title("Previsão de Atrito")

with st.container(border=True):
    st.write("### Informações pessoais")

    widget_genero = st.radio("Gênero", generos)

    widget_nivel_educacional = st.selectbox(
        "Nível Educacional",
        niveis_educacionais,
        format_func=lambda numero: niveis_educacionais_texto[numero]
    )

    widget_area_formacao = st.selectbox("Área de formação", area_formacao)

    widget_distancia_casa = st.slider(
        "Distância de casa em km", **colunas_slider_min_max["Distância casa"]
    )

with st.container(border=True):
    st.write("### Rotina na empresa")
     
    #criar colunas

    coluna_esquerda_rotina, coluna_direita_rotina = st.columns(2)

    with coluna_esquerda_rotina:
        widget_departamento = st.selectbox("Departamento", departamentos)
        widget_viagem_negocios = st.selectbox("Viagem Negócios", viagem_negocios)

    with coluna_direita_rotina:
        widget_cargo = st.selectbox(
            "Cargo",
            sorted(df[df["Departamento"] == widget_departamento]["Cargo"].unique())
        )
    
        widget_horas_extras = st.radio("Horas Extras", hora_extra)

    #fora das colunas
    widget_salario_mensal = st.slider(
        "Salário Mensal", **colunas_slider_min_max["Renda mensal"]
    )

with st.container(border=True):
    st.write("### Experiência profissional")
   
    #criar colunas

    coluna_esquerda_experiencia, coluna_direita_experiencia = st.columns(2)

    with coluna_esquerda_experiencia:
        widget_empresas_trabalhadas = st.slider(
            "Empresas trabalhadas", **colunas_slider_min_max["Nº empresas trab"]
        )
        widget_anos_trabalhados = st.slider(
            "Anos trabalhados", **colunas_slider_min_max["Anos traba"]
        )
        widget_anos_empresa = st.slider(
            "Anos na Empresa", **colunas_slider_min_max["Anos empresa"]
        )

    with coluna_direita_experiencia:
        widget_anos_cargo_atual = st.slider(
            "Anos no Cargo Atual", **colunas_slider_min_max["Anos cargo atual"]
        )
        widget_anos_mesmo_gerente = st.slider(
            "Anos com o Mesmo Gerente", **colunas_slider_min_max["Anos gerente atual"]
        )
        widget_anos_ultima_promocao = st.slider(
            "Anos Desde a Última Promoção",
            **colunas_slider_min_max["Anos ult prom"]
        )
        
with st.container(border=True):
    st.write("### Incentivos e métricas")
    
    coluna_esquerda_incentivo, coluna_direita_incentivo = st.columns(2)

    with coluna_esquerda_incentivo:
        widget_satisfacao_trabalho = st.selectbox(
            "Satisfação no Trabalho",
            satisfacao_trabalho,
            format_func=lambda numero: niveis_satisfacao_texto[numero],
        )

        widget_satisfacao_colegas = st.selectbox(
            "Satisfação com Colegas",
            satisfacao_colegas,
            format_func=lambda numero: niveis_satisfacao_texto[numero],
        )

        widget_envolvimento_trabalho = st.selectbox(
            "Envolvimento no Trabalho", envolvimento_trabalho
        )
        
    with coluna_direita_incentivo:
        widget_satisfacao_ambiente = st.selectbox(
            "Satisfação com Ambiente",
            satisfacao_ambiente,
            format_func=lambda numero: niveis_satisfacao_texto[numero],
        )
        
        widget_balanco_vida_trabalho = st.selectbox(
            "Balanço Vida-Trabalho",
            vida_trabalho,
            format_func=lambda numero: niveis_vida_trabalho_texto[numero],
        )

        widget_opcao_acoes = st.radio("Opção de Ações", opcao_acoes)

    widget_aumento_salarial = st.slider(
        "Aumento Salarial (%)",
        **colunas_slider_min_max["% aumento sal"]
    )
    
    widget_treinamentos_ultimo_ano = st.slider(
        "Treinamentos no Último Ano",
        **colunas_slider_min_max["Treinam ultm ano"]
    )



entrada_modelo = {
    "Idade": medianas_colunas_ignoradas["Idade"],
    "Viagens trab": widget_viagem_negocios,
    "Tarifa diária": medianas_colunas_ignoradas["Tarifa diária"],
    "Departamento": widget_departamento,
    "Distância casa": widget_distancia_casa,
    "Formação acad": widget_nivel_educacional,
    "Área form": widget_area_formacao,
    "Satisf amb": widget_satisfacao_ambiente,
    "Gênero": widget_genero,
    "Tarifa hora": medianas_colunas_ignoradas["Tarifa hora"],
    "Envolv trab": widget_envolvimento_trabalho,
    "Nível cargo": medianas_colunas_ignoradas["Nível cargo"],
    "Cargo": widget_cargo,
    "Satisf trab": widget_satisfacao_trabalho,
    "Estado civil": "Solteiro",
    "Renda mensal": widget_salario_mensal,
    "Tarifa mensal": medianas_colunas_ignoradas["Tarifa mensal"],
    "Nº empresas trab": widget_empresas_trabalhadas,
    "Avaliação desemp": medianas_colunas_ignoradas["Avaliação desemp"],
    "Hora extra": widget_horas_extras,
    "% aumento sal": widget_aumento_salarial,
    "Satisf relac": widget_satisfacao_colegas,
    "Opc ações": widget_opcao_acoes,
    "Anos traba": widget_anos_trabalhados,
    "Treinam ultm ano": widget_treinamentos_ultimo_ano,
    "Equil vida-trab": widget_balanco_vida_trabalho,
    "Anos empresa": widget_anos_empresa,
    "Anos cargo atual": widget_anos_cargo_atual,
    "Anos ult prom": widget_anos_ultima_promocao,
    "Anos gerente atual": widget_anos_mesmo_gerente,
}

df_entrada_modelo = pd.DataFrame([entrada_modelo])
#além da previsão eu quero um valor de probabilidade associado:

botao_previsao = st.button("Prever Atrito")

if botao_previsao:
    previsao = modelo.predict(df_entrada_modelo)[0]
    probabilidade_atrito = modelo.predict_proba(df_entrada_modelo)[0][1]
    #o zero é porque sai na forma de um array. eu quero a primeira posiçao e a segunda coluna (é um array de arrays)

    cor = ":red" if previsao == 1 else ":green"

    texto_probabilidade = (
        f"#### Probabilidade de Atrito: {cor}[{probabilidade_atrito:.1%}]"
    )
    texto_atrito = f"#### Atrito: {cor}[{'Sim' if previsao == 1 else 'Não'}]"

    st.markdown(texto_atrito)
    st.markdown(texto_probabilidade)