import easyocr #library for text extraction
import os
from datetime import datetime
import logging

# Set the logging level to suppress warnings
logging.getLogger('easyocr').setLevel(logging.ERROR)

output_directory = "output_text"

# Check if the output directory exists, and if not, create it
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Function to extract text from an image
def extract_text_from_image(image_path, count):
    # Initialize the easyocr Reader with the English language
    reader = easyocr.Reader(['en'])

    # Use easyocr to extract text from the given image
    output = reader.readtext(image_path)

    # Generate a unique filename based on the current timestamp
    current_time = datetime.now().strftime("%d_%m_%Y_%H_%M")

    # Loop through the extracted text entries
    for entry in output:
        output_text = entry[1]
        confidence_score = entry[2]

        # Skip entries with low confidence scores (less than 0.8)
        if confidence_score < 0.8:
            continue

        # Skip entries that do not have a specific length (e.g., not 6 characters)
        if len(output_text.replace('-', '')) != 6:
            continue

        # Format the extracted text and confidence score
        formatted_line = f"{output_text} (Confidence: {confidence_score})"

        # Define the output text file path
        output_text_file = os.path.join(output_directory, f"plate_{current_time}_{count}.txt")

        # Write the formatted line to the output text file
        with open(output_text_file, "w", encoding="utf-8") as text_file:
            text_file.write(formatted_line)

        print(f"Text extracted and saved to {output_text_file} with confidence score {confidence_score}")

    # print("Text extraction complete")