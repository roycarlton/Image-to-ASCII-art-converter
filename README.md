This project is unfinished, but should be in a workable state.

The "converter.py" script takes an image and generates lines of ASCII characters to ultimately resemble the source image.
Converter.py takes either 3 or 4 arguments: source image file name/dir name, font file name, pixel width, (optional) pixel height

The pixel width and height refer to the size of the chunks of the image which will each be represented by 1 ASCII character.
If the pixel height option is not entered it will be 1.4x the value of pixel width by default.

The program requires a .ttf font file because the character for each pixel is decided by comparing the pixel to small images of each ASCII character generated from that font to see which is most similar.
Later, when the program will output an image of the ASCII art, it will also use the given font.

The font file I recommend (and the only one I have tested with) is SpaceMono-Regular.ttf, found here: https://fonts.google.com/specimen/Space+Mono

Fonts must be placed in the "font" directory to be accessible.

Works best with large images.

To do:
 - Functionality to generate an image file of the ASCII art (currently the only output is text)
 - Functionality to convert whole directories
 - Functionality to convert gifs by separating into frames, converting and reassembling
 - Add options for effects e.g. different colours or scrolling characters in the blank space/background