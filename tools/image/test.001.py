from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color

def process_image(input_path, output_path):
    with Image(filename=input_path) as img:
        # Apply perspective transformation
        w,h = img.width, img.height
        img.distort('perspective', [
            #   From:   to:
                0, 0,        0,      0,
                w, 0,   w - 50,     50,
                0, h,       50, h - 50,
                w, h,   w - 50, h - 50
                ])

        # Create reflection
        with img.clone() as reflection:
            reflection.flip()
            reflection.evaluate('multiply', 0.5)  # Make reflection darker
            reflection.blur(radius=0, sigma=5)  # Blur the reflection

            # Combine original image and reflection
            combined_height = img.height + reflection.height
            with Image(width=img.width, height=combined_height) as combined:
                combined.composite(img, 0, 0)
                combined.composite(reflection, 0, img.height)

                # Add a shiny surface effect
                with Drawing() as draw:
                    draw.fill_color = Color('rgba(255, 255, 255, 0.5)')
                    draw.rectangle(left=0, top=img.height, width=img.width, height=reflection.height)
                    draw(combined)

                # Save the result
                combined.save(filename=output_path)

# Example usage
process_image('screenshot.png', 'output.png')
