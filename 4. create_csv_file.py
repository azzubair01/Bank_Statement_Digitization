import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET


def xml_to_csv(input_path, output_path):
    xml_list = []
    for xml_file in glob.glob(input_path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    xml_df.to_csv(output_path + 'labels.csv', index=None)
    return xml_df


# input_path = 'train/dataset/jpg_dataset'
input_path = 'train/dataset/augmented_dataset'
output_path = 'train/dataset/'
xml_to_csv(input_path, output_path)
