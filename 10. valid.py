import subprocess
import time

model_dir = 'train/training/'
pipeline_config_path = 'train/frcnn_v1.config'

start_time = time.time()
subprocess.call(
    "python train/models/research/object_detection/model_main_tf2.py --pipeline_config_path=" + f'{pipeline_config_path}' + \
    " --model_dir=" + f'{model_dir}' + \
    " --checkpoint_dir=" + f'{model_dir}')

print("--- %s hours ---" % ((time.time() - start_time) / 60 / 60))
