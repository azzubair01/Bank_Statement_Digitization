import fnmatch
import os
import lxml.etree
import glob
from tqdm import tqdm
from PIL import Image, ImageEnhance

# ---------------------------------------------------------------------------

input_path   = 'train/dataset/jpg_dataset/'
output_path1 = 'train/dataset/augmented_dataset/'
output_path2 = 'train/dataset/images/'

# ---------------------------------------------------------------------------

if not os.path.exists(output_path1):
    os.mkdir(output_path1)

# ---------------------------------------------------------------------------

xml_list = fnmatch.filter(os.listdir(input_path), "*.xml")

k = 0

for i in tqdm(range(len(xml_list))):
    img = Image.open(input_path + xml_list[i][:-4] + '.jpg')
    width, height = img.size
    img.save(output_path1 + 'image_' + str(i).zfill(3) + ".jpg", 'JPEG')
    tree = lxml.etree.parse(input_path + xml_list[i])
    root = tree.getroot()
    for member in root.findall('object'):
        root.find('filename').text = 'image_' + str(i).zfill(3) + ".jpg"
    tree.write(output_path1 + 'image_' + str(i).zfill(3) + ".xml")
    l = 0.3

    # augment by image brightness
    for j in range(2):
        factor = 0.5 + l
        enhancer = ImageEnhance.Brightness(img)
        im_output = enhancer.enhance(factor)
        im_output.save(output_path1 + 'image_' + str(i).zfill(3) + '_brightness_' + str(k).zfill(3) + ".jpg", 'JPEG')
        for member in root.findall('object'):
            root.find('filename').text = 'image_' + str(i).zfill(3) + '_brightness_' + str(k).zfill(3) + ".jpg"
        tree.write(output_path1 + 'image_' + str(i).zfill(3) + '_brightness_' + str(k).zfill(3) + ".xml")
        k += 1
        l += 0.3

    # augment by image contrast
    l = 0.3
    for j in range(2):
        factor = 0.5 + l
        enhancer = ImageEnhance.Contrast(img)
        im_output = enhancer.enhance(factor)
        im_output.save(output_path1 + 'image_' + str(i).zfill(3) + '_contrast_' + str(k).zfill(3) + ".jpg", 'JPEG')
        for member in root.findall('object'):
            root.find('filename').text = 'image_' + str(i).zfill(3) + '_contrast_' + str(k).zfill(3) + ".jpg"
        tree.write(output_path1 + 'image_' + str(i).zfill(3) + '_contrast_' + str(k).zfill(3) + ".xml")
        k += 1
        l += 0.3

    # augment by image sharpness
    l = 0
    for j in range(2):
        factor = 0.05 + l
        enhancer = ImageEnhance.Sharpness(img)
        im_output = enhancer.enhance(factor)
        im_output.save(output_path1 + 'image_' + str(i).zfill(3) + '_sharpness_' + str(k).zfill(3) + ".jpg", 'JPEG')
        for member in root.findall('object'):
            root.find('filename').text = 'image_' + str(i).zfill(3) + '_sharpness_' + str(k).zfill(3) + ".jpg"
        tree.write(output_path1 + 'image_' + str(i).zfill(3) + '_sharpness_' + str(k).zfill(3) + ".xml")
        k += 1
        l += 0.5

    # augment by image colour
    l = 0
    for j in range(2):
        factor = 0.05 + l
        enhancer = ImageEnhance.Color(img)
        im_output = enhancer.enhance(factor)
        im_output.save(output_path1 + 'image_' + str(i).zfill(3) + '_color_' + str(k).zfill(3) + ".jpg", 'JPEG')
        for member in root.findall('object'):
            root.find('filename').text = 'image_' + str(i).zfill(3) + '_color_' + str(k).zfill(3) + ".jpg"
        tree.write(output_path1 + 'image_' + str(i).zfill(3) + '_color_' + str(k).zfill(3) + ".xml")
        k += 1
        l += 0.5

    # # augment by flip top to bottom
    # k = 0
    # im_output = img.transpose(Image.FLIP_TOP_BOTTOM)
    # im_output.save(output_path1 + 'image_' + str(i).zfill(3) + '_flip_TopBottom_' + str(k).zfill(3) + ".jpg", 'JPEG')
    # tree = lxml.etree.parse(input_path + xml_list[i])
    # root = tree.getroot()
    # for member in root.findall('object'):
    #     root.find('filename').text = 'image_' + str(i).zfill(3) + '_flip_TopBottom_' + str(k).zfill(3) + ".jpg"
    #     member[4][0].text = str(int(member[4][0].text))
    #     member[4][1].text = str(height - int(member[4][1].text))
    #     member[4][2].text = str(int(member[4][2].text))
    #     member[4][3].text = str(height - int(member[4][3].text))
    # tree.write(output_path1 + 'image_' + str(i).zfill(3) + '_flip_TopBottom_' + str(k).zfill(3) + ".xml")
    #
    # # augment by flip left to right
    # k = 0
    # im_output = img.transpose(Image.FLIP_LEFT_RIGHT)
    # im_output.save(output_path1 + 'image_' + str(i).zfill(3) + '_flip_LeftRight_' + str(k).zfill(3) + ".jpg", 'JPEG')
    # tree = lxml.etree.parse(input_path + xml_list[i])
    # root = tree.getroot()
    # for member in root.findall('object'):
    #     root.find('filename').text = 'image_' + str(i).zfill(3) + '_flip_LeftRight_' + str(k).zfill(3) + ".jpg"
    #     member[4][0].text = str(width - int(member[4][0].text))
    #     member[4][1].text = str(int(member[4][1].text))
    #     member[4][2].text = str(width - int(member[4][2].text))
    #     member[4][3].text = str(int(member[4][3].text))
    # tree.write(output_path1 + 'image_' + str(i).zfill(3) + '_flip_LeftRight_' + str(k).zfill(3) + ".xml")

total_image = sorted(glob.glob1(output_path1, "*.jpg"))
total_xml = sorted(glob.glob1(output_path1, "*.xml"))
print("\nThere are " + str(len(total_image)) + " images after augmentation")

# ---------------------------------------------------------------------------

if not os.path.exists(output_path2):
    os.mkdir(output_path2)

# ---------------------------------------------------------------------------

for i in tqdm(range(len(total_image))):
    img = Image.open(output_path1 + total_image[i][:-4] + '.jpg')
    img.save(output_path2 + total_image[i], 'JPEG')

# ---------------------------------------------------------------------------

print("\nSuccessfully select " + str(len(total_image)) + " images only for model training")

# ---------------------------------------------------------------------------