# 📌 Análise emissão de CO2 por veículos 
![imagem](relatorios/imagens/imagem1.jpg)
<p align="center">
  <sub>
    Image by rawpixel.com on Freepik: https://br.freepik.com/fotos-gratis/trafego-lotado-e-movimentado-na-estrada_16497169.htm/
  </sub>
</p>


## 📊 Análise de Emissões de CO2 em Veículos

<sub>PT 🇧🇷</sub>

Visão Geral do Projeto

Este projeto tem como objetivo prever e analisar as emissões de CO2 em veículos automotores com base em características técnicas, de desempenho e categorização dos veículos. Foram utilizadas técnicas de machine learning para identificar os principais fatores que influenciam as emissões e desenvolver modelos preditivos precisos.

## 🔍 Contexto
Base retirada do site do [governo
canadense](https://open.canada.ca/data/en/dataset/98f1a129-f628-4ce4-b24d-6f16bf24dd64).

Os conjuntos de dados fornecem classificações de consumo de combustível específicas do
modelo e emissões estimadas de dióxido de carbono para novos veículos leves para venda
no varejo no Canadá entre os anos de 2005 e 2024.
![grafico](relatorios/imagens/grafico_barras.png)

## 📊 Análise Exploratória

#### Base: 

Nas análises gráficas, foi constatada a relação entre número de cilindros, tamanho do motor e especialmente consumo de combustível em litros por km , assim como indicação de uma relação inversamente proporcional entre emissão de CO2 e ano do modelo - pode estar relacionado com melhores tecnologias - precisa ser melhor avaliado para entender a razão.

No Canadá, o uso do etanol parece estar associado a veículos de maior porte.

Também é possível constatar uma queda na quantidade de veículos, no país. 


Para preparar a base para o modelo de machine learning optei por:

    * remoção de vazamento de dados (colunas que contêm informação do target)
    
    * agrupamento de categorias esparsas
    
    * criação de features mais robustas
    

#### Distribuições: 

É possível perceber que a distribuição das features numéricas estão bem próximas do normal, embora um pouco assimétricas (com exceção do model_year).



## ⚙️ Machine Learning

#### ESTRATÉGIA DE PRÉ-PROCESSAMENTO:

1. Variáveis categóricas não ordenadas: One-Hot Encoding
   (para classes sem relação ordinal)
2. Variáveis categóricas ordenadas: Ordinal Encoding
   (para classes com relação ordinal explícita)
3. Variáveis numéricas:
   - Normalização Min-Max para 'model_year' (distribuição quase normal)
   - Power Transform para outras numéricas (assimetria presente)

##### DIFERENCIAÇÃO DE PRÉ-PROCESSAMENTO:

1. Para modelos lineares/SVM/KNN: Normalização mais robusta
   - OneHotEncoding para categóricas
   - PowerTransformer para numéricas assimétricas
2. Para modelos baseados em árvores: Menos pré-processamento necessário
   - Apenas codificação ordinal/one-hot
   - Não requer normalização de features numéricas

#### ESTRATÉGIA DE MODELAGEM:
Testar diversos tipos de algoritmos:
    - Lineares (simples, interpretáveis)
    - Baseados em árvores (potentes para relações não-lineares)
    - SVM (para comparação)
    - Usar validação cruzada para avaliação robusta
    - Avaliar o melhor modelo para tunagem de hiperparâmetros



#### OBSERVAÇÕES INICIAIS:

1. Modelos lineares (Ridge, LinearRegression) apresentam excelente desempenho (R² ~1.0)
2. Lasso teve desempenho ruim 
3. Modelos baseados em árvores têm desempenho similar entre si (R² ~0.82)
4. KNN também apresentou excelente desempenho


### --- OTIMIZAÇÃO DO MODELO RIDGE ---


JUSTIFICATIVA PARA ESCOLHA DO RIDGE:

1. Excelente desempenho (melhor RMSE entre os lineares)
2. Permite interpretação dos coeficientes
3. Mais estável que LinearRegression puro
4. Menor tempo de execução que SVM/KNN

![grafico](relatorios/imagens/tipo_combustivel.png)

📉 Resultados
Melhor modelo: Ridge Regression (α=0.75)

RMSE: 3.72 g CO2/km

R²: 0.999

Interpretabilidade: Excelente (coeficientes lineares)

#### Comparativo de Modelos

🔎 Insights Principais
Fatores que AUMENTAM emissões:

Consumo urbano (+0.76 coeficiente)

Consumo rodoviário (+0.43)

Tamanho do motor (categorias superiores)

Fatores que REDUZEM emissões:

Uso de etanol (-2.15 vs gasolina)

Gasolina premium (-0.62 vs regular)

Veículos especiais (-0.03)

## 📌 Conclusão
Modelos lineares apresentaram desempenho excepcional, sugerindo forte relação linear entre features e target

O Ridge Regression mostrou o melhor equilíbrio entre desempenho e interpretabilidade

Variáveis de consumo (urbano/rodoviário) são os principais drivers das emissões

Combustíveis alternativos (como etanol) mostraram impacto positivo na redução de emissões

### Insights:

   - Pesquisar se a razão da redução de veículos está associada ao investimento de transporte público, carros elétricos ou a um cenário econômico. Avaliar se é uma tendência e seu impacto na redução de emissão CO2. 


![grafico](relatorios/imagens/ezgif-72d0dc05046601.gif)
## App

#### Nos links abaixo você encontra os links para um app com os dados, gráficos interativos e o resultado do modelo, onde você pode inserir os dados de um veículo e estimar quanto ele emite de dióxido de carbono.

O primeiro link traz um gráfico super bacana (treemap) que permite a interação por fabricante, ano do modelo, marca. Ao passar o cursor sobre ele, também mostra informações sobre combustível, quantidade de veículos e emissão de dióxido de carbono. Como esse gráfico traz muitas informações e 'interações', o carregamento do app é mais lento, exige um pouco de paciência.

['Clique aqui para explorar os dados e fazer uma estimativa '](https://emissaoco2-fbps.streamlit.app/)


O segundo app é para quem não gosta de esperar, traz todas as informações e gráficos menos o treemap e o filtro.

['Clique aqui para explorar os dados e fazer uma estimativa '](https://emissaoco2-fast-fbps.streamlit.app/)

![grafico](relatorios/imagens/ezgif-73f0a5d4dafbac.gif)

📌 CO2 Emissions Analysis by Vehicles


<sub>EN</sub>


## 📊 CO2 Emissions Analysis in Vehicles

🇬🇧 Project Overview
This project aims to predict and analyze CO2 emissions from motor vehicles based on technical specifications, performance, and vehicle categorization. Machine learning techniques were used to identify the main factors influencing emissions and to develop accurate predictive models.

## 🔍 Context
Dataset sourced from the Canadian government.

The datasets provide model-specific fuel consumption ratings and estimated carbon dioxide emissions for new light-duty vehicles available for retail sale in Canada between 2005 and 2024.
![grafico](relatorios/imagens/make_co2.png)

## 📊 Exploratory Analysis

Dataset:
The relationship between the number of cylinders, engine size, and especially fuel consumption in liters per km was observed in graphical analyses, along with an indication of an inverse relationship between CO2 emissions and model year.
This may be related to improved technology. Further analysis is needed to understand the reason.

In Canada, ethanol use appears to be associated with larger vehicles.

A decline in the number of vehicles in Canada was also observed.

To prepare the dataset for the machine learning model, I opted for:

Removal of data leakage (columns containing target information)

Grouping of sparse categories

Creation of more robust features

Distributions:
It is noticeable that the distribution of numerical features is close to normal, although slightly skewed (except for model_year).

## ⚙️ Machine Learning

#### PREPROCESSING STRATEGY:
Unordered categorical variables: One-Hot Encoding
(for classes without ordinal relationship)

Ordered categorical variables: Ordinal Encoding
(for classes with explicit ordinal relationship)

Numerical variables:

Min-Max Normalization for model_year (nearly normal distribution)

Power Transform for other numerical features (due to skewness)

#### DIFFERENTIATED PREPROCESSING:
For linear/SVM/KNN models: more robust normalization

OneHotEncoding for categorical variables

PowerTransformer for skewed numerical features

For tree-based models: less preprocessing required

Only ordinal/one-hot encoding

No normalization required for numerical features

#### MODELING STRATEGY:
Test various types of algorithms:

Linear models (simple, interpretable)

Tree-based models (powerful for non-linear relationships)

SVM (for comparison)

Use cross-validation for robust evaluation

Evaluate the best model for hyperparameter tuning

INITIAL OBSERVATIONS:
Linear models (Ridge, LinearRegression) showed excellent performance (R² ~1.0)

Lasso performed poorly

Tree-based models had similar performance (R² ~0.82)

KNN also performed very well

#### --- RIDGE MODEL OPTIMIZATION ---
REASONS FOR CHOOSING RIDGE:

Excellent performance (best RMSE among linear models)

Allows interpretation of coefficients

More stable than pure LinearRegression

Faster execution time than SVM/KNN


## 📉 Results
Best model: Ridge Regression (α=0.75)

RMSE: 3.72 g CO2/km
R²: 0.999
Interpretability: Excellent (linear coefficients)

## Model Comparison

###  🔎 Key Insights

Factors that INCREASE emissions:

City consumption (+0.76 coefficient)

Highway consumption (+0.43)

Engine size (higher categories)

Factors that DECREASE emissions:

Ethanol use (-2.15 vs gasoline)

Premium gasoline (-0.62 vs regular)

Special vehicles (-0.03)

## 📌 Conclusion
Linear models showed exceptional performance, suggesting a strong linear relationship between features and target.

Ridge Regression provided the best balance between performance and interpretability.

Consumption variables (city/highway) are the main drivers of emissions.

Alternative fuels (such as ethanol) showed a positive impact on reducing emissions.

Further Insights:
Investigate whether the reduction in the number of vehicles is associated with public transportation investment, electric vehicles, or economic conditions. Assess whether this is a trend and its impact on CO2 emissions.


## App

The links below take you to an app with the data, interactive charts, and the model results, where you can input vehicle data and estimate how much carbon dioxide it emits.
The first link includes a very cool treemap that allows interaction by manufacturer, model year, and brand. Hovering over the chart shows information about fuel type, number of vehicles, and CO2 emissions. Since this chart has lots of information and interaction, the app may take longer to load — a bit of patience is needed.

Click here to explore the data and make an estimate

['Clique aqui para explorar os dados e fazer uma estimativa '](https://emissaoco2-fbps.streamlit.app/)

The second app is for those who don't like waiting — it contains all the information and charts, except the treemap! =)

['Clique aqui para explorar os dados e fazer uma estimativa '](https://emissaoco2-fbps.streamlit.app/)

![grafico](relatorios/imagens/ezgif-72d0dc05046601.gif)



## Organização do projeto

```

├── dados              <- Arquivos de dados para o projeto.
├── modelos            <- Modelos gerados para o projeto.
|
├── notebooks          <- Cadernos Jupyter. 
│
|   └──src             <- Código-fonte para uso neste projeto.
|      │
|      ├── __init__.py  <- Torna um módulo Python
|      ├── auxiliares.py<- Funções auxiliares do projeto
|      ├── config.py    <- Configurações básicas do projeto
|      ├── graficos.py  <- Scripts para criar visualizações exploratórias e orientadas a resultados
|      └── modelos.py   <- Funções utilizadas no modelo
|
├── referencias        <- Dicionários de dados.
├── relatorios         <- Relatório gerado durante o projeto utilizando a biblioteca [ydata-profiling]
│   └── imagens        <- Gráficos e figuras gerados para serem usados em relatórios
├── ambiente.yml       <- O arquivo de requisitos para reproduzir o ambiente de análise
├── requirements.txt   <- O arquivo para instalar dependências via pip
├── LICENSE            <- Licença de código aberto se uma for escolhida
├── README.md          <- README principal para desenvolvedores que usam este projeto.
|
```

## Configuração do ambiente

1. Faça o clone do repositório que será criado a partir deste modelo.

    ```bash
    git clone ENDERECO_DO_REPOSITORIO
    ```

2. Crie um ambiente virtual para o seu projeto utilizando o gerenciador de ambientes de sua preferência.

    a. Caso esteja utilizando o `conda`, exporte as dependências do ambiente para o arquivo `ambiente.yml`:

      ```bash
      conda env export > ambiente.yml
      ```

    b. Caso esteja utilizando outro gerenciador de ambientes, exporte as dependências
    para o arquivo `requirements.txt` ou outro formato de sua preferência. Adicione o
    arquivo ao controle de versão, removendo o arquivo `ambiente.yml`.



Para mais informações sobre como usar Git e GitHub, [clique aqui](https://cienciaprogramada.com.br/2021/09/guia-definitivo-git-github/). Sobre ambientes virtuais, [clique aqui](https://cienciaprogramada.com.br/2020/08/ambiente-virtual-projeto-python/).

