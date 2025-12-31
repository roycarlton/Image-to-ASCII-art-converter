from PIL import Image, ImageFont, ImageDraw
import numpy as np
import sys

def similarity_score(im1, im2):
    """Compare similarity of 2 black and white images of the same size. Score = num of identical pixels"""
    w1 = im1.width
    h1 = im1.height
    w2 = im2.width
    h2 = im2.height
    if (w1 != w2) or (h1 != h2):
        print("\nEncountered images of different sizes when calculating similarity, exiting...")
        exit()
    score = 0
    im1 = np.asarray(im1)
    im2 = np.asarray(im2)
    for i in range(w1):
        for j in range(h1):
            if im1[i][j] == im2[i][j]:
                score += 1
    return score

def generate_character_images(min, max, font):
    """Load images of each character into a dictionary and return."""

    chr_imgs = {}

    for i in range(min, max):

        temp_chr = chr(i)
        (left, top, right, bottom) = font.getbbox(temp_chr)

        temp_img = Image.new("1", (font_size, font_size))
        draw = ImageDraw.Draw(temp_img)

        #print(left, top, right, bottom)

        draw.text(((font_size-right)/2, -(top/2)), temp_chr, "white", font=font)

        #print(np.asarray(temp_img)[5][5])

        chr_imgs[temp_chr] = temp_img

    return chr_imgs

if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("\nProgram requires exactly 3 arguments: source file name, font file name, pixel width")
        print("For example: python converter.py image.jpg, font.ttf, 5\n")
        exit()
    
    in_img_name = sys.argv[1]
    font_filename = sys.argv[2]
    pixel_width = int(sys.argv[3])

    #pixel width and height = size of each "pixel" we will take from the source img
    #and convert to a character. One "pixel" = one character
    #pixel_width = 2
    pixel_height = int(pixel_width * 1.4)

    font_size = 15

    #font_filename = input("Enter font filename (including extension): ")
    #font_filename = "mono.ttf"
    font = ImageFont.truetype("fonts/" + font_filename, font_size, encoding="utf-8")

    chr_imgs = generate_character_images(33, 127, font)

    #in_img_name = input("Enter input image filename: ")
    #in_img_name = "test.jpg"
    in_img = Image.open(in_img_name).convert("1")
    #print(in_img.width)

    # in_img.show()
    # input()

    im_height = in_img.height
    im_width = in_img.width

    pixel_rows = im_height // pixel_height
    pixel_cols = im_width // pixel_width

    text_rows = []

    print()

    #Crop each pixel and compare it to every character image we got earlier
    #Most similar character gets added to represent that "pixel"
    for row in range(pixel_rows):
        print("Converting row " + str(row) + " / " + str(pixel_rows), end="\r")
        temp_text_row = ""
        for col in range(pixel_cols):
            img_crop = in_img.crop((col*pixel_width, row*pixel_height, ((col+1)*pixel_width)-1, ((row+1)*pixel_height)-1))
            #img_crop = img_crop.resize((font_size, font_size), Image.LANCZOS)
            img_crop = img_crop.resize((font_size, font_size))

            # img_crop.show()
            # input()

            highest = 0
            closest_chr = "."
            for key in chr_imgs:
                temp_score = similarity_score(img_crop, chr_imgs[key])
                if temp_score > highest:
                    highest = temp_score
                    closest_chr = key

            # chr_imgs[closest_chr].show()
            # input()

            temp_text_row += closest_chr
        text_rows.append(temp_text_row)
        #print(temp_text_row)

    print()

    with open("out_text.txt", "w") as file:
        for row in text_rows:
            file.write(row + "\n")




    # print("height: " + str(im_height))
    # print("width: " + str(im_width))
    # print("pixel_rows: " + str(pixel_rows))
    # print("pixel_cols: " + str(pixel_cols))


    #take input image
    #dither to black and white
    #divide into 'pixels'
    #resize pixel appropriately to match character images
    #comare with each character to find best fit
