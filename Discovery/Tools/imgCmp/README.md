#Image Comparison

This folder contains a program to compare images. Specifically, the images will
be compared using a pixel-wise percent error calculation. If two images have
the same resolution, the code will get the difference between each pixel of
image A and the corresponding pixel of image B, and then divide by 255 (the
maximum pixel value) to get a percent difference. Once a percent difference has
been calculated for every pixel, the mean, median and standard deviation will
be returned.

This code is designed to be used on different images from the same camera. The
statistics it returns are to be used to determine how "interesting" a camera
is - i.e., how likely it is to change meaningfully from one frame to another.

The mean and median are provided as a way to measure the overall change
between the images, while the standard deviation is used to check if that
change is distributed evenly accross the image or not. An image that contains
a high mean percent difference but a low standard deviation might indicate that
most of the change is background change, possibly with the hue of the sunlight,
while the same mean percent difference with a high standard deviation would
indicate that objects entered or left the frame. 