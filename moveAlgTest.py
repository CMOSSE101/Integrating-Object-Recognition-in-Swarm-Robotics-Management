
robotPos = [[2,2],[2,2],[2,2],[2,2]]
objectPos = [[2,3],[2,1],[1,2],[3,2]]
knownAnswers = ["Above","Below","Left","Right"]
testPositions = 4


object_to_robot_global = "centure"

testResult = "PASS" # defualt answer


for i in range(0,testPositions):
    Xr = robotPos[i][0]
    Xd = objectPos[i][0]

    Yr = robotPos[i][1]
    Yd = objectPos[i][1]


    # find placementr of robot (global direction)
    if Yr < Yd: # if object above on Y axis
        object_to_robot_global = "Above"
    elif Yr > Yd: # if object below on Y axis
        object_to_robot_global = "Below"
    else: # if Y axis the same -> check X
        if Xr < Xd: # if object right on X axis
            object_to_robot_global = "Right"
        elif Xr > Xd: # if object left on X axis
            object_to_robot_global = "Left"
        else:
            print("Destination Error -- Robot in destination location")
            
    # display calculated and actual answers
    print(f"CALCULATED : Object to robot position: {object_to_robot_global}")
    print(f"ACTUAL : Object to robot position: {knownAnswers[i]}")
    
    # if ANY result is incorect, permemently set to failed test
    if (object_to_robot_global != knownAnswers[i]):
        testResult = "FAIL" # does return back to true, one fail and whole test failed

        
    
print("\n\nTEST COMPLETE")
print(f"\nTest Results : {testResult}")
    











