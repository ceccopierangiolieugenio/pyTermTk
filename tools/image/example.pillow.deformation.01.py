from PIL import Image, ImageDraw
import numpy as np

def find_coeffs(source_coords, target_coords):
    """
    Calculate coefficients for perspective transformation.
    """
    matrix = []
    for s, t in zip(source_coords, target_coords):
        matrix.extend([
            [s[0], s[1], 1, 0, 0, 0, -t[0] * s[0], -t[0] * s[1]],
            [0, 0, 0, s[0], s[1], 1, -t[1] * s[0], -t[1] * s[1]]
        ])

    A = np.matrix(matrix, dtype=np.float64)
    B = np.array(target_coords).reshape(8)

    try:
        res = np.linalg.solve(A, B)
        return tuple(np.array(res).flatten())
    except np.linalg.LinAlgError:
        print("Error: Could not solve transformation matrix.")
        return None

def main():
    # Load the input image
    try:
        image = Image.open("img4.png").convert("RGBA")
    except FileNotFoundError:
        print("Error: img1.png not found")
        return

    # Create an empty output image (transparent background)
    output_size = (800, 600)
    output_image = Image.new("RGBA", output_size, (0, 0, 0, 0))

    # Define the target quadrilateral (very small area in the output image)
    target_quad = [(50, 50), (100, 60), (120, 100), (45, 90)]

    # Define the source coordinates (entire input image)
    width, height = image.size
    source_quad = [(0, 0), (width, 0), (width, height), (0, height)]

    # Calculate the transformation coefficients
    coeffs = find_coeffs(source_quad, target_quad)
    if not coeffs:
        return

    # Calculate the bounding box of the target quadrilateral
    min_x = min(p[0] for p in target_quad)
    min_y = min(p[1] for p in target_quad)
    max_x = max(p[0] for p in target_quad)
    max_y = max(p[1] for p in target_quad)

    # Create a polygon mask to ensure transparency outside the target area
    mask = Image.new("L", output_size, 0)
    draw = ImageDraw.Draw(mask)
    draw.polygon(target_quad, fill=255)

    # Apply the transformation to the entire input image
    transformed = image.transform(
        output_size,
        Image.PERSPECTIVE,
        coeffs,
        Image.BILINEAR
    )

    # Apply the mask to keep only the transformed area within the target quadrilateral
    transformed.putalpha(mask)

    # Paste the transformed image onto the output image
    output_image.paste(transformed, (0, 0), transformed)

    # Save the result
    output_image.save("outImage.png")
    print("Image transformed and saved as outImage.png")

if __name__ == "__main__":
    main()