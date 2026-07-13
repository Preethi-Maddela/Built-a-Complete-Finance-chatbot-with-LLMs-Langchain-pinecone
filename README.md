# Finance AI Chatbot with LLMs, LangChain & Pinecone

An AI-powered finance assistant that combines Retrieval-Augmented Generation (RAG) with deterministic financial calculators. It answers banking and finance questions grounded in real bank policy documents, and performs EMI, loan eligibility, and maximum loan calculations using precise formulas — not LLM guesswork.

## Features

- **RAG-based Q&A** — answers questions about loans, credit cards, ATMs, and RBI policies using your own PDF documents as the knowledge source
- **EMI Calculator** — instantly computes monthly installment, total payment, and total interest for a loan
- **Loan Eligibility Check** — evaluates whether a requested loan fits within standard FOIR (Fixed Obligation to Income Ratio) limits
- **Max Eligible Loan Estimator** — estimates the maximum loan amount an applicant could likely be approved for
- Automatically detects whether a question needs document retrieval or a financial calculation, and routes it accordingly

## Tech Stack

- **Python**
- **LangChain** — RAG orchestration and chains
- **Groq (Llama 3.3 70B)** — LLM for response generation
- **Pinecone** — vector database for semantic search
- **HuggingFace Sentence Transformers** — embedding model (`all-MiniLM-L6-v2`)
- **FastAPI** — backend API framework
- **Uvicorn** — ASGI server

## How to run?

### STEP 01 - Clone the repository
```bash
git clone https://github.com/Preethi-Maddela/Built-a-Complete-Finance-chatbot-with-LLMs-Langchain-pinecone.git
cd Built-a-Complete-Finance-chatbot-with-LLMs-Langchain-pinecone
```

### STEP 02 - Create a conda environment
```bash
conda create -n financebot python=3.10 -y
conda activate financebot
```

### STEP 03 - Install the requirements
```bash
pip install -r requirements.txt
```

### STEP 04 - Create a `.env` file in the root directory
Add your Pinecone and Groq API keys:
```ini
PINECONE_API_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
GROQ_API_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### STEP 05 - Add your PDF documents
Place your finance/banking PDF documents inside the `data/` folder.

### STEP 06 - Store embeddings in Pinecone
```bash
python store_index.py
```

### STEP 07 - Run the application
```bash
uvicorn app:app --reload
```

### STEP 08 - Open the app
Open your browser and go to:
