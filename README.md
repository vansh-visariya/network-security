# Network Security System

An end-to-end network security system using MLOps and ETL pipeline for phishing detection and network threat analysis.

## 🚀 Project Overview

This project implements a comprehensive network security solution that leverages machine learning to detect phishing websites and network threats. The system includes data ingestion, validation, transformation, model training, and deployment components with MLOps best practices.

## 🏗️ Architecture

- **Data Pipeline**: ETL pipeline with MongoDB integration
- **ML Pipeline**: Automated training with drift detection
- **API**: FastAPI-based REST API for predictions
- **MLOps**: MLflow integration with DagsHub for experiment tracking
- **Deployment**: Docker containerization with CI/CD

## 📋 Features

- **Phishing Detection**: ML models to identify malicious websites
- **Data Drift Detection**: Automated monitoring of data distribution changes
- **Real-time Predictions**: FastAPI endpoints for live inference
- **Model Versioning**: MLflow integration for experiment tracking
- **Automated Pipeline**: End-to-end training and validation pipeline
- **Web Interface**: HTML templates for prediction visualization

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI, Uvicorn
- **Database**: MongoDB with PyMongo
- **ML Libraries**: Scikit-learn, Pandas, NumPy
- **MLOps**: MLflow, DagsHub
- **Deployment**: Docker, GitHub Actions
- **Frontend**: Jinja2 Templates, HTML/CSS

## 📦 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd network-security
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create .env file
MONGO_ALAS_PASS=your_mongodb_connection_string
```

## 🚀 Usage

### Training Pipeline
```bash
python -c "from network_security.pipeline.training_pipeline import TrainingPipeline; pipeline = TrainingPipeline(); pipeline.run_pipeline()"
```

### Start API Server
```bash
python app.py
```

### Make Predictions
- Upload CSV file to `/predict` endpoint
- View results in web interface

## 📊 API Endpoints

- `GET /`: Redirect to API documentation
- `GET /train`: Trigger model training pipeline
- `POST /predict`: Upload CSV for batch predictions

## 🐳 Docker Deployment

```bash
# Build image
docker build -t network-security .

# Run container
docker run -p 8080:8080 network-security
```

## 📁 Project Structure

```
network-security/
├── network_security/           # Main package
│   ├── components/            # Pipeline components
│   ├── pipeline/              # Training pipeline
│   ├── utils/                 # Utility functions
│   ├── logging/               # Logging configuration
│   └── exception/             # Custom exceptions
├── template/                  # HTML templates
├── test_data/                 # Test datasets
├── app.py                     # FastAPI application
├── push_data.py              # Data ingestion script
└── requirements.txt          # Dependencies
```

## 🔧 Configuration

The system uses YAML configuration files and environment variables for:
- Database connections
- Model parameters
- Pipeline settings
- Drift detection thresholds

## 📈 Monitoring

- **Data Drift**: Kolmogorov-Smirnov test for distribution changes
- **Model Performance**: Automated evaluation metrics
- **Logging**: Comprehensive logging throughout the pipeline

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Vansh Visariya**

---

*Built with ❤️ for network security and machine learning*
