import numpy as np

def project_point(camera_position, look_at, point_3d):
    """
    Project a 3D point into a normalized projection matrix.

    Args:
        camera_position: The 3D position of the camera (x, y, z).
        look_at: The 3D position the camera is looking at (x, y, z).
        point_3d: The 3D point to project (x, y, z).

    Returns:
        The 2D coordinates of the projected point in normalized space.
    """
    # Step 1: Calculate the forward, right, and up vectors
    def normalize(v):
        return v / np.linalg.norm(v)

    forward = normalize(np.array(look_at) - np.array(camera_position))
    right = normalize(np.cross(forward, [0, 1, 0]))
    up = np.cross(right, forward)

    # Step 2: Create the view matrix
    view_matrix = np.array([
        [right[0], right[1], right[2], -np.dot(right, camera_position)],
        [up[0], up[1], up[2], -np.dot(up, camera_position)],
        [-forward[0], -forward[1], -forward[2], np.dot(forward, camera_position)],
        [0, 0, 0, 1]
    ])

    # Step 3: Create the projection matrix
    near = 1.0  # Near plane normalized to 1
    width = 1.0  # Width of the near plane
    height = 1.0  # Height of the near plane
    aspect_ratio = width / height

    projection_matrix = np.array([
        [1 / aspect_ratio, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, -1, -2 * near],
        [0, 0, -1, 0]
    ])

    # Step 4: Transform the 3D point into clip space
    point_3d_homogeneous = np.array([point_3d[0], point_3d[1], point_3d[2], 1])
    view_space_point = view_matrix @ point_3d_homogeneous
    clip_space_point = projection_matrix @ view_space_point

    # Step 5: Perform perspective divide to get normalized device coordinates (NDC)
    if clip_space_point[3] == 0:
        raise ValueError("Invalid projection: w component is zero.")
    ndc_x = clip_space_point[0] / clip_space_point[3]
    ndc_y = clip_space_point[1] / clip_space_point[3]

    return ndc_x, ndc_y


# Example usage
camera_position = (0, 0, 0)  # Camera position
look_at = (0, 0, -1)  # Camera is looking along the negative Z-axis
point_3d = (0.5, 0.5, -2)  # A 3D point to project

projected_point = project_point(camera_position, look_at, point_3d)
print("Projected 2D Point in NDC:", projected_point)