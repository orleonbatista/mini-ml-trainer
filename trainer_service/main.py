import os
from fastapi import FastAPI, HTTPException, UploadFile, Form
import pandas as pd
from dataset_manager.dataset_manager import DatasetManager
from training_pipeline.trainer import Trainer
from training_pipeline.utils import parse_model_params, parse_columns_to_drop
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_FACTORY = {
    "RandomForestClassifier": RandomForestClassifier,
    "RandomForestRegressor": RandomForestRegressor,
    "LogisticRegression": LogisticRegression,
}

app = FastAPI(
    title="Trainer Service",
    description=(
        "API para treinamento de modelos de Machine Learning.\n\n"
        "### Funcionalidades principais:\n"
        "- Treinar modelos de Machine Learning utilizando datasets enviados ou padrões.\n"
        "- Suporte para múltiplos algoritmos como Random Forest e Logistic Regression.\n\n"
        "#### Observações:\n"
        "- Apenas arquivos CSV são aceitos como entrada.\n"
        "- Caso nenhum dataset seja enviado, será utilizado o dataset padrão.\n"
        "- Caso a coluna alvo (`target_column`) não seja especificada, será usada a última coluna do dataset."
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

@app.post(
    "/train",
    summary="Treinar Modelo",
    description=(
        "Endpoint para treinar um modelo de Machine Learning. "
        "Aceita um arquivo CSV contendo os dados para treinamento e permite configurar "
        "o tipo de modelo, parâmetros adicionais e colunas a serem descartadas."
    ),
    tags=["Treinamento"]
)
async def train(
    dataset_file: UploadFile = None,
    model_type: str = Form("RandomForestClassifier", description="Tipo do modelo de Machine Learning a ser treinado (e.g., RandomForestClassifier, LogisticRegression)."),
    model_params: str = Form("{}", description="Parâmetros do modelo em formato JSON. Exemplo: `{\"n_estimators\": 100}`."),
    target_column: str = Form(None, description="Nome da coluna alvo no dataset. Caso não seja especificado, será usada a última coluna."),
    columns_to_drop: str = Form(None, description="Lista de colunas a serem descartadas no dataset, separadas por vírgula (opcional).")
):
    """
    Treinar um modelo de Machine Learning.

    **Parâmetros:**
    - **dataset_file** (*UploadFile*): Arquivo CSV contendo os dados para treinamento (opcional).
    - **model_type** (*str*): Tipo do modelo a ser treinado. Exemplo: `RandomForestClassifier`, `LogisticRegression`.
    - **model_params** (*str*): Parâmetros adicionais para o modelo em formato JSON. Exemplo: `{"n_estimators": 100, "max_depth": 5}`.
    - **target_column** (*str*): Nome da coluna alvo no dataset. Caso não seja especificada, será usada a última coluna.
    - **columns_to_drop** (*str*): Lista de colunas a serem descartadas no dataset, separadas por vírgula (opcional).

    **Retornos:**
    - **200**: Sucesso. Retorna as métricas de avaliação do modelo e o caminho do modelo salvo.
    - **400**: Erro no formato do arquivo ou nos dados fornecidos.
    - **500**: Erro no treinamento ou ao carregar o dataset padrão.
    """
    if model_type not in MODEL_FACTORY:
        raise HTTPException(status_code=400, detail="Modelo não suportado.")

    dataset_manager = DatasetManager(default_dataset="iris")

    if dataset_file:
        try:
            data = pd.read_csv(dataset_file.file)
            logger.info(f"Dataset carregado com sucesso a partir do arquivo {dataset_file.filename}.")
        except Exception as e:
            logger.error(f"Erro ao carregar o arquivo CSV: {e}")
            raise HTTPException(status_code=400, detail=f"Erro ao carregar o arquivo CSV: {e}")
    else:
        try:
            data = dataset_manager.load_default_dataset()
            logger.info("Dataset padrão carregado com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao carregar o dataset padrão: {e}")
            raise HTTPException(status_code=500, detail=f"Erro ao carregar o dataset padrão: {e}")

    if target_column is None:
        target_column = data.columns[-1]
        logger.info(f"Coluna alvo não especificada. Usando a última coluna: {target_column}.")
    elif target_column not in data.columns:
        logger.error(f"A coluna alvo '{target_column}' não foi encontrada no dataset.")
        raise HTTPException(status_code=400, detail=f"Coluna alvo '{target_column}' não encontrada no dataset.")

    columns_to_drop_list = parse_columns_to_drop(columns_to_drop)
    model_params_dict = parse_model_params(model_params)
    model_class = MODEL_FACTORY[model_type]

    trainer = Trainer(
        model_dir="/shared-data/models",
        model_class=model_class,
        model_params=model_params_dict
    )
    try:
        metrics, model_path = trainer.train(
            data=data,
            target_column=target_column,
            columns_to_drop=columns_to_drop_list
        )
        logger.info(f"Modelo treinado com sucesso: {model_path}")
        return {"metrics": metrics, "model_path": model_path}
    except Exception as e:
        logger.error(f"Erro no treinamento: {e}")
        raise HTTPException(status_code=500, detail=f"Erro no treinamento: {e}")


@app.get(
    "/",
    summary="Status do Serviço",
    description="Verificar se o Trainer Service está ativo e pronto para treinar modelos.",
    tags=["Status"]
)
def root():
    """
    Verificar o status do serviço.

    **Retornos:**
    - **200**: Sucesso. O serviço está ativo.
    """
    return {"message": "Trainer Service ativo e pronto para treinar modelos!"}
