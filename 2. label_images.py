import subprocess

# ---------------------------------------------------------------------------

input_path = 'train\\dataset\\jpg_dataset\\'
# input_path = 'train\\dataset\\augmented_dataset\\'
subprocess.call("python train\\labelImg\\labelImg.py " + input_path)

# ---------------------------------------------------------------------------