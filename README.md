# braille-ascii
Converts input image to ASCII art using braille glyph characters via command line. Features include setting manual threshold value, creating ASCII art for the inverted image, 
setting the pixel width of the ASCII art, and saving to a .txt file. If a threshold value is not set, an automatic thresholding algorithm is used instead (Otsu's method).

# Usage
Here are the following command line arguments to use:
```
--img       # Input image filepath
--width     # Width of ASCII art in pixels
--save      # Filepath to save ASCII art to
--inv       # Create ASCII art of the inverted input image
--thresh    # Set manual threshold value instead of automatic thresholding
```

# Example
```
$python braille.py --img 'filepath/example.jpg' --width 30 --save 'ascii.txt' --inv True --thresh 150
```
