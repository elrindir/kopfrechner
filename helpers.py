

from enum import Enum
import configparser

# Enum alle Rechendisziplinen zum auswählen
class rechenDisziplin(Enum):
    PLUS="+"
    MINUS="-"
    MAL="*"
    GETEILT="/"

def isValidNumber(input: str) -> bool:
    try:
        int(input)
        return True
    except ValueError:
        return False

# Hilfsfunktion für Punkteberechnen
def points(mode, arguments: list, correct):
    i = 0

    if correct:    
        # answer was correct, give points for difficulty
        match mode:
            case rechenDisziplin.PLUS:
                i+=1
            case rechenDisziplin.MINUS:
                i+=1
            case rechenDisziplin.MAL:
                i+=1 * len(arguments)
            case rechenDisziplin.GETEILT:
                i+=3

        for arg in arguments:
            if arg < 0: i+=2
            if abs(arg) > 21: i+=1
            if abs(arg) > 100: i+=1
            if abs(arg) > 500: i+=1
            if abs(arg) > 1000: i+=1
            if abs(arg) > 10000: i+=1
            if abs(arg) > 100000: i+=1
    else:
        # answer was false, take points away
        i = -5

    return i


def currentModesString(modes):
    currentModeStr = ""
    for m in modes:
        currentModeStr += m.value
    return currentModeStr

def setModesByString(modes, string):
    plus = string.find("+")
    minus = string.find("-")
    mal = string.find("*")
    geteilt = string.find("/")

    if plus == minus == mal == geteilt == -1:
        print("No valid input.")
    else:
        modes.clear()
        if plus != -1: modes.append(rechenDisziplin.PLUS)
        if minus != -1: modes.append(rechenDisziplin.MINUS)
        if mal != -1: modes.append(rechenDisziplin.MAL)
        if geteilt != -1: modes.append(rechenDisziplin.GETEILT)
        print("Modes changed to: " + currentModesString(modes))
        


def printFile(file):
    f = open(file,"r")
    file_contents = f.read()
    print(file_contents)
    return


def create_config(filename, name, modesStr, numOperands, lowerBound, upperBound):
    config = configparser.ConfigParser()
 
    # Add sections and key-value pairs
    config['Settings'] = {'name':   name,
                        'modes':    modesStr,
                        'numoperands':  numOperands,
                        'lowerbound':   lowerBound,
                        'upperbound':   upperBound}
 
    # Write the configuration to a file
    with open(filename + ".ini", 'w') as configfile:
        config.write(configfile)
 
def read_config(filename):
    # Create a ConfigParser object
    config = configparser.ConfigParser()
 
    # Read the configuration file
    config.read(filename + ".ini")
 
    # Access values from the configuration file
    name = config.get('Settings', 'name')
    modesStr = config.get('Settings', 'modes')
    numOperands = config.get('Settings', 'numoperands')
    lowerBound = config.get('Settings', 'lowerbound')
    upperBound = config.get('Settings', 'upperbound')
 
    # Return a dictionary with the retrieved values
    config_values = {
        'name': name,
        'modesStr': modesStr,
        'numOperands': numOperands,
        'lowerBound': lowerBound,
        'upperBound': upperBound
    }
 
    return config_values
 