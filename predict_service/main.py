import os
from fastapi import FastAPI, HTTPException, UploadFile, Form
import pandas as pd
from training_pipeline.trainer import Trainer
from training_pipeline.utils import parse_columns_to_drop
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Predict Service",
    description=(
        "API para realizar predições utilizando modelos de Machine Learning previamente treinados.\n\n"
        "### Funcionalidades principais:\n"
        "- Realizar predições com base em datasets fornecidos.\n"
        "- Suporte para exclusão de colunas específicas durante o processamento dos dados.\n\n"
        "#### Observações:\n"
        "- Apenas arquivos CSV são aceitos como entrada.\n"
        "- Certifique-se de que um modelo treinado está disponível no caminho configurado antes de realizar predições."
    ),
    version="1.0.0",
    contact={
        "name": "Equipe de Suporte",
        "email": "suporte@predict-service.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
)

@app.post(
    "/predict",
    summary="Realizar Predições",
    description=(
        "Enviar um dataset para gerar predições utilizando um modelo previamente treinado. "
        "Este endpoint aceita um arquivo CSV contendo os dados e permite especificar colunas que devem ser ignoradas."
    ),
    tags=["Predições"]
)
async def predict(
    input_file: UploadFile,
    columns_to_drop: str = Form(None, description="Lista de colunas a serem descartadas no dataset, separadas por vírgula (opcional).")
):
    """
    Realizar predições utilizando um modelo treinado.

    **Parâmetros:**
    - **input_file** (*UploadFile*): Arquivo CSV contendo os dados para realizar as predições.
    - **columns_to_drop** (*str*): Lista de colunas a serem ignoradas no dataset, separadas por vírgula (opcional).

    **Retornos:**
    - **200**: Sucesso. Retorna as predições geradas pelo modelo.
    - **404**: Modelo não encontrado no caminho especificado.
    - **400**: Erro ao ler o arquivo CSV fornecido.
    - **500**: Erro ao realizar as predições ou ao carregar o modelo.
    """
    model_path = "/shared-data/models/model.pkl"
    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail="Modelo não encontrado.")

    try:
        data = pd.read_csv(input_file.file)
        logger.info(f"Dataset carregado com sucesso a partir do arquivo {input_file.filename}.")
    except Exception as e:
        logger.error(f"Erro ao ler o arquivo CSV: {e}")
        raise HTTPException(status_code=400, detail=f"Erro ao ler o arquivo CSV: {e}")

    columns_to_drop_list = parse_columns_to_drop(columns_to_drop)
    trainer = Trainer(model_dir="/shared-data/models", model_class=None)
    try:
        trainer.load_model()
        logger.info("Modelo carregado com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao carregar o modelo: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao carregar o modelo: {e}")

    try:
        predictions = trainer.predict(data, columns_to_drop=columns_to_drop_list)
        logger.info(f"Predições realizadas com sucesso.")
        return {"predictions": predictions}
    except Exception as e:
        logger.error(f"Erro ao fazer predições: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao fazer predições: {e}")


@app.get(
    "/",
    summary="Status do Serviço",
    description="Verificar se o Predict Service está ativo e pronto para gerar predições.",
    tags=["Status"]
)
def root():
    """
    Verificar o status do serviço.

    **Retornos:**
    - **200**: Sucesso. O serviço está ativo.
    """
    return {"message": "Predict Service ativo e pronto para gerar predições!"}
