<div style="text-align:right"><img src="./references/windows.png" width="50" height="50" align="right"/></div>
<div style="text-align:right"><img src="./references/cuda.png" width="70" height="60" align="right"/></div>
<div style="text-align:right"><img src="./references/anaconda.png" width="50" height="50" align="right"/></div>

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

### <b>f) Put the bank statements dataset in the train/raw_dataset directory</b>
  - Ensure the PDF files are all text based
  
### <b>g) Run the scripts in sequence</b>
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

### <b>h) Example of prediction output</b>

<img src="./references/output_cimb.PNG" width="750" height="375" align="center"/>


#### Note: The current table parser only works on Maybank & CIMB banks using rule-based codings
