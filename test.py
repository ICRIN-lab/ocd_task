from PIL import Image

image = Image.open("img/test1a.png")

width, height = image.size

print(width, height)
