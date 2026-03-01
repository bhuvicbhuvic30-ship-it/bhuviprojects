import cv2
import numpy as np
import datetime
import logging
import smtplib
from email.mime.text import MIMEText
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
import tensorflow as tf
import faiss
from ultralytics import YOLO
from twilio.rest import Client

# ---------------------------
# CONFIG
# ---------------------------

DATABASE_URL = "postgresql://postgres:password@localhost:5432/surveillance"

EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "app_password"
EMAIL_RECEIVER = "admin@gmail.com"

TWILIO_SID = "YOUR_SID"
TWILIO_TOKEN = "YOUR_TOKEN"
TWILIO_NUMBER = "+1234567890"
ADMIN_PHONE = "+91XXXXXXXXXX"

FAISS_THRESHOLD = 0.6
INTRUSION_START_HOUR = 18

# ---------------------------
# LOGGING
# ---------------------------

logging.basicConfig(
    filename="surveillance.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("AI-Surveillance")

# ---------------------------
# DATABASE
# ---------------------------

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Person(Base):
    __tablename__ = "persons"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    type = Column(String)
    person_id = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)

# ---------------------------
# FACE EMBEDDING MODEL
# ---------------------------

base_model = tf.keras.applications.MobileNetV2(
    input_shape=(160,160,3),
    include_top=False,
    weights="imagenet"
)

def get_embedding(frame):
    img = cv2.resize(frame, (160,160))
    img = np.expand_dims(img, axis=0)
    embedding = base_model(img)
    return np.mean(embedding.numpy(), axis=(1,2))[0]

# ---------------------------
# FAISS RE-ID
# ---------------------------

dimension = 128
index = faiss.IndexFlatL2(dimension)
person_ids = []

def add_person_embedding(embedding, person_id):
    index.add(np.array([embedding]).astype("float32"))
    person_ids.append(person_id)

def search_person(embedding):
    if len(person_ids) == 0:
        return None
    D, I = index.search(np.array([embedding]).astype("float32"), k=1)
    if D[0][0] < FAISS_THRESHOLD:
        return person_ids[I[0][0]]
    return None

# ---------------------------
# YOLO INTRUSION DETECTION
# ---------------------------

yolo_model = YOLO("yolov8n.pt")

def detect_intrusion(frame):
    results = yolo_model(frame)
    hour = datetime.datetime.now().hour
    for box in results[0].boxes:
        cls = int(box.cls[0])
        if yolo_model.names[cls] == "person" and hour >= INTRUSION_START_HOUR:
            return True
    return False

# ---------------------------
# ALERT SYSTEM
# ---------------------------

twilio_client = Client(TWILIO_SID, TWILIO_TOKEN)

def send_sms(message):
    twilio_client.messages.create(
        body=message,
        from_=TWILIO_NUMBER,
        to=ADMIN_PHONE
    )

def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
    server.quit()

# ---------------------------
# MULTI-CAMERA SYSTEM
# ---------------------------

camera_sources = [0]  # Add RTSP URLs if needed
cameras = [cv2.VideoCapture(src) for src in camera_sources]

def process_cameras():
    db = SessionLocal()
    while True:
        for cam in cameras:
            ret, frame = cam.read()
            if not ret:
                continue

            # Intrusion detection
            if detect_intrusion(frame):
                logger.warning("Intrusion detected!")
                send_sms("🚨 Intrusion detected!")
                send_email("Intrusion Alert", "Unauthorized person detected.")

                event = Event(type="intrusion")
                db.add(event)
                db.commit()

            # Face ReID
            embedding = get_embedding(frame)
            person_id = search_person(embedding)

            if person_id is None:
                new_person = Person(name="Unknown")
                db.add(new_person)
                db.commit()
                add_person_embedding(embedding, new_person.id)
                logger.info("New person registered")
            else:
                logger.info(f"Recognized Person ID: {person_id}")

        cv2.waitKey(1)

# ---------------------------
# FASTAPI APP
# ---------------------------

app = FastAPI()

@app.get("/")
def root():
    return {"status": "AI Surveillance System Running"}

@app.get("/start")
def start_system():
    process_cameras()
    return {"message": "Processing started"}
