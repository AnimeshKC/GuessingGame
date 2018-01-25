#An AI based guessing game-style program
#Animesh KC
import random as r
import time


#Open the file with the instructions
infoFile = open("Information.txt", "r")

gameData = []

def main(dataList):
    print ("Welcome to this number guessing game.")

    #Call the introduce function
    introduce()
    
    #Call the gameLoop
    gameLoop(dataList)

    #After gameLoop ends, check whether the player wants a rematch.
    rematchLoop = True
    while rematchLoop:
        question1 = "Would you like to play again(y or n)? "
        option1 = stringInput(question1)
        if option1:
            
            #Check whether game data is empty. 
            if len(dataList) > 0:
                question2 = "Would you like to reset the gameData(y or n)? "
                option2 = stringInput(question2)
                if option2:
                    dataList = []
                    print ("The game data has been reset")
                elif not option2:
                    print ("The game data has stayed the same")
            gameLoop(dataList)
        elif not option1:
            print ("Until next time.")
            rematchLoop = False

def gameLoop(dataList):
    loop = True
    playerPoints = 0
    computerPoints = 0    
    while loop:
        #Call rounds function to orchestrate rounds
        output = rounds(dataList)

        #Output becomes false if the player types "q"
        if output is False:
            loop = False
        else:
            difference = output
            if difference <100:
                addedPoints = 100 - difference
                print ("\nthe computer gains " + str(addedPoints) + " points")
                computerPoints +=addedPoints
            elif 100<=difference<200:
                playerAddition= abs(100-difference)
                print ("\nthe player gains " + str(playerAddition) + " points")
                playerPoints += (playerAddition)
            else: 
                print ("No one gains points")
                
            print ("\nPlayer's points: " + str(playerPoints))
            print ("Computer's points: " + str(computerPoints))
            
            #Check whether someone has 300 points
            playerCheck = checkGame(playerPoints)
            computerCheck = checkGame(computerPoints)
            
            if playerCheck:
                print ("You win. Congratulations")
                loop = False
            elif computerCheck:
                print ("The computer wins. Good Try.")
                loop = False    
        

def introduce():
    introQuestion = "Would you like to look at the instructions for this game(y or n)? "
    option = stringInput(introQuestion)
    
    if option:
        readData(infoFile)
    
    elif option ==False:
        print ("You probably have played this before then")
    
    print ("Now, let the game begin!")
def rounds(gameList):
    if len (gameList) == 0:
        #The number is generated randomly if no data exists yet. 
        computerNumb = r.randrange(1,501)
    elif len (gameList) > 0:
        #Call the compManager function in order to generate the number
        computerNumb = compManager(gameList)
    theChoice = playerChoice()
    if not theChoice:
        diff = False
    elif 0<theChoice<=500:
        print ("The computer chose: " + str(computerNumb))
        diff = abs(theChoice - computerNumb)
        print ("The difference is "+ str(diff))
        gameDataAppend(gameList,theChoice)
    return diff


def compManager(gameList):

    #Generate a raw version of the gameList that displays only the numbers.
    gameListRaw = createRawGameList(gameList)

    #Initially set lowestNum as a number above 500 
    #Any number will replace it.
    lowestNum = 510
    highestNum = 0
    modeList = [0,0]
    modeDiff = []
    
    for i in range (len(gameList)):
        theNum = gameList[i][0]
        frequency = gameList[i][1]
        if frequency > modeList[0]:
            modeList = [frequency,theNum]
        elif frequency == modeList[0]:
            modeList.append(theNum)
        if theNum > highestNum:
            highestNum = theNum
        if theNum < lowestNum:
            lowestNum = theNum
    
    mean = meanofList(gameListRaw)
    
    #Append to the modeDiff list
    for i in range (1, len(modeList)):
        meanabs = abs(mean - modeList[i])
        modeDiff.append(meanabs)
    
    #Find the modeMean
    modeMean = meanofList(modeDiff)
    
    highEndValue = mean+modeMean
    lowEndValue = abs(mean-modeMean)
    
    #Check how many numbers are above and below high and low end values
    highRangeTotal = comparisonCheck(gameListRaw,highEndValue)
    lowRangeTotal = comparisonCheck(gameListRaw,lowEndValue,False)
    
    #Generate the list that the computer will use
    listTotal = (highRangeTotal+lowRangeTotal) * 2.5

    #Set totalRatio and modeMultiplier
    totalRatio = 0.60
    modeFrequency = modeList[0]
    modeMultiplier = 0.92 ** modeFrequency

    #Check whether the modeDiff consists of primarily one number. 
    meanDominanceRatio = listDominanceDeterminer(modeDiff)

    #The higher the modeFrequency, the lower the modeMultiplier
    wildCardRatio = totalRatio*meanDominanceRatio*0.82*modeMultiplier
    
    #Wildcard ratio will always be at least 10% of the computer
    if wildCardRatio < 0.10:
        wildCardRatio = 0.10
    wildCardRatio = round(wildCardRatio,2)

    #Find the meanRatioValue
    meanRatioValue = totalRatio - wildCardRatio

    #Extend the highest and lowest ranges
    #If the gameList is concentrated too heavily by a single number
    gameListRatio = listDominanceDeterminer(gameListRaw)
    if gameListRatio > 0.50:
        deviation = round((gameListRatio-0.50)*500)
        if lowestNum >= deviation:
            lowestNum -= deviation
        elif lowestNum < deviation:
            lowestNum = 0
        if highestNum + deviation <= 500:
            highestNum += deviation
        elif highestNum + deviation > 500:
            highestNum = 500
    meanRangeTotal = round(meanRatioValue*listTotal)
    wildRangeTotal = round(wildCardRatio*listTotal)
    computerList = []
    
    #Append to the computerList using the required information
    computerList = rangeAppend(computerList,lowestNum,lowEndValue,lowRangeTotal)
    computerList = rangeAppend(computerList,lowEndValue,highEndValue+1,meanRangeTotal)
    computerList = rangeAppend(computerList,highEndValue,highestNum+1,highRangeTotal)
    computerList = rangeAppend(computerList,0,501,wildRangeTotal)
    
    computerChoice = r.choice(computerList)
    return computerChoice

def playerChoice():
    while True:
        try:
            playerInput = input("Enter a number between 1 and 500, or enter 'q' to quit:")
            if playerInput == "q":
                print ("The game will now end.")
                return False
            else:
                playerInput = int(playerInput)
                if 0 < playerInput <= 500:
                    print ("\nThe player chose "+ str(playerInput))
                    return playerInput
        except:
            pass
                
def stringInput(prompt):
    while True:
        try:
            choice = str.lower(input(prompt))
            if choice == "y" or choice =="yes":
                state = True
            elif choice == "n" or choice == "no":
                state = False
            return state
        except:
            pass

def comparisonCheck(aList,checkValue,checking=True):
    """
    Key arguments:
    aList — the list that will be checked
    checkValue — the number that the function will compare
    to all the numbers in the list.
    checking — if true, the function counts the number of values
    in the list larger than the checkValue. If false, the function counts
    the number of values in the list below the checkValue

    Returns trueInstances, the number of values either above or below
    the checkValue
    """
    trueInstances = 0
    
    for i in range(len(aList)):
        num = aList[i]
        if checking:
            if num >= checkValue:
                trueInstances += 1
        elif not checking:
            if num <= checkValue:
                trueInstances +=1
    return trueInstances    

def listDominanceDeterminer(aList):
    """
    A function that finds the ratio of the instances of the most frequent 
    number to the length of the list.
    
    returns theRatio
    """
    theLength = len(aList)
    theRatio = 0
    for i in range (theLength):
        numEquivalence = 0
        testNum = aList[i]
        numCount = 0
        for a in range (theLength):
            if testNum == aList[a]:
                #Add to the num count every time the same number is found
                numCount +=1
                
        #Replace numEquivalence if numCount is higher
        numEquivalence = greaterReplacement(numEquivalence,numCount)
        tempRatio = round((numEquivalence/theLength),2)
        theRatio = greaterReplacement(theRatio,tempRatio)
    return theRatio

def greaterReplacement(firstValue,secondValue):
    if secondValue> firstValue:
        firstValue = secondValue
    return firstValue

def checkGame(points):
    if points >= 300:
        return True
    elif points <300:
        return False            
def readData(aFile):
    for line in aFile:
        time.sleep(0.8)
        print (line)
        time.sleep(0.8)
def meanofList(aList):
    theSum = 0
    frequency = 0
    for i in range (len(aList)):
        theSum += aList[i]
        frequency += 1
    theMean = round(theSum / frequency)
    return theMean

def createRawGameList(aList):
    newList = []
    for i in range(len(aList)):
        value = aList[i][0]
        frequency = aList[i][1]
        for i in range(frequency):
            newList.append(value)
    return newList

def rangeAppend(aList,lowRange,highRange,rangeTotal):
    for i in range(rangeTotal):
        if lowRange == highRange:
            num = lowRange
        else:
            num = r.randrange(lowRange,highRange)
        aList.append(num)
    return aList
def gameDataAppend(theGameData,theNum):
    if len(gameData) ==0:
        theGameData.append([theNum,1])
    elif len(gameData)>0:
        numOnlyList = []
        for i in range(len(theGameData)):
            numOnlyList.append(theGameData[i][0])
        if theNum in numOnlyList:
            for i in range(len(theGameData)):
                if theNum == theGameData[i][0]:
                    theGameData[i][1] += 1
        elif theNum not in numOnlyList:
            theGameData.append([theNum,1])
    
    return theGameData    




    
        
    
main(gameData)
infoFile.close()

    

