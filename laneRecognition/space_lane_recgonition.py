import cv2
from google.colab.patches import cv2_imshow
import numpy as np
import matplotlib as mt


def main():
    image = cv2.imread("/content/Car_space1.jpg")
    lane_image = np.copy(image)
    canny_image = canny(lane_image)
   # cv2_imshow(canny_image)
    cropped_image = region_of_interest(canny_image)
    cv2_imshow(cropped_image)
    lines =cv2.HoughLinesP(cropped_image, 1, np.pi/180, 50, np.array([]), minLineLength= 40, maxLineGap = 5)
    print(lines)
    averaged_lines = average_slope_intercept(image, lines)
    print (averaged_lines)
    line_image = display_lines(lane_image, lines)
    combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)
    cv2_imshow(combo_image)
    #line_image
    cv2.waitKey(0)
    #use pltmatlib to get cooridinates
    #cropped_image = region_of_interest(canny_image)



def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if abs(slope) < 0.001:
            continue
        elif slope < 0:
            left_fit.append((slope,intercept))
        else:
            right_fit.append((slope, intercept))
    left_fit_average = np.average(left_fit, axis = 0)
    right_fit_average = np.average(right_fit, axis = 0)
    left_line = make_coordinates(image, left_fit_average)
    right_line = make_coordinates(image, right_fit_average)
    return np.array([left_line, right_line])

def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1 * 3/5)
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept))


def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)
        return line_image

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray,(5, 5), 0)
    canny_image = cv2.Canny(blur, 50, 150) #can do 2:1 ratios or 3:1 eg (50, 100) either 
    return canny_image

def region_of_interest(image):
    height = image.shape[0]
    triangle = np.array([
        [(0,height), (1000,height), (150,120)]
    ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, triangle, 255)
    masked_image = cv2.bitwise_and(image,mask)
    return masked_image
    return mask

main()