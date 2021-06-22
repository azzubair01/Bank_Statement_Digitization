import re
num_classes = 5
num_steps = 7500
num_eval_steps = 1000
batch_size = 1
checkpoint_type = 'detection'

train_record_path = 'train/dataset/train.record'
test_record_path = 'train/dataset/val.record'
model_dir = 'train/training/'
labelmap_path = 'train/label_map.pbtxt'

pipeline_config_path = 'train/frcnn_v1.config'
fine_tune_checkpoint = 'train/frcnn_v1/checkpoint/ckpt-0'

# pipeline_config_path = 'train/mobilenet_v2.config'
# fine_tune_checkpoint = 'train/mobilenet_v2/checkpoint/ckpt-0'

with open(pipeline_config_path) as f:
    config = f.read()

with open(pipeline_config_path, 'w') as f:
    # Set labelmap path
    config = re.sub('label_map_path: ".*?"',
                    'label_map_path: "{}"'.format(labelmap_path), config)

    # Set fine_tune_checkpoint path
    config = re.sub('fine_tune_checkpoint: ".*?"',
                    'fine_tune_checkpoint: "{}"'.format(fine_tune_checkpoint), config)

    # Set train tf-record file path
    config = re.sub('(input_path: ".*?)(PATH_TO_BE_CONFIGURED/train)(.*?")',
                    'input_path: "{}"'.format(train_record_path), config)

    # Set test tf-record file path
    config = re.sub('(input_path: ".*?)(PATH_TO_BE_CONFIGURED/val)(.*?")',
                    'input_path: "{}"'.format(test_record_path), config)

    # Set number of classes.
    config = re.sub('num_classes: [0-9]+',
                    'num_classes: {}'.format(num_classes), config)

    # Set batch size
    config = re.sub('batch_size: [0-9]+',
                    'batch_size: {}'.format(batch_size), config)

    # Set training steps
    config = re.sub('num_steps: [0-9]+',
                    'num_steps: {}'.format(num_steps), config)

    # Set checkpoint type
    config = re.sub('fine_tune_checkpoint_type: "classification"',
                    'fine_tune_checkpoint_type: "{}"'.format(checkpoint_type), config)

    f.write(config)
