# opencv-conversion-to-single-plane
This is a opencv python program to convert a curved perspective or a two planar image to a single plane image (bird's eye view).

The first program i.e. 11.py is to convert a curved perspective image or a tilted perspective image to single planar image.
The second program i.e. 12.py is to convert a two planar image to a single planar image.
I wasn't able to write a single program for both because when I tried, different methods worked for those images i.e. contour method worked well for test1.jpg (for 11.py) but hough transform method worked for test2.jpg (12.py).
The images were of very low resolution and I was unable to detect the slant lines in test2.py. so, I had to opt for a different approach.
I'm still working on a generic code which gives out desired results for an image with any perspective. My knowledge at this point helped me write the codes but I need a deeper understanding for writing a generic code.
