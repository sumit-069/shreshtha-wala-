# 🛡️ Fraud Shield — Online Payment Fraud Detection

Real-time online payment fraud detection web application powered by Machine Learning and Streamlit. Built using the synthetic financial dataset PaySim to classify transactions into legitimate or fraudulent.

---

## 🌟 Features

- **Real-Time Classification:** Instant fraud risk evaluation for incoming transaction parameters.
- **Interactive Modern UI:** Premium glassmorphism dark theme with animated probability gauges and metric cards.
- **Custom Risk Thresholding:** Adjust decision boundaries on the fly (0.10 to 0.90) to tune between precision and recall.
- **Detailed Feature Inspector:** View the exact one-hot encoded vector supplied to the ML classifier.

---

## 🛠️ Tech Stack & Libraries

- **Frontend & App Framework:** [Streamlit](https://streamlit.io/)
- **Machine Learning & Preprocessing:** [Scikit-Learn](https://scikit-learn.org/), [XGBoost](https://xgboost.readthedocs.io/), [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Model Serialization:** [Joblib](https://joblib.readthedocs.io/)

---

## 📁 Repository Structure

```text
├── app.py                                       # Streamlit web application
├── Online_Payment_Fraud_Detection_Basic.ipynb   # Model training & EDA notebook
├── fraud_detection_model.pkl                    # Serialized best-performing ML model
├── fraud_detection_features.pkl                 # List of feature column names
├── requirements.txt                             # Python dependencies
└── README.md                                    # Project documentation
```

---

## 🚀 Getting Started

### 1. Clone or Download Repository
```bash
git clone <YOUR_REPO_URL>
cd "Online-Payment-Fraud-Detection"
```

### 2. Install Dependencies
Make sure you have Python 3.9+ installed. Run:
```bash
pip install -r requirements.txt
```

### 3. Launch Streamlit Application
```bash
streamlit run app.py
```
The app will automatically open in your default browser at `http://localhost:8501`.

---

## 📊 Features & Model Inputs

| Feature Name | Description |
|---|---|
| `step` | Time step in simulation (1 hour per step, up to 744 hours / 30 days) |
| `type` | Transaction type: `CASH_IN`, `CASH_OUT`, `DEBIT`, `PAYMENT`, `TRANSFER` |
| `amount` | Transaction value in currency units |
| `oldbalanceOrg` | Initial balance of sender before transaction |
| `newbalanceOrig` | New balance of sender after transaction |
| `oldbalanceDest` | Initial balance of recipient before transaction |
| `newbalanceDest` | New balance of recipient after transaction |

---

## 📜 License
This project is open-source and available under the MIT License.
