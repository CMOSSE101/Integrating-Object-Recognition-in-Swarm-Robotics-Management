
import time

# grid
grid = [['|A|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|A|'],
        ['|9|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|9|'],
        ['|8|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|8|'],
        ['|7|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|7|'],
        ['|6|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|6|'],
        ['|5|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|5|'],
        ['|4|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|4|'],
        ['|3|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|3|'],
        ['|2|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|2|'],
        ['|1|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|1|'],
        ['---','-','-','-','-','-','-','-','-','-','-','---'],
        ['   ','1','2','3','4','5','6','7','8','9','A','   ']]

gridBlank = [['|A|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|A|'],
        ['|9|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|9|'],
        ['|8|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|8|'],
        ['|7|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|7|'],
        ['|6|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|6|'],
        ['|5|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|5|'],
        ['|4|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|4|'],
        ['|3|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|3|'],
        ['|2|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|2|'],
        ['|1|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|1|'],
        ['---','-','-','-','-','-','-','-','-','-','-','---'],
        ['   ','1','2','3','4','5','6','7','8','9','A','   ']]

# Initial Placments
robots = [[9,9,'R', 1],
          [2,2,'C', 2]]

bads = [[3,4,'B'],
        [5,8,'B']]

goods = [[5,3,'G'],
         [9,7,'G']]

objects_Bad = []
objects_Good = []
objectsBuf_1 = []
createRoute_1 = []
objectsBuf_2 = []
createRoute_2 = []

objectsBuf = [[],
              []]

createRoute = [[],[]]

print("CreateRoute : ",createRoute)


# Displaying grid function
def dispGrid():
    for i in range(0,12):
        #print(grid[i])
        #disp[i]=
        print(' '.join(grid[i]))


# place object on grid
def place(item):
    grid[10-item[1]][item[0]] = item[2]


# add objects from list
def addObjects(items):
    for item in items:
        place(item)


# calculate disctance
def distance(robot,item):
    dist = abs(robot[0] - item[0]) + (2 * (abs(robot[1] - item[1])))
    buffer = [item[0],item[1],item[2], dist]
    return buffer

    
# order buffer list
def sortObjects():
    global objects_Bad
    global objects_Good
    global objectsBuf_1
    global objectsBuf_2
    global objectsBuf
    distanceScores1 = []
    distanceScores2 = []

    # get distance scores
    for obj in objectsBuf_1:
        distanceScores1.append(obj[3])
    for obj in objectsBuf_2:
        distanceScores2.append(obj[3])
    
    # sort scores in size order
##    distanceScores1.sort()
##    print(distanceScores1)
##    distanceScores2.sort()
##    print(distanceScores2)

    # Save array in buffer array
    objectsBuf_1 = objectsBuf[0]
    objectsBuf_2 = objectsBuf[1]
    
    # add objects in object list in order
    objects_Bad = sorted(objectsBuf_1, key=lambda objectsBuf_1:objectsBuf_1[3])
    objects_Good = sorted(objectsBuf_2, key=lambda objectsBuf_2:objectsBuf_2[3])
    

# route path - x first
def routeX(robot,item,num):
    xDiff = robot[0] - item[0]
    routeBuf = []
    # place on x
    if(item[0] > robot[0]):
        for i in (range(robot[0], item[0])):
            i=i+1
            if grid[10-robot[1]][i] not in [robot[3], robot[2]]: # if another char present
                grid[10-robot[1]][i] = str(num)
                routeBuf.append([i,robot[1],num])
                #dispGrid()
                #input("1")
    else:
        for i in reversed(range(item[0], robot[0])):
            if grid[10-robot[1]][i] not in [robot[3], robot[2]]: # if another char present
                grid[10-robot[1]][i] = str(num)
                routeBuf.append([i,robot[1],num])
                #dispGrid()
                #input()
        
            
    # place on y
    if(item[1] < robot[1]):
        for i in reversed(range(robot[1], item[1])):
            if grid[10-robot[1]][i] not in [robot[3], robot[2]]: # if another char present
                grid[10-i][item[0]] = str(num)
                routeBuf.append([item[0],i,num])
                #dispGrid()
                #input()
    else:
        for i in reversed(range(item[1], robot[1])):
            if grid[10-robot[1]][i] not in [robot[3], robot[2]]: # if another char present

                grid[10-i][item[0]] = str(num)
                routeBuf.append([item[0],i,num])
                #dispGrid()
                #input()
            
    return routeBuf


# route path - y first
def routeY(robot,item,num):
    xDiff = robot[0] - item[0]
    routeBuf = []

    # place on y
    if(item[1] > robot[1]):
        for i in reversed(range(robot[1], item[1])):
            #if grid[10-i][item[0]] != str(robot[3]): # if another char present
            grid[10-i][robot[0]] = str(num)
            routeBuf.append([robot[0],i,num])
            #dispGrid()
            #input()
    else:
        for i in reversed(range(item[1], robot[1])):
            #if grid[10-i][item[0]] != str(robot[3]): # if another char present
            grid[10-i][robot[0]] = str(num)
            routeBuf.append([robot[0],i,num])
            #dispGrid()
            #input()
    
    # place on x
    if(item[0] > robot[0]):
        for i in reversed(range(robot[0], item[0])):
            #if grid[10-robot[1]][i] != str(robot[3]): # if another char present
            grid[10-item[1]][i] = str(num)
            routeBuf.append([i,item[1],num])
            #dispGrid()
            #input()
    else:
        for i in reversed(range(item[0], robot[0])):
            #i = i+1
            #if grid[10-robot[1]][i] != str(robot[3]): # if another char present
            grid[10-item[1]][i] = str(num)
            routeBuf.append([i,item[1],num])
            #dispGrid()
            #input()
            
    return routeBuf

    
# move on route
def moveRoute(robot, movement):
    grid[10-robot[1]][robot[0]] = str(' ') # remove object from current dest
    robot[0] = movement[0]
    robot[1] = movement[1]
    #grid[10-robot[1]][robot[0]] = str(robot[2]) # remove object from current dest
    return robot

# MAIN FUNCTION
while(True):
    objects_Bad.clear()
    objects_Good.clear()
    objectsBuf[0].clear()
    objectsBuf[1].clear()
    createRoute[0].clear()
    createRoute[1].clear()

    # Add objects to grid
    addObjects(robots)
    addObjects(bads)
    addObjects(goods)

    # update screen
    print("\n\n\n\n\n\n\n\n")
    print("        LAST STEP")
    dispGrid()
    print("\n")

    print("Bads : ", bads)
    print("Goods : ", goods)
    for i in range(0,len(bads)):
        #print(robots[0])
        #print(bads[i])
        objectsBuf[0].append(distance(robots[0], bads[i]))
    for i in range(0,len(goods)):
        objectsBuf[1].append(distance(robots[1], goods[i]))

    print("Object buffer 1 ",objectsBuf[0])
    print("Object buffer 2 ",objectsBuf[1])
    sortObjects()
    print("Sorted objects 1 ",objectsBuf[0])
    print("Sorted objects 2 ",objectsBuf[1])

    #objectsBuf[0] = objects_Bad
    #objectsBuf[1] = objects_Good
    print("robots[0] ", robots[0])
    print("objects_Bad[0] ", objects_Bad[0])
    print("robots[0][3] ", robots[0][3])

    # create routes
    createRoute[0] = routeX(robots[0],objects_Bad[0],robots[0][3])
    if not createRoute[0]: # check if empty (Failed route)
        print("no valid paths or finished")
    createRoute[1] = routeX(robots[1],objects_Good[0],robots[1][3])
    if not createRoute[1]: # check if empty (Failed route)
        print("no valid paths or finished")
        

    print("Created route 1 ",createRoute[0])
    print("Created route 2 ",createRoute[1])
    print("Steps route 1 : ", len(createRoute[0]))
    print("Steps route 2 : ", len(createRoute[1]))
    

    # update screen
    print("\n")
    print("        NEXT STEP")
    dispGrid()
    print("\n")

    # Display route (Bad)
    for movement in createRoute[0]:
        print("Robot X :",robots[0][0]," Robot Y: ",robots[0][1])
        robots[0] = moveRoute(robots[0],movement)
        print("Robot X :",robots[0][0]," Robot Y: ",robots[0][1])
        break

    # Display route (Good)
    for movement in createRoute[1]:
        print("Robot X :",robots[1][0]," Robot Y: ",robots[1][1])
        robots[1] = moveRoute(robots[1],movement)
        print("Robot X :",robots[1][0]," Robot Y: ",robots[1][1])
        break
    
    # end of main loop
    time.sleep(1)
    input("Cont...")
    grid = gridBlank
    
