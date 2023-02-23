
#import relevent librarys
import time
import numpy as np
import cv2


# define a camera
#cam = cv2.VideoCapture(0) # Use defualt camera


# initialise grid dimention variables
dimGX = 0
dimGY = 0


# Other grid and image size variables
dimFX = 0
dimFY = 0
dimX = 0
dimY = 0

# initialise object lists
objectsOrange = []
objectsPurple = []


# HSV thresholds for orange
orangeLower = np.array([10, 200, 255])
orangeUpper = np.array([30, 255, 255])

# HSV thresholds for purple
purpleLower = np.array([130, 50, 255]) # 130
purpleUpper = np.array([175, 255, 255]) # 170



def calNewSize():
    global dimX, dimY, dimFX, dimFY
    
    # calculate new image size
    unitSquare = 100 # 10x10 pixel square units
    dimFX = unitSquare * dimGX
    dimFY = unitSquare * dimGY

    # calc grid segment sizes
    dimX = int(dimFX / dimGX)
    dimY = int(dimFY / dimGY)
    

    
#algorythm that draws grid
def gridDraw(img):
    # vertical
    accume = 0
    for i in range(0,dimGX):
        accume = accume + dimX
        gridFrameBuild = cv2.line(img, (accume,0), (accume,dimFY), (255,255,255), 2)
        #print(accume)
        
    # horizontal
    accume = 0
    for i in range(0,dimGY):
        accume = accume + dimY
        gridFrameBuild = cv2.line(gridFrameBuild, (0,accume), (dimFX,accume), (255,255,255), 2)
        #print(accume)

    return gridFrameBuild


def takeImageSample(): # requires camera reading from
    
    
    #ret, raw = cam.read() # gets a frame capture
    
    #ret, raw = cam.read() # gets a frame capture

    raw = cv2.imread('test_image4.png')

    # flip camera image
    frame = cv2.flip(raw,1)

    # store frame in HSV
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frameHSV = cv2.cvtColor(frameHSV, cv2.COLOR_BGR2HSV)
    frameHSV = cv2.cvtColor(frameHSV, cv2.COLOR_BGR2HSV)

    # update frame with new sizeing
    # resizing frames
    frame = cv2.resize(frame, (dimFX, dimFY))
    frameHSV = cv2.resize(frameHSV, (dimFX, dimFY))


    # Create mask layer for purple
    purpleMask = cv2.inRange(frameHSV, purpleLower, purpleUpper)

    # Create mask layer for orange
    orangeMask = cv2.inRange(frameHSV, orangeLower, orangeUpper)

    # store raw frame
    rawFrame = frame.copy()

    # get grid frame
    gridFrame = gridDraw(frame)
    gridFrameOrange = gridFrame.copy()
    gridFramePurple = gridFrame.copy()

    # find contours of objects
    contoursOrange, hierarchyOrange = cv2.findContours(orangeMask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contoursPurple, hierarchyPurple = cv2.findContours(purpleMask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


    # if contours were found
    if len(contoursOrange) != 0:
        for contour in contoursOrange: # for each detected
            # check size (not too small e.g. anomolies)
            if cv2.contourArea(contour) > 500: # 500
                # get dimantions and location
                x, y, w, h, = cv2.boundingRect(contour)
                # draw rectangle
                cv2.rectangle(gridFrameOrange, (x,y), (x+w, y+h), (0, 0, 255), 2)
                
                # calculate object centure and grid location
                objectCenture = [x+(w/2),y+(h/2)] # calculate ceture of object
                GridObjectX = int(objectCenture[0]/(dimFX/dimGX)) # calculate grid location on x-axis (snapping)
                GridObjectY = int(objectCenture[1]/(dimFY/dimGY)) # calculate grid location on x-axis (snapping)

                # log object in memory
                GridObject=[GridObjectX,GridObjectY,'A'] # create buffer grid obejct with calculated values
                if GridObject not in objectsOrange: # check not already in memory
                    objectsOrange.append(GridObject) # ad object into the list


    # if contours were found
    if len(contoursPurple) != 0:
        for contour in contoursPurple: # for each detected
            # check size (not too small e.g. anomolies)
            if cv2.contourArea(contour) > 300: # 500
                # get dimantions and location
                x, y, w, h, = cv2.boundingRect(contour)
                # draw rectangle
                cv2.rectangle(gridFramePurple, (x,y), (x+w, y+h), (0, 0, 255), 2)

                # calculate object centure and grid location
                objectCenture = [x+(w/2),y+(h/2)] # calculate ceture of object
                GridObjectX = int(objectCenture[0]/(dimFX/dimGX)) # calculate grid location on x-axis (snapping)
                GridObjectY = int(objectCenture[1]/(dimFY/dimGY)) # calculate grid location on x-axis (snapping)

                # log object in memory
                GridObject=[GridObjectX,GridObjectY,'B'] # create buffer grid obejct with calculated values
                if GridObject not in objectsPurple: # check not already in memory
                    objectsPurple.append(GridObject) # ad object into the list



    # highlight the grid space of detected obejcts
    for objectOrange in objectsOrange:
        gridX1 = int(objectOrange[0] * (dimFX/dimGX))
        gridY1 = int(objectOrange[1] * (dimFY/dimGY))
        
        gridX2 = int(gridX1 + (1 * (dimFX/dimGX)))
        gridY2 = int(gridY1 + (1 * (dimFY/dimGY)))
        # draw rectangle
        cv2.rectangle(gridFrameOrange, (gridX1,gridY1), (gridX2, gridY2), (0, 255, 0), 4)

    # highlight the grid space of detected obejcts
    for objectPurple in objectsPurple:
        gridX1 = int(objectPurple[0] * (dimFX/dimGX))
        gridY1 = int(objectPurple[1] * (dimFY/dimGY))
        
        gridX2 = int(gridX1 + (1 * (dimFX/dimGX)))
        gridY2 = int(gridY1 + (1 * (dimFY/dimGY)))
        # draw rectangle
        cv2.rectangle(gridFramePurple, (gridX1,gridY1), (gridX2, gridY2), (0, 0, 255), 4)
        

    # draw baorders arounnd frames BGR
    cv2.rectangle(rawFrame, (0,0), (dimGX*100, dimGY*100), (255, 0, 0), 5)
    cv2.rectangle(gridFrameOrange, (0,0), (dimGX*100, dimGY*100), (0, 165, 255), 5)
    cv2.rectangle(gridFramePurple, (0,0), (dimGX*100, dimGY*100), (128, 0, 128), 5)
    cv2.rectangle(orangeMask, (0,0), (dimGX*100, dimGY*100), (255, 255, 255), 5)
    cv2.rectangle(purpleMask, (0,0), (dimGX*100, dimGY*100), (255, 255, 255), 5)


    if (True):
        allImagesGrid = np.concatenate((rawFrame,gridFrameOrange,gridFramePurple),axis=1)
        allImagesMask = np.concatenate((orangeMask,purpleMask),axis=1)
        cv2.imshow("Detection Frames (Raw, Orange, Purple)",allImagesGrid)
        cv2.imshow("Mask Frames (Orange, Purple)",allImagesMask)
    else:
        # display image frames
        cv2.imshow("Raw",rawFrame)
        cv2.imshow("Grid",gridFrame)
        cv2.imshow('Grid Orange',gridFrameOrange)
        cv2.imshow('Orange Mask',orangeMask)
        cv2.imshow('Purple Mask',purpleMask)

    # check for exit key
    #if cv2.waitKey(1) & 0xFF == ord('q'):
        #break


    
    #cv2.destroyAllWindows() # close all cv2 windows



def takeAnalysedSamples():
    global objectsOrange, objectsPurple

    calNewSize()

    print("\nTaking Image Captures For Analyses")

    # define a camera
    #cam = cv2.VideoCapture(0) # Use defualt camera
    #ret, raw = cam.read() # gets a frame capture DEBUG
    time.sleep(1)

    # take multiple runs
    for i in range(4):
        print("Image Analyses Run: ",i)
        
        # get sample and analyse
        takeImageSample()
        # small delay
        cv2.waitKey(500)

    # Remove out of date detections
    #listGarbageCollection()

    #cam.release() # release camera

    # return lists
    return objectsOrange, objectsPurple




cv2.waitKey()


# end of program
#input("\n\nEND")
#cam.release() # release camera
#cv2.destroyAllWindows() # close all cv2 windows
    
    

