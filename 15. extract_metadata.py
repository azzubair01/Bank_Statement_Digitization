import os
import subprocess
import pytesseract
import cv2
import glob
from PIL import Image
import pandas as pd
import numpy as np
from tqdm import tqdm
from pytesseract import Output

# --------------------------------------------------------------------------------------------------------------

## Prediction on CIMB transactions
coordinates_df = pd.read_csv('C:\\Users\\DataMicron\\Desktop\\Bank_Statement_Reader\\predicted_coordinates_cimb.csv')
input_path = 'C:\\Users\\DataMicron\\Desktop\\Bank_Statement_Reader\\processing_images\\cimb\\'
process_path = 'C:\\Users\\DataMicron\\Desktop\\Bank_Statement_Reader\\cropped_images\\cimb\\'
output_path = 'C:\\Users\\DataMicron\\Desktop\\Bank_Statement_Reader\\overall_output\\'
excel_file_path = 'C:\\Users\\DataMicron\\Desktop\\Bank_Statement_Reader\\transaction_output\\cimb\\'
excel_files = sorted(os.listdir(excel_file_path))

# --------------------------------------------------------------------------------------------------------------

if not os.path.exists(process_path):
    subprocess.call("powershell mkdir " + process_path)

if not os.path.exists(output_path):
    subprocess.call("powershell mkdir " + output_path)

images = glob.glob1(input_path, "*.jpg")
tessdata_dir_config = r'-l "eng+msa" --tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata" --psm 6'
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# --------------------------------------------------------------------------------------------------------------

rows = []
for i in tqdm(range(len(coordinates_df))):
    for j in range(len(images)):
        if coordinates_df['Image'][i] == images[j]:
            image = Image.open(input_path + images[j])
            results = pytesseract.image_to_data(image, config=tessdata_dir_config, output_type=Output.DICT)

            # (This is not mandatory)
            width, height = image.size

            # Setting the points for cropped image
            left = coordinates_df['xmin'][i] * width
            top = coordinates_df['ymin'][i] * height
            right = coordinates_df['xmax'][i] * width
            bottom = coordinates_df['ymax'][i] * height

            # Cropped image of above dimension
            # (It will not change orginal image)
            im1 = image.crop((left, top, right, bottom))
            im1 = im1.resize((im1.size[0] * 5, im1.size[1] * 5), resample = 5)

            # # Shows the image in image viewer
            # im1.show()
            im1.save(process_path + images[j])
            text = pytesseract.image_to_string(im1, lang='eng+msa', config=tessdata_dir_config)

            row = list([images[j], coordinates_df['Classes'][i], text])
            rows.append(row)


raw_info = pd.DataFrame(rows, columns=['Image', 'Key', 'Value'])

# --------------------------------------------------------------------------------------------------------------

for i, excel in tqdm(enumerate(excel_files)):
    output_df = pd.read_excel(excel_file_path + excel)
    statement_name1 = excel[12:-5]
    with pd.ExcelWriter(output_path + excel[:-5] + '.xlsx', engine='xlsxwriter') as writer:
        rows = []
        for j in range(len(raw_info)):
            statement_name2 = raw_info['Image'][j][:15]
            if (statement_name1 == statement_name2) and (raw_info['Key'][j] != 'transactions'):
                row = list(raw_info.iloc[j][1:])
                rows.append(row)
                df = pd.DataFrame(rows, columns=['Key', 'Value'])
                df = df.drop_duplicates()
        output_df.to_excel(writer, sheet_name='transactions', index=False)
        df.to_excel(writer, sheet_name='metadata', index=False)


# --------------------------------------------------------------------------------------------------------------

# # Prediction on Maybank transactions
coordinates_df2 = pd.read_csv('C:\\Users\\DataMicron\\Desktop\\Bank_Statement_Reader\\predicted_coordinates_mayb.csv')
input_path2 = 'C:\\Users\\DataMicron\\Desktop\\Bank_Statement_Reader\\processing_images\\mayb\\'
process_path2 = 'C:\\Users\\DataMicron\\Desktop\\Bank_Statement_Reader\\cropped_images\\mayb\\'
output_path2 = 'C:\\Users\\DataMicron\\Desktop\\Bank_Statement_Reader\\overall_output\\'
excel_file_path2 = 'C:\\Users\\DataMicron\\Desktop\\Bank_Statement_Reader\\transaction_output\\mayb\\'
excel_files2 = sorted(os.listdir(excel_file_path2))

# --------------------------------------------------------------------------------------------------------------

if not os.path.exists(process_path2):
    subprocess.call("powershell mkdir " + process_path2)

if not os.path.exists(output_path2):
    subprocess.call("powershell mkdir " + output_path2)

images2 = glob.glob1(input_path2, "*.jpg")
tessdata_dir_config = r'-l "eng+msa" --tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata" --psm 6'
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# --------------------------------------------------------------------------------------------------------------

rows2 = []
for i in tqdm(range(len(coordinates_df2))):
    for j in range(len(images2)):
        if coordinates_df2['Image'][i] == images2[j]:
            image = Image.open(input_path2 + images2[j])
            results = pytesseract.image_to_data(image, config=tessdata_dir_config, output_type=Output.DICT)

            # (This is not mandatory)
            width, height = image.size

            # Setting the points for cropped image
            left = coordinates_df2['xmin'][i] * width
            top = coordinates_df2['ymin'][i] * height
            right = coordinates_df2['xmax'][i] * width
            bottom = coordinates_df2['ymax'][i] * height

            # Cropped image of above dimension
            # (It will not change orginal image)
            im1 = image.crop((left, top, right, bottom))
            im1 = im1.resize((im1.size[0] * 5, im1.size[1] * 5), resample = 5)

            # # Shows the image in image viewer
            # im1.show()
            im1.save(process_path2 + images2[j])
            text = pytesseract.image_to_string(im1, lang='eng+msa', config=tessdata_dir_config)

            row = list([images2[j], coordinates_df2['Classes'][i], text])
            rows2.append(row)


raw_info2 = pd.DataFrame(rows2, columns=['Image', 'Key', 'Value'])

# --------------------------------------------------------------------------------------------------------------

for i, excel in tqdm(enumerate(excel_files2)):
    output_df2 = pd.read_excel(excel_file_path2 + excel)
    statement_name1 = excel[12:-5]
    with pd.ExcelWriter(output_path2 + excel[:-5] + '.xlsx', engine='xlsxwriter') as writer2:
        rows = []
        for j in range(len(raw_info2)):
            statement_name2 = raw_info2['Image'][j][:18]
            if (statement_name1 == statement_name2) and (raw_info2['Key'][j] != 'transactions'):
                row = list(raw_info2.iloc[j][1:])
                rows.append(row)
                df2 = pd.DataFrame(rows, columns=['Key', 'Value'])
                df2 = df2.drop_duplicates()
        output_df2.to_excel(writer2, sheet_name='transactions', index=False)
        df2.to_excel(writer2, sheet_name='metadata', index=False)

# --------------------------------------------------------------------------------------------------------------