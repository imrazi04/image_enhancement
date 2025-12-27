import cv2
import numpy as np


def enhance_image(image):
    """Perform simple histogram equalization on the luminance channel only.

    This preserves colors and the original image dimensions while improving
    brightness/contrast via equalizing the Y channel in YCrCb color space.
    """
    if image is None:
        return image

    # Ensure image is uint8 BGR
    if image.dtype != np.uint8:
        image = cv2.convertScaleAbs(image)

    # Convert BGR to YCrCb and equalize the Y (luma) channel
    ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    y, cr, cb = cv2.split(ycrcb)
    y_eq = cv2.equalizeHist(y)

    ycrcb_eq = cv2.merge((y_eq, cr, cb))
    enhanced = cv2.cvtColor(ycrcb_eq, cv2.COLOR_YCrCb2BGR)

    return enhanced
