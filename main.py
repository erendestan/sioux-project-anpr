import cv2
import os
import time
from read_plate import extract_text_from_image  # Import the text extraction function(read_plate.py)

# Path to the Haar Cascade XML file for license plate detection
haarcascade = "model/haarcascade_russian_plate_number.xml"

# Initialize a video capture object to capture frames from the default camera (camera index 0)
cap = cv2.VideoCapture(0)

# Set the width and height of the camera feed to 1000 pixels
cap.set(3, 1000)  # width
cap.set(4, 1000)  # height

# Minimum area required for a detected object to be considered a license plate
min_area = 500

count = 0

output_folder = "output_images"

# Check if the output folder exists, and if not, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

license_plate_detected = False  # Flag to track if a license plate has been detected
last_detection_time = 0  # Time of the last license plate detection

# Start an infinite loop to continuously capture and process frames from the camera feed
while True:
    # Capture a frame from the camera
    success, img = cap.read()

    # Create a Haar Cascade classifier for license plate detection
    plate_cascade = cv2.CascadeClassifier(haarcascade)

    # Convert the captured frame to grayscale for better processing
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Use the detectMultiScale method to identify potential license plates in the grayscale frame
    plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

    # Loop through the detected license plate regions
    for (x, y, w, h) in plates:
        area = w * h

        # Check if the area of the region is greater than min_area and a license plate has not been previously detected
        if area > min_area and not license_plate_detected:
            # Draw a rectangle around the license plate
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Add text indicating it's a "Number Plate"
            cv2.putText(img, "Number Plate", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)

            # Extract the license plate region
            img_roi = img[y: y + h, x: x + w]

            # Check if at least 4 seconds have passed since the last detection
            if time.time() - last_detection_time >= 4:
                # Save the license plate image to the output folder with a unique filename
                output_path = os.path.join(output_folder, "plate_img_" + str(count) + ".jpg")
                cv2.imwrite(output_path, img_roi)
                count += 1

                 # Update the last detection time
                last_detection_time = time.time()

                 # Extract text from the license plate using extract_text_from_image method(read_plate.py)
                extract_text_from_image(output_path, count)
            
            license_plate_detected = True  # Set the flag to True
        else:
            license_plate_detected = False  # Reset the flag to False

    # Display the frame with potential license plate regions marked
    cv2.imshow("Result", img)

    # Check if the 'q' key is pressed to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
