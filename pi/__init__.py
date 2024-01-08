import RPi.GPIO as GPIO
import time
from pymongo import MongoClient
from datetime import datetime
from picamera2 import PiCamera2

# MongoDB connection settings
mongo_uri = "mongodb+srv://jeremysoh222:kk6dGaMao5h7CoLW@cluster0.ke2biwp.mongodb.net"
database_name = "SmartParking"
collection_name = "camera_Image"

# GPIO pin for the motion sensor
motion_pin = 12

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(motion_pin, GPIO.IN)

# Initialize MongoDB client
try:
    client = MongoClient(mongo_uri)
    db = client[database_name]
    collection = db[collection_name]
    print("Connected to MongoDB")

    # Initialize PiCamera
    picam2 = PiCamera2()
    picam2.resolution = (640, 480)  # Set your desired resolution

    print("Motion sensor and camera script running...")

    while True:
        # Read the motion sensor state
        motion_detected = GPIO.input(motion_pin)

        # Get the current timestamp
        timestamp = datetime.now()

        if motion_detected:
            print("Motion Detected")

            # Capture an image
            imagepath = f"image{timestamp.strftime('%Y%m%d%H%M%S')}.jpg"
            picam2.capture(image_path)

            # Insert data into MongoDB for motion detected
            data_to_insert = {
                "timestamp": timestamp,
                "motion_detected": True,
                "image_path": image_path
            }
        else:
            print("No Motion Detected")

            # Insert data into MongoDB for no motion detected
            data_to_insert = {"timestamp": timestamp, "motion_detected": False}

        collection.insert_one(data_to_insert)

        # Pause for a short time to avoid high CPU usage
        time.sleep(0.1)

except Exception as e:
    print(f"Error: {e}")

finally:
    # Clean up GPIO and close the MongoDB connection on script exit
    GPIO.cleanup()
    client.close()

    # Close the PiCamera
    if picam2:
        picam2.close()