# import cv2
# import os
# import random
# import numpy as np

# # Paths to environment and bee images
# env_img_path = "path_to_environment_images"
# bee_img_path = "path_to_bee_images"
# output_img_path = "path_to_output_images"
# output_label_path = "path_to_output_labels"

# # Function to overlay bee on environment image at a random position
# def overlay_bee(env_img, bee_img, position):
#     y1, y2 = position[1], position[1] + bee_img.shape[0]
#     x1, x2 = position[0], position[0] + bee_img.shape[1]

#     # Check boundaries
#     if y2 > env_img.shape[0] or x2 > env_img.shape[1]:
#         return env_img, None

#     alpha_s = bee_img[:, :, 3] / 255.0
#     alpha_l = 1.0 - alpha_s

#     for c in range(0, 3):
#         env_img[y1:y2, x1:x2, c] = (alpha_s * bee_img[:, :, c] +
#                                     alpha_l * env_img[y1:y2, x1:x2, c])

#     # Calculate YOLOv8 bounding box
#     x_center = (x1 + x2) / 2 / env_img.shape[1]
#     y_center = (y1 + y2) / 2 / env_img.shape[0]
#     width = bee_img.shape[1] / env_img.shape[1]
#     height = bee_img.shape[0] / env_img.shape[0]

#     return env_img, [x_center, y_center, width, height]

# # Get all environment and bee images
# env_images = [f for f in os.listdir(env_img_path) if f.endswith(".jpg")]
# bee_images = [f for f in os.listdir(bee_img_path) if f.endswith(".png")]

# # Process each environment image
# for env_img_name in env_images:
#     env_img = cv2.imread(os.path.join(env_img_path, env_img_name))

#     # Generate random number of bees (1 to 10)
#     num_bees = random.randint(1, 10)
#     labels = []

#     for _ in range(num_bees):
#         bee_img_name = random.choice(bee_images)
#         bee_img = cv2.imread(os.path.join(bee_img_path, bee_img_name), cv2.IMREAD_UNCHANGED)

#         # Resize bee image randomly
#         scale = random.uniform(0.1, 0.5)
#         bee_img = cv2.resize(bee_img, (0, 0), fx=scale, fy=scale)

#         # Random position
#         x_offset = random.randint(0, env_img.shape[1] - bee_img.shape[1])
#         y_offset = random.randint(0, env_img.shape[0] - bee_img.shape[0])

#         # Overlay bee on environment image
#         env_img, bbox = overlay_bee(env_img, bee_img, (x_offset, y_offset))

#         if bbox:
#             labels.append(f"0 {bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]}")

#     # Save the generated image
#     output_img_name = f"bee_{env_img_name}"
#     cv2.imwrite(os.path.join(output_img_path, output_img_name), env_img)

#     # Save the label file in YOLOv8 format
#     label_file_name = os.path.splitext(output_img_name)[0] + ".txt"
#     with open(os.path.join(output_label_path, label_file_name), "w") as f:
#         for label in labels:
#             f.write(label + "\n")

# print("Dataset generation complete.")


import time
import os

# Get the directory of the current script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Specify the output file in the same directory
output_file = os.path.join(script_directory, "output.txt")

# Initialize a counter
counter = 0

while True:
    # Open the file in append mode
    with open(output_file, "a") as file:
        file.write(f"Hello {counter}\n")
    
    # print(f"Written: Hello {counter}")

    # Increment the counter
    counter += 1

    # Wait for 10 seconds
    time.sleep(10)

