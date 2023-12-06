import cv2
import os
import time
from read_plate import extract_text_from_image
import serial
import threading

# Path to the Haar Cascade XML file for license plate detection
haarcascade = "model/haarcascade_russian_plate_number.xml"

# Camera setup
cap = cv2.VideoCapture(0)
cap.set(3, 1000)  # width
cap.set(4, 1000)  # height

# License plate detection variables
min_area = 500
count = 0
output_folder = "output_images"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

license_plate_detected = False
last_detection_time = 0

# Serial communication setup for ultrasonic sensor
arduino_port = 'COM4'
arduino_baudrate = 9600

ser = serial.Serial(arduino_port, arduino_baudrate, timeout=1)
time.sleep(2)

# Flag to signal threads to stop
exit_threads = False

# Function to handle ultrasonic sensor
def ultrasonic_task():
    global previous_status
    global isFull
    previous_status = None  # Initialize previous_status
    isFull = False

    try:
        while not exit_threads:
            # Trigger the ultrasonic sensors
            ser.write(b'H')  # 'H' is just a signal to Arduino to start measuring
            # Read the parking status from Arduino
            arduino_data = ser.readline().rstrip()

            if arduino_data:
                status = int(arduino_data.decode('utf-8'))

                if status == 3:
                    current_status = "Both Taken"
                    isFull = True
                elif status == 2:
                    current_status = "Space 1 Taken"
                    isFull = False
                elif status == 1:
                    current_status = "Space 2 Taken"
                    isFull = False
                else:
                    current_status = "None Taken"
                    isFull = False

                if current_status != previous_status:
                    print("Parking space status:", current_status)
                    previous_status = current_status

            time.sleep(1)  # Adjust the delay as needed

    except KeyboardInterrupt:
        print("Exiting ultrasonic task")

    finally:
        ser.close()


# Create a thread for the ultrasonic task
ultrasonic_thread = threading.Thread(target=ultrasonic_task)
ultrasonic_thread.start()

# Placeholder function for license plate detection
def license_plate_detection():
    global license_plate_detected
    global last_detection_time
    global count

    try:
        while not exit_threads:
            success, img = cap.read()
            plate_cascade = cv2.CascadeClassifier(haarcascade)
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

            for (x, y, w, h) in plates:
                area = w * h

                if area > min_area and not license_plate_detected:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(img, "Number Plate", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)
                    img_roi = img[y: y + h, x: x + w]

                    if time.time() - last_detection_time >= 4:
                        output_path = os.path.join(output_folder, "plate_img_" + str(count) + ".jpg")
                        cv2.imwrite(output_path, img_roi)
                        count += 1

                        last_detection_time = time.time()

                        extract_text_from_image(output_path, count)

                    license_plate_detected = True
                else:
                    license_plate_detected = False

            cv2.imshow("Result", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Exiting license plate detection")

    finally:
        cap.release()
        cv2.destroyAllWindows()

# Create a thread for the license plate detection task
license_plate_thread = threading.Thread(target=license_plate_detection)
license_plate_thread.start()

# Wait for user to press 'q'
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Signal threads to stop
exit_threads = True

# Wait for both threads to finish
ultrasonic_thread.join()
license_plate_thread.join()

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
