# appServer.py
# coding=utf-8
from __future__ import division, print_function
import os
import numpy as np
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
from secrets import EMAIL_PASSWORD

from predict import *
from utils import *
from config import get_config
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

global classesM
classesM = ['N','V','L','R','Paced','A','F']
print('Check http://127.0.0.1:5002/')
# keep track of last uploaded file
last_uploaded_file = None
def mailResult(result):
    
# ---------- CONFIG ----------
    sender_email = "mohammedhasnaine2005@gmail.com"
    receiver_email = "mohammedmultazam17@gmail.com"
    password = EMAIL_PASSWORD  # Use an App Password, not your Gmail password, imported from secrets.py,
    subject = "ECG Result"
    body = result

# ---------- CREATE MESSAGE ----------
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

# ---------- SEND EMAIL ----------
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure connection
            server.login(sender_email, password)
            server.send_message(msg)
            print("Email sent successfully!")
    except Exception as e:
        print("Error:", e)
        
def format_result(text):
    # Extract the summary part at the end
    summary_start = text.rfind(")") + 1
    summary = text[summary_start:].strip()
    data = text[:summary_start].strip()

    # Format the summary sentence
    summary_parts = summary.split(", ")
    formatted_summary = "The results show: "
    formatted_summary += ", ".join(
        f"{part.split('-')[1]} beats labeled as {part.split('-')[0]}"
        for part in summary_parts
    )

    # Combine the formatted parts
    formatted_text = f"{data}, {formatted_summary}."
    return formatted_text
def model_predict(csv_path):
    """Use your existing processing pipeline."""
    data = uploadedData(csv_path, csvbool=True)
    sr = data[0]
    data = data[1:]
    size = len(data)
    if size > 9001:
        size = 9001
        data = data[:size]
    div = size // 1000
    data, peaks = preprocess(data, config)
    return predictByPart(data, peaks)

@app.route('/', methods=['GET'])
def index():
    default_esp_ip = "192.168.68.105"
    return render_template('index.html', esp_ip=default_esp_ip)

@app.route('/predict', methods=['POST'])
def predict_upload():
    """Handle fresh uploads."""
    global last_uploaded_file
    f = request.files.get('file')
    if not f:
        return jsonify({"error": "No file uploaded"}), 400

    filename = secure_filename(f.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    try:
        os.remove(file_path)
    except:
        pass
    f.save(file_path)
    last_uploaded_file = file_path

    try:
        predicted, result = model_predict(file_path)
        length = len(predicted)
        logging.info("The predicted", predicted)
        print("The predicted", predicted)
        sumPredict = sum(predicted[x][1] for x in range(len(predicted)))
        avgPredict = sumPredict/len(predicted)
                # This line calculates the suggestion and stays the same
        sugg = get_ekg_suggestion(classesM[avgPredict.argmax()])

        # Modify this line to add the suggestion
        prediction_message = "The most predicted label is {} with {:3.1f}% certainty.\nSuggestion: {}".format(classesM[avgPredict.argmax()], 100 * max(avgPredict), sugg)
        #prediction_message = "The most predicted label is {} with {:3.1f}% certainty".format(classesM[avgPredict.argmax()], 100*max(avgPredict))
        result_text = f"{prediction_message}.{length} parts of the divided data were estimated as the followings with paired probabilities.\n{result}"
        formatted = format_result(result_text)
        mailResult(formatted);
        return jsonify({"result": formatted, "filename": filename})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predict_last', methods=['GET'])
def predict_last():
    """Re-run prediction on the last uploaded file."""
    global last_uploaded_file
    if not last_uploaded_file or not os.path.exists(last_uploaded_file):
        return jsonify({"error": "No previously uploaded file found."}), 404
    try:
        predicted, result = model_predict(last_uploaded_file)
        length = len(predicted)
        sumPredict = sum(predicted[x][1] for x in range(len(predicted)))
        avgPredict = sumPredict/len(predicted)
        prediction_message = "The most predicted label is {} with {:3.1f}% certainty".format(classesM[avgPredict.argmax()], 100*max(avgPredict))
        result_text = f"{prediction_message}.{length} parts of the divided data were estimated as the followings with paired probabilities.\n{result}"
        formatted = format_result(result_text)
        prediction_message = "The most predicted label is {} with {:3.1f}% certainty".format(classesM[avgPredict.argmax()], 100*max(avgPredict))
        return jsonify({"result": formatted, "filename": os.path.basename(last_uploaded_file)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/list_files', methods=['GET'])
def list_files():
    """Return all CSV files in uploads/."""
    files = [f for f in os.listdir(UPLOAD_FOLDER) if f.lower().endswith('.csv')]
    return jsonify({"files": sorted(files)})

def get_ekg_suggestion(beat_code):
    """
    Provides a general, non-medical suggestion based on an EKG beat code.

    *** Disclaimer: This function is for informational purposes only
    and does NOT constitute medical advice. Always consult a
    qualified healthcare professional for any medical concerns. ***
    """
    
    # This dictionary maps the EKG beat codes to their general suggestions.
    # Note that case matters (e.g., 'A' vs 'a').
    suggestions_map = {
        'N': 'No action needed. This is the expected, healthy beat.. Thank you.',
        'L': 'Consult doctor for evaluation. This can be a sign of underlying heart disease (like hypertension or weak heart muscle). Further tests (like an echocardiogram) may be needed.. Thank you.',
        'R': 'Consult doctor for evaluation. This is often benign in healthy people but can be related to lung or heart conditions. A doctor will determine if it\'s new or clinically significant.. Thank you.',
        'B': 'Consult doctor for evaluation. Same as L and R; this finding needs a medical review to determine the cause and significance.. Thank you.',
        'A': 'Consult doctor. Often benign. If asymptomatic, monitoring may be all that\'s needed. If causing palpitations, reducing caffeine/alcohol/stress is often suggested.. Thank you.',
        'a': 'Consult doctor. This is a type of \'A\' beat. The suggestion is the same: often benign, but monitoring is needed to assess frequency and symptoms.. Thank you.',
        'J': 'Consult doctor. Similar to \'A\', these are often benign. The doctor will assess frequency and symptoms to see if any action is needed.. Thank you.',
        'S': 'Consult doctor. This is a general term for \'A\' or \'J\' beats. Suggestion is the same: often benign, but monitoring and lifestyle changes (less caffeine/stress) may be advised.. Thank you.',
        'V': 'Consult doctor. Low-dose beta-blockers (e.g., metoprolol 25mg) may be prescribed if beats are frequent or symptomatic. Lifestyle changes are also recommended.. Thank you.',
        'r': 'Seek prompt medical evaluation. This is a high-risk type of \'V\' beat that can trigger dangerous, fast rhythms. Requires urgent assessment by a doctor.. Thank you.',
        'F': 'Consult doctor for workup. This beat is a sign of an underlying rhythm (like ventricular tachycardia). It is not a diagnosis itself but requires investigation.. Thank you.',
        'e': 'Consult doctor. This is a "safety" beat. It means the heart\'s main pacemaker is too slow. The underlying slow heart rate (bradycardia) must be investigated.. Thank you.',
        'j': 'Consult doctor. Like \'e\', this is a "backup" beat. It signals that the primary pacemaker is failing. The underlying slow heart rate is the problem that needs investigation.. Thank you.',
        'n': 'Consult doctor. This is a general term for \'e\' or \'j\'. The suggestion is the same: the underlying slow heart rate must be evaluated.. Thank you.. Thank you.',
        'E': 'Seek prompt medical evaluation. This is a serious "last resort" safety beat. It indicates a significant failure of the heart\'s primary and secondary pacemakers (e.g., AV block).. Thank you.',
        '/': 'Inform your cardiologist. This is an expected beat if you have a pacemaker. If you feel dizzy or have palpitations, the pacemaker may need to be checked.. Thank you.',
        'f': 'Inform your cardiologist. This is common with pacemakers. It means your own heart beat and the pacemaker fired at the same time. Usually benign, but good to review at your next device check.. Thank you.',
        'Q': 'Repeat the EKG. The quality of the reading was not good enough (e.g., due to movement) for the machine to classify the beat. A new test is needed.. Thank you.',
        '?': 'Repeat the EKG. Similar to \'Q\', the beat could not be identified. The EKG must be reviewed by a human expert or repeated.. Thank you.'
    }
    
    # Use the .get() method to safely retrieve the suggestion.
    # If the beat_code isn't found, it returns the default message.
    suggestion = suggestions_map.get(beat_code, "Unknown beat code. Please provide a valid initial.")
    
    return suggestion

@app.route('/predict_file/<filename>', methods=['GET'])
def predict_existing(filename):
    """Predict a specific uploaded file by name."""
    file_path = os.path.join(UPLOAD_FOLDER, secure_filename(filename))
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found."}), 404
    try:
        predicted, result = model_predict(file_path)
        length = len(predicted)
        logging.info("The predicted", predicted)
        print("The predicted", predicted)
        sumPredict = sum(predicted[x][1] for x in range(len(predicted)))
        avgPredict = sumPredict/len(predicted)
        sugg = get_ekg_suggestion(classesM[avgPredict.argmax()])

        # Modify this line to add the suggestion
        prediction_message = "The most predicted label is {} with {:3.1f}% certainty.\nSuggestion: {}".format(classesM[avgPredict.argmax()], 100 * max(avgPredict), sugg)
        
        #prediction_message = "The most predicted label is {} with {:3.1f}% certainty".format(classesM[avgPredict.argmax()], 100*max(avgPredict))
        result_text = f"{prediction_message}.{length} parts of the divided data were estimated as the followings with paired probabilities.\n{result}"
        formatted = format_result(result_text)
        mailResult(formatted)
        return jsonify({"result": formatted, "filename": filename})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    config = get_config()
    http_server = WSGIServer(('0.0.0.0', 5002), app)
    print("Serving Flask app on http://0.0.0.0:5002 (Accessible via your machine's IP address on the local network)")
    http_server.serve_forever()
