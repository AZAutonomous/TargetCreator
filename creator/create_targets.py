import cv2
import numpy as np

from components import *

# Temporary test code
img = cv2.imread(letter[0])

# The two lines below are only necessary for an interactive python session
# cv2.startWindowThread()
# cv2.namedWindow("Image")

cv2.imshow("Image", img)

cv2.waitKey(0)
cv2.destroyAllWindows()
