

TestRelations = ["Above","Below","Left","Right"]

currentDirection = 90

desiredDirection = 90

relation = TestRelations[0]

movements = [] # to keep track of robot movements

testNums = 4



def turnRight():
    global currentDirection,movements
    movements.append("Turn-Right")
    currentDirection = currentDirection + 90

def turnLeft():
    global currentDirection,movements
    movements.append("Turn-Left")
    currentDirection = currentDirection - 90





#         N(90)
#          |
# W(0) ----|----E(180)
#          |
#        S(270)

for i in range(0,testNums):

    # reset movement list
    movements.clear()
    
    # get relation for test
    relation = TestRelations[i]

    
    # turn relations into angles
    if relation == "Above":
        desiredDirection = 90
    if relation == "Below":
        desiredDirection = 270
    if relation == "Left":
        desiredDirection = 0
    if relation == "Right":
        desiredDirection = 180

    # error check current direction
    if (currentDirection == 360):
        currentDirection = 0

    # display robot values
    print(f"\nBEFORE: Test direction: {relation}, Current direction: {currentDirection}, Desired direction {desiredDirection}")


    # check what direcvtion the robot needs to turn
    while(currentDirection != desiredDirection): # while robot direction not at desired
        # display robot values
        print(f"DURING: Current direction: {currentDirection}, Desired direction {desiredDirection}")
        if currentDirection < desiredDirection: # if desires is more, turn clockwise
            turnRight() 
        if currentDirection > desiredDirection: # if desires is less, turn anti-clockwise
            turnLeft() 

    # display robot values
    print(f"\nAFTER: Test direction: {relation}, Current direction: {currentDirection}, Desired direction {desiredDirection}")


    # display movements calculated
    print("\n\nCalculated Movements: ")
    for movement in movements:
        print(movement)

    input("Press 'Enter' To Continue...")



    


