from PIL import Image

def crop_square(image:Image) -> Image:

    width, height = image.size

    if width == height:
        return image

    if width > height:
        left = (width - height) / 2
        right = width - left
        top = 0
        bottom = height
    else:
        top = (height - width) / 2
        bottom = height - top
        left = 0
        right = width

    return image.crop((left, top, right, bottom))