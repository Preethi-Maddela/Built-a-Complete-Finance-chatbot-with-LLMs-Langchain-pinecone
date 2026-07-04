# Built-a-Complete-Finance-chatbot-with-LLMs-Langchain-pinecone
# How to run?
### STEPS:

Clone the repository

```bash
git clonehttps://github.com/Preethi-Maddela/Built-a-Complete-Finance-chatbot-with-LLMs-Langchain-pinecone.git
```
### STEP 01- Create a conda environment after opening the repository

```bash
conda create -n financebot python=3.10 -y
```

```bash
conda activate financebot
```


### STEP 02- install the requirements
```bash
pip install -r requirements.txt
```


### Create a `.env` file in the root directory and add your Pinecone & openai credentials as follows:

```ini
PINECONE_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
GROQ_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```


```bash
# run the following command to store embeddings to pinecone
python store_index.py
```

```bash
# Finally run the following command
python app.py
```

Now,
```bash
open up localhost:
```


### Techstack Used:

- Python
- LangChain
- Flask
- GPT
- Pinecone



# Azure-CICD-Deployment-with-Github-Actions

## 1. Login to Azure Portal.

## 2. Create a Service Principal for deployment

	#with specific access

	1. Azure Container Registry access : To push/pull docker images

	2. Azure Container Apps / App Service access : To deploy and run the container


	#Description: About the deployment

	1. Build docker image of the source code

	2. Push your docker image to Azure Container Registry (ACR)

	3. Create/Configure Azure Container App

	4. Pull your image from ACR into the Container App

	5. Launch your docker image on Azure Container Apps

	#Role Assignments:

	1. AcrPush

	2. Contributor

	
## 3. Create Azure Container Registry (ACR) to store/save docker image
    - Save the Login Server URI: financechatbotacr.azurecr.io/financebot

	
## 4. Create Azure Container App Environment 

## 5. Configure the Container App to pull and run the Docker image:
	
	
	#optional

	az acr login --name financechatbotacr

	
	#required

	az acr build --registry financechatbotacr --image financebot:latest .

	az containerapp create --name financebot --resource-group finance-rg \
	  --image financechatbotacr.azurecr.io/financebot:latest \
	  --target-port 8000 --ingress external

	az containerapp update --name financebot --resource-group finance-rg \
	  --image financechatbotacr.azurecr.io/financebot:latest
	
# 6. Configure GitHub Actions as the deployment runner:
    settings > secrets and variables > actions > new repository secret > add Azure credentials one by one


# 7. Setup github secrets:

   - AZURE_CLIENT_ID
   - AZURE_TENANT_ID
   - AZURE_SUBSCRIPTION_ID
   - ACR_LOGIN_SERVER
   - ACR_USERNAME
   - ACR_PASSWORD
   - PINECONE_API_KEY
   - OPENAI_API_KEY