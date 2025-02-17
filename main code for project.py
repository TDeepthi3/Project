import pytesseract
from PIL import Image
import os
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def read_business_card(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"Error processing image: {e}")
        return ""

def extract_contact_info(text):
    contact_info = {
        'Name': '',
        'Job Title': '',
        'Company': '',
        'Phone': '',
        'Email': ''
    }
    phone_pattern = re.compile(r'\+?(\d[\d\-\(\) ]{7,}\d)')
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    phone_match = phone_pattern.findall(text)
    email_match = email_pattern.findall(text)
    if phone_match:
        contact_info['Phone'] = phone_match[0]
    if email_match:
        contact_info['Email'] = email_match[0]
    lines = text.split('\n')
    contact_info['Name'] = lines[0].strip() if len(lines) > 0 else 'Not Found'
    contact_info['Job Title'] = lines[1].strip() if len(lines) > 1 else 'Not Found'
    contact_info['Company'] = lines[2].strip() if len(lines) > 2 else 'Not Found'
    return contact_info

def process_images_in_folder(folder_path):
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
    output_file_path = os.path.join(folder_path, 'extracted_contacts.txt')
    with open(output_file_path, 'w') as output_file:
        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)
            extracted_text = read_business_card(image_path)
            if not extracted_text:
                continue
            contact_info = extract_contact_info(extracted_text)
            output_file.write(f"--- Contact from {image_file} ---\n")
            for key, value in contact_info.items():
                output_file.write(f"{key}: {value}\n")
            output_file.write("\n")
    print(f"Extraction complete. Results saved to: {output_file_path}")

def main():
    folder_path = r'C:\Users\asus\Desktop\PROJECT'
    process_images_in_folder(folder_path)

if __name__ == "__main__":
    main()
