import subprocess
import time
start_time = time.time()
subprocess.call("python train/dataset/generate_tf_records.py -l train/label_map.pbtxt -o train/dataset/train.record -i train/dataset/images/train -csv train/dataset/train_labels.csv")
subprocess.call("python train/dataset/generate_tf_records.py -l train/label_map.pbtxt -o train/dataset/val.record -i train/dataset/images/val -csv train/dataset/val_labels.csv")
print("--- %s seconds ---" % ((time.time() - start_time)))
