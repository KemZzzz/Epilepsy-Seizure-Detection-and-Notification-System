from flask import Flask, request, jsonify, render_template, redirect
from main import EMGClassifier
import firebase_admin
from firebase_admin import credentials, db
from werkzeug.utils import secure_filename
from flask_mqtt import Mqtt
from datetime import datetime
import os
cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred, {
  'databaseURL': 'https://epilert-230ca-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Now you can interact with your Firebase Realtime Database
ref = db.reference('/seizures')

app = Flask(__name__)


'''
Classify the signals by recieving the signal file
then save it to apply our model
and get the results:
    - the class of that signal either seizure or no seizure
    - the probability that the signal belongs to seizure class
    - the probability that the signal belongs to no seizure class
'''
# Folder to store uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

classifier = EMGClassifier()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/classify_emg', methods=['POST'])
def classify_emg():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        result = classifier.classify_emg(file_path)
        data = classifier.classification(result)
        data["timestamp"] = timestamp
        ref.set(data)
        return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)