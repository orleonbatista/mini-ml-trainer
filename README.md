# How to
docker build -t mini-ml-platform-train -f docker/train.Dockerfile .
docker run --rm mini-ml-platform-train


# Considerações Futuras
## Versionamento de Modelos:
* Armazenar os modelos treinados em S3 (ou similar) com controle de versão.
* Permitir a seleção de modelos ja existem em qualquer versão
## Gerenciamento de Experimentos:
* Integração futura com ferramentas como MLflow ou DVC para registrar parâmetros e métricas.
