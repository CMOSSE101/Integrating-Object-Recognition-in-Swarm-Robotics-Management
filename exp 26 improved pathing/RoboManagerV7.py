
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

serverAdress = ('192.168.0.200', 4032) # adress of server

s = socket(AF_INET, SOCK_DGRAM) # set up UDP socket
s.settimeout(4) # timout setting 1 sec 

#data = ''
recieved = False


# Robots in memory
robotsList = []

# action robot to do when given location
action = 0

# robot buffer with defualt values
robotBuff = {
    "ID" : 0,
    "Mode" : "X",
    "Xr" : 4,
    "Yr" : 4,
    "Direction" : "X",
    "Type" : "X",
    "IP" : "192.168.0.200",
    "Payload" : False,
    "Status" : "OFFLINE",
    "Connected" : False
}

robotsList.append(robotBuff)

# current selected robot in memory
selectedRobot = {
    "ID" : 0,
    "Mode" : "X",
    "Xr" : 4,
    "Yr" : 4,
    "Direction" : "X",
    "Type" : "X",
    "IP" : "192.168.XXX.XXX",
    "Payload" : False,
    "Status" : "OFFLINE",
    "Connected" : False
}


# Connection Check
def checkConnection():
        request = "<" + "X" + ">" # send mode of 'X' (Connection Check)
        requestSender(request,"VERIFIED")
        return recieved # return status of if any reply messages were recived


# Check robot status
def statusCheck():
        # build request
        # send request,checking
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
	

def requestSender(request, status):
	# clearing attempts variables
	global recieved
	#recieved = not recieved # true = receive expected
	recieved = False


	attempts = 0 # amount of attempts
	# try send up to three attempts (expecting responce)
	while((recieved == False ) & (attempts < 3)):
		attempts += 1
		# try read data responce
		try:
			print("<COMMS> Sending : ",request, " Attempt : ", attempts)
			s.sendto(request.encode(), serverAdress) # request to server
			responce, addr = s.recvfrom(2048) #Read whole responce
			print("Responce : ",responce)
			time.sleep(2) # small delay
			recieved = True
			# change robot status
			selectedRobot["Status"] = status
			
		except:
			pass
		time.sleep(2) # small delay
	# report issue of detected
	if (attempts > 2):
		print("\n\tMessage failed after 3 attempts\n")






# only if program rundirect
if __name__ == "__main__":
        print("Run as Main")
        input("Press Enter To Proceed")
        ipCorrect = False
        while True:
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

                #print("\n\nSending Robot Grid Destination Grid Position")
                #sendGrid("3",5,4)


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



