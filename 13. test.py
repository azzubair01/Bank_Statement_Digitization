import os
import subprocess
import tensorflow as tf
import cv2
from object_detection.utils import label_map_util
import pikepdf
from PyPDF2 import PdfFileReader
from tqdm import tqdm
from pdf2image import convert_from_path
import pandas as pd
import os
import subprocess


zipped_model = 'inferenceutils.py'
if not os.path.exists(zipped_model):
    subprocess.call('powershell -Command "Invoke-WebRequest https://raw.githubusercontent.com/hugozanini/object-detection/master/inferenceutils.py -OutFile .\\inferenceutils.py"')

# ---------------------------------------------------------------------------------------------------------------------

zipped_model = 'test_cimb\\saved_model'
if not os.path.exists(zipped_model):
    subprocess.call("powershell Expand-Archive -Path 'test_cimb\\saved_model.zip' -DestinationPath 'test_cimb\\saved_model\\'")

output_directory = 'inference_graph'
labelmap_path = 'test_cimb\\saved_model\\saved_model\\label_map.pbtxt'

category_index = label_map_util.create_category_index_from_labelmap(labelmap_path, use_display_name=True)
tf.keras.backend.clear_session()
model = tf.saved_model.load(f'test_cimb\\saved_model\\saved_model')

test = pd.read_csv('test_cimb\\saved_model\\saved_model\\test_labels.csv')


input_path = 'test_cimb\\saved_model\\saved_model\\test_new\\'
# input_path = 'test_cimb\\saved_model\\saved_model\\test\\'
if not os.path.exists(input_path):
    subprocess.call("powershell mkdir " + input_path)

input_path1 = 'test_cimb\\saved_model\\saved_model\\raw_dataset\\'
output_path = 'test_cimb\\saved_model\\saved_model\\predicted_coordinates.csv'

# ---------------------------------------------------------------------------------------------------------------------

# zipped_model = 'test_mayb\\saved_model'
# if not os.path.exists(zipped_model):
#     subprocess.call("powershell Expand-Archive -Path 'test\\saved_model.zip' -DestinationPath 'test_mayb\\saved_model\\'")
#
# output_directory = 'inference_graph'
# labelmap_path = 'test_mayb\\saved_model\\saved_model\\label_map.pbtxt'
#
# category_index = label_map_util.create_category_index_from_labelmap(labelmap_path, use_display_name=True)
# tf.keras.backend.clear_session()
# model = tf.saved_model.load(f'test_mayb\\saved_model\\saved_model')
#
# test = pd.read_csv('test_mayb\\saved_model\\saved_model\\test_labels.csv')
#
#
# input_path = 'test_mayb\\saved_model\\saved_model\\test_new\\'
# # input_path = 'test_mayb\\saved_model\\saved_model\\test\\'
# if not os.path.exists(input_path):
#     subprocess.call("powershell mkdir " + input_path)
#
# input_path1 = 'test_mayb\\saved_model\\saved_model\\raw_dataset\\'

# ---------------------------------------------------------------------------------------------------------------------

for i, pdf in tqdm(enumerate(os.listdir(input_path1))):
    file = pikepdf.open(input_path1 + pdf, allow_overwriting_input=True)
    file.save(input_path1 + pdf)

for i, pdf in tqdm(enumerate(os.listdir(input_path1))):
    input = PdfFileReader(open(input_path1 + pdf, 'rb'))
    width = input.getPage(0).mediaBox[2]
    height = input.getPage(0).mediaBox[3]
    images = convert_from_path(input_path1 + pdf, size=(width, height))
    for i, image in enumerate(images):
        image.save(input_path + pdf[:-4] + '_page_' + str(i) + '.jpg', 'JPEG')

# Getting 3 random images to test
# images = list(test.sample(n=5)['filename'])
images = os.listdir(input_path)

# for multiple images, use this code
from inferenceutils import *

for image_name in images:
    image_np = load_image_into_numpy_array(input_path + image_name)
    output_dict = run_inference_for_single_image(model, image_np)
    vis_util.visualize_boxes_and_labels_on_image_array(
        image_np,
        output_dict['detection_boxes'],
        output_dict['detection_classes'],
        output_dict['detection_scores'],
        category_index,
        instance_masks=output_dict.get('detection_masks_reframed', None),
        use_normalized_coordinates=True,
        line_thickness=3)
    cv2.imshow(str(image_name), image_np)


# for multiple image, use this code
import pandas as pd

rows = []

final_dataframe = pd.DataFrame(columns=['Image', 'Score', 'Class', 'Ymin', 'Xmin', 'Ymax', 'Xmax'])
for image_name in images:

    image_np = load_image_into_numpy_array(input_path + image_name)
    output_dict = run_inference_for_single_image(model, image_np)

    # store boxes in dataframe!
    cut_off_scores = len(list(filter(lambda x: x >= 0.1, output_dict['detection_scores'])))

    for j in range(cut_off_scores):
        name = image_name
        scores = output_dict['detection_scores'][j]
        classes = output_dict['detection_classes'][j]
        for i in range(1, len(category_index) + 1):
            if output_dict['detection_classes'][j] == category_index[i]['id']:
                classes = category_index[i]['name']
        ymin = output_dict['detection_boxes'][j][0]
        xmin = output_dict['detection_boxes'][j][1]
        ymax = output_dict['detection_boxes'][j][2]
        xmax = output_dict['detection_boxes'][j][3]

        row = list([name, scores, classes, ymin, xmin, ymax, xmax])
        rows.append(row)

final_df = pd.DataFrame(rows, columns=['Image', 'Scores', 'Classes', 'ymin', 'xmin', 'ymax', 'xmax'])
final_df.to_csv(output_path, index=False)

cv2.waitKey(0)
