AI-Driven Real-Time ECG Detection Device Using Convolutional Neural Networks
Overview

This project implements a real-time ECG monitoring and arrhythmia detection system using an ESP32 microcontroller, BioAmp Heart Candy analog front-end, and a trained Convolutional Neural Network (CNN).
The device collects single-lead ECG signals, displays them on an OLED screen, transmits them to a backend server, and performs automated heartbeat classification and alerting.

Features

Real-time ECG acquisition

Wireless transmission via ESP32 (Wi-Fi)

CNN-based arrhythmia classification

Web dashboard visualization

Email alerts for abnormal ECGs

Portable wearable hardware

Flask-based Python backend

Technology Stack

Hardware: ESP32-WROOM, BioAmp Heart Candy, 1.3" OLED, Li-ion battery
Backend: Python, Flask
ML Framework: TensorFlow / Keras
Frontend: HTML, JavaScript, Chart.js
Dataset: MIT-BIH Arrhythmia Database

Project Structure
arrhythmia-detection/
│
├── dataset/                # (Not included)
├── models/                 # (Not included)
├── results/                # Evaluation outputs
├── src/
│   ├── static/             
│   ├── templates/          
│   ├── uploads/           
│   ├── appServer.py        
│   ├── predict.py          
│   ├── config.py           
│   ├── graph.py            
│   ├── testMail.py         
│   ├── train/             
│   └── utils/              
│
├── training2017/           # (Not included)
├── requirements.txt
└── README.md

Installation
1. Clone the repository
git clone https://github.com/Mohammedhasnaine/arrhythmia-detection
cd arrhythmia-detection

2. Create a virtual environment
python -m venv venv
venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Configure secrets

Create a file src/secrets.py:

EMAIL_ADDRESS = "your_email"
EMAIL_PASSWORD = "your_app_password"

Running the Server
cd src
python appServer.py


Then open:

http://localhost:5000

Files Not Included (Important)

Due to GitHub restrictions and dataset licenses, these are not uploaded:

dataset/
models/
training2017/
training2017.zip
*.keras


These contain:

MIT-BIH dataset

Trained CNN model

Large training archives

Preprocessed ECG segments

To run the project:

Download dataset from:
https://physionet.org/content/mitdb/1.0.0/

Place the files into:

dataset/
models/
training2017/

How the System Works
1. ECG Signal Acquisition

ESP32 reads analog ECG data from BioAmp Heart Candy.

2. Transmission

Samples are sent to the server using HTTP POST.

3. Processing on Server

Resampling

Normalization

Segmentation

R-Peak alignment

4. Classification

CNN predicts heartbeat types such as:

Normal

Ventricular

Fusion

5. Visualization

Web UI displays ECG graph and model prediction.

6. Alerts

Email is triggered for abnormal beats.

Model Summary

Conv1D layers

ReLU activation

MaxPooling1D

Dense classifier

Softmax output probabilities

Trained on MIT-BIH dataset

License

This project is provided for academic and research use.