import cv2

img = cv2.imread('sample image.jif.jfif')                    # read the image
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)              # make grey copy of the image and store it in imgray
_, th1 = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY)  # set threshold
contours, hierarchy = cv2.findContours(th1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # find contours of the image

squares = 0
rectangles = 0
triangles = 0
circles = 0

min_p = 150   # minimum premiter for the shape
max_p = 500   # maximum premiter for the shape
min_A = 1000  # minimum Area for the shape
for contour in contours:
    approx = cv2.approxPolyDP(contour, 0.025 * cv2.arcLength(contour, True), True)
    x = approx.ravel()[0]           # x coordinate of the contour
    y = approx.ravel()[1]           # y coordinate of the contour
    if min_p <= cv2.arcLength(contour, True) <= max_p and cv2.contourArea(contour) >= min_A:  # To exclude the noises
        if len(approx) == 3:        # polygon with three sides
            cv2.drawContours(img, [approx], 0, (0, 255, 255), 1)            # draw a frame around the detected triangle
            cv2.putText(img, "Triangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))    # Type polygon name
            triangles += 1          # increase the number of triangles detected by one
        elif len(approx) == 4:      # polygon with four sides
            x, y, w, h = cv2.boundingRect(approx)
            aspectRatio = float(w)/h
            if 0.95 <= aspectRatio <= 1.05:  # if aspect ratio near to 1, then it's square
                cv2.drawContours(img, [approx], 0, (0, 0, 255), 1)
                cv2.putText(img, "Square", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
                squares += 1
            else:                   # if aspect ratio not near to 1, then it's rectangle
                cv2.drawContours(img, [approx], 0, (0, 255, 0), 1)
                cv2.putText(img, "Rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
                rectangles += 1
        else:                       # polygon with many sides
            cv2.drawContours(img, [approx], 0, (255, 0, 0), 1)
            cv2.putText(img, "Circle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
            circles += 1
print("Number of triangles = ", triangles)
print("Number of squares = ", squares)
print("Number of rectangles = ", rectangles)
print("Number of circles = ", circles)

cv2.imshow('img', img)  # Show the image after editing
cv2.waitKey(0)          # Wait for manual close for the window
