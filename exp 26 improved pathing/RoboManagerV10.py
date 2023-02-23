
# syntax for robot command (EXAMPLE)
#       current
#          |     Dest
#          |       |    +-Steps
# <Mode>[Xr:Yr]{Xd:Yd}(Xr,Yr,Zr)


# ROBOT COMMANDS
#----------------

# robot set up
# <Mode>#ID[Xr,Yr]{Direction}(Type)

# Grid Controll
# <Mode>{Dx:Dy}[Action]

# Manual Controll
# <Mode>{Direction}[Steps]

# Connection Check
# <Mode>

# Check Status
# <Mode> -> Replies <status>


# Modes
# X. Connection Check
# 0. Robot Initialise
# 1. Normal Operation
# 2. Manual Controll
# 3. Grid Controll
# 4. Robot Test
# 5. Status Update

# Direction
# (N)orth
# (E)ast
# (S)outh
# (W)est

# Type
# (C)ollector
# (R)emover



from socket import *
import time

# serverAdress = ('192.168.0.200', 4032) # adress of server


############# Set-Up Socket ############# Start #############
serverAdress_R1 = ('192.168.0.201', 4031) # adress of server
serverAdress_R2 = ('192.168.0.202', 4032) # adress of server
serverAdress_R3 = ('192.168.0.203', 4033) # adress of server
serverAdress_R4 = ('192.168.0.204', 4034) # adress of server

s_R1 = socket(AF_INET, SOCK_DGRAM) # set up UDP socket
s_R2 = socket(AF_INET, SOCK_DGRAM) # set up UDP socket
s_R3 = socket(AF_INET, SOCK_DGRAM) # set up UDP socket
s_R4 = socket(AF_INET, SOCK_DGRAM) # set up UDP socket

s_R1.settimeout(2) # timout setting 1 sec 
s_R2.settimeout(2) # timout setting 1 sec 
s_R3.settimeout(2) # timout setting 1 sec 
s_R4.settimeout(2) # timout setting 1 sec 
############# Set-Up Socket ############# End #############

#data = ''
recieved = False
robotResponce = None


# Robots in memory
robotsList = []
avalabilityList = []

robotsListIDs = []

# action robot to do when given location
action = 0

# robot buffer with defualt values
robotBuff = {
    "ID" : 1,
    "Mode" : "C",
    "Xr" : 1,
    "Yr" : 1,
    "Direction" : "X",
    "Type" : "X",
    "IP" : "192.168.0.200", # defualt
    "Port" : 4032, # defualt
    "Socket" : s_R1, # defualt
    "Payload" : False,
    "Status" : "OFFLINE",
    "Connected" : False
}

#robotsList.append(robotBuff)

# current selected robot in memory
selectedRobot = {
    "ID" : 1,
    "Mode" : "C",
    "Xr" : 1,
    "Yr" : 1,
    "Direction" : "X",
    "Type" : "X",
    "IP" : "192.168.XXX.XXX", # defualt
    "Port" : 4032, # defualt
    "Socket" : s_R1, # defualt
    "Payload" : False,
    "Status" : "OFFLINE",
    "Connected" : False
    
}



# finds active robots on network and adds them to the availability list
def searchAvalability():
    #selectedRobot = robotBuff # initialise selected robot
    counter_ID = 1 # initialise counter ID value

    #print(avalabilityList)
    print("")
    print("SEARCHIGN FOR ROBOTS ON KNOWN CONNECTIONS (Reserved)")
    print("----------------------------------------------------")

    selectedRobot["IP"] = serverAdress_R1[0]
    selectedRobot["Port"] = serverAdress_R1[1]
    selectedRobot["Socket"] = s_R1
    #print(selectedRobot["IP"])
    print("\nSearching on IP:",serverAdress_R1[0]," Port:",serverAdress_R1[1])
    if checkConnection():
        selectedRobot["ID"] = counter_ID
        buffer_robot = dict(selectedRobot)
        avalabilityList.append(buffer_robot)
        counter_ID +=1

    #print(avalabilityList)

    selectedRobot["IP"] = serverAdress_R2[0]
    selectedRobot["Port"] = serverAdress_R2[1]
    selectedRobot["Socket"] = s_R2
    print("\nSearching on IP:",serverAdress_R2[0]," Port:",serverAdress_R2[1])
    if checkConnection():
        selectedRobot["ID"] = counter_ID
        buffer_robot = dict(selectedRobot)
        avalabilityList.append(buffer_robot)
        counter_ID +=1

    

def dispAvaliability():
    # display length of availability list
    print("\n\nRobots discovered : ", len(avalabilityList))

    # display all avaliable robots in a table
    print("")
    print("      Availability List       ")
    print("      -----------------       ")
    print("|Num--|ID-|IP----------------|")
    print("|=====|===|==================|")

    if len(avalabilityList) > 0:
        for i in range(len(avalabilityList)):
            print("| #",i+1,"|",avalabilityList[i]["ID"],"| ",avalabilityList[i]["IP"],"|")
            print("|-----|---|------------------|")
    else:
        print("No robots avaliable...")


def dispFleet():
    # display length of robot list
    print("\n\nRobots in fleet : ", len(robotsList))

    # display all robots in fleet in table
    print("")
    print("         Fleet List       ")
    print("         ----------       ")
    print("|Num--|ID-|IP----------------|")
    print("|=====|===|==================|")

    if len(robotsList) > 0:
        for i in range(len(robotsList)):
            print("| #",i+1,"|",robotsList[i]["ID"],"| ",robotsList[i]["IP"],"|")
            print("|-----|---|------------------|")
    else:
        print("No robots in fleet...")



# Adds selected robots to the fleet (robotsList)
def addToFleet():
    robotsChosen = False
    while robotsChosen == False: # repeat until successfull

        # display avalable and feeted robots
        dispAvaliability()
        dispFleet()

        # add robots to fleet
        try: # check that a number was passed
            robotChoice = int(input("\nEnter a robot 'Num' to add to fleet (0 to exit)>... "))
            robotsChosen = False

            # check if in range
            if robotChoice > 0:
                if robotChoice <= len(avalabilityList):
                    
                    # check robot not already in list
                    if avalabilityList[robotChoice-1]["ID"] not in robotsListIDs:
                        robotsList.append(avalabilityList[robotChoice-1]) # add robot to fleet
                        robotsListIDs.append(avalabilityList[robotChoice-1]["ID"]) # add ID to ID's list
                        print("Robot Added...")
                    else:
                        print("Robot already in fleet...")

            else: # all robots chosen
                robotsChosen = True

        except Exception as e:
            print("\nInvalid 'Num' Value Entered (Ensure Number Presented) >... ")



# configure the robots in the fleet
def updateRobotConfig():
    global selectedRobot

    for robot in robotsList: # for each robot
        print ("\n\n")
        print ("ROBOT CONFIGURATION")
        print ("-------------------")


        try:
            # Display robot identification
            print("")
            print("Robot ID : ", robot["ID"])
            print("Robot IP : ", robot["IP"])



            # Get type of robot
            #------------------
            roboType = " "
            while (roboType not in ('R','C')): # make sure input is valid
                roboType = input("\nEnter type of robot (Collector/Remover) <C/R> >... ")
            robot["Type"] = roboType

            # Get robot coordinates
            #----------------------
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

            # Update coordinates
            robot["Xr"] = roboX
            robot["Yr"] = roboY

            # Get robot compas direction
            #---------------------------
            compassDirection=' '
            while (compassDirection not in ('N','E','S','W')): # make sure input is valid
                print("\nEnter closest robot compas direction")
                compassDirection = input(" (N,E,S,W) >... ")

            # Update robot compas direction
            robot["Direction"] = compassDirection



            # Send initiation message to robot
            #---------------------------------
            print("\n")
            print("Sending CONFIG data to robot")
            print("----------------------------\n")
            
            # select robot
            print("Entered robot configuration:")
            print(robot)
            selectedRobot = dict(robot)
            # print("Configration to be sent:")
            # print(selectedRobot)
            # send intiiataion message
            initRobot()

        # If an error occured   
        except Exception as e:
            # Show error message and try again
            print("ROBOT FAILED TO UPDATE")
            print(e)



# Connection Check
def checkConnection():
        request = "<" + "X" + ">" # send mode of 'X' (Connection Check)
        requestSender(request,"VERIFIED")
        selectedRobot["Connected"] = True
        return recieved # return status of if any reply messages were recived


# Check robot status
def statusCheck():
        # build request
        request = "<" + str(5) + ">"
        # send request,checking
        requestSender(request,"Checking")

        print("Robot Responce", robotResponce)
        # if responce = "idle"
        print("\n\tRobot At Destination")
        selectedRobot["Status"] = "IDLE"
              


# contructs robot grid movement message
def sendGrid(mode,Xd,Yd,action):
	# <Mode>{Xd,Yd}
	# building request to send
	request = "<" + str(mode) + ">"
	request += "{" + str(Xd) + "," + str(Yd) + "}"
	request += "[" + str(action) + "]"
	requestSender(request,"MOBILE")


# contructs robot settings value message
def sendSetup(mode,ID,Xr,Yr,Direction,Type):
	# <Mode>[Xr,Yr]{Direction}(Type)<ID>
	# building request to send
	request = "<" + str(mode) + ">"
	request += "#" + str(ID)
	request += "[" + str(Xr) + "," + str(Yr) + "]"
	request += "{" + Direction + "}"
	request += "(" + Type + ")"
	requestSender(request,"ONLINE")

#def updateResponce(responceLast):
    #a = responceLast
	

def requestSender(request, status):
    # clearing attempts variables
    global recieved, robotResponce
    #recieved = not recieved # true = receive expected
    recieved = False

    # retriving IP and Port
    robotIP = selectedRobot["IP"]
    robotPort = selectedRobot["Port"]
    robotSocket = selectedRobot["Socket"]
    robotAdress = (robotIP,robotPort)


    attempts = 0 # amount of attempts
    # try send up to three attempts (expecting responce)
    while((recieved == False ) & (attempts < 3)):
        attempts += 1
        # try read data responce
        try:
            print("<COMMS> Sending : ",request, " Attempt : ", attempts)
            robotSocket.sendto(request.encode(), robotAdress) # request to server
            responce, addr = robotSocket.recvfrom(2048) #Read whole responce
            
            print("Responce : ",responce)
            #updateResponce(responce)
            robotResponce = responce
            

            time.sleep(2) # small delay
            recieved = True
            # change robot status
            selectedRobot["Status"] = status
			
        except:
            pass

        #time.sleep(2) # small delay
        # report issue of detected
        if (attempts > 2):
            print("\n\tMessage failed after 3 attempts\n")


    time.sleep(10)



def initRobot():
    global selectedRobot
    # display configuration details being sent
    print("Configration to be sent:")
    print(selectedRobot)

    ipCorrect = False
    while ipCorrect == False:
        print("\n\nCheching connection to robot (Verify IP)")
        ipCorrect = checkConnection()

        # print status of connection attempt
        if ipCorrect:
            print("\n\nIP Verified")
        else:
            print("\n\nIP  --NOT--  Verified")

        time.sleep(2)

    print("\n\nSending Robot Config Settings")
    #mode = selectedRobot["Mode"]
    id = selectedRobot["ID"]
    x = selectedRobot["Xr"]
    y = selectedRobot["Yr"]
    direction = selectedRobot["Direction"]
    roboType = selectedRobot["Type"]

    #sendSetup("0",1,1,1,"X","X")
    sendSetup(0,id,x,y,direction,roboType)
    #input("Press Enter To Send Next Message")
    time.sleep(1)


# only if program rundirect
if __name__ == "__main__":
        print("Run as Main")
        input("Press Enter To Proceed")
        ipCorrect = False
        while True:

            # check that IP is valid / exists on network
            while ipCorrect == False:
                print("\n\nChecking to see if connection to robot can be made (Verify IP)")
                ipCorrect = checkConnection()

                # print status of connection attempt
                if ipCorrect:
                    print("\n\nIP Verified")
                else:
                    print("\n\nIP  --NOT--  Verified")

                input("Press Enter To Proceed")

            print("\n\nSending Robot Config Settings")
            sendSetup("0",3,4,4,"X","X")
            input("Press Enter To Send Next Message")

            while True:
                print("\n\nSending robot to custom grid location")
                try:
                    # get input
                    x = int(input("Enter grid X: "))
                    y = int(input("Enter grid Y: "))
                    
                    # get action (do while style)
                    action = 0
                    while (action not in [1,2,3]):
                                    action = int(input("Enter an Action (1: Go-To, 2: Pick-Up, 3: Drop-Off) > "))

                    # send to robot
                    sendGrid("3",x,y,action)
                except:
                    break


            input("\n\nEND OF PROGRAM (Any Key To Repeat)")



