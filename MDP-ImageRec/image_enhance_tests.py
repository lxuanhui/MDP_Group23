from PIL import Image, ImageEnhance

# Open the image file
from w9_check import l_r_imagerec

image = Image.open('server_image.jpg')

# Create an ImageEnhance object with brightness factor 1.5 (increase by 50%)
enhancer_brightness = ImageEnhance.Brightness(image)
bright_image = enhancer_brightness.enhance(3)

enhancer_contrast = ImageEnhance.Contrast(image)
contrasted_image = enhancer_contrast.enhance(0.5)

# Save the image file
bright_image.save('bright_image.jpg')
l_r_imagerec('bright_image.jpg')

# Save the image file
contrasted_image.save('contrast_image.jpg')
l_r_imagerec('contrast_image.jpg')
