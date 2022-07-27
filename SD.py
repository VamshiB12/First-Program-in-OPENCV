import cv2
import math

#Function for checking if two sides are equal or not
#calculates the ratio of the distances between points p1 & p2 and point p3 and p4
def ratio(p1, p2, p3, p4):
    try:
        j = math.dist(p1, p2)/math.dist(p3, p4)
    except ZeroDivisionError:
        j = 0

    #handling small inaccuracies
    if j > 0.8 and j < 1.2:
        return True
    else:
        return False

#reading the image
original = cv2.imread("shapes.jpg")
#creating a copy of image, so we can process and compare it with the original image
img = original.copy()

#creating grayscale of the image, coz canny function requires grayscale image
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#Canny function used for edge detection
canny = cv2.Canny(gray, 125, 175)

#Finding contours and hierarchy
contours, hier = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


s = str(input("Enter a shape:")).lower()

#font size for printing text
fontSize = 0.5
boundaryColor = [0,0,255] #(Blue, Green, Red) format

#iterating through each contours
for x in contours:
    #Polygon approximation, returns list of coordinates of vertices 
    approx = cv2.approxPolyDP(x, 0.01 * cv2.arcLength(x, True), True)

    #number of sides is equal to number of veritices
    sides = len(approx)

    #finding median, to print text approximately at the center of the shape
    i, j = 0, 0
    for a in range(sides):
        i += approx[a][0][0]
        j += approx[a][0][1]

    i /= sides
    j /= sides

    #if number of vertices = 3
    if sides == 3 and s == "triangle":
        cv2.putText(img, "Triangle", (int(i) - 32,int(j)), cv2.FONT_HERSHEY_COMPLEX, fontSize, 0, 1)   
        cv2.drawContours(img, x, -1, boundaryColor, 2)

    #if number of vertices = 4
    elif sides == 4:

        #finding the coordinates of 4 vertices so we can find the distance between vertices and decide the shape
        p1 = approx[0][0]
        p2 = approx[1][0]
        p3 = approx[2][0]
        p4 = approx[3][0]

        
        if ratio(p1, p2, p2, p3):#checking whether adjacent sides are equal or not
            if ratio(p1, p3, p2, p4) and s == "square": #checking whether diagonals are equal or not
                cv2.putText(img, "Square", (int(i) - 24,int(j)), cv2.FONT_HERSHEY_COMPLEX, fontSize, 0, 1)
                cv2.drawContours(img, x, -1, boundaryColor, 2)
            elif s == "rhombus":
                cv2.putText(img, "Rhombus", (int(i) - 28,int(j)), cv2.FONT_HERSHEY_COMPLEX, fontSize, 0, 1)
                cv2.drawContours(img, x, -1, boundaryColor, 2)
                
        elif ratio(p1, p2, p3, p4) and ratio(p2, p3, p4, p1):#checking whether pair of opposite sides are equal
            if ratio(p1, p3, p2, p4) and s == "rectangle": #checking whether diagonals are equal or not
                cv2.putText(img, "Rectangle", (int(i) - 36,int(j)), cv2.FONT_HERSHEY_COMPLEX, fontSize, 0, 1)
                cv2.drawContours(img, x, -1, boundaryColor, 2)
            elif not(ratio(p1, p3, p2, p4)) and s == "parallelogram":
                cv2.putText(img, "Parallelogram", (int(i) - 52,int(j)), cv2.FONT_HERSHEY_COMPLEX, fontSize, 0, 1)
                cv2.drawContours(img, x, -1, boundaryColor, 2)

        elif (ratio(p1,p2,p3,p4) or ratio(p2,p3,p4,p1)) and s == "trapezium":#checking whether only if one pair of opposite sides are equal

            #the slope of the parallel sides should be equal
            if math.floor(math.fabs(p1[1] - p2[1])/math.fabs(p1[0] - p2[0])) == math.floor(math.fabs(p4[1] - p3[1])/math.fabs(p4[0] - p3[0])) :
                cv2.putText(img, "Trapezium", (int(i) - 36,int(j)), cv2.FONT_HERSHEY_COMPLEX, fontSize, 0, 1)
                cv2.drawContours(img, x, -1, boundaryColor, 2)
            elif math.floor(math.fabs(p1[1] - p2[1])/math.fabs(p1[0] - p2[0])) == math.floor(math.fabs(p4[1] - p3[1])/math.fabs(p4[0] - p3[0])):
                cv2.putText(img, "Trapezium", (int(i) - 36,int(j)), cv2.FONT_HERSHEY_COMPLEX, fontSize, 0, 1)
                cv2.drawContours(img, x, -1, boundaryColor, 2)
        elif s == "quadrilateral":
            #if none of the cases match, it should be a quadrilateral
            cv2.putText(img, "Quadrilateral", (int(i) - 52,int(j)), cv2.FONT_HERSHEY_COMPLEX, fontSize, 0, 1)
            cv2.drawContours(img, x, -1, boundaryColor, 2)
            
    #if number of vertices = 5
    elif sides == 5 and s == "pentagon":
        cv2.putText(img, "Pentagon", (int(i) - 32,int(j)), cv2.FONT_HERSHEY_COMPLEX, fontSize, 0, 1)   
        cv2.drawContours(img, x, -1, boundaryColor, 2)

    #if number of vertices = 6
    elif sides == 6 and s == "hexagon":
        cv2.putText(img, "Hexagon", (int(i) - 28,int(j)), cv2.FONT_HERSHEY_COMPLEX, fontSize, 0, 1)   
        cv2.drawContours(img, x, -1, boundaryColor, 2)

    #if number of vertices = 7
    elif sides == 7 and s == "heptagon":
        cv2.putText(img, "Heptagon", (int(i) - 32,int(j)), cv2.FONT_HERSHEY_COMPLEX, fontSize, 0, 1)   
        cv2.drawContours(img, x, -1, boundaryColor, 2)

    #if number of vertices = 8
    elif sides == 8 and s == "octagon":
        cv2.putText(img, "Octagon", (int(i) - 28,int(j)), cv2.FONT_HERSHEY_COMPLEX, fontSize, 0, 1)   
        cv2.drawContours(img, x, -1, boundaryColor, 2)

    elif sides > 8:
        #getting coordinates of 4 extreme points, assuming that the shape is either circle or ellipse
        p1 = approx[0][0]
        p2 = approx[sides//4][0]
        p3 = approx[sides//2][0]
        p4 = approx[3*sides//4][0]

        #print(ratio(p1,p3,p2,p4))
        #if the diameters are equal
        if ratio(p1,p3,p2,p4) and s == "circle":
            #print("Circle: " + str(ratio(p1,p3,p2,p4)))
            cv2.putText(img, "Circle", (int(i) - 24,int(j)), cv2.FONT_HERSHEY_COMPLEX, fontSize, 0, 1)   
            cv2.drawContours(img, x, -1, boundaryColor, 2)
            
        elif not(ratio(p1,p3,p2,p4)) and (s == "ellipse" or s == "oval"):
            #print("Ellipse: " + str(ratio(p1,p3,p2,p4)))
            cv2.putText(img, "Ellipse", (int(i) - 28,int(j)), cv2.FONT_HERSHEY_COMPLEX, fontSize, 0, 1)   
            cv2.drawContours(img, x, -1, boundaryColor, 2)

#displaying original image
cv2.imshow('Original', original)
#displaying detected shapes
cv2.imshow('Detected Shapes', img)


