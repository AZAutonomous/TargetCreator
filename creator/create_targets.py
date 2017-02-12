import cv2
import numpy as np
import os
import argparse
import random

import azautil.jsonify

from components import *

DEBUG = False 

parser = argparse.ArgumentParser(description='Generate sample targets based on resources as specified in components.py')
parser.add_argument('-s', '--size', metavar='size', type=int, help="Output image resolution. Output is always square")
parser.add_argument('format', choices=['json', 'jpg', 'all'], help="Output image format. Acceptable options are json and jpg and all", metavar='format')

args = parser.parse_args()

# Iterate through backgrounds
for background in backgrounds:
    bg = cv2.imread(background[1])
    # Iterate through shapes
    for shape in shapes:
        # Read shape in. Note current iteration has shape as black on white
        targetShape = cv2.imread(shape[1])
        # Iterate through letters
        for letter in letters:
            # Read letter in. Note current iteration has letter as white on black
            targetLetter = cv2.imread(letter[1])
            # Iterate through target colors
            for color in colors:
                targetColor = color[1]
                # Iterate through letter colors
                for letterColor in colors:
                    # Check for same colors, skip (assume will never have)
                    if letterColor == color:
                        continue
                    targetLetterColor = letterColor[1]
                    
                    # Grab random slice of background
                    x = random.randint(0, bg.shape[0]-targetShape.shape[0])
                    y = random.randint(0, bg.shape[1]-targetShape.shape[1])
                    targetBg = bg[x:x+targetShape.shape[0], y:y+targetShape.shape[1]]
                    
                    # Convert images to masks
                    targetShape_gray = cv2.cvtColor(targetShape, cv2.COLOR_BGR2GRAY)
                    ret, targetShape_mask = cv2.threshold(targetShape_gray, 200, 255, cv2.THRESH_BINARY)
                    targetLetter_gray = cv2.cvtColor(targetLetter, cv2.COLOR_BGR2GRAY)
                    ret, targetLetter_mask = cv2.threshold(targetLetter_gray, 200, 255, cv2.THRESH_BINARY)
                   
                    blank = np.full(targetBg.shape, 255, dtype=(np.uint8))
                    # Construct target
                    target_top = cv2.bitwise_and(blank, targetLetterColor, mask=cv2.bitwise_not(targetLetter_mask))
                    target_mid = cv2.bitwise_and(blank, targetColor, mask=cv2.bitwise_and(cv2.bitwise_not(targetShape_mask), targetLetter_mask))
                    target_bot = cv2.bitwise_and(targetBg, targetBg, mask=targetShape_mask)
                    target = cv2.bitwise_or(target_top, target_mid)
                    target = cv2.bitwise_or(target, target_bot)

                    # Resize images
                    if args.size is not None:
                        target = cv2.resize(target, (args.size, args.size), interpolation = cv2.INTER_AREA)

                    if DEBUG:
                        cv2.imshow("Top", target_top)
                        cv2.imshow("Mid", target_mid)
                        cv2.imshow("Bot", target_bot)

                    # Save target
                    directory = '../generated/'
                    if not (os.path.isdir(directory)):
                        os.mkdir(directory)
                    filename = background[0] + '_' + color[0] + '_' + shape[0] + '_' + letterColor[0] + '_' + letter[0]
                    if args.format == 'all':
                        # save as JSON with labels
                        packet = {}
                        packet["image"] = filename + '.jpg'
                        packet["shape"] = shape[0]
                        packet["shapeColor"] = color[0]
                        packet["letter"] = letter[0]
                        packet["letterColor"] = letterColor[0]
                        packet["orientation"] = "n"
                        azautil.jsonify.save(packet, directory + filename + '.json')
                        cv2.imwrite(directory + filename + '.jpg', target)
                    elif args.format == 'json':
                        # save as JSON with labels
                        packet = {}
                        packet["image"] = filename + '.jpg'
                        packet["shape"] = shape[0]
                        packet["shapeColor"] = color[0]
                        packet["letter"] = letter[0]
                        packet["letterColor"] = letterColor[0]
                        packet["orientation"] = "n"
                        azautil.jsonify.save(packet, directory + filename + '.json')
                    elif args.format == 'jpg':
                        cv2.imwrite(directory + filename + '.jpg', target)
                    else:
                        print("No output format specified")
                    if DEBUG:
                        cv2.imshow("Debug", target)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
