from pathlib import Path
PASTA_PROJETO = Path(__file__).resolve().parents[2]
PASTA_RELATORIOS = PASTA_PROJETO / "relatorios"

PASTA_DADOS = PASTA_PROJETO / "dados"
PASTA_IMAGENS = PASTA_RELATORIOS / "imagens"
PASTA_MODELOS = PASTA_PROJETO / "modelos"


DADOS_ORIGINAIS = PASTA_DADOS / "employee_attrition.csv"
DADOS_TRATADOS = PASTA_DADOS / "employee_attrition_tratados.parquet"
DADOS_LIMPOS = PASTA_DADOS / "employee_attrition_limpos.parquet" 


RELATORIO = PASTA_RELATORIOS / "00-fbps-eda.html"
MODELO = PASTA_MODELOS / "modelo.pkl"
MODELO_FINAL = PASTA_MODELOS / "logistic_regression.joblib"





