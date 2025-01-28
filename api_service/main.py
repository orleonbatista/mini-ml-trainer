import os
import requests
from fastapi import FastAPI, HTTPException, UploadFile, Form
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API Front",
    description=(
        "API para gerenciamento de treinamento e predição de modelos de Machine Learning.\n\n"
        "### Funcionalidades principais:\n"
        "- Enviar datasets para treinamento de modelos de Machine Learning.\n"
        "- Realizar predições usando modelos treinados.\n"
        "- Verificar o status dos serviços conectados.\n\n"
        "#### Observações:\n"
        "- Apenas arquivos no formato CSV são suportados para upload.\n"
        "- Utilize a configuração adequada para os parâmetros dos modelos durante o treinamento."
    ),
    version="1.0.0",
    contact={
        "name": "Orleon Batista",
        "email": "orleonbatista@gmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
)

TRAINER_URL = os.environ.get("TRAINER_URL", "http://trainer:8001")
PREDICT_URL = os.environ.get("PREDICT_URL", "http://predict:8002")

@app.post(
    "/train",
    summary="Treinar Modelo",
    description=(
        "Enviar um dataset para treinar um modelo de Machine Learning. Este endpoint aceita "
        "um arquivo CSV contendo os dados de treinamento e permite configurar o tipo de modelo, "
        "parâmetros adicionais e a coluna alvo para o treinamento."
    ),
    tags=["Treinamento"]
)
async def train(
    dataset_file: UploadFile,
    model_type: str = Form("RandomForestClassifier", description="Tipo do modelo a ser treinado (e.g., RandomForestClassifier, LogisticRegression)."),
    model_params: str = Form("{}", description="Parâmetros do modelo em formato JSON."),
    target_column: str = Form(..., description="Nome da coluna alvo no dataset."),
    columns_to_drop: str = Form(None, description="Nomes das colunas a serem ignoradas no dataset (se aplicável).")
):
    """
    Treinar um modelo usando um dataset fornecido.

    **Parâmetros:**
    - **dataset_file** (*UploadFile*): Arquivo CSV contendo os dados para treinamento.
    - **model_type** (*str*): Tipo do modelo de Machine Learning. Valor padrão: `RandomForestClassifier`.
    - **model_params** (*str*): Parâmetros adicionais para o modelo em formato JSON. Exemplo: `{"n_estimators": 100, "max_depth": 5}`.
    - **target_column** (*str*): Nome da coluna alvo no dataset para o treinamento.
    - **columns_to_drop** (*str*): Lista de colunas a serem ignoradas no dataset, separadas por vírgula (opcional).

    **Retornos:**
    - **200**: Sucesso. Retorna detalhes do treinamento e métricas do modelo.
    - **400**: Erro no formato do arquivo ou nos dados fornecidos.
    - **500**: Erro ao chamar o serviço Trainer.
    """
    if dataset_file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Apenas arquivos CSV são suportados.")

    files = {"dataset_file": (dataset_file.filename, dataset_file.file)}
    data = {
        "model_type": model_type,
        "model_params": model_params,
        "target_column": target_column,
        "columns_to_drop": columns_to_drop
    }
    try:
        response = requests.post(f"{TRAINER_URL}/train", files=files, data=data, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao chamar Trainer Service: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao chamar Trainer Service: {e}")


@app.post(
    "/predict",
    summary="Fazer Predições",
    description=(
        "Enviar um dataset para realizar predições usando um modelo treinado. "
        "Este endpoint aceita um arquivo CSV contendo os dados para predição e permite "
        "especificar colunas que devem ser ignoradas."
    ),
    tags=["Predição"]
)
async def predict(
    input_file: UploadFile,
    columns_to_drop: str = Form(None, description="Nomes das colunas a serem ignoradas no dataset para predição (se aplicável).")
):
    """
    Fazer predições usando um modelo treinado.

    **Parâmetros:**
    - **input_file** (*UploadFile*): Arquivo CSV contendo os dados para predição.
    - **columns_to_drop** (*str*): Lista de colunas a serem ignoradas no dataset, separadas por vírgula (opcional).

    **Retornos:**
    - **200**: Sucesso. Retorna as predições geradas pelo modelo.
    - **400**: Erro no formato do arquivo ou nos dados fornecidos.
    - **500**: Erro ao chamar o serviço Predict.
    """
    if input_file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Apenas arquivos CSV são suportados.")

    files = {"input_file": (input_file.filename, input_file.file)}
    data = {"columns_to_drop": columns_to_drop}
    try:
        response = requests.post(f"{PREDICT_URL}/predict", files=files, data=data, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao chamar Predict Service: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao chamar Predict Service: {e}")


@app.get(
    "/",
    summary="Status da API",
    description="Verificar o status da API Front e dos serviços conectados.",
    tags=["Status"]
)
def root():
    """
    Verificar o status dos serviços Trainer e Predict.

    **Retornos:**
    - **200**: Sucesso. Retorna informações sobre o status dos serviços Trainer e Predict.
    - **500**: Erro ao obter o status dos serviços conectados.
    """
    trainer_status = predict_status = None

    try:
        trainer_response = requests.get(f"{TRAINER_URL}/")
        trainer_response.raise_for_status()
        trainer_status = trainer_response.json()
    except requests.exceptions.RequestException as e:
        trainer_status = {"error": f"Trainer Service indisponível: {e}"}

    try:
        predict_response = requests.get(f"{PREDICT_URL}/")
        predict_response.raise_for_status()
        predict_status = predict_response.json()
    except requests.exceptions.RequestException as e:
        predict_status = {"error": f"Predict Service indisponível: {e}"}

    return {
        "message": "API Front ativa!",
        "trainer_status": trainer_status,
        "predict_status": predict_status
    }
