# GENEWISE

GENEWISE is an AI-powered web application that predicts rare diseases based on gene variant data. Designed for clinicians, geneticists, and researchers, GENEWISE leverages advanced machine learning and Gen Ai models to analyze genomic data and provide accurate disease predictions, variant classifications, and actionable insights.

## 🚀 Features

- 🧬 Input raw patient gene data (e.g., VCF, gene variants)
- 🤖 AI-powered gene variant classification
- 🧠 Gen-Ai disease prediction using custom knowledge base
- 📊 Knowledge database integration for efficient data retrieval
- 🧾 Clinically-relevant recommendations based on analysis
- 🔍 Transparent and interpretable AI decisions
- 💻 User-friendly web interface for ease of use

## 🧩 Tech Stack

- **Frontend:** React
- **Backend:** Python, FastAPI
- **AI/ML:** 
  - Custom LLM (Large Language Model) for gene interpretation
  - Gene variant classifier
- **Database:** 
  - Non Relational DB (e.g., MongoDB Atlas cloud)
- **Deployment:** Docker, CI/CD pipelines

## 🧪 How It Works

1. **Data Input:** Clinicians upload or input patient-specific genetic variant data.
2. **Variant Classification:** The system uses AI to classify variants based on known patterns and annotations.
3. **Disease Prediction:** A custom-trained LLM with a connected knowledge base predicts potential rare diseases and API.
4. **Recommendation Output:** Users receive a detailed report with predicted diseases, variant interpretation, and suggested clinical actions.

## 🛠️ Setup & Installation

### Prerequisites

- Python 3.9+
- Docker (optional, for containerized setup)

### Backend Setup

```bash
git clone https://github.com/your-username/genewise.git
cd genewise/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### FrontEnd Demo
https://genewise.github.io/GoogleDevSolChan/

### ML Model
https://genewiseml-ngqhbv9g3ikmntruqeaztn.streamlit.app/
https://genewisetumors-hrc5yds5eppm8akvedspcj.streamlit.app/
