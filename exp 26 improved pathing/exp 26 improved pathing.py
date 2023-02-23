import basicColourRec as objRec
import RoboManagerV10 as RM

import time

print("\n\nEnter grid dimentions >...")
dimX = int(input("Enter X dim: "))
dimY = int(input("Enter Y dim: "))


objRec.dimGX = dimX
objRec.dimGY = dimY


#robots=[[1,1,'R',1]]
robots=[]

dropZones = [[1,3,'#'],[1,1,'#']]
deadDrops = []


goodObjects = []
badObjects = []


grid = []
objectGrid = []
gridBlank = []
gridBuild = []


# used to store route
createRoute = []
path_error = False


# place object on grid
def place(item):
    # Grid coordinates have to go Y,X not X,Y. Origin has to be moved due to grid labels
    gridBuild[(dimY)-item[1]][item[0]] = item[2]
    objectGrid[(dimY)-item[1]][item[0]] = item[2]

# add objects from list
def addObjects(items):
    for item in items:
        place(item)


# Displays lists fo good and bad objects
def displayLists():
    # print list of objects detected
    print("\n\nDETECTED OBJECTS: ")
    # orange objects
    print("\nCAT A (Good) Objects")
    for goodObject in goodObjects: 
        print(goodObject)
    # purple objects
    print("\nCAT B (Purple) Objects")
    for badObject in badObjects:
        print(badObject)


# clears old objects from the lists
def clearObjectLists():
    goodObjects = []
    badObjects = []
    objRec.objectsOrange = []
    objRec.objectsPurple = []


# Convert origin point to gridding software standard
def convertOriginPoint():
    # Get updated list
    goodObjects = objRec.objectsOrange
    badObjects = objRec.objectsPurple

    # Corrent origin point   
    if (len(goodObjects) > 0):
        for i in range(0, len(goodObjects)): 
            goodObjects[i][1] = dimY  - goodObjects[i][1] # correct Y
            goodObjects[i][0] = goodObjects[i][0] + 1 # correct X
    if (len(badObjects) > 0):
        for i in range(0, len(badObjects)): 
            badObjects[i][1] = dimY  - badObjects[i][1] # correct Y
            badObjects[i][0] = badObjects[i][0] + 1 # correct X
            

def dispGrid():
    # print("")
    # print("Main Grid")
    # print("---------")
    # print("")
    for i in range(0,dimY+2): # plus 2 duw to bottom axis labels
        print(' '.join(gridBuild[i]))
        #print(gridBuild[i])


def dispObjects():
    print("")
    print("Object Overview")
    print("---------------")
    print("")
    for i in range(0,dimY+2): # plus 2 duw to bottom axis labels
        print(' '.join(objectGrid[i]))
        #print(gridBuild[i])


def genGrid():
    # For every row
    for i in range(0,dimY):
            buffY = [] # clear buffer
            rowName = hex(dimY-i).lstrip("0x") # get name in HEX form
            buffY.append('|'+rowName+'|') # add header
            # Make each column
            for i in range(0,dimX):
                    buffY.append(' ') # add an column element
                    
            buffY.append('|'+rowName+'|') # add terminator
            # add buffer row into actual rows
            gridBuild.append(buffY)
            objectGrid.append(buffY)
            
    # add bottom row
    bottomBuffA = ['---']
    bottomBuffB = ['  ']
    for i in range(0,dimX+1):
        colName = hex(i).lstrip("0x") # get name in HEX form
        bottomBuffA.append('-')
        bottomBuffB.append(''+colName+'')
    bottomBuffA.append('---')
    bottomBuffB.append('   ')

    # add bottom row to grid list
    gridBuild.append(bottomBuffA)
    gridBuild.append(bottomBuffB)
    objectGrid.append(bottomBuffA)
    objectGrid.append(bottomBuffB)

    grid = gridBuild


# route path - x first
def routeX(robot,item,num,action):
    grid = gridBuild
    path_error = False

    xDiff = robot[0] - item[0]
    routeBuf = []
    # place on x
    if(item[0] > robot[0]):
        for i in (range(robot[0], item[0])):
            i=i+1
            if grid[dimX-robot[1]][i] not in [robot[3], robot[2], 'A', 'B', 'X', '#']: # if another char present
                grid[dimX-robot[1]][i] = str(num)
                routeBuf.append([i,robot[1],num,1])
                #dispGrid()
                #input("1")
            else:
                path_error = True


            # ---- DIAG ----
            print("----DIAG---- ( X: i>R )")
            print("I: ", i)
            print("routeBuff.append(",[i,robot[1],num,1],")")
            print("path_error: ", path_error)
            print("routeBuff: ", routeBuf)
            # ---- DIAG ----
    else:
        for i in reversed(range(item[0], robot[0])):
            if grid[dimX-robot[1]][i] not in [robot[3], robot[2], 'A', 'B', 'X', '#']: # if another char present
                grid[dimX-robot[1]][i] = str(num)
                routeBuf.append([i,robot[1],num,1])
                #dispGrid()
                #input()
            else:
                path_error = True
        
            # ---- DIAG ----
            print("----DIAG---- ( X: i<R )")
            print("I: ", i)
            print("routeBuff.append(",[i,robot[1],num,1],")")
            print("path_error: ", path_error)
            print("routeBuff: ", routeBuf)
            # ---- DIAG ----
            
    # place on y
    if(item[1] < robot[1]):
        for i in reversed(range(item[1], robot[1])):
            if grid[dimX-robot[1]][i] not in [robot[3], robot[2], 'A', 'B', 'X', '#']: # if another char present
                grid[dimX-i][item[0]] = str(num)
                routeBuf.append([item[0],i,num,1])
                #dispGrid()
            else:
                path_error = True

            # ---- DIAG ----
            print("----DIAG---- ( Y: i<R )")
            print("I: ", i)
            print("routeBuff.append(",[item[0],i,num,1],")")
            print("path_error: ", path_error)
            print("routeBuff: ", routeBuf)
            # ---- DIAG ----
                
    else:
        for i in range(robot[1], item[1]):
            #i=i+1
            if grid[dimX-robot[1]][i] not in [robot[3], robot[2], 'A', 'B', 'X', '#']: # if another char present

                grid[dimX-i][item[0]] = str(num)
                routeBuf.append([item[0],i,num,1])
                #dispGrid()
                #input()
                #input("1")
            else:
                path_error = True


            # ---- DIAG ----
            print("----DIAG---- ( Y: i>R )")
            print("I: ", i)
            print("routeBuff.append(",[item[0],i,num,1],")")
            print("path_error: ", path_error)
            print("routeBuff: ", routeBuf)
            # ---- DIAG ----

    # add last command        
    routeBuf.append([item[0],item[1],num,action]) # add action for destination

    if path_error == True:
        routeBuf.clear()

    return routeBuf



def routeY(robot,item,num,action):
    grid = gridBuild
    path_error = False

    xDiff = robot[0] - item[0]
    routeBuf = []

    # place on y
    if(item[1] < robot[1]):
        for i in reversed(range(item[1], robot[1])):
            if grid[dimX-robot[1]][i] not in [robot[3], robot[2], 'A', 'B', 'X', '#']: # if another char present
                grid[dimX-i][item[0]] = str(num)
                routeBuf.append([item[0],i,num,1])
                #dispGrid()
                
    else:
        for i in range(robot[1], item[1]):
            i=i+1
            if grid[dimX-robot[1]][i] not in [robot[3], robot[2], 'A', 'B', 'X', '#']: # if another char present

                grid[dimX-i][item[0]] = str(num)
                routeBuf.append([item[0],i,num,1])
                #dispGrid()
                #input()
                #input("1")

    
    # place on x
    if(item[0] > robot[0]):
        for i in (range(robot[0], item[0])):
            i=i+1
            if grid[dimX-robot[1]][i] not in [robot[3], robot[2], 'A', 'B', 'X', '#']: # if another char present
                grid[dimX-robot[1]][i] = str(num)
                routeBuf.append([i,robot[1],num,1])
                #dispGrid()
                #input("1")
    else:
        for i in reversed(range(item[0], robot[0])):
            if grid[dimX-robot[1]][i] not in [robot[3], robot[2], 'A', 'B', 'X', '#']: # if another char present
                grid[dimX-robot[1]][i] = str(num)
                routeBuf.append([i,robot[1],num,1])
                #dispGrid()
                #input()
        
            
    routeBuf.append([item[0],item[1],num,action]) # add action for destination

    #if path_error == True:
        #routeBuf = []

    return routeBuf



# # set up robot position
# RM.selectedRobot["Xr"] = 1
# RM.selectedRobot["Xy"] = 1
# RM.selectedRobot["Payload"] = False
# robots[0][0] = 1
# robots[0][1] = 1

# # intialise robot connection
# print("\n\nInitialising Robot Connection (RM-1)")
# RM.serverAdress = ('192.168.0.200', 4032) # adress of robot 1
# RM.initRobot()



# # set up robot position
# RM2.selectedRobot["Xr"] = 1
# RM2.selectedRobot["Xy"] = 2
# RM2.selectedRobot["Payload"] = False
# robots[0][0] = 1
# robots[0][1] = 2 
# # intialise robot connection
# print("\n\nInitialising Robot Connection (RM-2)")
# RM2.serverAdress = ('192.168.0.201', 4132) # adress of robot 2
# RM2.initRobot()


# find all avaliable robots on netowrk
RM.searchAvalability()

# diplsay found robots
RM.dispAvaliability()
input("\nPress ENTER to continue...")


# add robots to the fleet
print ("\n\n")
print ("ADDING ROBOTS TO FLEET")
print ("----------------------")
RM.addToFleet()
input("\nPress ENTER to continue...")


# configure robots
RM.updateRobotConfig()
input("\nPress ENTER to continue...")


# add robot coordiantes to system grid
def initGridRobots():
    global robots
    print("")
    print("Adding Robots To Grid Memory")
    print("----------------------------")
    robots = [] # clear robots lists

    # for each robot, update
    for robot in RM.robotsList:
        robotX = robot["Xr"]
        robotY = robot["Yr"]
        robotType = robot["Type"]
        robotID = robot["ID"]
        bufferRobot = [robotX,robotY,robotType,robotID]
        print("Adding Robot : ", bufferRobot)
        robots.append(bufferRobot) # add robot to memory
        createRoute.append([]) # add index to store future route (path)

    # display robots in memory
    print("Robots Memory (Robot Manager):\n")
    print(RM.robotsList)
    print("Robots Memory (Grid):\n")
    print(robots)


# add robots to grid system memory
initGridRobots()
print("\n\n\n\n<WARNING> Entering AUTOMATIC MANAGMENT")
input("\n\n\nPress ENTER to continue to \n\tSYSTEM RUN (AUTO)...")

# run main loop
while(True):
    # clear old objects from lists
    clearObjectLists()
    
    # scane test area for obejcts
    print("\nTaking automated image samples")
    goodObjects,badObjects = objRec.takeAnalysedSamples()

    # Convert origin point to that required for gridding software
    displayLists()
    convertOriginPoint()
    
    # Displays lists fo good and bad objects
    displayLists()
    

    ##input("\nPress ENTER to continue to AUTOMATIC MANAGMENT...")
    time.sleep(2)

    gridBuild = []
    objectGrid = []
    objectGrid.clear()

    genGrid()

    addObjects(goodObjects)
    addObjects(badObjects)
    addObjects(dropZones)
    addObjects(robots)  # make sure that robots are on top


    print("\n\nDiscovered Objects")
    print("------------------\n")
    dispGrid()
    time.sleep(2)

    # controll each robot in fleet
    for i in range(0,len(RM.robotsList)):

        RM.selectedRobot = dict(RM.robotsList[i]) 


        gridBuild = []
        objectGrid = []
        objectGrid.clear()

        genGrid()


        addObjects(goodObjects)
        addObjects(badObjects)
        addObjects(dropZones)
        addObjects(deadDrops)
        addObjects(robots)  # make sure that robots are on top

        #objectGrid = gridBuild[:] # make duplicate of grid (no path)

        # object selection 
        #------------------
        try:
            if RM.selectedRobot["Type"] == "R":
                objectToCollect = goodObjects[0]
            else:
                objectToCollect = badObjects[0]
        # If an error occured   
        except Exception as e:
            print("Cannot give robot an object...")


        # path generation
        #-----------------
        print("")
        print ("Path Generation")
        print ("---------------")
        try:
            # checking if carrying payload
            if RM.selectedRobot["Payload"] == False: # if robot DOES NOT have payload
                action = 2 # Pick-Up
                print ("Robot : ", robots[i])
                print ("Object : ", objectToCollect)
                createRoute[i] = routeX(robots[i],objectToCollect,robots[i][3], action) # create path to object
                if createRoute[i] == []:
                    createRoute[i] = routeY(robots[i],objectToCollect,robots[i][3], action) # create path to object
                if createRoute[i] == []:
                    print("No Path Avaliable")

            else: # robot has payload
                action = 3 # Drop-Off
                print ("Robot : ", robots[i])
                print ("Object : ", objectToCollect)
                createRoute[i] = routeX(robots[i],dropZones[0],robots[i][3], action) # create path to drop zone
                if createRoute[i] == []:
                    createRoute[i] = routeY(robots[i],dropZones[0],robots[i][3], action) # create path to drop zone
                if createRoute[i] == []:
                    print("No Path Avaliable")

        # If an error occured   
        except Exception as e:
            print("Cannot create route for robot...")
            

        

        # display grids
        #dispObjects() 
        print("")
        print("Main Grid")
        print("---------")
        print("")     
        dispGrid()

        #ddObjects(robots) # make sure that robots are on top

        #input("\nPress ENTER to continue...")
        time.sleep(1)

        print ("\nCreated Route")
        print(createRoute[i])

        #input("\nPress ENTER to continue...")
        #time.sleep(1)

        # print("Initialising Robot Connection")
        # RM.initRobot()

        #input("\nPress ENTER to continue...")



        # send the first movement
        try:
            print("\nSENDING ROBOT GRID COMMAND")
            x = createRoute[i][0][0]
            y = createRoute[i][0][1]
            action = createRoute[i][0][3]
            RM.sendGrid("3",x,y,action)
            time.sleep(10)
        # If an error occured   
        except Exception as e:
            print("Cannot send path to robot")


        # Updating payload status
        action = createRoute[i][0][3]
        if action == 2: # if picking up object
            RM.selectedRobot["Payload"] = True
        if action == 3: # if drop up object
            RM.selectedRobot["Payload"] = False



        # updating drop of locations
        if action == 3: # if drop up object
            dropZones[0][2] = 'X'
            deadDrops.append(dropZones[0])
            dropZones.remove(dropZones[0])
            


        # update robot variable
        robots[i][0] = x
        robots[i][1] = y

        print("Robot Position >  X:",x," Y:",y)
        #time.sleep(1)

        # update robot list copy of robot
        RM.robotsList[i] = dict(RM.selectedRobot)






