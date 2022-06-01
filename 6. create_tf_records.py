import subprocess
from tqdm import tqdm
import pandas as pd

df = pd.read_csv('train/dataset/labels.csv')
entity_names = df['class'].unique().tolist()

with open('train/label_map.pbtxt', 'w') as file:
    for i in tqdm(range(len(entity_names))):
        file.write('item {\n name: "' + entity_names[i] + '"\n id: ' + str(i+1) + '\n}\n')

subprocess.call("python train/dataset/generate_tf_records.py -l train/label_map.pbtxt -o train/dataset/train.record -i train/dataset/images/train -csv train/dataset/train_labels.csv")
subprocess.call("python train/dataset/generate_tf_records.py -l train/label_map.pbtxt -o train/dataset/val.record -i train/dataset/images/val -csv train/dataset/val_labels.csv")
