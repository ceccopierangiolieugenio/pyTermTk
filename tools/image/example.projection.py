import numpy as np

def project_3d_to_2d(square_3d, observer, look_at, fov=90, aspect_ratio=1, near=0.1, far=1000):
    """
    Project a 3D square onto a 2D plane.

    Args:
        square_3d: List of 4 points representing the square in 3D space [(x, y, z), ...].
        observer: The observer's position in 3D space (x, y, z).
        look_at: The point the observer is looking at in 3D space (x, y, z).
        fov: Field of view in degrees.
        aspect_ratio: Aspect ratio of the 2D plane (width/height).
        near: Near clipping plane.
        far: Far clipping plane.

    Returns:
        List of 2D points [(x, y), ...].
    """
    # Step 1: Create the view matrix
    def normalize(v):
        return v / np.linalg.norm(v)

    forward = normalize(np.array(look_at) - np.array(observer))
    right = normalize(np.cross(forward, [0, 1, 0]))
    up = np.cross(right, forward)

    view_matrix = np.array([
        [right[0], right[1], right[2], -np.dot(right, observer)],
        [up[0], up[1], up[2], -np.dot(up, observer)],
        [-forward[0], -forward[1], -forward[2], np.dot(forward, observer)],
        [0, 0, 0, 1]
    ])

    # Step 2: Create the projection matrix
    fov_rad = np.radians(fov)
    f = 1 / np.tan(fov_rad / 2)
    projection_matrix = np.array([
        [f / aspect_ratio, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far + near) / (near - far), (2 * far * near) / (near - far)],
        [0, 0, -1, 0]
    ])

    # Step 3: Transform the 3D points to 2D
    square_2d = []
    for point in square_3d:
        # Convert to homogeneous coordinates
        point_3d = np.array([point[0], point[1], point[2], 1])
        # Apply view and projection transformations
        transformed_point = projection_matrix @ view_matrix @ point_3d
        # Perform perspective divide
        x = transformed_point[0] / transformed_point[3]
        y = transformed_point[1] / transformed_point[3]
        square_2d.append((x, y))

    return square_2d


# Example usage
square_3d = [
    (1, 1, 5),  # Top-right
    (-1, 1, 5),  # Top-left
    (-1, -1, 5),  # Bottom-left
    (1, -1, 5)  # Bottom-right
]
observer = (0, 0, 0)  # Observer's position
look_at = (0, 0, 1)  # Observer is looking along the positive Z-axis

square_2d = project_3d_to_2d(square_3d, observer, look_at)
print("2D Coordinates of the square:", square_2d)