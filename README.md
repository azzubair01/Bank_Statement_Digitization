# Bank Statement Digitization
Optical character recognition (OCR) is a subset of machine vision technology that focuses on recognizing written letters and characters and reproducing them digitally for later use. This opens up many possibilities for banking industry, including security solutions, and document digitization. In this project, we parsed the transactions in bank statements from PDF files into excel files using Camelot library. Also, we added other important informations from the documents using Tensorflow Object Detection API and Google Tesseract.

## How to use this repository?
### <b>a) Create a virtual environment using anaconda</b>
  - Install python 3.7

### <b>b) Check your computer's CUDA driver version.</b>
  - We used CUDA 11.2 and it is only compatible with Tensorflow 2.5.0
  - Please make sure you install the correct CUDA, & CUDNN for your machine with the correct Tensorflow version
  - Refer this table for confirmation https://www.tensorflow.org/install/source#gpu
  
### <b>c) Open the train directory and clone the labelImg repository</b>
  - git clone https://github.com/tzutalin/labelImg.git
  
### <b>d) Open the train directory and clone the tensorflow/models repository</b>
  - git clone https://github.com/tensorflow/models.git
  
### <b>e) Install dependencies</b>
  - conda install cudatoolkit
  - pip install -r 'requirements.txt'

### <b>f) Install Poppler</b>
  - Install poppler from here: https://blog.alivate.com.au/poppler-windows/

### <b>g) Copy protos from tensorflow directory to anaconda environment </b>
  - Copy all files from '..\models\research\object_detection\protos' to '..\anaconda3\envs\Bank_Statement_Digitization\Lib\site-packages\object_detection\protos'

### <b>h) Change object detection path in requirements.txt </b>
  - At line 67, change 'object-detection @ file:///../Bank_Statement_Digitization/train/models/research' accordingly

### <b>i) Change object detection path in requirements.txt </b>
  - Copy setup.py from '..\models\research\object_detection\packages\tf2' to '..\models\research'

### <b>j) Put the bank statements dataset in the train/raw_dataset directory</b>
  - Ensure the PDF files are all text based
  
### <b>k) Run the scripts in sequence</b>
  - Before running the scripts, ensure that all paths are correctly defined
    - Run preprocess_images.py
    - Run label_images.py
    - Run augment_images.py
    - Run split_dataset.py
    - Run create_csv_file.py
    - Run create_tf_records.py
    - Run download_model.py
    - Run configure_settings.py
    - Run train.py
    - Run valid.py
    - Run tensorboard.py
    - Run test.py
    - Run pdf_extract_table.py
    - Run extract_metadata.py

### <b>l) Example of prediction output</b>

<img src="./references/output_cimb.PNG" width="750" height="375" align="center"/>


#### Note: The current table parser only works on Maybank & CIMB banks using rule-based codings
