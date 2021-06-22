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

# ## Prediction on CIMB transactions
# coordinates_df = pd.read_csv('test_cimb\\saved_model\\saved_model\\predicted_coordinates.csv')
# # input_path = 'test_cimb\\saved_model\\saved_model\\test\\'
# input_path = 'test_cimb\\saved_model\\saved_model\\test_new\\'
# process_path = 'test_cimb\\saved_model\\saved_model\\processed_images\\'
# output_path = 'test_cimb\\saved_model\\saved_model\\transactions\\'
# excel_files = sorted(os.listdir('test_cimb\\saved_model\\saved_model\\transactions\\'))

# --------------------------------------------------------------------------------------------------------------

# Prediction on Maybank transactions
coordinates_df = pd.read_csv('test_mayb\\saved_model\\saved_model\\predicted_coordinates.csv')
# input_path = 'test_mayb\\saved_model\\saved_model\\test\\'
input_path = 'test_mayb\\saved_model\\saved_model\\test_new\\'
process_path = 'test_mayb\\saved_model\\saved_model\\processed_images\\'
output_path = 'test_mayb\\saved_model\\saved_model\\transactions\\'
excel_files = sorted(os.listdir('test_mayb\\saved_model\\saved_model\\transactions\\'))

# --------------------------------------------------------------------------------------------------------------

if not os.path.exists(process_path):
    subprocess.call("powershell mkdir " + process_path)

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
    output_df = pd.read_excel(output_path + excel)
    with pd.ExcelWriter(output_path + excel[:-5] + '.xlsx', engine='xlsxwriter') as writer:
        rows = []
        for j in range(len(raw_info)):
            if (excel[12:-5] == raw_info['Image'][j][:15]) and (raw_info['Key'][j] != 'transactions'):
                row = list(raw_info.iloc[j][1:])
                rows.append(row)
                df = pd.DataFrame(rows, columns = ['Key', 'Value'])
                df = df.drop_duplicates()
        output_df.to_excel(writer, sheet_name='transactions', index=False)
        df.to_excel(writer, sheet_name='metadata', index=False)

# --------------------------------------------------------------------------------------------------------------