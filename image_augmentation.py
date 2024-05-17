import os
import cv2
from keras.preprocessing.image import ImageDataGenerator
from tqdm import tqdm

############################## image augmentation part ##################################

# Initialize the image data generator with various augmentations
datagen = ImageDataGenerator(
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Define the base directory where subfolders with images are located
base_dir = '/content/dataset'  # Update this path to your dataset folder

# Loop over each subdirectory in the base directory
for subdir in tqdm(os.listdir(base_dir)):
    subdir_path = os.path.join(base_dir, subdir)

    # Check if the path is indeed a directory
    if os.path.isdir(subdir_path):
        images = []
        filenames = []

        # Load images
        for filename in os.listdir(subdir_path):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):  # Check for image formats
                img_path = os.path.join(subdir_path, filename)
                img = cv2.imread(img_path)
                if img is not None:
                    images.append(img)
                    filenames.append(filename)

        # Calculate how many augmentations are needed per image
        num_images = len(images)
        if num_images == 0:
            print(f"No images found in {subdir_path}. Skipping this directory.")
            continue

        augmentations_per_image = max(0, (300 - num_images) // num_images)

        # Perform the augmentations
        for i, img in enumerate(images):
            img = img.reshape((1,) + img.shape)  # Reshape the image for the ImageDataGenerator
            j = 0
            # Save augmented images in the subdir_path itself
            for batch in datagen.flow(img, batch_size=1, save_to_dir=subdir_path, save_prefix='aug', save_format='jpg'):
                j += 1
                if j >= augmentations_per_image:
                    break  # Break the loop when we reach the desired number of augmentations


######################## image resizing part ###############################
                
import os
import cv2
from tqdm import tqdm

# Define the base directory where subfolders with images are located
base_dir = '/content/dataset'  # Replace with the path to your dataset folder

# Desired size
desired_width, desired_height = 256, 256

# Loop over each subdirectory in the base directory
for subdir in tqdm(os.listdir(base_dir), desc="Processing subdirectories"):
    subdir_path = os.path.join(base_dir, subdir)
    
    # Check if the path is indeed a directory
    if os.path.isdir(subdir_path):
        
        # Loop over all files in the subdirectory
        for filename in tqdm(os.listdir(subdir_path), desc=f"Processing images in {subdir}"):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff')):
                img_path = os.path.join(subdir_path, filename)
                
                # Read the image from file
                img = cv2.imread(img_path)
                if img is not None:
                    # Check if the image is already the desired size
                    if img.shape[:2] == (desired_height, desired_width):
                        # Convert BGR to RGB
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    else:
                        # Resize the image
                        img = cv2.resize(img, (desired_width, desired_height), interpolation=cv2.INTER_AREA)
                        # Convert BGR to RGB after resizing
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    
                    # Save the image back to disk in RGB format
                    cv2.imwrite(img_path, img)


############################## image deletection part (images that are in the wrong formats) ########################################
import imghdr
import cv2
import os                    

DATA_DIR = "/content/dataset"
ACCEPTED_FORMAT = ["jpeg" , "jpg" , "png" , "bmp"]

# removing dodgy images
for image_class in os.listdir(DATA_DIR):
    for file_path in os.listdir(os.path.join(DATA_DIR , image_class)):

        image_path = os.path.join(DATA_DIR , image_class , file_path)

        try:
            img = cv2.imread(image_path)
            data_type = imghdr.what(image_path)

            if data_type not in ACCEPTED_FORMAT :
                print("the image with " + str(image_path) + "is not supported , will be removed " )
                os.remove(image_path)

        except Exception as e:
            print(f"the image {image_path} could not be read")
            os.remove(image_path)