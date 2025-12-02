AI-Driven Real-Time ECG Detection Device Using Convolutional Neural Networks

Overview

This project implements a real-time ECG monitoring and arrhythmia detection system using an ESP32 microcontroller, BioAmp Heart Candy analog front-end, and a trained Convolutional Neural Network (CNN) model.
The device acquires single-lead ECG signals, displays the waveform locally on an OLED module, transmits samples to a backend server, and generates automated analysis and alerts using a deep learning classifier.

The purpose of this project is to provide a low-cost, portable, and intelligent cardiac monitoring solution suitable for telemedicine and continuous health assessment.

Features

Real-time ECG acquisition using BioAmp Heart Candy

Wireless data transmission via ESP32 (Wi-Fi)

CNN-based arrhythmia classification

Web dashboard for waveform visualization

Automated email alerts for abnormal ECG detection

Portable hardware with rechargeable power supply

Python backend for inference and processing

Technology Stack

Hardware: ESP32-WROOM, BioAmp Heart Candy, 1.3-inch OLED (I2C), Li-ion battery
Backend: Python, Flask
Machine Learning: TensorFlow / Keras
Frontend: HTML, JavaScript, Chart.js
Dataset: MIT-BIH Arrhythmia Database

Project Structure
arrhythmia-detection/
│
├── dataset/                # (Not included) Raw and processed ECG data
├── models/                 # (Not included) Trained CNN model (.keras)
├── results/                # Graphs and evaluation outputs
├── src/
│   ├── static/             # CSS, JS
│   ├── templates/          # HTML files
│   ├── uploads/            # Uploaded ECG CSVs
│   ├── appServer.py        # Flask backend server
│   ├── config.py
│   ├── data.py
│   ├── graph.py
│   ├── predict.py          # Model loading & prediction logic
│   ├── testMail.py         # Email alert functionality
│   ├── train/
│   └── utils/
│
├── training2017/           # (Not included) Training dataset
├── training2017.zip        # (Not included)
├── requirements.txt
└── README.md

Installation
1. Clone the repository
git clone https://github.com/Mohammedhasnaine/arrhythmia-detection
cd arrhythmia-detection

2. Create a virtual environment
python -m venv venv
venv\Scripts\activate      (Windows)

3. Install dependencies
pip install -r requirements.txt

4. Configure secrets

Create secrets.py inside src/:

EMAIL_ADDRESS = "your_email"
EMAIL_PASSWORD = "your_app_password"

Running the Server
cd src
python appServer.py


Open in browser:

http://localhost:5000

Files Not Included in Repository

Due to GitHub file-size restrictions and dataset licensing, the following items are not uploaded:

dataset/
models/
training2017/
training2017.zip
*.keras (trained model files)


These directories contain:

MIT-BIH training and testing samples

Trained CNN model used for arrhythmia classification

Preprocessed heartbeat segments

Large dataset archives

To run the project locally:

Download MIT-BIH dataset from PhysioNet:
https://physionet.org/content/mitdb/1.0.0/

Place the files in:

dataset/


Place the trained model in:

models/


(Optional) Place training data files in:

training2017/

How the System Works
1. ECG Signal Acquisition

ESP32 samples the analog waveform from BioAmp Heart Candy at a defined sampling rate.

2. Transmission

ECG samples are sent to the Python backend via HTTP POST requests.

3. Processing

The backend performs resampling, scaling, segmentation, and R-peak alignment.

4. Classification

A CNN model predicts heartbeat categories such as Normal, Ventricular, Fusion, etc.

5. Visualization

The web UI displays:

Real-time ECG waveform

Predicted label

Probability score

6. Alerts

Abnormal patterns trigger email notifications.

Model Summary

CNN with multiple Conv1D layers

ReLU activation

Max-pooling

Dense classification head

Trained on MIT-BIH Arrhythmia Database

Softmax output for probability distribution


 License

MIT License — Free to modify and distribute.