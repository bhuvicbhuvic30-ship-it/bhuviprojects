from flask import Flask, Response, request, jsonify
import cv2
import numpy as np
import mysql.connector
from datetime import datetime
from mtcnn import MTCNN
from keras.models import load_model
from sklearn.preprocessing import Normalizer
import pickle
import dlib
from scipy.spatial import distance as dist
from imutils import face_utils

app = Flask(__name__)

# ---------------- DATABASE ----------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yourpassword",
    database="attendance_db"
)
cursor = db.cursor()

# ---------------- LOAD MODELS ----------------
facenet_model = load_model("facenet_keras.h5")
with open("classifier.pkl", "rb") as f:
    svm_model = pickle.load(f)

detector = MTCNN()

# ---------------- LIVENESS ----------------
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
face_detector = dlib.get_frontal_face_detector()

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

# ---------------- EMBEDDING ----------------
def get_embedding(face):
    face = cv2.resize(face, (160, 160))
    face = face.astype('float32')
    mean, std = face.mean(), face.std()
    face = (face - mean) / std
    sample = np.expand_dims(face, axis=0)
    return facenet_model.predict(sample)[0]

# ---------------- MARK ATTENDANCE ----------------
def mark_attendance(name):
    now = datetime.now()
    cursor.execute(
        "INSERT INTO attendance (name,date,time) VALUES (%s,%s,%s)",
        (name,
         now.strftime("%Y-%m-%d"),
         now.strftime("%H:%M:%S"))
    )
    db.commit()

# ---------------- VIDEO STREAM ----------------
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        rects = face_detector(gray, 0)
        for rect in rects:
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            leftEye = shape[42:48]
            ear = eye_aspect_ratio(leftEye)

            if ear < 0.25:   # Blink detected
                results = detector.detect_faces(frame)

                for result in results:
                    x, y, w, h = result['box']
                    face = frame[y:y+h, x:x+w]

                    embedding = get_embedding(face)
                    embedding = Normalizer(norm='l2').transform([embedding])
                    prediction = svm_model.predict(embedding)
                    name = prediction[0]

                    mark_attendance(name)

                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                    cv2.putText(frame, name, (x,y-10),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1,(0,255,0),2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# ---------------- ROUTES ----------------
@app.route('/')
def home():
    return "<h2>AI Face Attendance Running...</h2><img src='/video'>"

@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/recognize', methods=['POST'])
def recognize_api():
    file = request.files['image']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    results = detector.detect_faces(img)
    for result in results:
        x, y, w, h = result['box']
        face = img[y:y+h, x:x+w]

        embedding = get_embedding(face)
        embedding = Normalizer(norm='l2').transform([embedding])
        prediction = svm_model.predict(embedding)
        name = prediction[0]

        mark_attendance(name)

        return jsonify({"status": "Marked", "name": name})

    return jsonify({"status": "No Face Found"})

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
