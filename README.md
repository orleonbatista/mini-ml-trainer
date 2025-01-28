# iFood ML Engineer Test

The goal of the exercises below is to evaluate the candidate knowledge and problem solving expertise regarding the main development focuses for the iFood ML Platform team.

## Mini ML Platform

Part of the ML Engineer job is to ensure the models developed by the Data Scientists are correctly deployed to the production environment, and are accessible via a REST microservice.

### Deliverables

There are two goals for this exercise. The first one is to create an automated ML model training process.

The second one is to create a Rest API documented with Swagger that serves a ML model predictions.

This process/pipeline should be generic enough to implement any models, with any data.

Languages, frameworks, platforms are not a constraint, but your solution must be inside a docker image, docker compose, script or notebook ready to be run. Training a model or serving the Rest API/Swagger structure should be as simple as running a script or something similar. You should also provide a README file on how to execute the training job, and how to request the API or Swagger. There are a lot of tools that solve most of this problem; while you are free to use them, please try to balance the time you will save by using them with being able to show your programming skills by not using them as much.

Important:
- Your solution must be easily deployed on a personal machine. Provide all the instructions required to be able to run your code.
- You are building a Mini Platform, mini because you will not have the time to build something completely, so you can document some of your future decisions in your README or code.
- Remember that you are not building the ML Model Itself. We'll not evaluate the results of your inference (just use iris dataset with any algorithm as a sample if you want to). We'll evaluate the experience
of deploying a new model. You should consider the evaluators as the Model Developers using your platform.


## AWS infrastructure

The last skill a ML Engineer must have is cloud proficiency. For iFood, AWS is our cloud of choice.

For this exercise, we would like for you to propose an AWS architecture to serve a solution for one of the two previous exercises. A single page describing the resources needed is sufficient, although you are free to provide code if you like it. Please have in mind that this structure must be reliable, scalable and as cheap as possible without compromising the other two requisites.

## BONUS!!

These exercises are all optional! They are not required to evaluate how you'll perform in this job, and they require no skills listed in the job description whatsoever! They are fun and difficult, though 😈

Let's get to it!

### Level 1 and 2

Can you figure out the passwords for the binaries `bonus/level01` and `bonus/level02`?

### Level 3

Can you get a shell from the binary `bonus/level03`?

```
 Ex.
 $ ./bonus/level03
 [+] calling some crazy function, can you get a shell?
 password: something_that_executes_/bin/sh
 $ echo "Habemus shell!"
```






# How to
docker build -t mini-ml-platform-train -f docker/train.Dockerfile .
docker run --rm mini-ml-platform-train


# Considerações Futuras
## Versionamento de Modelos:
* Armazenar os modelos treinados em S3 (ou similar) com controle de versão.
* Permitir a seleção de modelos ja existem em qualquer versão
## Gerenciamento de Experimentos:
* Integração futura com ferramentas como MLflow ou DVC para registrar parâmetros e métricas.



mini_ml_platform/
│
├── dataset_manager/               # Módulo de gerenciamento de datasets
│   ├── __init__.py                # Indica que é um pacote Python
│   ├── default_datasets.py        # Contém métodos para carregar datasets padrão (ex: Iris)
│   ├── local_datasets.py          # Contém métodos para carregar datasets locais (CSV, Excel)
│   └── dataset_manager.py         # Classe central para gerenciar os datasets (default + local)
│
├── api/                           # Módulo para a API de previsão
│   ├── __init__.py
│   ├── main.py                    # Entrypoint para a API (FastAPI/Flask)
│   ├── endpoints.py               # Definições dos endpoints da API
│   └── models/                    # Diretório para armazenar os modelos treinados
│       └── model.pkl              # Exemplo de modelo treinado (serializado)
│
├── training_pipeline/             # Módulo para pipeline de treinamento
│   ├── __init__.py
│   ├── trainer.py                 # Pipeline genérico de treinamento de modelos
│   └── utils.py                   # Funções auxiliares para o pipeline de treinamento
│
├── tests/                         # Diretório para testes automatizados
│   ├── __init__.py
│   ├── test_dataset_manager.py    # Testes para o módulo dataset_manager
│   ├── test_api.py                # Testes para a API
│   └── test_training_pipeline.py  # Testes para o pipeline de treinamento
│
├── Dockerfile                     # Configuração do Docker para containerização
├── docker-compose.yml             # Arquivo para orquestração com Docker Compose
├── requirements.txt               # Dependências Python do projeto
├── README.md                      # Instruções de uso e configuração do projeto
└── run.py                         # Entrypoint para execução do projeto
