This project is unfinished, but should be in a workable state.

The "converter.py" script takes an image and generates lines of ASCII characters to ultimately resemble the source image.
Converter.py takes 3 or 4 arguments: source image file name, font file name, pixel width, (optional) pixel height

The pixel width and height refer to the size of the chunks of the image which will each be represented by 1 ASCII character.
If the pixel height option is not entered it will be 1.4x the value of pixel width by default.

Fonts must be placed in the "font" directory to be accessible.

To do:
 - Functionality to generate an image file of the ASCII art (currently the only output is text)
 - Functionality to convert whole directories
 - Functionality to convert gifs by separating into frames, converting and reassembling
 - Add options for effects e.g. different colours or scrolling characters in the blank space/background