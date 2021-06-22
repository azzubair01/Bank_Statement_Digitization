import os

import tensorflow as tf
import subprocess

with open('C:\\Users\\azzub\\anaconda3\\envs\\myOCR_Bank\\Lib\\site-packages\\official\\modeling\\tf_utils.py') as f:
    tf_utils = f.read()

with open('C:\\Users\\azzub\\anaconda3\\envs\\myOCR_Bank\\Lib\\site-packages\\official\\modeling\\tf_utils.py', 'w') as f:
  # Set labelmap path
  throw_statement = "raise TypeError('Expected Operation, Variable, or Tensor, got ' + str(x))"
  tf_utils = tf_utils.replace(throw_statement, "if not isinstance(x, str):" + throw_statement)
  f.write(tf_utils)

output_directory = 'train/inference_graph'
model_dir = 'train/training/'
pipeline_config_path = 'train/frcnn_v1.config'

subprocess.call("python train/models/research/object_detection/exporter_main_v2.py \
    --trained_checkpoint_dir "+f'{model_dir}' + "\
    --output_directory "+f'{output_directory}' +" \
    --pipeline_config_path "+f'{pipeline_config_path}')

subprocess.call("powershell copy train\\label_map.pbtxt train\\inference_graph\\saved_model\\")
subprocess.call("powershell copy train\\dataset\\test_labels.csv train\\inference_graph\\saved_model\\")
subprocess.call("powershell mkdir train\\inference_graph\\saved_model\\test")
subprocess.call("powershell copy train\\dataset\\images\\test\\* train\\inference_graph\\saved_model\\test")
if not os.path.exists('test'):
    subprocess.call("powershell mkdir test")
subprocess.call("powershell Compress-Archive -LiteralPath train\\inference_graph\\saved_model\\ -DestinationPath test\\saved_model.zip")