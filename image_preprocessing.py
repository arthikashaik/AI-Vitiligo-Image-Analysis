import cv2
import os

input_folder = "dataset/raw"
output_folder = "dataset/processed"

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):

    input_path = os.path.join(input_folder, filename)

    if filename.lower().endswith((".jpg", ".jpeg", ".png")):

        image = cv2.imread(input_path)

        if image is None:
            print("Could not read:", filename)
            continue

        resized = cv2.resize(image, (224, 224))

        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, resized)

        print("Processed:", filename)

        # Show the processed image
        cv2.imshow("Processed Image", resized)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

print("Image preprocessing completed!")