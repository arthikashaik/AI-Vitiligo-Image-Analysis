import cv2
import numpy as np
import os

# -----------------------------------------
# Folders
# -----------------------------------------

input_folder = "dataset/processed"
results_folder = "dataset/results"

os.makedirs(results_folder, exist_ok=True)

# -----------------------------------------
# Images
# -----------------------------------------

image_files = [
    "image3.jpg",
    "image4.jpg",
    "image5.jpg"
]

all_results = []

# -----------------------------------------
# Process images
# -----------------------------------------

for filename in image_files:

    print("\n================================")
    print("Testing:", filename)
    print("================================")

    image_path = os.path.join(
        input_folder,
        filename
    )

    image = cv2.imread(image_path)

    if image is None:
        print("Image not found:", filename)
        continue

    print("Image loaded successfully!")
    print("Image size:", image.shape)

    # -----------------------------------------
    # HSV
    # -----------------------------------------

    hsv = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2HSV
    )

    # -----------------------------------------
    # Skin detection
    # -----------------------------------------

    lower_skin = np.array([0, 15, 30])
    upper_skin = np.array([35, 255, 255])

    skin_mask = cv2.inRange(
        hsv,
        lower_skin,
        upper_skin
    )

    # Clean skin mask
    kernel = np.ones(
        (5, 5),
        np.uint8
    )

    skin_mask = cv2.morphologyEx(
        skin_mask,
        cv2.MORPH_OPEN,
        kernel
    )

    skin_mask = cv2.morphologyEx(
        skin_mask,
        cv2.MORPH_CLOSE,
        kernel
    )

    # -----------------------------------------
    # Brightness and saturation
    # -----------------------------------------

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    saturation = hsv[:, :, 1]

    # -----------------------------------------
    # Local brightness
    # -----------------------------------------

    local_average = cv2.GaussianBlur(
        gray,
        (31, 31),
        0
    )

    # Difference between pixel and nearby skin
    brightness_difference = (
        gray.astype(np.float32)
        - local_average.astype(np.float32)
    )

    # -----------------------------------------
    # Candidate detection
    # -----------------------------------------

    candidate_mask = np.zeros_like(
        gray
    )

    candidate_mask[
        (skin_mask == 255) &
        (brightness_difference > 12) &
        (saturation < 100)
    ] = 255

    # -----------------------------------------
    # Remove small noise
    # -----------------------------------------

    small_kernel = np.ones(
        (3, 3),
        np.uint8
    )

    candidate_mask = cv2.morphologyEx(
        candidate_mask,
        cv2.MORPH_OPEN,
        small_kernel
    )

    candidate_mask = cv2.morphologyEx(
        candidate_mask,
        cv2.MORPH_CLOSE,
        small_kernel
    )

    # -----------------------------------------
    # Find contours
    # -----------------------------------------

    contours, _ = cv2.findContours(
        candidate_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # -----------------------------------------
    # Filter regions
    # -----------------------------------------

    clean_mask = np.zeros_like(
        candidate_mask
    )

    minimum_area = 30

    kept_regions = 0

    for contour in contours:

        area = cv2.contourArea(
            contour
        )

        if area >= minimum_area:

            cv2.drawContours(
                clean_mask,
                [contour],
                -1,
                255,
                thickness=cv2.FILLED
            )

            kept_regions += 1

    # -----------------------------------------
    # Calculate percentage
    # -----------------------------------------

    skin_pixels = np.sum(
        skin_mask == 255
    )

    candidate_pixels = np.sum(
        clean_mask == 255
    )

    if skin_pixels > 0:

        percentage = (
            candidate_pixels /
            skin_pixels
        ) * 100

    else:

        percentage = 0

    # -----------------------------------------
    # Print result
    # -----------------------------------------

    print(
        "Skin pixels:",
        skin_pixels
    )

    print(
        "Candidate pixels:",
        candidate_pixels
    )

    print(
        "Detected candidate regions:",
        kept_regions
    )

    print(
        "Estimated candidate area:",
        round(percentage, 2),
        "%"
    )

    # -----------------------------------------
    # Create result image
    # -----------------------------------------

    result = image.copy()

    result[
        clean_mask == 255
    ] = [0, 0, 255]

    for contour in contours:

        area = cv2.contourArea(
            contour
        )

        if area >= minimum_area:

            x, y, w, h = cv2.boundingRect(
                contour
            )

            cv2.rectangle(
                result,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                1
            )

    # -----------------------------------------
    # Save result
    # -----------------------------------------

    result_name = filename.replace(
        ".jpg",
        "_improved_result.jpg"
    )

    result_path = os.path.join(
        results_folder,
        result_name
    )

    cv2.imwrite(
        result_path,
        result
    )

    print(
        "Result saved:",
        result_path
    )

    # -----------------------------------------
    # Store result
    # -----------------------------------------

    all_results.append(
        (
            filename,
            percentage,
            kept_regions
        )
    )

# -----------------------------------------
# Comparison report
# -----------------------------------------

report_path = os.path.join(
    results_folder,
    "improved_comparison_report.txt"
)

with open(
    report_path,
    "w"
) as report:

    report.write(
        "VITILIGO IMAGE ANALYSIS PROTOTYPE\n"
    )

    report.write(
        "=================================\n\n"
    )

    report.write(
        "Improved candidate-region detection\n\n"
    )

    for filename, percentage, regions in all_results:

        report.write(
            f"{filename}\n"
        )

        report.write(
            f"Estimated Candidate Area: "
            f"{percentage:.2f}%\n"
        )

        report.write(
            f"Candidate Regions: "
            f"{regions}\n\n"
        )

    report.write(
        "NOTE:\n"
    )

    report.write(
        "This is an educational image-processing "
        "prototype. Candidate regions are not "
        "a medical diagnosis.\n"
    )

print("\n================================")
print("IMPROVED TESTING COMPLETED!")
print("================================")

print(
    "Report saved at:",
    report_path
)