import os
from tqdm import tqdm
from PIL import Image
from pdf2image import convert_from_path

# ---------------------------------------------------------------------------

input_path = 'train\\dataset\\raw_dataset\\'
output_path = 'train\\dataset\\jpg_dataset\\'

# ---------------------------------------------------------------------------

if not os.path.exists(output_path):
    os.mkdir(output_path)

# ---------------------------------------------------------------------------

for i, image_path in tqdm(enumerate(sorted(os.listdir(input_path)))):
    if image_path.endswith(".png"):
        image = Image.open(input_path + image_path).convert('RGB')
        image = image.resize((600, 600))
        image.save(output_path + 'jpg_image_' + str(i).zfill(3) + '.jpg')
    elif image_path.endswith(".jpeg"):
        image = Image.open(input_path + image_path).convert('RGB')
        image = image.resize((600, 600))
        image.save(output_path + 'jpg_image_' + str(i).zfill(3) + '.jpg')
    elif image_path.endswith(".jpg"):
        image = Image.open(input_path + image_path).convert('RGB')
        image = image.resize((600, 600))
        image.save(output_path + 'jpg_image_' + str(i).zfill(3) + '.jpg')
    elif image_path.endswith(".tif"):
        image = Image.open(input_path + image_path).convert('RGB')
        image = image.resize((600, 600))
        image.save(output_path + 'jpg_image_' + str(i).zfill(3) + '.jpg')
    elif image_path.endswith(".pdf"):
        images = convert_from_path(input_path + image_path, size=(600, 600))
        for i, image in enumerate(images):
            image.save(output_path+image_path[:-4]+'_page_'+str(i)+'.jpg', 'JPEG')
print("There are", len(os.listdir(output_path)), "jpg images after standardizing image format and dimension")

# ---------------------------------------------------------------------------
