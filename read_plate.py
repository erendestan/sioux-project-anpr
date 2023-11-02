import easyocr
import os
from datetime import datetime

output_directory = "output_text"

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

def extract_text_from_image(image_path, count):
    reader = easyocr.Reader(['en'])

    output = reader.readtext(image_path)

    # Generate a unique filename based on the current timestamp
    current_time = datetime.now().strftime("%d_%m_%Y_%H_%M")

    for entry in output:
        output_text = entry[1]
        confidence_score = entry[2]

        if confidence_score < 0.8:
            continue

        if len(output_text.replace('-', '')) != 6:
            continue

        formatted_line = f"{output_text} (Confidence: {confidence_score})"

        output_text_file = os.path.join(output_directory, f"plate_{current_time}_{count}.txt")

        with open(output_text_file, "w", encoding="utf-8") as text_file:
            text_file.write(formatted_line)

        print(f"Text extracted and saved to {output_text_file} with confidence score {confidence_score}")

    print("Text extraction complete")
