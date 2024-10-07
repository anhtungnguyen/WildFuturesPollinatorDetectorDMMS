import cv2
import os
import random
import numpy as np

# Paths to environment and bee images
env_img_path = "../data/input/flowers_images"
bee_img_path = "../data/input/bees"
output_img_path = "../data/input/fake_data"
output_label_path = "../data/input/fake_labels"

# Function to overlay a resized bee (32x32) on the environment image at a random position
def overlay_bee(env_img, bee_img, position):
    # Resize bee image to 32x32 pixels
    bee_img_resized = cv2.resize(bee_img, (64, 64))
    
    y1, y2 = position[1], position[1] + bee_img_resized.shape[0]
    x1, x2 = position[0], position[0] + bee_img_resized.shape[1]

    # Check boundaries
    if y2 > env_img.shape[0] or x2 > env_img.shape[1]:
        return env_img, None

    # Check if the bee image has an alpha channel
    if bee_img_resized.shape[2] == 4:
        # Use alpha channel for blending
        alpha_s = bee_img_resized[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        for c in range(0, 3):
            env_img[y1:y2, x1:x2, c] = (alpha_s * bee_img_resized[:, :, c] +
                                        alpha_l * env_img[y1:y2, x1:x2, c])
    else:
        # If no alpha channel, simply overlay the image without transparency
        env_img[y1:y2, x1:x2] = bee_img_resized

    # Calculate YOLOv8 bounding box
    x_center = (x1 + x2) / 2 / env_img.shape[1]
    y_center = (y1 + y2) / 2 / env_img.shape[0]
    width = bee_img_resized.shape[1] / env_img.shape[1]
    height = bee_img_resized.shape[0] / env_img.shape[0]

    return env_img, [x_center, y_center, width, height]

# Get all environment and bee images
env_images = [f for f in os.listdir(env_img_path) if f.endswith(".jpg")]
bee_images = [f for f in os.listdir(bee_img_path) if f.endswith(".jpg")]

# Process each environment image
for env_img_name in env_images:
    env_img = cv2.imread(os.path.join(env_img_path, env_img_name))

    # Generate random number of bees (1 to 10)
    num_bees = random.randint(1, 10)
    labels = []

    for _ in range(num_bees):
        bee_img_name = random.choice(bee_images)
        bee_img = cv2.imread(os.path.join(bee_img_path, bee_img_name), cv2.IMREAD_UNCHANGED)

        # Random position
        x_offset = random.randint(0, env_img.shape[1] - 32)  # 32 = bee image width
        y_offset = random.randint(0, env_img.shape[0] - 32)  # 32 = bee image height

        # Overlay bee on environment image
        env_img, bbox = overlay_bee(env_img, bee_img, (x_offset, y_offset))

        if bbox:
            labels.append(f"0 {bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]}")

    # Save the generated image
    output_img_name = f"bee_{env_img_name}"
    cv2.imwrite(os.path.join(output_img_path, output_img_name), env_img)

    # Save the label file in YOLOv8 format
    label_file_name = os.path.splitext(output_img_name)[0] + ".txt"
    with open(os.path.join(output_label_path, label_file_name), "w") as f:
        for label in labels:
            f.write(label + "\n")

print("Dataset generation complete.")
