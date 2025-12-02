# AI-Driven Real-Time ECG Detection Device Using Convolutional Neural Networks

## 📌 Overview
This project implements a real-time ECG monitoring and arrhythmia detection system using an ESP32 microcontroller, BioAmp Heart Candy analog front-end, and a trained Convolutional Neural Network (CNN).  
The system acquires ECG data, displays it on an OLED, transmits samples to a backend server, and performs heartbeat classification using deep learning.

The goal is to provide a low-cost, portable, and intelligent cardiac monitoring solution suitable for telemedicine and continuous health assessment.

---

## 🚀 Features
- Real-time ECG acquisition using BioAmp Heart Candy  
- Wireless data transmission via ESP32 (Wi-Fi)  
- CNN-based arrhythmia classification  
- Web dashboard for real-time waveform visualization  
- Automated email alerts for abnormal ECG detection  
- Portable hardware with rechargeable power supply  
- Python backend for processing and inference  

---

## 🧰 Technology Stack
**Hardware:** ESP32-WROOM, BioAmp Heart Candy, OLED 1.3"  
**Backend:** Python, Flask  
**Machine Learning:** TensorFlow / Keras  
**Frontend:** HTML, JavaScript, Chart.js  
**Dataset:** MIT-BIH Arrhythmia Database  

---

## 📂 Project Structure

![Project_Structure](project_structure-1-1.png)

---

## ⚙️ Installation

### **1️⃣ Clone the repository**
git clone https://github.com/Mohammedhasnaine/arrhythmia-detection


cd arrhythmia-detection


### **2️⃣ Create a virtual environment**
python -m venv venv
venv\Scripts\activate # Windows


### **3️⃣ Install dependencies**
pip install -r requirements.txt


### **4️⃣ Configure Secrets**
Create `src/secrets.py`:

EMAIL_ADDRESS = "your_email"
EMAIL_PASSWORD = "your_app_password"


---

## ▶️ Running the Server

cd src


python appServer.py


Open in browser:

http://localhost:5000


---

## 🛑 Files Not Included in GitHub  
Due to GitHub’s file-size limits:

❌ `dataset/`  
❌ `models/`  
❌ `training2017/`  
❌ `training2017.zip`  
❌ `*.keras` model files  

These contain:

- MIT-BIH ECG recordings  
- Trained CNN model  
- Preprocessed heartbeat segments  

Download MIT-BIH dataset from PhysioNet:  
https://physionet.org/content/mitdb/1.0.0/

Place files manually in:

dataset/
models/
training2017/


---

## 🔬 How the System Works

### **1. ECG Signal Acquisition**
ESP32 samples analog ECG waveform from BioAmp Heart Candy.

### **2. Transmission**
Samples are sent to backend server via HTTP POST.

### **3. Processing**
Backend performs:
- Resampling  
- Scaling  
- Segmentation  
- R-peak alignment  

### **4. Classification**
CNN predicts heartbeat categories:
Normal, Ventricular, Fusion, etc.

### **5. Visualization**
Web UI displays:
- ECG waveform  
- Predicted label  
- Probability score  

### **6. Alerts**
Abnormal patterns → Email notification.

---

## 🧠 Model Summary
- Conv1D layers  
- ReLU activation  
- Max-Pooling  
- Dense fully-connected layers  
- Softmax classifier  
- Trained on MIT-BIH Arrhythmia Dataset  

---

## 📄 License
MIT License — Free for modification and distribution.