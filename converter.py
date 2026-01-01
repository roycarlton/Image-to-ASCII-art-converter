from PIL import Image, ImageFont, ImageDraw
import numpy as np
import sys, os.path

lotta_spaces = "                        "

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

def generate_character_images(min, max, font, font_size):
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

def generate_ASCII_art_image(text_rows, font, font_size, colour):
    """Takes a list of text rows and returns an image displaying them"""

    out_img = Image.new("RGB", (font_size * len(text_rows[0]), font_size * len(text_rows)))
    draw = ImageDraw.Draw(out_img)

    counter = 0
    for row in text_rows:
        draw.text((0, counter*font_size), row, colour, font=font)
        counter += 1

    return out_img

if __name__ == "__main__":

    output_dir = "out"
    font_dir = "fonts"

    if len(sys.argv) == 4 or len(sys.argv) == 5:

        input_dir = ""
        if os.path.isdir(sys.argv[1]):
            image_q = os.listdir(sys.argv[1])
            input_dir = sys.argv[1] + "/"
        elif os.path.isfile(sys.argv[1]):
            image_q = [sys.argv[1]]
        else:
            print("\nFirst argument must be either a valid directory or image file.\n")
            exit()

        if os.path.isfile(font_dir + "/" + sys.argv[2]):
            font_filename = font_dir + "/" + sys.argv[2]
        else:
            print("\nSecond argument must be a valid font file.\n")
            exit()

        if sys.argv[3].isdigit():
            pixel_width = int(sys.argv[3])
        else:
            print("\nThird argument must be an integer.\n")
            exit()

        #pixel width and height = size of each "pixel" we will take from the source img
        #and convert to a character. One "pixel" = one character
        #pixel_width = 2
        if len(sys.argv) == 5:
            if sys.argv[4].isdigit():
                pixel_height = int(sys.argv[4])
            else:
                print("\nFourth argument must be an integer.\n")
                exit()
        else:
            pixel_height = int(pixel_width * 1.4)
    

    else:
        print("\nProgram requires either 3 or 4 arguments: source file name/dir name, font file name, pixel width, (optional) pixel height")
        print("For example: python converter.py image.jpg, font.ttf, 5\n")
        exit()


    if not os.path.isdir(output_dir):
        print("\nThere must be a valid output directory named '"+ output_dir +"'\n")
        exit()

    font_size = 20

    font = ImageFont.truetype(font_filename, font_size, encoding="utf-8")

    chr_imgs = generate_character_images(33, 127, font, font_size)

    # chr_imgs["a"].show()
    # input()
    # chr_imgs["!"].show()
    # input()
    # chr_imgs["0"].show()
    # input()
    # chr_imgs["W"].show()
    # input()
    # exit()

    counter = 0
    for in_img_name in image_q:

        in_img = Image.open(input_dir + in_img_name).convert("1")

        # in_img.show()
        # input()

        im_height = in_img.height
        im_width = in_img.width

        pixel_rows = im_height // pixel_height
        pixel_cols = im_width // pixel_width

        text_rows = []

        print("Working on: " + in_img_name)

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

        print("Finished converting " + in_img_name + lotta_spaces + "\n")

        stub_filename = output_dir + "/" + str(counter).zfill(4)
        text_filename = stub_filename + ".txt"
        image_filename = stub_filename + ".jpg"
        with open(text_filename, "w") as file:
            for row in text_rows:
                file.write(row + "\n")

        print("\nGenerated ASCII written to " + text_filename)

        ASCII_image = generate_ASCII_art_image(text_rows, font, font_size, "white")

        ASCII_image.save(image_filename)

        print("\nGenerated image written to " + image_filename)

        counter += 1


    # print("height: " + str(im_height))
    # print("width: " + str(im_width))
    # print("pixel_rows: " + str(pixel_rows))
    # print("pixel_cols: " + str(pixel_cols))


    #take input image
    #dither to black and white
    #divide into 'pixels'
    #resize pixel appropriately to match character images
    #comare with each character to find best fit
