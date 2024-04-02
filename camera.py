# import necessary libraries

import cv2 as cv
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk


def process(img):
    # Makes image grayscale
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    gray = cv.GaussianBlur(gray, (5, 5), 1)

    # Finds the edges in an image
    gray_edge = cv.Canny(gray, 50, 150)

    return gray_edge


def mask(img):  # create a mask
    # Code from https://www.tutorialspoint.com/how-to-mask-an-image-in-opencv-python Example 2
    # Dimensions
    height, width = img.shape
    # Region to mask
    roi = np.array([
            [(100, height), (450, 305), (735, 305), (width, height)]
                    ])

    # Set Whole image as black
    mask = np.zeros_like(img)

    # Make roi white
    mask = cv.fillPoly(mask, roi, 255)

    # Make the mask
    masked_img = cv.bitwise_and(img, mask)

    return masked_img


def detect_lines(img):  # This detects line using Hough Lines P function in opencv
    # code from https://www.geeksforgeeks.org/line-detection-python-opencv-houghline-method/ Example 2
    left = []
    right = []
    lines = cv.HoughLinesP(
        img,  # edge image
        rho=cv.HOUGH_PROBABILISTIC,
        theta=np.pi / 180,
        threshold=100,  # Sets the num of intersections on polar plane to consider a line
        minLineLength=40,  # Line must be over set pixels
        maxLineGap=5  # max allowed gap to consider a separate line
    )

    # Change to slope-intercept line
    if lines is not None:
        for x in lines:
            x1, y1, x2, y2 = x[0]
            y_int_line = np.polyfit((x1, x2), (y1, y2), 1)

            if y_int_line[0] < 0:
                right.append((y_int_line[0], y_int_line[1]))  # slope & y intercept
            if y_int_line[0] > 0:
                left.append((y_int_line[0], y_int_line[1]))  # slope & y intercept

        # Average
        if len(left) > 0:
            line_left = np.average(left, axis=0)
        else:
            line_left = None

        if len(right) > 0:
            line_right = np.average(right, axis=0)
        else:
            line_right = None

    else:
        line_left = None
        line_right = None

    return line_left, line_right


def make_endpoints(line, img):
    if line is not None:
        slope, yint = line[0], line[1]
        y1 = img.shape[0]
        y2 = int(y1 * (1 / 2))
        x1 = int((y1 - yint) / slope)
        x2 = int((y2 - yint) / slope)

        if x1 > 100000 or x2 > 100000 or x1 < 0 or x2 < 0:
            return None, None, None, None
        cv.line(img, (x1, y1), (x2, y2), (0, 255, 0), 15)
        return x1, y1, x2, y2
    else:
        return None, None, None, None


def draw_lines(right_line, left_line, img):
    # code from https://www.geeksforgeeks.org/line-detection-python-opencv-houghline-method/ example 2 math is my code

    x1, y1, x2, y2 = make_endpoints(left_line, img)  # Makes points and then draws
    x3, y3, x4, y4 = make_endpoints(right_line, img)
    if x1 is not None and x3 is not None:
        if right_line is not None:
            pt1_mid = int((x3 + x1) / 2), int((y3 + y1) / 2)
            pt2_mid = int((x4 + x2) / 2), int((y4 + y2) / 2)
            cv.line(img, pt1_mid, pt2_mid, (0, 0, 255), 15)

    # for averages in right_line, left_line:
    #     if averages is not None:
    #         slope, yint = averages
    #         y1 = img.shape[0]
    #         y2 = int(y1*(1/2))
    #         x1 = int((y1 - yint) / slope)
    #         x2 = int((y2-yint) / slope)
    #         cv.line(img, (x1, y1), (x2, y2), (0, 255, 0), 15)
    #     else:
    #         continue

    return img


def predict_turn(img):
    left_img = cv.imread("Leftturn.png")
    right_img = cv.imread("Rightturn.png")
    left_img = cv.cvtColor(left_img, cv.COLOR_BGR2GRAY)
    right_img = cv.cvtColor(right_img, cv.COLOR_BGR2GRAY)
    # Code below from  https://www.geeksforgeeks.org/perspective-transformation-python-opencv/
    height, width, depth = img.shape
    # Region to mask
    pts1 = np.float32([
        [(100, height), (width, height), (450, 305), (735, 305)]
    ])
    pts2 = np.float32([[0, 640], [400, 640],
                       [0, 0], [400, 0]])
    # Apply Perspective Transform Algorithm
    matrix = cv.getPerspectiveTransform(pts1, pts2)
    result = cv.warpPerspective(img, matrix, (400, 640))
    result = cv.cvtColor(result, cv.COLOR_BGR2GRAY)

    # https://forum.opencv.org/t/template-matching-with-video-input/6563

    left_true = cv.matchTemplate(result, left_img, cv.TM_CCOEFF_NORMED)
    l_min_val, l_max_val, l_min_loc, l_max_loc = cv.minMaxLoc(left_true)

    right_true = cv.matchTemplate(result, left_img, cv.TM_CCOEFF_NORMED)
    r_min_val, r_max_val, r_min_loc, r_max_loc = cv.minMaxLoc(right_true)

    # Checks for match in turn detection
    if l_max_val >= 0.6:
        new_img = cv.putText(img, "Turn Prediction: <---", (50, 50), cv.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 0))
    elif r_max_val >= 0.5:
        new_img = cv.putText(img, "Turn Prediction: --->", (50, 50), cv.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 0))
    else:
        new_img = cv.putText(img, "Turn Prediction: Straight", (50,50), cv.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 0))
    return result, new_img


