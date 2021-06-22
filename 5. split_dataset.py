import os
import numpy as np
import shutil
import random
import glob

# # Creating Train / Val / Test folders (One time use)
dataset_dir = 'train/dataset/'
image_dir = 'augmented_dataset/'
image_dir = 'images/'
# image_dir = 'jpg_dataset/'

val_ratio = 0.15
test_ratio = 0.05

# Creating directories for train, val, & test
myFileList = glob.glob1(dataset_dir + image_dir, "*.jpg")
print("\nThere are", len(myFileList), "images read by Python")
np.random.shuffle(myFileList)

os.makedirs(dataset_dir + image_dir + 'train')
os.makedirs(dataset_dir + image_dir + 'val')
os.makedirs(dataset_dir + image_dir + 'test')

# Creating partitions of the data after shuffeling
np.random.shuffle(myFileList)
train_FileNames, val_FileNames, test_FileNames = np.split(np.array(myFileList),
                                                          [int(len(myFileList) * (1 - val_ratio + test_ratio)),
                                                           int(len(myFileList) * (1 - test_ratio))])
train_FileNames = [dataset_dir + image_dir + name for name in train_FileNames.tolist()]
val_FileNames = [dataset_dir + image_dir + name for name in val_FileNames.tolist()]
test_FileNames = [dataset_dir + image_dir + name for name in test_FileNames.tolist()]
print('Total images: ', len(myFileList))
print('Training: ', len(train_FileNames))
print('Validation: ', len(val_FileNames))
print('Testing: ', len(test_FileNames))

# Copy-pasting images
for name in train_FileNames:
    shutil.copy(name, dataset_dir + image_dir + '/train')
for name in val_FileNames:
    shutil.copy(name, dataset_dir + image_dir + '/val')
for name in test_FileNames:
    shutil.copy(name, dataset_dir + image_dir + '/test')

# Remove images not in their specific directories
for file in os.listdir(dataset_dir + image_dir):
    if file.endswith('.jpg'):
        os.remove(dataset_dir + image_dir + file)

# Generate csv files for train, val, & test
import pandas as pd

labels_df = pd.read_csv(dataset_dir + 'labels.csv')
train_images_path = os.listdir(dataset_dir + image_dir + '/train')
val_images_path = os.listdir(dataset_dir + image_dir + '/val')
test_images_path = os.listdir(dataset_dir + image_dir + '/test')

# Split invoice_labels_train.csv into train_labels, val_labels, & test_labels
from tqdm import tqdm

train_list = []
val_list = []
test_list = []

for i in tqdm(range(len(labels_df))):
    for j in range(len(train_images_path)):
        if labels_df['filename'][i] == train_images_path[j]:
            train_list.append(labels_df.iloc[i][:])
    for j in range(len(val_images_path)):
        if labels_df['filename'][i] == val_images_path[j]:
            val_list.append(labels_df.iloc[i][:])
    for j in range(len(test_images_path)):
        if labels_df['filename'][i] == test_images_path[j]:
            test_list.append(labels_df.iloc[i][:])

# Convert lists to dataframes
train_df = pd.DataFrame(train_list)
val_df = pd.DataFrame(val_list)
test_df = pd.DataFrame(test_list)

# Save dataframes as csv files
train_df.to_csv(dataset_dir + '/train_labels.csv', index=False)
val_df.to_csv(dataset_dir + '/val_labels.csv', index=False)
test_df.to_csv(dataset_dir + 'test_labels.csv', index=False)

print('Successfully splitted images into train, val, & test')
