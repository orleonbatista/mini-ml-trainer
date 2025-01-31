# **Mini-ML-Platform**

Plataforma modular para treinamento e predição de modelos de Machine Learning, baseada em containers Docker.

---

## **📌 Arquitetura e Funcionamento**
A plataforma utiliza uma **arquitetura baseada em microserviços** para garantir **escalabilidade, confiabilidade e eficiência de custos**.

Ela se divide em **três serviços distintos**, rodando como containers separados:

1. **API Service (`mini-ml-api`)**: Responsável por expor os endpoints REST e encaminhar requisições para os serviços adequados.
2. **Trainer Service (`mini-ml-trainer`)**: Realiza o treinamento de modelos de Machine Learning e os salva para uso posterior.
3. **Predict Service (`mini-ml-predict`)**: Carrega modelos treinados e realiza predições sobre novos dados.

Cada serviço opera **de forma independente**, garantindo modularidade e escalabilidade.

Para um detalhamento completo da arquitetura AWS de predição e treinamento de modelos, consulte a [Arquitetura](ARCHITECTURE.md).

---

## **📌 Tecnologias Utilizadas**

### **📌 Frameworks e Bibliotecas**
| Tecnologia | Função |
|------------|--------|
| **FastAPI** | Framework web para criação dos serviços REST (API, Trainer e Predict) |
| **Uvicorn** | Servidor ASGI leve e rápido para executar os serviços FastAPI |
| **Scikit-learn** | Biblioteca principal para treinamento e inferência de modelos de ML |
| **Pandas** | Manipulação de datasets e pré-processamento de dados |
| **Joblib** | Serialização e persistência dos modelos treinados |
| **Requests** | Comunicação entre microserviços via chamadas HTTP |
| **Pydantic** | Validação de dados e tipagem para entrada das APIs |

---

### **📌 Infraestrutura e Containerização**
| Tecnologia | Função |
|------------|--------|
| **Docker** | Containerização dos serviços |
| **Docker Compose** | Orquestração dos containers, definindo dependências e comunicação entre serviços |
| **Volumes Docker** | Compartilhamento de arquivos (modelos treinados) entre serviços |
| **Redes Docker** | Comunicação eficiente entre os microserviços |

---

## **📌 Como Usar**

### **Pré-requisitos**
- Docker instalado na máquina.
- Docker Compose instalado.
- Python 3.9+ instalado (para execução de testes).

---

### **📌 Passos para Build e Execução**

1. **Clone o repositório**:
   ```sh
   git clone https://github.com/orleonbatista/mini-ml-trainer.git
   ```

2. **Navegue até o diretório do projeto**:
   ```sh
   cd mini-ml-trainer/
   ```

3. **Construa e inicie os containers**:
   ```sh
   docker-compose up --build
   ```

4. **Para parar a execução dos containers**:
   ```sh
   docker-compose down
   ```

---

## **📌 Executando Testes**
1. **Rodar os testes unitários e de integração**:
   ```sh
   pytest
   ```

2. **Testar manualmente via Swagger ou cURL** (detalhado abaixo).

---

## **📌 Testando a API via Swagger**

O **Swagger UI** fornece uma interface interativa para testar os endpoints sem precisar usar `curl` ou Postman.

1. **Acesse a documentação interativa**:
   - **API Principal**: [`http://localhost:8000/docs`](http://localhost:8000/docs)
   - **Trainer Service**: [`http://localhost:8001/docs`](http://localhost:8001/docs)
   - **Predict Service**: [`http://localhost:8002/docs`](http://localhost:8002/docs)

2. **Testando um endpoint**:
   - Clique no endpoint desejado (`/train` ou `/predict`).
   - Clique em **Try it out**.
   - No campo `dataset_file`, selecione um arquivo CSV.
   - Preencha os outros parâmetros conforme necessário.
   - Clique em **Execute** para enviar a requisição.

---

## **📌 Testando a API via cURL**
Os arquivos de exemplo estão disponíveis no diretório **`samples/`** para facilitar os testes.

### **1. Treinamento de Modelo**
Executa o treinamento de um modelo usando o dataset `iris.csv`:
```sh
curl -X 'POST' \
  'http://localhost:8000/train' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'dataset_file=@samples/iris.csv;type=text/csv' \
  -F 'model_type=RandomForestClassifier' \
  -F 'model_params={}' \
  -F 'target_column=variety' \
  -F 'columns_to_drop='
```

---

### **2. Predição com Modelo Treinado**
Executa a predição usando um modelo treinado e o dataset `iris_predict.csv`:
```sh
curl -X 'POST' \
  'http://localhost:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'input_file=@samples/iris_predict.csv;type=text/csv' \
  -F 'columns_to_drop=["variety"]'
```

---

## **📌 Acessando os Serviços Manualmente**
Os serviços estarão disponíveis nas seguintes portas:

- **API Principal (`API Gateway`)**: [`http://localhost:8000`](http://localhost:8000)
- **Serviço de Treinamento (`Trainer Service`)**: [`http://localhost:8001`](http://localhost:8001)
- **Serviço de Predição (`Predict Service`)**: [`http://localhost:8002`](http://localhost:8002)

---

## **📌 Melhorias Futuras**
- **Versionamento de Modelos**:
  - Armazenar modelos em storage remoto com controle de versão.
  - Permitir seleção de modelos por versão.
- **Gerenciamento de Experimentos**:
  - Integração com ferramentas como MLflow ou DVC.
- **Tratamento de Exceções**:
  - Aprimorar identificação de falhas.
- **Volumes Nomeados ou Storage Externo**:
  - Uso de volumes ou storage remoto para persistência e escalabilidade.
- **Timeouts e Retentativas**:
  - Adicionar timeouts e lógica de retry nas comunicações HTTP.
- **Testes de unidade**:
  - Implementar e finalizar testes de unidade
- **Gerenciamento de Logs**:
  - Centralizar logs detalhados para facilitar monitoramento.
- **Configuração Baseada em Ambiente**:
  - Utilizar arquivos `.env` para variáveis sensíveis.
- **Segurança**:
  - Adicionar autenticação básica ou tokens JWT nos endpoints sensíveis.
- **Monitoramento em Tempo Real**:
  - Configurar métricas e monitoramento contínuo.
- **Escalabilidade**:
  - Migrar para ECS ou Kubernetes para maior resiliência e escalabilidade.

---

## **📌 Bônus**
Para verificar os desafios bônus, acesse essa [doc](BONUS.md).