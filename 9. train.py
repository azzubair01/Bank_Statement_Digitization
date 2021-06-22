import os

num_steps = 7500
num_eval_steps = 1000

model_dir = 'train/training/'

pipeline_config_path = 'train/frcnn_v1.config'

import subprocess
import time
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
start_time = time.time()
subprocess.call(
    "python train/models/research/object_detection/model_main_tf2.py --pipeline_config_path=" + f'{pipeline_config_path}' + \
    " --model_dir=" + f'{model_dir}' + \
    " --alsologtostderr --num_train_steps=" + f'{num_steps}' + \
    " --sample_1_of_n_eval_examples=1 --num_eval_steps=" + f'{num_eval_steps}')
print("--- %s hours ---" % ((time.time() - start_time) / 60 / 60))
