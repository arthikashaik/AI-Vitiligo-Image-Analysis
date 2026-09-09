code vitiligo_detection.py# Vitiligo Area Estimation - Offline Prototype

def calculate_vitiligo_coverage(total_pixels, affected_pixels):
    """
    Calculate the percentage of affected skin area.
    """

    if total_pixels == 0:
        return 0.0

    percentage = (affected_pixels / total_pixels) * 100

    return round(percentage, 2)


# Sample data for testing
sample_total_skin_area = 50000
sample_vitiligo_area = 7500

# Calculate percentage
result = calculate_vitiligo_coverage(
    sample_total_skin_area,
    sample_vitiligo_area
)

# Display result
print("--- Vitiligo Analysis Result ---")
print(f"Total Skin Area Analyzed: {sample_total_skin_area} pixels")
print(f"Affected Area: {sample_vitiligo_area} pixels")
print(f"Estimated Affected Percentage: {result}%")
