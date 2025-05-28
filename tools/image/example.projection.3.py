import math

def project_3d_to_2d(observer, look_at, fov_h, fov_v, screen_width, screen_height, point_3d):
    """
    Project a 3D point onto a 2D screen.

    Args:
        observer: The observer's position in 3D space (x, y, z).
        look_at: The point the observer is looking at in 3D space (x, y, z).
        fov_h: Horizontal field of view in radians.
        fov_v: Vertical field of view in radians.
        screen_width: Width of the 2D screen.
        screen_height: Height of the 2D screen.
        point_3d: The 3D point to project (x, y, z).

    Returns:
        The 2D coordinates of the projected point (x, y) on the screen.
    """
    # Step 1: Calculate the forward, right, and up vectors
    def normalize(v):
        length = math.sqrt(sum(coord ** 2 for coord in v))
        return tuple(coord / length for coord in v)

    forward = normalize((look_at[0] - observer[0], look_at[1] - observer[1], look_at[2] - observer[2]))
    right = normalize((
        forward[1] * 0 - forward[2] * 1,
        forward[2] * 0 - forward[0] * 0,
        forward[0] * 1 - forward[1] * 0
    ))
    up = (
        right[1] * forward[2] - right[2] * forward[1],
        right[2] * forward[0] - right[0] * forward[2],
        right[0] * forward[1] - right[1] * forward[0]
    )

    # Step 2: Transform the 3D point into the observer's coordinate system
    relative_point = (
        point_3d[0] - observer[0],
        point_3d[1] - observer[1],
        point_3d[2] - observer[2]
    )
    x_in_view = sum(relative_point[i] * right[i] for i in range(3))
    y_in_view = sum(relative_point[i] * up[i] for i in range(3))
    z_in_view = sum(relative_point[i] * forward[i] for i in range(3))

    # Step 3: Perform perspective projection
    if z_in_view <= 0:
        raise ValueError("The point is behind the observer and cannot be projected.")

    aspect_ratio = screen_width / screen_height
    tan_fov_h = math.tan(fov_h / 2)
    tan_fov_v = math.tan(fov_v / 2)

    ndc_x = x_in_view / (z_in_view * tan_fov_h * aspect_ratio)
    ndc_y = y_in_view / (z_in_view * tan_fov_v)

    # Step 4: Map normalized device coordinates (NDC) to screen coordinates
    screen_x = (ndc_x + 1) / 2 * screen_width
    screen_y = (1 - ndc_y) / 2 * screen_height

    return screen_x, screen_y


# Example usage
observer = (0, 0, 0)  # Observer's position
look_at = (0, 0, 1)  # Observer is looking along the positive Z-axis
fov_h = math.radians(90)  # Horizontal FOV in radians
fov_v = math.radians(60)  # Vertical FOV in radians
screen_width = 800  # Screen width
screen_height = 600  # Screen height
point_3d = (1, 1, 5)  # The 3D point to project

projected_2d_point = project_3d_to_2d(observer, look_at, fov_h, fov_v, screen_width, screen_height, point_3d)
print("Projected 2D Point:", projected_2d_point)