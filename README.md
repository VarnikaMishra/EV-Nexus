# EV-NEXUS 🏭⚡

**AI-Powered Industrial Asset Performance Management & Supply Chain Intelligence Platform**  
*Submission for ET AI Hackathon 2026*

<img width="1691" height="238" alt="image" src="https://github.com/user-attachments/assets/5143a268-2d8e-4b68-9e9a-2a05d6a05463" />



<img width="1881" height="802" alt="image" src="https://github.com/user-attachments/assets/2369eaac-ddeb-4a0c-b441-e601bd737e66" />



<img width="1847" height="798" alt="image" src="https://github.com/user-attachments/assets/1799f304-9550-4624-b157-282f2e90e6b0" />



<img width="1841" height="786" alt="image" src="https://github.com/user-attachments/assets/1875eaac-c3c4-4ec8-b007-fa0042f4331d" />



<img width="1842" height="744" alt="image" src="https://github.com/user-attachments/assets/3030a5cf-eab0-4c39-bfe4-2febff5c2f5f" />

**Tech-Stack**
![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-FF4B4B.svg)
![Gemini 3](https://img.shields.io/badge/AI_Engine-Gemini_3_Flash-8E75B2.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📖 Overview
**EV-NEXUS** is an enterprise-grade, dual-mode intelligence platform engineered to accelerate industrial fleet electrification and streamline upstream manufacturing quality control. It bridges the critical gap between downstream commercial fleet operations and upstream EV manufacturing traceability using advanced multi-modal reasoning.

## 🎯 The Problem & Solution Approach
* **The Commercial EV Gap:** Heavy industrial and commercial fleet sectors lag below 2.5% adoption due to unpredictable battery degradation and high operational risk. EV-Nexus solves this via **Portal 1 (Fleet APM & Dynamic Routing)** for real-time asset tracking and electrochemical state-of-health forecasting.
* **Supply Chain Fragility:** EV manufacturers face severe vulnerabilities in multi-tier material sourcing (Lithium, Cobalt, NMC/LFP cells). EV-Nexus provides **Portal 2 (OEM Command Center)** featuring a Quality Management System (QMS) drift detector and automated mitigation copilots.

## ⚙️ Tech Stack
* **Frontend & Dashboard:** Streamlit
* **Core Intelligence Engine:** Google GenAI / LangChain (`ChatGoogleGenerativeAI` with `gemini-3-flash-preview`)
* **Machine Learning & Analytics:** Scikit-learn (`RandomForestRegressor`), Joblib, NumPy, Pandas
* **Routing & Spatial Mapping:** Open Source Routing Machine (OSRM) API, Requests

## 🚀 Key Features
* **Battery Degradation Prediction:** Real-time cell telemetry combined with electrochemical physics equations to forecast State-of-Health (SoH).
* **AI Trip & APM Consultant:** Powered by Gemini 3 Flash to provide natural language conversational insights on active vehicle configurations.
* **OSRM Live Route Estimator:** Computes real-world coordinates and trip distances via OpenStreetMap Nominatim and OSRM servers.
* **QMS Manufacturing Drift Detector:** Correlates internal resistance variations and cell-to-cell voltage spreads to isolate assembly flaws before final pack production.
* **Multilingual Localization:** Dynamic toggle support for English and Hindi operational controls.

## 🛠️ Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone [https://github.com/your-username/EV-Nexus.git](https://github.com/your-username/EV-Nexus.git)
   cd EV-Nexus
   ```
2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Install Dependencies**
  GOOGLE_API_KEY=your_gemini_api_key_here
   ```bash
   Configure Environment Variables
   ```
4. **Add Machine Learning Model**
   Ensure your pre-trained model file (battery_model.pkl) is placed in the root directory. If omitted, the system will fall back to baseline      mathematical calculations automatically.
6. **Run the Application**
   ```bash
   streamlit run app.py
   ```
   
