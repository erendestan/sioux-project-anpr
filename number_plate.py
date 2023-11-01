# import cv2
# import os

# haarcascade = r"C:\Users\erend\OneDrive\Desktop\Fontys Software - 2nd Year\Group Project - Sioux\Clone Trials\Car-Number-Plates-Detection\model\haarcascade_russian_plate_number.xml" #Change path

# # harcascade = "model/haarcascade_russian_plate_number.xml"
# # C:\Users\erend\OneDrive\Desktop\Fontys Software - 2nd Year\Group Project - Sioux\Clone Trials\Car-Number-Plates-Detection\model

# cap = cv2.VideoCapture(0)

# cap.set(3, 640) # width
# cap.set(4, 480) #height

# min_area = 500
# count = 0

# while True:
#     success, img = cap.read()

#     plate_cascade = cv2.CascadeClassifier(haarcascade)
#     img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

#     for (x,y,w,h) in plates:
#         area = w * h

#         if area > min_area:
#             cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
#             cv2.putText(img, "Number Plate", (x,y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)

#             img_roi = img[y: y+h, x:x+w]
#             cv2.imshow("ROI", img_roi)



#     cv2.imshow("Result", img)


#     if cv2.waitKey(1) & 0xFF == ord('s'):
#         output_folder = r'C:\Users\erend\OneDrive\Desktop\Fontys Software - 2nd Year\Group Project - Sioux\Clone Trials\Car-Number-Plates-Detection\plates' #Change path
#         output_path = os.path.join(output_folder, "scaned_img_" + str(count) + ".jpg")


#         # cv2.imwrite("plates/scaned_img_" + str(count) + ".jpg", img_roi)
#         cv2.imwrite(output_path, img_roi)

#         cv2.rectangle(img, (0,200), (640,300), (0,255,0), cv2.FILLED)
#         cv2.putText(img, "Plate Saved", (150, 265), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), 2)
#         cv2.imshow("Results",img)
#         cv2.waitKey(500)
#         count += 1

import cv2
import os
import time

harcascade = r"./model/haarcascade_russian_plate_number.xml"

cap = cv2.VideoCapture(0)
cap.set(3, 640)  # width
cap.set(4, 480)  # height

min_area = 500
count = 0
output_folder = r"./plates"

license_plate_detected = False  # Flag to track if a license plate has been detected
last_detection_time = 0  # Time of the last license plate detection

while True:
    success, img = cap.read()

    plate_cascade = cv2.CascadeClassifier(harcascade)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

    for (x, y, w, h) in plates:
        area = w * h

        if area > min_area and not license_plate_detected:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, "Number Plate", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)

            img_roi = img[y: y + h, x: x + w]

            if time.time() - last_detection_time >= 2:  # Check if 2 seconds have passed
                output_path = os.path.join(output_folder, "scaned_img_" + str(count) + ".jpg")
                cv2.imwrite(output_path, img_roi)
                count += 1
                last_detection_time = time.time()

            license_plate_detected = True  # Set the flag to True
        else:
            license_plate_detected = False  # Reset the flag to False

    cv2.imshow("Result", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
