# Sioux SEM-3 Group-2 Licence Plate Detection

This Python ANPR app uses [OpenCV-Python](https://pypi.org/project/opencv-python/) for real-time license plate detection from a live camera feed. It uses a Haar Cascade Classifier, sourced from [GitHub](https://github.com/spmallick/mallick_cascades/blob/master/haarcascades/haarcascade_russian_plate_number.xml), to identify license plates in the video frames. Text recognition from detected plates is achieved using [EasyOCR](https://pypi.org/project/easyocr/), which provides an efficient way to extract text from images.

## Installation

1. Install dependencies
   ```
   pip install -r requirements.txt
   ```
2. Run the application
   ```
   python main.py
   ```

## Usage

1. Point the license plate you want to recognize at the camera.

![alt text](/screenshots/1_recognition.jpeg "Number plate recognition")

2. The app will automatically crop the license plate region from the image and save it to the /output_images directory.

![alt text](/screenshots/2_license_plate.jpeg "Number plate image output")

3. The app will perform optical character recognition (OCR) on the cropped license plate image, extracting the text from it and saving it to the /output_text directory. This output also includes a confidence score ranging from 0 to 1, where a score closer to 1 indicates higher accuracy.

![alt text](/screenshots/3_text_output.jpeg "Number plate text output")
