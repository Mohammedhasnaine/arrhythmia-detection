AI-Driven Real-Time ECG Arrhythmia Detection System using CNN & ESP32

This project implements an AI-powered real-time ECG monitoring system using the ESP32 microcontroller, BioAmp Heart Candy analog front-end, and a Convolutional Neural Network (CNN) for automated heartbeat classification.
The device captures ECG signals, sends them wirelessly to a backend server, processes them with a trained deep-learning model, and updates a web dashboard with real-time alerts.

 Features

Real-time ECG waveform acquisition using BioAmp Heart Candy

Wireless ECG streaming using ESP32 (Wi-Fi)

CNN-based arrhythmia classification (MIT-BIH dataset)

Web dashboard for live ECG visualization

Automatic email alert system for abnormal heartbeat detection

Noise-filtered and preprocessed ECG cycles

Backend built using Flask / Python

Deployable and portable biomedical monitoring device

 Project Structure
arrhythmia-detection/
│
├── dataset/               # MIT-BIH dataset (not included here)
├── models/                # Saved CNN model (.h5)
├── results/               # Graphs, metrics, and evaluation outputs
├── src/                   # Main project source code
│   ├── appServer.py       # Flask backend server for ECG processing
│   ├── utils/             # Helper utilities: filtering, segmentation, etc.
│   ├── train/             # Model training scripts
│   ├── predict/           # Real-time prediction pipeline
│   ├── templates/         # HTML files for Web UI
│   ├── static/            # CSS, JS, images
│   ├── secrets.py         # (Ignored) holds private passwords/API keys
│   └── ...
│
├── training2017/          # Training zip file (optional)
├── requirements.txt       # All Python dependencies
└── README.md              # THIS file

 Model Overview (CNN)

Input: 1-D ECG segment (resampled 360 samples)

Architecture:
Conv1D → ReLU → MaxPool → Conv1D → ReLU → Flatten → Dense → Softmax

Output Classes: {N, V, A, F}

Training Dataset: MIT-BIH Arrhythmia Database

Evaluation metrics: Accuracy, Precision, Recall, Confusion Matrix

 Hardware Used

ESP32-WROOM

BioAmp Heart Candy ECG Front-End

1.3-inch OLED Display (I²C)

Push Button

2200mAh Battery + 5V Power Bank Shell

ECG Chest Strap Electrodes

 How to Run the Backend Server
1️. Clone the repository
git clone https://github.com/<your-username>/arrhythmia-detection.git
cd arrhythmia-detection/src

2️. Install dependencies
pip install -r requirements.txt

3️. Create secrets.py

Inside src/ create:

EMAIL_ID = "your_email@gmail.com"
EMAIL_PWD = "your_app_password"


(This file stays local only, not uploaded to GitHub.)

4️. Start the Flask server
python appServer.py

5️. ESP32 will stream ECG to server automatically

The web dashboard opens at:

http://127.0.0.1:5000

 Web Dashboard

Displays real-time ECG waveform

Shows predicted heartbeat class

Triggers email alert if abnormal ECG detected

Stores uploaded ECG segments

 ESP32 Firmware Summary

Reads ECG analog values from BioAmp Heart Candy

Converts analog values → digital samples

Sends packets via Wi-Fi → Flask server using HTTP/POST

Displays short ECG preview on OLED

 Results Summary

CNN Accuracy: 97–99% (depending on training split)

Handles noise reasonably well with preprocessing

Successfully detects abnormal beats in real time

Low latency real-time system suitable for portable monitoring

 Disclaimer

This project is for academic and research purposes only.
It is NOT a medical device and must not be used for clinical diagnosis.


 License

MIT License — Free to modify and distribute.