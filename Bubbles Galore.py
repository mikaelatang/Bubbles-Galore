####################################################################
#Coded By: Mikaela Tang                                            #
#Last edited: 06/17/2019 5:24pm                                    #
#Purpose: This game tests the user's speed and accuracy when it    #
#         comes to popping the magical bubbles before the time runs#
#         out.                                                     #
####################################################################
############LAYOUT FOR INSTRUCTIONS WORK BEST ON SCHOOL COMPUTERS###############

from tkinter import *
from math import * 
from time import *
from random import *

root = Tk()
s = Canvas(root, width=800, height=800, background="black")

#Don't want this value to reset if user replays
highScore = -1000000000


#********************************Game Preparation******************************#
def setInitialValues():
    global xMouse, yMouse, continueGame
    global startTime, clockDisplay, timerCountdown
    global bubbleDrawings, xBubble, yBubble, xBubbleSpeed, yBubbleSpeed, bubbleRadius, numBubbles, alreadyOnScreen, initialRelease
    global minBubbleSize, maxBubbleSize
    global xBubbleShade, yBubbleShade, oddEvenBubble, bubbleShadeColour, bubbleShadeDrawings1, bubbleShadeDrawings2, minUpSpeed, maxUpSpeed
    global xBird, yBird, xBirdSpeed, birdDrawings, bird1, bird2, numBirds, birdFrames, birdAmplitude, birdFrequency, f, birdPosition, y
    global treeColour
    global popArray, popBubble, timePopOnScreen, numPopped, numMisclicks
    global penalty, penaltyText, penaltyTextTime
    global background, qPressed, win

    xBubble = []
    yBubble = []
    xBubbleSpeed = []
    yBubbleSpeed = []
    xBubbleShade = []
    yBubbleShade = []
    xBird = []
    yBird = []
    xBirdSpeed = []
    bubbleRadius = []
    oddEvenBubble = [] #Decides which side the white shading is on
    bubbleDrawings = []
    bubbleShadeDrawings1 = []
    bubbleShadeDrawings2 = []
    birdDrawings = []
    timePopOnScreen = [] #Keeps track of how long 'pop' image has been on screen
    alreadyOnScreen = []
    popArray = []
    birdAmplitude = []
    birdFrequency = []
    birdFrames = [] #Used to control how often bird flaps wings
    birdPosition = []
    y = []

    startTime = time()
    f = 0 #Used in calculation of parbolic motion of bird
    penaltyTextTime = 0
    numMisclicks = 0
    numPopped = 0

    bird1 = PhotoImage(file = "Bird1.gif") #Wings up position of bird flying
    bird2 = PhotoImage(file = "Bird2.gif") #Wings dowm position of birds flying

    bubbleShadeColour = "#FFFFFF"
    penalty = False
    popBubble = False
    win = False
    qPressed = False
    continueGame = True

    if gameMode == "easy":
        background = PhotoImage(file = "Sky.gif")
        treeColour = "#003300"
        timerCountdown = 51
        numBubbles = 20 #Controls max number of bubbles that can be on screen at once (before user misclicks)
        initialRelease = 10 #How many bubbles are released when player first starts game
        minBubbleSize = 40
        maxBubbleSize = 75
        numBirds = 3
        minUpSpeed = -5
        maxUpSpeed = -1

    elif gameMode == "normal":
        background = PhotoImage(file = "Sky1.gif")
        timerCountdown = 41
        numBubbles = 25 
        initialRelease = 15
        minBubbleSize = 25
        maxBubbleSize = 50
        numBirds = 5
        minUpSpeed = -6
        maxUpSpeed = -2

    else:
        background = PhotoImage(file = "Sky2.gif")
        timerCountdown = 41
        numBubbles = 35 
        initialRelease = 15
        minBubbleSize = 10
        maxBubbleSize = 40
        numBirds = 7
        minUpSpeed = -6
        maxUpSpeed = -4

    clockDisplay = s.create_text(625, 50, text = str(timerCountdown), font = "msserif 30 italic", fill = "white")
    penaltyText = s.create_text(730, 50, text = "")


def drawBackground():
    s.create_image(400, 400, image = background)

    #Tree tips
    if gameMode == "easy":
        for i in range(20):
            x = randint(0, 700)
            y = randint(725, 775)
            height = randint(175, 400)
            width = randint(20, 50)

            s.create_polygon(x, y, x+width, y+height, x-width, y+height, fill = treeColour, outline = treeColour)



def initialTimer():
    #Timer counts down the seconds BEFORE game starts
    global gameMode, level, timeText

    level = gameMode
    gameMode = "timerRunning"

    #User has 3 seconds to prepare
    timer = 4
    beginTime = time()
    clock = s.create_text(400, 400, text = str(timer), font = "fixedsys 100 bold", fill = "white")

    while timer > 1:
        passedTime = time() - beginTime

        if passedTime >= 1:
            s.delete(clock)
            timer -= 1
            clock = s.create_text(400, 400, text = str(timer), font = "fixedsys 100 bold", fill = "white")
            beginTime = time()
            s.update()
            
    s.update()
    sleep(1)
    s.delete(clock)
    goSignal = s.create_text(400, 400, text = "GO!", font = "fixedsys 100 bold", fill = "white")
    
    s.update()
    sleep(1)
    s.delete(goSignal)

    timeText = s.create_text(500, 50, text = "Time remaining: ", font = "msserif 30 italic", fill = "white")

    gameMode = level


#********************************Bubble Procedures*****************************#
def createRandomBubbles():
    #Assigns initial values for bubbles
    global xBubble, yBubble, initialRelease
    
    for i in range(numBubbles):    
        xBubble.append(randint(100, 700))
        if initialRelease > 0:
            yBubble.append(800)
            initialRelease -= 1
        else:
            yBubble.append(randint(900, 1100))
        alreadyOnScreen.append(False)
        appendToList()
        

def appendToList(): #Procedure created because this section is used more than once in program
    global xBubbleSpeed, yBubbleSpeed, bubbleRadius, xBubbleShadow, yBubbleShadow, xBubbleShade, yBubbleShade, bubbleDrawings, bubbleShadowDrawings, bubbleShadeDrawings
    xBubbleSpeed.append(randint(-3, 5))
    yBubbleSpeed.append(uniform(minUpSpeed, maxUpSpeed))
    bubbleRadius.append(uniform(minBubbleSize, maxBubbleSize))
    oddEvenBubble.append(randint(0, 1))
    if oddEvenBubble[-1] == 0:
        xBubbleShade.append(uniform(xBubble[-1], xBubble[-1]+bubbleRadius[-1]/2.5))
    else:
        xBubbleShade.append(uniform(xBubble[-1]-bubbleRadius[-1]/2.5, xBubble[-1]))        
    yBubbleShade.append(yBubble[-1]-bubbleRadius[-1]*(4/5))
    bubbleDrawings.append(0)
    bubbleShadeDrawings1.append(0)
    bubbleShadeDrawings2.append(0)
    

def drawBubbles():
    #Draws bubbles in starting positions
    global bubbleDrawings, bubbleShadowDrawings, bubbleShadeDrawings
    
    for i in range(numBubbles):
        bubbleDrawings[i] = s.create_oval(xBubble[i]-bubbleRadius[i], yBubble[i]-bubbleRadius[i], xBubble[i]+bubbleRadius[i], yBubble[i]+bubbleRadius[i], outline = "white")
        bubbleShadeDrawings1[i] = s.create_oval(xBubbleShade[i], yBubbleShade[i], xBubbleShade[i]+bubbleRadius[i]/4, yBubbleShade[i]+bubbleRadius[i]/4, fill = bubbleShadeColour, outline = bubbleShadeColour)
        if oddEvenBubble[i] == 0:
            bubbleShadeDrawings2[i] = s.create_oval(xBubbleShade[i]+bubbleRadius[i]/6, yBubbleShade[i]+bubbleRadius[i]/6, xBubbleShade[i]+(bubbleRadius[i]/5)*2, yBubbleShade[i]+(bubbleRadius[i]/5)*2, fill = bubbleShadeColour, outline = bubbleShadeColour)
        else:
            bubbleShadeDrawings2[i] = s.create_oval(xBubbleShade[i]-bubbleRadius[i]/6, yBubbleShade[i]+bubbleRadius[i]/6, xBubbleShade[i]-(bubbleRadius[i]/5)*2, yBubbleShade[i]+(bubbleRadius[i]/5)*2, fill = bubbleShadeColour, outline = bubbleShadeColour)

            
def updateBubblePosition():
    global bubbleDrawings, xBubble, yBubble, xBubbleSpeed, yBubbleSpeed, xBubbleShade, yBubbleShade

    for i in range(numBubbles):
        #Can only enter screen once
        if alreadyOnScreen[i] == False:
            
            #Bubble is officially on screen if its top edge is less than 800
            if yBubble[i]-bubbleRadius[i] < 800:
                alreadyOnScreen[i] = True

        else:
            #Once the bubble is already on screen it will 'bounce' between the top and bottom walls as well
            if yBubble[i]-bubbleRadius[i] < 0 or yBubble[i]+bubbleRadius[i] > (800+bubbleRadius[i]*2+1):
                yBubbleSpeed[i] = -yBubbleSpeed[i]

        #Stays within certain x-values regardless of location
        if xBubble[i]-bubbleRadius[i] < 0 or xBubble[i]+bubbleRadius[i] > 800:
            xBubbleSpeed[i] = -xBubbleSpeed[i]
            
        xBubble[i] += xBubbleSpeed[i]
        yBubble[i] += yBubbleSpeed[i]
        xBubbleShade[i] += xBubbleSpeed[i]
        yBubbleShade[i] += yBubbleSpeed[i]


def deleteImages():
    for i in range(numBubbles):
        s.delete(bubbleDrawings[i], bubbleShadeDrawings1[i], bubbleShadeDrawings2[i])

    for i in range(numBirds):
        s.delete(birdDrawings[i])
        

def deletePop():
    #A pop image is drawn when the user pops a bubble (see mouseClickHandler)
    #This procedure deletes that image after a certain amount of time
    global timePopOnScreen, popBubble, popArray

    #Multiple arrays are used just in case user pops more than one bubble within five frames of each other
    if continueGame == True:
        
        #If the size of the two arrays are not equal, the difference will be added to timePopOnScreen array
        if len(timePopOnScreen) != len(popArray):
            for i in range(len(popArray)-len(timePopOnScreen)):
                timePopOnScreen.append(1) #The pop graphic has been on screen for zero frames (using '1' for later calculation)

        for i in range(len(timePopOnScreen)):
            #Only deletes pop graphic after it has been on screen for five frames
            if timePopOnScreen[i]%6 == 0:
                for f in range(15):
                    s.delete(popArray[f])

                del popArray[0:15]
                del timePopOnScreen[0:15]
                break

        #Remaining numbers in array increase by an incriment of 1
        for i in range(len(timePopOnScreen)):
            timePopOnScreen[i] += 1
            
        #Once the last bubble pop in array is deleted, procedure is not called on until user pops another bubble
        if len(popArray) == 0:
            popBubble = False

    else:
        #Delete last pop(s) when game stops running
         for f in range(len(popArray)):
            s.delete(popArray[f])

         del popArray[0:len(popArray)]
         del timePopOnScreen[0:len(timePopOnScreen)]


#*******************************Bird Procedures********************************#
def createRandomBirds():
    global xBird, yBird, xBirdSpeed, birdDrawings, birdFrames, birdAmplitude, birdFrequency

    for i in range(numBirds):
        xBird.append(randint(850, 1000))
        yBird.append(randint(100, 700))
        xBirdSpeed.append(randint(-10, -1))
        birdFrames.append(randint(1, 10)) #Prevent birds from flying in unison
        birdPosition.append(choice([True, False]))
        birdAmplitude.append(randint(10, 60))
        birdFrequency.append(uniform(0.01, 0.1))
        birdDrawings.append(0)
        y.append(0)
        


def drawBirds():
    for i in range(numBirds):
        #Parabolic motion
        y[i] = yBird[i] - birdAmplitude[i]*sin(birdFrequency[i]*f)

        #Wing changes position every 10 frames
        if birdFrames[i] % 10 == 0:
            if birdPosition[i] == True:
                birdPosition[i] = False

            else:
                birdPosition[i] = True
            

        if birdPosition[i] == True:
            birdDrawings[i] = s.create_image(xBird[i], y[i], image = bird1)

        else:
            birdDrawings[i] = s.create_image(xBird[i], y[i], image = bird2)
    


def updateBirdPosition():
    global xBird, yBird, f
    
    for i in range(numBirds):
        if xBird[i] < -50:
            xBird[i] = randint(850, 1000)
            yBird[i] = randint(100, 700)
            
        xBird[i] += xBirdSpeed[i]
        birdFrames[i] += 1
        
    f += 1
    


#*******************************Bind Procedures********************************#
def mouseClickHandler(event):
    #Clicking does nothing if game has not started yet
    if gameMode not in ["intro screen", "pause", "timerRunning"]:
        if continueGame == True:
            global xMouse, yMouse, bubbleDrawings, xBubble, yBubble, xBubbleShade, yBubbleShade, bubbleShadeDrawings1, bubbleShadeDrawings2, numBubbles
            global popArray, popBubble, numMisclicks, numPopped, timerCountdown, penalty, penaltyTextTime, minUpSpeed, maxUpSpeed
            
            xMouse = event.x
            yMouse = event.y
            bubNum = -1 #Set negative value to variable (must be -1 for possible later use)

            #Test if click was on a bird
            for i in range(numBirds):
                if xMouse >= xBird[i]-60 and xMouse <= xBird[i]+60 and yMouse >= y[i]-15 and yMouse <= y[i]+15:
                    #Subtract 2 seconds for 3 second penalty
                    timerCountdown -= 2
                    updateGameClock("")
                    penalty = True
                    penaltyTextTime = 0 #In case user clicks on more than ones bird within time frame
                    

            for i in range(numBubbles):
                
                #Testing if the click was in a bubble 
                if int(sqrt((yMouse-yBubble[i])**2 + (xMouse-xBubble[i])**2)) < bubbleRadius[i]:
                    bubNum = i
                    
                    #Only possible to click on one bubble at a time
                    break
                
            #If a bubble was clicked, the bubble pops
            if bubNum >= 0:
                oldx = xBubble[bubNum]
                oldy = yBubble[bubNum]
                
                #Reset x and y coordinates of bubble to outside of screen
                #Bubble is magically teleported outside of screen
                xBubble[bubNum] = randint(100, 700)
                yBubble[bubNum] = randint(900, 5000)
                if oddEvenBubble[bubNum] == 0:
                    xBubbleShade[bubNum] = (uniform(xBubble[bubNum], xBubble[bubNum]+bubbleRadius[bubNum]/2.5))
                else:
                    xBubbleShade[bubNum] = (uniform(xBubble[bubNum]-bubbleRadius[bubNum]/2.5, xBubble[bubNum]))
                yBubbleShade[bubNum] = (yBubble[bubNum]-bubbleRadius[bubNum]*(4/5))
                
                s.delete(bubbleDrawings[bubNum], bubbleShadeDrawings1[bubNum], bubbleShadeDrawings2[bubNum])
                
                bubbleDrawings[bubNum] = s.create_oval(xBubble[bubNum]-bubbleRadius[bubNum], yBubble[bubNum]-bubbleRadius[bubNum], xBubble[bubNum]+bubbleRadius[bubNum], yBubble[bubNum]+bubbleRadius[bubNum], outline = "white")
                bubbleShadeDrawings1[bubNum] = s.create_oval(xBubbleShade[bubNum], yBubbleShade[bubNum], xBubbleShade[bubNum]+bubbleRadius[bubNum]/4, yBubbleShade[bubNum]+bubbleRadius[bubNum]/4, fill = bubbleShadeColour, outline = bubbleShadeColour)
                if oddEvenBubble[bubNum] == 0:
                    bubbleShadeDrawings2[bubNum] = s.create_oval(xBubbleShade[bubNum]+bubbleRadius[bubNum]/6, yBubbleShade[bubNum]+bubbleRadius[bubNum]/6, xBubbleShade[bubNum]+(bubbleRadius[bubNum]/5)*2, yBubbleShade[bubNum]+(bubbleRadius[bubNum]/5)*2, fill = bubbleShadeColour, outline = bubbleShadeColour)
                else:
                    bubbleShadeDrawings2[bubNum] = s.create_oval(xBubbleShade[bubNum]-bubbleRadius[bubNum]/6, yBubbleShade[bubNum]+bubbleRadius[bubNum]/6, xBubbleShade[bubNum]-(bubbleRadius[bubNum]/5)*2, yBubbleShade[bubNum]+(bubbleRadius[bubNum]/5)*2, fill = bubbleShadeColour, outline = bubbleShadeColour)


                alreadyOnScreen[bubNum] = False
                numPopped += 1
                
                #Bubble pops
                #Local variables only used in this procedure are created
                xPop1 = []
                xPop2 = []
                yPop1 = []
                yPop2 = []
                
                n = 15
                deltaTheta = 2*pi/n
                theta = 0

                for i in range(n):
                    popArray.append(0)

                #Creates inner 'dots'
                for i in range(n):
                    xPop1.append(oldx + bubbleRadius[bubNum]*cos(theta))
                    yPop1.append(oldy - bubbleRadius[bubNum]*sin(theta))

                    theta += deltaTheta

                deltaTheta = 2*pi/n
                theta = 0

                #Creates outer 'dots'
                for i in range(n):
                    xPop2.append(oldx + (bubbleRadius[bubNum]+5)*cos(theta))
                    yPop2.append(oldy - (bubbleRadius[bubNum]+5)*sin(theta))

                    theta += deltaTheta

                #Connects the 'dots'
                for i in range(n):
                    popArray[i] = s.create_line(xPop1[i], yPop1[i], xPop2[i], yPop2[i], fill = 'white')

                popBubble = True

                #It is only possible to win if bubble is popped recently
                testForWin()
                
            #Misclicking causes a brand new bubble to appear
            else:
                xBubble.append(xMouse)
                yBubble.append(yMouse)
                alreadyOnScreen.append(True)
                #Bubbles created by misclicks move faster than normal
                minUpSpeed = -10
                maxUpSpeed = -6
                appendToList()

                bubbleDrawings[bubNum] = s.create_oval(xBubble[bubNum]-bubbleRadius[bubNum], yBubble[bubNum]-bubbleRadius[bubNum], xBubble[bubNum]+bubbleRadius[bubNum], yBubble[bubNum]+bubbleRadius[bubNum], outline = "white")
                bubbleShadeDrawings1[bubNum] = s.create_oval(xBubbleShade[bubNum], yBubbleShade[bubNum], xBubbleShade[bubNum]+bubbleRadius[bubNum]/4, yBubbleShade[bubNum]+bubbleRadius[bubNum]/4, fill = bubbleShadeColour, outline = bubbleShadeColour)
                if oddEvenBubble[bubNum] == 0:
                    bubbleShadeDrawings2[bubNum] = s.create_oval(xBubbleShade[bubNum]+bubbleRadius[bubNum]/6, yBubbleShade[bubNum]+bubbleRadius[bubNum]/6, xBubbleShade[bubNum]+(bubbleRadius[bubNum]/5)*2, yBubbleShade[bubNum]+(bubbleRadius[bubNum]/5)*2, fill = bubbleShadeColour, outline = bubbleShadeColour)
                else:
                    bubbleShadeDrawings2[bubNum] = s.create_oval(xBubbleShade[bubNum]-bubbleRadius[bubNum]/6, yBubbleShade[bubNum]+bubbleRadius[bubNum]/6, xBubbleShade[bubNum]-(bubbleRadius[bubNum]/5)*2, yBubbleShade[bubNum]+(bubbleRadius[bubNum]/5)*2, fill = bubbleShadeColour, outline = bubbleShadeColour)

                numBubbles += 1
                numMisclicks += 1

    

def keyDownHandler(event):
    #Tests if player wants to quit or pause game
    global continueGame, qPressed, gameMode  

    if event.keysym in ["q", "Q"]:
        continueGame = False
        qPressed = True

    elif event.keysym in ["p", "P"]:
        pauseScreen()



#******************************Miscellaneous Procedures************************#
def updateGameClock(c):
    global clockDisplay

    s.delete(clockDisplay)
    clockDisplay = s.create_text(625, 50, text = str(round(timerCountdown, 1)) + "" + str(c), font = "msserif 30 italic", fill = "white")


def testForWin():
    global continueGame, win
            
    if True in alreadyOnScreen:
        pass

    else:
        continueGame = False
        win = True
            
def pauseScreen():
    global gameMode, continueButton, level, pause
    
    level = gameMode
    gameMode = "pause"

    pause = s.create_text(400, 300, text = "PAUSED", font = "fixedsys 100", fill = "white")

    #Create button
    continueButton = Button(root, text = "CONTINUE", font = "fixedsys 30", command = continueButtonPressed, anchor = CENTER)
    continueButton.pack()
    continueButton.place(x = 300, y = 500, width = 200, height = 70)


def continueButtonPressed():
    global gameMode

    s.delete(pause)

    #Destroy Button
    continueButton.destroy()

    if level not in ["easyAfterPause", "normalAfterPause", "hardAfterPause"]:
        gameMode = level + "AfterPause"

    else:
        gameMode = level

    runGame()


def timePenalty():
    global penaltyText, penaltyTextTime, penalty

    penaltyTextTime += 1

    if penaltyTextTime == 1:
        penaltyText = s.create_text(725, 50, text = "-3 seconds", font = "messrif 30", fill = "white")

    if penaltyTextTime % 15 == 0:
        s.delete(penaltyText)
        penalty = False
        penaltyTextTime = 0
        
        

#*********************************End Screen***********************************#
def gameStats():
    global highScore, menuButton, replayButton, exitButton
    
    s.delete(clockDisplay, timeText, penaltyText)

    #Score calculation (negative scores are possible, even if you win)
    if qPressed == True:
        score = 0
    else:
        #More points are earned for popping bubbles in higher levels
        if gameMode in ["easy", "easyAfterPause"]:
            popPoints = numPopped * 5

        elif gameMode in ["normal", "normalAfterPause"]:
            popPoints = numPopped * 10

        else:
            popPoints = numPopped * 15
            
        score = (timerCountdown) * 10 + popPoints - numMisclicks * 5

        #Additional points are rewarded if player wins and points are deducted for loss
        if win == True:
            score += 100

        else:
            score -= 100

    if score > highScore:
        highScore = score

    if numPopped > 0:
        accuracy = round((numPopped/(numPopped+numMisclicks)*100), 2)

    else:
        accuracy = 0.00
    
    s.create_text(400, 100, text = "GAME OVER", font = "fixedsys 70 bold", fill = "white")

    if win == True:
        s.create_text(400, 175, text = "You Won", font = "fixedsys 30 bold", fill = "white")

    else:
        s.create_text(400, 175, text = "You Lost", font = "fixedsys 30 bold", fill = "white")

    s.create_text(400, 250, text = "Bubbles popped: " + str(numPopped), font = "fixedsys 30", fill = "white")
    s.create_text(400, 300, text = "Misclicks: " + str(numMisclicks), font = "fixedsys 30", fill = "white")
    s.create_text(400, 350, text = "Time remaining: " + str(timerCountdown), font = "fixedsys 30", fill = "white")
    s.create_text(400, 400, text = "Accuracy: "+ str(accuracy)+ "%", font = "fixedsys 30", fill = "white")

    s.create_text(400, 475, text = "Score " + str(score), font = "fixedsys 50 bold", fill = "white")
    s.create_text(400, 540, text = "High Score " + str(highScore), font = "fixedsys 50 bold", fill = "white")

    #Create buttons
    replayButton = Button(root, text = "REPLAY", font = "fixedsys 30", command = replayButtonPressed, anchor = CENTER)
    replayButton.pack()
    replayButton.place(x = 50, y = 650, width = 150, height = 70)

    menuButton = Button(root, text = "MENU", font = "fixedsys 30", command = menuButtonPressed, anchor = CENTER)
    menuButton.pack()
    menuButton.place(x = 325, y = 650, width = 150, height = 70)

    exitButton = Button(root, text = "EXIT", font = "fixedsys 30", command = exitButtonPressed, anchor = CENTER)
    exitButton.pack()
    exitButton.place(x = 600, y = 650, width = 150, height = 70)


def replayButtonPressed():
    global gameMode
    
    #Destroy buttons
    replayButton.destroy()
    menuButton.destroy()
    exitButton.destroy()

    if gameMode == "easyAfterPause":
        gameMode = "easy"

    elif gameMode == "normalAfterPause":
        gameMode = "normal"

    elif gameMode == "hardAfterPause":
        gameMode = "hard"
    
    runGame()


def menuButtonPressed():
    #Destroy buttons
    replayButton.destroy()
    menuButton.destroy()
    exitButton.destroy()

    start()

def exitButtonPressed():
    root.destroy()
    exit()

#**********************************Main Loop***********************************#
def runGame():
    global startTime, timerCountdown, continueGame

    if gameMode not in ["easyAfterPause", "normalAfterPause", "hardAfterPause"]:
        setInitialValues()
        drawBackground()
        createRandomBubbles()
        createRandomBirds()
        s.update()
        initialTimer()

    while continueGame == True:
        elapsedTime = time() - startTime

        if elapsedTime >= 1:
            timerCountdown -= 1
            updateGameClock("")
            startTime = time()

        if timerCountdown == 0:
            testForWin()
            continueGame = False
            break

        drawBubbles()
        drawBirds()
        
        updateBubblePosition()
        updateBirdPosition()

        if penalty == True:
            timePenalty()

        s.update()
        sleep(0.03)
        deleteImages()
        if popBubble == True:
            deletePop()

        if gameMode == "pause":
            return #Immediately breaks procedure
        
    gameStats()



#****************************Introduction Screens******************************#
def easyButtonPressed():
    global gameMode

    #Destroy buttons
    easyButton.destroy()
    normalButton.destroy()
    hardButton.destroy()

    gameMode = "easy"
    runGame()


def normalButtonPressed():
    global gameMode

    #Destroy buttons
    easyButton.destroy()
    normalButton.destroy()
    hardButton.destroy()

    gameMode = "normal"
    runGame()


def hardButtonPressed():
    global gameMode

    #Destroy buttons
    easyButton.destroy()
    normalButton.destroy()
    hardButton.destroy()

    gameMode = "hard"
    runGame()

    
def playButtonPressed():
    global easyButton, normalButton, hardButton, background
    
    #Destroy buttons
    playButton.destroy()
    #instructionsButton.destroy()

    background = PhotoImage(file = "IntroBackground1.gif")
    s.create_image(400, 400, image = background)

    #Instructions
    s.create_text(245, 100, text = "Click on bubbles to pop them.", font = "fixedsys 20", fill = "#FFFFFF")
    s.create_text(365, 150, text = "Pop all the bubbles on screen in the alloted", font = "fixedsys 20", fill = "#FFFFFF")
    s.create_text(110, 200, text = "time to win.", font = "fixedsys 20", fill = "#FFFFFF")
    s.create_text(385, 250, text = "Misclicking will result in score penalties and", font = "fixedsys 20", fill = "#FFFFFF")
    s.create_text(250, 300, text = "cause a new bubble to appear.", font = "fixedsys 20", fill = "#FFFFFF")
    s.create_text(360, 350, text = "Be weary of traversing birds as clicking on", font = "fixedsys 20", fill = "#FFFFFF")
    s.create_text(295, 400, text = "them will result in a time penalty.", font = "fixedsys 20", fill = "#FFFFFF")
    s.create_text(295, 450, text = "Press 'Q' to quit and 'P' to pause.", font = "fixedsys 20", fill = "#FFFFFF")


    ##ALSO ADD THAT PRESS 'Q' TO QUIT AND 'P' TO PAUSE ANYTIME##

    #Create level buttons
    easyButton = Button(root, text = "EASY", font = "fixedsys 30", command = easyButtonPressed, anchor = CENTER)
    easyButton.pack()
    easyButton.place(x = 25, y = 675, width = 150, height = 70)

    normalButton = Button(root, text = "NORMAL", font = "fixedsys 30", command = normalButtonPressed, anchor = CENTER)
    normalButton.pack()
    normalButton.place(x = 325, y = 675, width = 150, height = 70)

    hardButton = Button(root, text = "HARD", font = "fixedsys 30", command = hardButtonPressed, anchor = CENTER)
    hardButton.pack()
    hardButton.place(x = 625, y = 675, width = 150, height = 70)


def introScreen():
    global playButton, background

    #Intro background
    background = PhotoImage(file = "IntroBackground.gif")
    s.create_image(370, 400, image = background)

    xPop1 = []
    yPop1 = []
    xPop2 = []
    yPop2 = []

    n = 20
    deltaTheta = 2*pi/n
    theta = 0

    for i in range(n):
        xPop1.append(300 + 150*cos(theta))
        yPop1.append(575 - 150*sin(theta))

        theta += deltaTheta

    deltaTheta = 2*pi/n
    theta = 0

    for i in range(n):
        xPop2.append(300 + 170*cos(theta))
        yPop2.append(575 - 170*sin(theta))

        theta += deltaTheta

    for i in range(n):
        s.create_line(xPop1[i], yPop1[i], xPop2[i], yPop2[i], fill = 'white', width = 3)

    #Create buttons
    playButton = Button(root, text = "PLAY", font = "fixedsys 30", command = playButtonPressed, anchor = CENTER)
    playButton.pack()
    playButton.place(x = 500, y = 600, width = 225, height = 75)

    s.update()


def start():
    global gameMode

    gameMode = "intro screen"
    introScreen()


root.after( 0, start )

s.bind( "<Button-1>", mouseClickHandler )
s.bind( "<Key>", keyDownHandler )

s.pack()
s.focus_set()
root.mainloop()
