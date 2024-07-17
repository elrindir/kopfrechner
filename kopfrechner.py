import random, datetime
import helpers



global modes, lowerBound, upperBound, numOperands, score

# Parametriere hier, was du haben willst
modes = [helpers.rechenDisziplin.PLUS,helpers.rechenDisziplin.MINUS,helpers.rechenDisziplin.MAL]     # Rechendisziplinen
lowerBound = 0                  # ab welchem Zahlenbereich z.B. 0 oder -100 für negative Rechnungen
upperBound = 20                 # bis welchen Zahlenbereich z.B. 100 oder bis 1000
numOperands = 2                 # wie viele Operanden in einer Rechnung

# Zuckerl
name = "player"
score = 0

# Backend variablen
abort = False



# Schleife
while not abort:
    # Erst mal eine Disziplin aus der liste auswählen
    actualMode = random.choice(modes)
    
    # Rechenoperanden random ermitteln
    if actualMode == helpers.rechenDisziplin.GETEILT: numOperands=2     # Geteil macht nur mit 2 Operanden Sinn.
    operands = [0] * numOperands  

    # Suche so lange nach Operanden, bis die Bedingungen erfüllt sind
    while True:
        for i in range(numOperands):
            operands[i] = random.randint(lowerBound,upperBound)

        # 0 nicht erwünscht 
        foundZero = False
        for op in operands:
            if op == 0:
                foundZero = True
                break

        # 1 nicht erwünscht bei Multiplikation und Division
        foundOne = False
        if actualMode == helpers.rechenDisziplin.MAL or actualMode == helpers.rechenDisziplin.GETEILT:
            for op in operands:
                if op == 1:
                    foundOne = True
                    break
                
        if not foundZero and not foundOne: break
        
    # Bilde die Rechenaufgabe je nach Modus (gewählter Disziplin)
    match actualMode:
        case helpers.rechenDisziplin.PLUS:
            # Summe bilden
            result = 0
            for op in operands:
                result += op

            # Rechenaufgabe schreiben
            aufgabeStr = "Enter the sum: "
            rechnungStr = ""
            for i in range(numOperands):
                rechnungStr += str(operands[i]) 
                if i < numOperands-1: rechnungStr += " + "
                
        case helpers.rechenDisziplin.MINUS:
            # Differenz bilden
            result = operands[0]
            for i in range(1,numOperands):
                result -= operands[i]

            # Rechenaufgabe schreiben
            aufgabeStr = "Enter the difference: "
            rechnungStr = ""
            for i in range(numOperands):
                rechnungStr += str(operands[i]) 
                if i < numOperands-1: rechnungStr += " - "
            

        case helpers.rechenDisziplin.MAL:
            # Produkt bilden
            result = 1
            for op in operands:
                result *= op

            # Rechenaufgabe schreiben
            aufgabeStr = "Enter the product: "
            rechnungStr = ""
            for i in range(numOperands):
                rechnungStr += str(operands[i]) 
                if i < numOperands-1: rechnungStr += " * "

        case helpers.rechenDisziplin.GETEILT:
            # Quotient bilden
            result = operands[0] / operands[1]

            # Rechenaufgabe schreiben
            aufgabeStr = "Enter the quotient: " + str(result)
            rechnungStr = str(operands[0]) + " : " + str(operands[1])    



# Rechenaufgabe stellen
    print(rechnungStr + " = ")

# Zeit starten
    start = datetime.datetime.now()

# Antwort anfordern
    answer = input(aufgabeStr)

# Zeit stoppen
    stop = datetime.datetime.now()
    timeDiff = stop-start

# Antwort auswerten
    if answer == "abort" or answer == "exit":
        exit()
    elif answer == "help":
        helpers.printFile("help.txt")
    elif answer == "readme":
        helpers.printFile("README.txt")
    elif answer == "mode" or answer == "modes":
        print("Curent modes:")
        print("  " + helpers.currentModesString(modes))
        newmodesStr=input("Enter new mode selection with '+' '-' '*' '/'-Symbols: ")

        helpers.setModesByString(modes, newmodesStr)


    elif answer == "range":
        print("Curent settings:")
        print("  number operands is : " + str(numOperands))
        print("  operands range from: " + str(lowerBound))
        print("                   to: " + str(upperBound))
        numOp=input("Enter new number operands: ")
        if not numOp.isnumeric(): 
            print("Input must be numeric")
            continue
        if int(numOp) < 2:
            print("Input must be at least 2.")
            continue
        
        lb=input("Enter new operand range from: ")
        if not lb.isnumeric(): 
            print("Input must be numeric")
            continue

        ub=input("Enter new operand range from: ")
        if not ub.isnumeric(): 
            print("Input must be numeric")
            continue
                
        
        numOperands = int(numOp)
        lowerBound = int(lb)
        upperBound = int(ub)
    elif answer == "score":
        print("Your current score is " + str(score))
        print("You need to type 'save' to save your score to the scoreboard.")
    elif answer == "scoreboard" or answer == "sb":
        helpers.printFile("scoreboard.txt")
    elif answer == "name":
        newName=input("Enter your name: ")
        if newName != "": name = newName
    elif answer == "save":
        if name == "player":
            print("You haven't set a name. Default name is 'player'. If you want to change your name in the scoreboard, use command 'name' or enter a name now.")
            newName=input("Enter your name: ")
            if newName != "": name = newName
        
        # prepare new line in scoreboard
        newScoreEntryStr = str(datetime.datetime.now()) + "; " + name + "; " + str(score) + "\n"

        # write to file
        with open("scoreboard.txt", "a") as myFile:
            myFile.write(newScoreEntryStr)

    elif answer == "store":
        helpers.create_config(name,
                              helpers.currentModesString(modes),
                              numOperands,
                              lowerBound,
                              upperBound)
    elif answer == "restore":
        configData = helpers.read_config()
        name=configData['name']
        helpers.setModesByString(modes, configData['modesStr'])
        numOperands= int(configData['numOperands'])
        lowerBound = int(configData['lowerBound'])
        upperBound = int(configData['upperBound'])


    # Keine Antwort
    elif answer == "":
        continue

    # Ab hier erwarte ich nur noch numerische eingaben!
    elif not answer.isnumeric():
        print("That was no valid answer.")

    # Richtige Antwort
    elif int(answer) == result:
        point = helpers.points( actualMode, operands, True )
        print("Correct! You earned " + str(point) + " points on your score. You took " + str(timeDiff.seconds) + "s." )
        score += point
    # Falsche Antwort
    else:
        if score >= 0:
            print("False. The correct answer is " + str(result))
        else:
            print("False you stupid fuck. If you had a fucking brain, you would know, the correct answer is " + str(result))
        score += helpers.points( actualMode, operands, False)
    
        


