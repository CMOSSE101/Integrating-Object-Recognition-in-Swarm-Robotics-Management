

# Libraries
#------------------
import time # for delays
#import roboManualControlv1 as roboComms
import RoboManagerV7 as RM


grid = []
gridBlank = []
gridBuild = []

#dimX = int(input("Enter X dim: "))
#dimY = int(input("Enter Y dim: "))

dimX = 1
dimY = 1

movegrid = False

# Notes if a robot selection is required
selectNeeded = False

#buffY = []
#buffX = []

# sudo switch statement using dictionaly
# file name for scanerio choices
choicesDict = {
    1: "scenario_1_5x5.txt",
    2: "scenario_2_10x10.txt",
}




def loadMenu():
    # print program description
    print("\n\n")
    print("|##########|###################|")
    print("| Title:   |   Swarm Gridder   |")
    print("|----------|-------------------|")
    print("| Topic:   |  Robo Grid Move   |")
    print("|----------|-------------------|")
    print("| Version: | 2                 |")
    print("|##########|###################|")
    print("\n\n")
    print ("Program starting is 2 seconds...\n\n")
    time.sleep(2)
    
    # get operation mode from user
    opModeStr = " " # initial value
    opMode = 0 # initial value
    while (opModeStr not in ('1','2','3','4','5')): # make sure answer is acceptable
        # Print menu
        print("\n\n")
        print("|###################################|")
        print("|       Select Operation Method     |")
        print("|###################################|")
        print("|  X  | Normal Operation (Full Sys) |")
        print("|-----|-----------------------------|")
        print("|  1  | Load Existing Scenario      |")
        print("|-----|-----------------------------|")
        print("|  2  | Make Custom Scenario        |")
        print("|-----|-----------------------------|")
        print("|  3  | Robot Manual Controll       |")
        print("|-----|-----------------------------|")
        print("|  4  | Robot Grid Controll         |")
        print("|-----|-----------------------------|")
        print("|  5  | Fleet Setup                 |")
        print("|-----|-----------------------------|")
        print("|  X  | System Test                 |")
        print("|-----|-----------------------------|\n")
        opModeStr = input("Please Select and option >..")
        try:
            opMode = int(opModeStr) # try convert to int number
        except Exception as e:
            print("Please select a valid option \n") # announce invalid input
    return opMode
    


    
def dispGrid():
    print("\n\n")
    for i in range(0,dimY+2): # plus 2 duw to bottom axis labels
        print(' '.join(gridBuild[i]))
        #print(gridBuild[i])


def makeGrid():
    global grid
    print("\n\n")
    # display grid size
    print("Grid Size (",dimX,",",dimY,")\n")
    # For every row7
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
            
    # add bottom row
    bottomBuffA = ['---']
    bottomBuffB = ['  ']
    for i in range(0,dimX):
        colName = hex(i).lstrip("0x") # get name in HEX form
        bottomBuffA.append('-')
        bottomBuffB.append(''+colName+'')
    bottomBuffA.append('---')
    bottomBuffB.append('   ')

    # add bottom row to grid list
    gridBuild.append(bottomBuffA)
    gridBuild.append(bottomBuffB)
    grid = gridBuild
    

def loadFile(chosenFile):
    global dimX, dimY
    f = open(chosenFile, "r")
    # read X dimention value
    dimX = int(f.readline())
    # read Y dimention value
    dimY = int(f.readline())
    f.close()


def createCustomGrid():
    global dimX, dimY
    # display grid image
    print("\n")
    print("Example Grid (4,4)")
    print("     _ _ _ _ ")
    print("    |_|_|_|_|")
    print("Dim |_|_|_|_|")
    print(" Y  |_|_|_|_|")
    print("    |_|_|_|_|")
    print("      Dim X  ")
    dimX = int(input("\nPlease enter value for Dim X >..."))
    dimY = int(input("\nPlease enter value for Dim Y >..."))
   
    
def chooseScenario():
    choiceStr = 0 # initial value

    while (choiceStr not in ('1','2')): # make sure answer is acceptable
        # display option table
        print("\n\n")
        print("        Scenario List      ")
        print("|===|============|========|")
        print("| 1 | Scenario 1 | 5x5    |")
        print("|---|------------|--------|")
        print("| 2 | Scenario 2 | 10x10  |")
        print("|---|------------|--------|")
        print("\n")
        # request answer
        choiceStr = input("Please Select and option >.. ")
    # valid option must have been shosen, convert to int
    choice = int(choiceStr)
    # get file name using choce dictionary
    loadFile(choicesDict[choice])


def manualMove():
    dirStr = ' '
    stepsStr = ' '
    # Display options
    while (dirStr not in ('F','R','B','L')): # make sure answer is acceptable
        print("\n\n")
        print("      F      ")
        print("      |      ")
        print(" L <--|--> R ")
        print("      |      ")
        print("      B      ")
        print("\n COMMAND in form <Direction>:<Steps> E.G. F:1  (Steps 0 - 4)")
        dirStr = input("\nPlease Select A Direction >.. ")
        while (stepsStr not in ('0','1','2','3','4')): # make sure answer is acceptable
            stepsStr = input("\nPlease Select Quantity Of Steps >.. ")
        # convert steps to int form
        steps = int(stepsStr)
        intructBuff = [dirStr,steps] # buffer intruction list
        return intructBuff


# Displays and adds/removes robots from fleet
def fleetDisplay():
    choiceStr = '0' # initial value
    print("\n\n")
    print("         Fleet List       ")
    print("         ----------       ")
    print("|Num--|ID-|IP----------------|")
    print("|=====|===|==================|")

    # Display Robots in system
    robotsListBuff = RM.robotsList
    for i in range(len(robotsListBuff)):
        print("| #",i+1,"|",RM.robotsList[i]["ID"],"| ",RM.robotsList[i]["IP"],"|")
        print("|-----|---|------------------|")

    if len(robotsListBuff) == 0:
        print("\nNo-Valid-Robots-In-Fleet")


    # display option to user
    while (choiceStr not in ('1','2','3')): # check for valid option
        print("\n\n")
        print("          Fleet Options        ")
        print("|===|=========================|")
        print("| 1 | Select Robot From Fleet |")
        print("|---|-------------------------|")
        print("| 2 | Add Robot To Fleet      |")
        print("|---|-------------------------|")
        print("| 3 | Remove Robot From Fleet |")
        print("|===|=========================|")
        print("\n")
        # Get user input
        choiceStr = input("Please Select and option >.. ")
        # if no robot to remove
        if len(robotsListBuff) == 0:
            if choiceStr == '1': # if no robot to remove
                print("\nNo-Valid-Robots-In-Fleet")
                choiceStr = '0'
            if choiceStr == '3': # if no robot to remove
                print("\nNo-Valid-Robots-In-Fleet")
                choiceStr = '0'

    # Convert valid option to int
    choice = int(choiceStr)

    # Go to next area
    if choice == 1:
        if selectNeeded:
            selectRobot()
        else:
            print("\nSelection Not Needed")
    if choice == 2: # choice 2
        addNewRobot() # add new robot
    if choice == 3:
        # if choice 3
        print("Option No Avaliable Yet") ## show option not avalible


# Select a robot to use
def selectRobot():
    choiceStr = '0' # initial value
    print("\n\n")
    print("        Selection List        ")
    print("       ----------------       ")
    print("|Num--|ID-|IP----------------|")
    print("|=====|===|==================|")

    # Display Robots in system
    robotsListBuff = RM.robotsList
    for i in range(len(robotsListBuff)):
        print("| #",i+1,"|",RM.robotsList[i]["ID"],"| ",RM.robotsList[i]["IP"],"|")
        print("|-----|---|------------------|")

    if len(robotsListBuff) == 0:
        print("\nNo-Valid-Robots-In-Fleet")
        input("Press Enter to goto fleet manager")
        fleetDisplay()

    
    robotChosen = False
    while robotChosen == False: # repeat until successfull
        try: # check that a number was passed
            robotChoice = int(input("\nEnter a robot 'Num' to use >... "))
            robotChosen = True
            # check if in range
            if robotChoice > len(robotsListBuff):
                robotChosen = False
        except Exception as e:
            print("\nInvalid 'Num' Value Entered (Ensure Number Presented) >... ")
    
    # store dtails of selected robot
    RM.selectedRobot = RM.robotsList[robotChoice-1]

    print("\nRobot Selected:")
    print(RM.selectedRobot)

    


# Adds robot to fleet
def addNewRobot():
    # Add new data to robot buffer
    #------------------------------
    # Get robot IP
    RM.robotBuff["IP"] = input("Enter Robot IP >...")
    #get robot ID
    idValid = False
    while idValid == False: # repeat until successfull
        try: # check that a number was passed
            # Get robot ID value
            ID = int(input("Enter robot ID >... "))
            idValid = True
        except Exception as e:
            print("Invalid ID Value Entered (Ensure Number Presented)")
    # Store robot ID
    RM.robotBuff["ID"] = ID

    # Get type of robot
    roboType = " "
    while (roboType not in ('R','C')): # make sure input is valid
           roboType = input("\nEnter type of robot (Collector/Remover) <C/R> >... ")
    RM.robotBuff["Type"] = roboType

    #get robot coordinates
    coordsValid = False
    while coordsValid == False: # repeat until successfull
        try: # check that a number was passed
            # Get robot X value
            roboX = int(input("Enter robot X value >... "))
            # Get robot X value
            roboY = int(input("Enter robot Y value >... "))
            coordsValid = True
        except Exception as e:
            print("Invalid Coordinate Valuw Entered (Ensure Number Presented)")

    # Store coordinates
    RM.robotBuff["Xr"] = roboX
    RM.robotBuff["Yr"] = roboY

    # Get robot compas direction
    compassDirection=' '
    while (compassDirection not in ('N','E','S','W')): # make sure input is valid
        print("\nEnter closest robot compas direction")
        compassDirection = input(" (N,E,S,W) >... ")

    # Store robot compas direction
    RM.robotBuff["Direction"] = roboType

    # Add robot to robot list
    try:
        # Add to list
        RM.robotsList.append(RM.robotBuff)
    except Exception as e:
        # Show error message and try again
        print("ROBOT FAILED TO ADD")
        addNewRobot()


    # print sucess message
    print("\n\nROBOT ID:",RM.robotBuff["ID"]," IP:",RM.robotBuff["IP"]," SUCESSFULLY ADDED TO FLEET")
    input("\n\nPress Enter To Continue")
    fleetDisplay()


def checkGridoption(option):
    # check the option is not out of bounds
    global dimX, dimY
    if option[0] <= dimX:
        #print(option[0] <= dimX)
        if option[0] >=0:
            #print(option[0] >=0)
            if option[1] <= dimY:
                #print(option[1] <= dimY)
                if option[1] >=0:
                    #print(option[1] >=0)
                    return True
    return False
    

def manualMoveGrid():
    global dimX, dimY
    dirStr = ' '
    #stepsStr = ' '

    # Get robot x,y
    roboX = 4#RM.selectedRobot["Xr"]
    roboY = 4#RM.selectedRobot["Yr"]

    # Add avaliable movement options to the grid
    option1=[roboX-1,roboY,False]
    option2=[roboX,roboY+1,False]
    option3=[roboX+1,roboY,False]
    option4=[roboX,roboY-1,False]

    option1[2]=checkGridoption(option1)
    option2[2]=checkGridoption(option2)
    option3[2]=checkGridoption(option3)
    option4[2]=checkGridoption(option4)

##    print(dimX, dimY)
##
##    print(roboX)
##    print(roboY)
##
##    print(option1)
##    print(option2)
##    print(option3)
##    print(option4)
##
##    input("")
    
    if option1[2]:
        place([option1[0],option1[1],"1"])
    if option2[2]:
        place([option2[0],option2[1],"2"])
    if option3[2]:
        place([option3[0],option3[1],"3"])
    if option4[2]:
        place([option4[0],option4[1],"4"])

    dispGrid() # displays the grid

    # Print robot status
    print("\n\n")
    print("|ID-|IP----------------|Status---|")
    print("|===|==================|=========|")
    print("|",RM.selectedRobot["ID"],"| ",RM.selectedRobot["IP"],"|",RM.selectedRobot["Status"],"|")
        
    
    # Display options
    optionStr = ' '
    while (optionStr not in ('1','2','3','4')): # make sure answer is acceptable
        print("\n\n")
        if option1[2]:
            print("| option 1 |",option1[0],",",option1[1],"|")
        if option2[2]:
            print("| option 2 |",option2[0],",",option2[1],"|")
        if option3[2]:
            print("| option 3 |",option3[0],",",option3[1],"|")
        if option4[2]:
            print("| option 4 |",option4[0],",",option4[1],"|")
        optionStr = input("\nPlease Select A Option >.. ")
        
    # convert steps to int form
    option = int(optionStr)

    gridToSend = []

    if option == 1:
        if option1[2]:
            gridToSend = option1
    if option == 2:
        if option2[2]:
            gridToSend = option2
    if option == 3:
        if option3[2]:
            gridToSend = option3
    if option == 4:
        if option4[2]:
            gridToSend = option4

    # send requesto to robot
    RM.sendGrid(3,gridToSend[0],gridToSend[1])

    # check if recived
    if RM.recieved == True:
    #if True:
        # wait for robot status to change
        while(RM.selectedRobot["Status"] != "IDLE"):
            # add checkCounter for timeout
            print("Waiting for robot to reach destination")
            time.sleep(2)
            # check status
            RM.statusCheck()
    else:
        print("Robot Did Not Receive Message... Try Again")

    
# place object on grid
def place(item):
    global dimX, dimY
    global grid
    grid[dimY-item[1]][item[0]] = item[2]

def getDestination():
    print("\n")
    # Get robot X value
    destX = int(input("Enter destination X value >... "))
    # Get robot X value
    destY = int(input("Enter destination Y value >... "))
    destBuff = [destX,destY,'X']
    # Display destination details
    print("\nENTERED DESTINATION : ",destBuff)
    return destBuff

    
### get placment of robot manually
##def placeRobotManual():
##    gridBot = [0,0,' ']
##    
##    # Get type of robot
##    roboType = " "
##    while (roboType not in ('R','C')): # make sure input is valid
##           roboType = input("\nEnter type of robot (Collector/Remover) <C/R> >... ")
##    # Get robot X value
##    roboX = int(input("Enter robot X value >... "))
##    # Get robot X value
##    roboY = int(input("Enter robot Y value >... "))
##    # update grid bot buffer
##    gridBot = [roboX,roboY,roboType]
##    # Display robot details
##    print("\nENTERED ROBOT : ",gridBot)
##    # add robot to grid
##    return gridBot


        
# START OF PROGRAM
#------------------
while (True):
    # Reset global grid variables
    grid = []
    gridBlank = []
    gridBuild = []
    

    mode = loadMenu()
    if mode == 1:
        chooseScenario() # load existing grid
        makeGrid() # creates the grid
        gridBlank = gridBuild
        dispGrid() # displays the grid
        
    if mode == 2:
        createCustomGrid() # create custom grid
        makeGrid() # creates the grid
        gridBlank = gridBuild
        dispGrid() # displays the grid
        
    if mode == 4:
        print("\nOperation Mode : Grid Controll")
        createCustomGrid() # create custom grid
        makeGrid() # creates the grid
        
        #gridBlank = gridBuild
        #madeBot = placeRobotManual() # get robot details
        #place(madeBot) # place robot on grid

        # enable robot selection
        selectNeeded = True
        # Select robot
        fleetDisplay()

        # Place selected robot on grid
        gridBotBuff = [RM.selectedRobot["Xr"],RM.selectedRobot["Yr"],RM.selectedRobot["Type"]]    
        place(gridBotBuff)

        dispGrid() # displays the grid
        roboDest = getDestination()
        place(roboDest)
        dispGrid() # displays the grid
        movegrid = True
        while movegrid == True:
            manualMoveGrid()# get robot movement
        
        
    if mode == 3:
        keepRun = "Y"
        while (keepRun == "Y"):
            command = manualMove()
            print("\nCOMMAND ENTERED : ",command) # gets command
            #roboComms.sendReq(command,True)
            RM.sendMove(command,True)
            keepRun = input("\nPress Y to conntinue >.. ")

    if mode == 5:
        fleetDisplay()
        


    # Warn end of prgram has been reached
    print("\n\nPress Enter to return to main menu")
    print("\n        __________________________ ")
    print("WARNING | End Of Program Reached | ")
    input("        ----------<Enter>--------- \n")
    # end of program




