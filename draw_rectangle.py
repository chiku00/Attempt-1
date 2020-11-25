import cv2
import numpy as np


# Variables
drawing = False # Initialize it as False. It will become True when the mouse 
# has been pressed down and it will continue to remain true till the mouse button 
# has been lifted, after which it again becomes False
ix,iy=-1,-1 # These are the initial points that are kept after the pressing down
# of the mouse button. That's an anchor of the rectangle
max_x = 0 # Initialize the max of all points during the button pressed down as 0
max_y = 0
min_x = 10**4 # Initialize the min of all points during the button pressed down as some arbitarily large number
min_y = 10**4
rectangles_drawn = np.empty((0,2,2), int)

# Function
def draw_rectangle(event,x,y,flags,params):
    global ix,iy,drawing,max_x,max_y,min_x,min_y,rectangles_drawn
    if event == cv2.EVENT_LBUTTONDOWN:
        
        drawing = True
        
        ix,iy=x,y
        min_x = x
        min_y = y
        max_x = 0 # Initialize the max of all points during the button pressed down as 0
        max_y = 0
    elif event == cv2.EVENT_MOUSEMOVE:
        
        if drawing == True:
            
            
            cv2.rectangle(img,pt1=(ix,iy),pt2=(x,y),color=(0,255,0),thickness=-1)
            if min_x>x:
                min_x = x # Update the min value of x while the mouse is being moved around while pressed down
            if min_y>y:
                min_y = y # Update the min value of y while the mouse is being moved around while pressed down
            if max_x<x:
                max_x = x # Update the max value of x while the mouse is being moved around while pressed down
            if max_y<y:
                max_y = y # Update the max value of y while the mouse is being moved around while pressed down
                
                
    elif event == cv2.EVENT_LBUTTONUP:
        
        drawing = False
        # Refresh the region b/w min-max values of x and y to black
        cv2.rectangle(img,pt1=(min_x,min_y),pt2=(max_x,max_y),color=(0,0,0),thickness=-1)
        # re-draw portions of the rectangles that may have been erased
        if rectangles_drawn.size != 0: # Rectangles have been previously drawn
            for rec in rectangles_drawn:
                x_1_temp = np.max([rec[0][0],min_x])
                #print(x_1_temp)
                y_1_temp = np.max([rec[0][1],min_y])
                #print(y_1_temp)
                x_2_temp = np.min([rec[1][0],max_x])
                #print(x_2_temp)
                y_2_temp = np.min([rec[1][1],max_y])
                #print(y_2_temp)
                # Check if the length x_2_temp-x_1_temp is >0 and y_2_temp-y_1_temp is >0
                if ((x_2_temp-x_1_temp)>0) & ((y_2_temp-y_1_temp)>0): # This means that there actually is an intersection
                    cv2.rectangle(img,pt1=(x_1_temp,y_1_temp),pt2=(x_2_temp,y_2_temp),color=(0,255,0),thickness=-1)
        # Draw the actual rectangle
        cv2.rectangle(img,pt1=(ix,iy),pt2=(x,y),color=(0,255,0),thickness=-1)
        rectangles_drawn = np.append(rectangles_drawn,[[[ix,iy],[x,y]]],axis=0)

# Showing the image

img = np.zeros((512,512,3),np.uint8)
cv2.namedWindow(winname='my_drawing')
cv2.setMouseCallback('my_drawing',draw_rectangle)

while True:
    cv2.imshow('my_drawing',img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()