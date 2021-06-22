import os
import subprocess

# ---------------------------------------------------------------------------

model_name = 'train\\frcnn_v1'
if not os.path.exists(model_name):
    subprocess.call('powershell -Command "Invoke-WebRequest http://download.tensorflow.org/models/object_detection/tf2/20200711/faster_rcnn_resnet50_v1_640x640_coco17_tpu-8.tar.gz -OutFile train\\frcnn_v1.tar.gz"')

# ---------------------------------------------------------------------------

zipped_model = 'train\\frcnn_v1.tar.gz'
unzipped_model = "'train\\'"
if os.path.exists(zipped_model):
    subprocess.call("powershell tar -xvzf " + zipped_model + " -C " + unzipped_model)

# ---------------------------------------------------------------------------

model_name = 'train\\faster_rcnn_resnet50_v1_640x640_coco17_tpu-8'
renamed_model = 'train\\frcnn_v1'
if not os.path.exists(renamed_model):
    os.rename(model_name, renamed_model)

# ---------------------------------------------------------------------------

model_name = 'train\\frcnn_v1.tar.gz'
if os.path.exists(model_name):
    os.remove(model_name)

# ---------------------------------------------------------------------------

model_config = 'train\\frcnn_v1.config'
if not os.path.exists(model_config):
    subprocess.call('powershell -Command "Invoke-WebRequest https://raw.githubusercontent.com/tensorflow/models/master/research/object_detection/configs/tf2/faster_rcnn_resnet50_v1_640x640_coco17_tpu-8.config -OutFile train\\frcnn_v1.config"')

# # ---------------------------------------------------------------------------
#
# model_name = 'train/ssd_mobilenet_v2_fpnlite_640x640_coco17_tpu-8.tar.gz'
# if not os.path.exists(model_name):
#     subprocess.call('powershell -Command "Invoke-WebRequest http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_mobilenet_v2_fpnlite_640x640_coco17_tpu-8.tar.gz -OutFile ./ssd_mobilenet_v2_fpnlite_640x640_coco17_tpu-8.tar.gz"')
#
# # ---------------------------------------------------------------------------
#
# zipped_model = 'train/ssd_mobilenet_v2_fpnlite_640x640_coco17_tpu-8.tar.gz'
# if os.path.exists(zipped_model):
#     subprocess.call("tar -xvzf " + zipped_model)
#
# # ---------------------------------------------------------------------------
#
# model_name = 'train/ssd_mobilenet_v2_fpnlite_640x640_coco17_tpu-8'
# renamed_model = 'train/mobilenet_v2'
# if not os.path.exists(renamed_model):
#     os.rename(model_name, renamed_model)

# # ---------------------------------------------------------------------------
#
# model_name = 'train\\ssd_mobilenet_v2_fpnlite_640x640_coco17_tpu-8'
# if os.path.exists(model_name):
#     os.remove(model_name)
#
# # ---------------------------------------------------------------------------
#
# model_config = 'train/ssd_mobilenet_v2_fpnlite_640x640_coco17_tpu-8.config'
# if not os.path.exists(model_config):
#     subprocess.call('powershell -Command "Invoke-WebRequest https://raw.githubusercontent.com/tensorflow/models/master/research/object_detection/configs/tf2/ssd_mobilenet_v2_fpnlite_640x640_coco17_tpu-8.config -OutFile ./mobilenet_v2.config"')
#
# # ---------------------------------------------------------------------------