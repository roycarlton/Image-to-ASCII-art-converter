from PIL import Image, ImageFont, ImageDraw
import numpy as np

pixel_size = 20
font_size = 15

font_filename = input("Enter font filename (including extension): ")
font = ImageFont.truetype("fonts/" + font_filename, font_size, encoding="utf-8")

temp_img = Image.new("1", (font_size, font_size))
draw = ImageDraw.Draw(temp_img)

(left, top, right, bottom) = font.getbbox("a")

print(left, top, right, bottom)

draw.text((0, -top), "a", "white", font=font)

print(np.asarray(temp_img)[5][5])

temp_img.show()

exit()

in_img_name = input("Enter input image filename: ")
in_img = Image.open(in_img_name).convert("1")
print(in_img.width)




#take input image
#dither to black and white
#divide into 'pixels'
#resize pixel appropriately to match character images
#comare with each character to find best fit
