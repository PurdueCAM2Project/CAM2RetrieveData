# Image Comparison Algorithm

This folder contains a program to compare images. Specifically, the images will
be compared using a pixel-wise squared difference calculation. If two images
have the same resolution, the code will get the difference between each pixel
of image A and the corresponding pixel of image B, and then square this value.
Once a squared difference has been calculated for every pixel, the mean, median
and standard deviation will be returned.

This code is designed to be used on different images from the same camera. The
statistics it returns are to be used to determine how "interesting" a camera
is - i.e., how much the frames change due to object movement.

The mean and median are provided as a way to measure the overall change
between the images, while the standard deviation is used to check if that
change is distributed evenly accross the image or not. An image that contains
a high mean squared difference but a low standard deviation might indicate that
most of the change is background change, possibly with the hue of the sunlight,
while the same mean percent difference with a high standard deviation would
indicate that objects entered or left the frame.

# Results

Initial testing has shown that the relationship between median and standard
deviation has the most predictive power in estimating the change in objects
from between one image and another. When there is a lot of object change, but
not a lot of background change, the median tends to be much lower than the
standard deviation, usually by multiple factors of 10. Alternatively, when the
background changes but there is not a lot of object change, the median and
standard deviation tend to be much closer, with the median sometimes being
larger than the standard deviation. When there is very little change, either in
the background or foreground, both the median and standard deviation will be
low.