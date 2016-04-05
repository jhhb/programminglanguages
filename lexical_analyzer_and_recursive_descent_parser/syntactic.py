import sys


iNextToken = 0 #Next token index
tokenStream = []
lexemeStream = [] #not used for parsing

def main(inputFileName):


    #You define all of your streams in here, read the file in, and
    #from here call the first function, which in turn calls all others

    #Anytime you get an error, the program calls error and exits
    #Otherwise if correct, the program says "Syntactically Correct!"

    global tokenStream, lexemeStream, iNextToken
    tokenStream = []
    lexemeStream = []
    iNextToken = 0
    #Process the input file and build lists of tokens and lexemes
    inputFileObj = open(inputFileName, "r")
    bigStr = inputFileObj.read()
    bigList = bigStr.split() #bigList is a list of tokens and lexemes (alternating)
    tokenStream = bigList[0::2] #List of tokens sliced from bigList (even elements)
    lexemeStream = bigList[1::2] #List of lexemes

    myFileString = ""
    
    program()

    if iNextToken < len(tokenStream):
        error()
    else:
        print("Syntactically Correct!")

def program():
    type()

#If we aren't checking the first token, then just check type, if we are at start, then call main2
def type():
    global iNextToken

    if iNextToken == 0:
        if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "type":
            iNextToken += 1
            main2()
        else:
            error()

    elif iNextToken > 0:

        if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "type":
            iNextToken += 1
        else:
            error()

def main2():
    global iNextToken

    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "main":
        iNextToken += 1
        parens()


def parens():
    global iNextToken

    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "(":
        iNextToken += 1

        if iNextToken < len(tokenStream) and tokenStream[iNextToken] == ")":
            iNextToken += 1

            if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "{":

                lbrace()
            else:
                error()

    else:
        error()

def rbrace():
    global iNextToken

    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "}":
        iNextToken += 1

    else:
        error()


def lbrace():
    global iNextToken

    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "{":
        iNextToken += 1
        declarations()
        statements()

        if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "}":
            rbrace()
        else:
            error()

    else:
        error()


def declarations():

    declaration()


def declaration():
    global iNextToken

    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "type":
        type() ##call type for type id
        if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "id":
            id()

            while iNextToken < len(tokenStream) and tokenStream[iNextToken] == ",":
                iNextToken += 1
                id()

            if iNextToken < len(tokenStream) and tokenStream[iNextToken] == ";":
                semicolon()

                if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "type":
                    declarations()

            else:
                error()
        else:
            error()
    else:
        error()

def id():
    global iNextToken

    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "id":

        iNextToken += 1

    else:
        error()

def semicolon():

    global iNextToken

    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == ";":
        iNextToken += 1

    else:
        error()

def statements():


    while iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "id" or tokenStream[iNextToken] == "print" or tokenStream[iNextToken] == "if" or tokenStream[iNextToken] == "while" or tokenStream[iNextToken] == "return"):

        statement()

#Use ifs / elifs because you pick one so they are not nested

def statement():

    global iNextToken

    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "id":

        assignment()

    elif iNextToken < len(tokenStream) and tokenStream[iNextToken] == "print":

        printstmt()

    elif iNextToken < len(tokenStream) and tokenStream[iNextToken] == "if":

        ifstatement()

    elif iNextToken < len(tokenStream) and tokenStream[iNextToken] == "while":

        whilestmt()

    elif iNextToken < len(tokenStream) and tokenStream[iNextToken] == "return":

        returnstmt()

    else:
        error()

def assignment():
    global iNextToken

    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "id":
        id()

        if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "assignOp":
            assignOp()

            if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "id" or tokenStream[iNextToken] == "boolLiteral" or tokenStream[iNextToken] == "intLiteral" or tokenStream[iNextToken] == "floatLiteral"):
                expression()

                if iNextToken < len(tokenStream) and tokenStream[iNextToken] == ";":
                    semicolon()

                else:
                    error()

            else:
                error()
        else:
            error()
    else:
        error()

def assignOp():
    global iNextToken

    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "assignOp":
        iNextToken += 1

    else:
        error()

def expression():
    global iNextToken


    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "id" or tokenStream[iNextToken] == "boolLiteral" or tokenStream[iNextToken] == "floatLiteral" or tokenStream[iNextToken] == "intLiteral" or tokenStream[iNextToken] == "("):

        conjunction()
    else:
        error()

    while iNextToken < len(tokenStream) and tokenStream[iNextToken] == "||":
        iNextToken +=1

        if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "id" or tokenStream[iNextToken] == "boolLiteral" or tokenStream[iNextToken] == "floatLiteral" or tokenStream[iNextToken] == "intLiteral" or tokenStream[iNextToken] == "("):

            conjunction()
        else:
            error()

def conjunction():
    global iNextToken

    equality()

    while iNextToken < len(tokenStream) and tokenStream[iNextToken] == "&&":
        iNextToken +=1

        if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "id" or tokenStream[iNextToken] == "intLiteral" or tokenStream[iNextToken] == "boolLiteral" or tokenStream[iNextToken] == "floatLiteral"):

            equality()
        else:
            error()

def equality():
    global iNextToken

    relation()


    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "equOp"):
        equOp()

        if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "id" or tokenStream[iNextToken] == "intLiteral" or tokenStream[iNextToken] == "boolLiteral" or tokenStream[iNextToken] == "floatLiteral" or tokenStream[iNextToken] == "("):
            relation()

        else:
            error()

def equOp():
    global iNextToken

    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "equOp"):
        iNextToken += 1

    else:
        error()

def relation():
    global iNextToken

    addition()


    #Optional so optional if
    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "relOp"):
        relOp()

        if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "id" or tokenStream[iNextToken] == "intLiteral" or tokenStream[iNextToken] == "boolLiteral" or tokenStream[iNextToken] == "floatLiteral"):

            addition()
        else:
            error()


def relOp():
    global iNextToken

    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "relOp"):

        iNextToken += 1

    else:
        error()

def addition():
    global iNextToken

    term()

    while iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "addOp"):
        iNextToken +=1

        if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "id" or tokenStream[iNextToken] == "intLiteral" or tokenStream[iNextToken] == "boolLiteral" or tokenStream[iNextToken] == "floatLiteral"):
            term()
        else:
            error()

def addOp():
    global iNextToken

    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "addOp"):
        iNextToken += 1

    else:
        error()

def term():

    global iNextToken


    factor()

    while iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "multOp"):
        iNextToken += 1

        if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "id" or tokenStream[iNextToken] == "intLiteral" or tokenStream[iNextToken] == "boolLiteral" or tokenStream[iNextToken] == "floatLiteral"):

            factor()
        else:
            error()

def multOp():

    global iNextToken

    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "multOp"):
        iNextToken += 1

    else:
        error()

def factor():
    global iNextToken


    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "id"):
        id()
    elif iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "intLiteral"):
        intLiteral()
    elif iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "boolLiteral"):
        boolLiteral()
    elif iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "floatLiteral"):
        floatLiteral()
    elif iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "("):
        lparen()

        if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "id" or tokenStream[iNextToken] == "intLiteral" or tokenStream[iNextToken] == "boolLiteral" or tokenStream[iNextToken] == "floatLiteral"):
            expression()

            if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == ")"):
                rparen()
            else:
                error()

        else:
            error()
    else:
        error()

def whilestmt():
    global iNextToken

    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "while"):
        consumewhile()
        if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "(":
            lparen()

            if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "id" or tokenStream[iNextToken] == "intLiteral" or tokenStream[iNextToken] == "boolLiteral" or tokenStream[iNextToken] == "floatLiteral"):
                expression()

                if iNextToken < len(tokenStream) and tokenStream[iNextToken] == ")":
                    rparen()
                    statement()
                else:
                    error()
            else:
                error()
        else:
            error()
    else:
        error()

def consumewhile():
    global iNextToken

    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "while"):
        iNextToken += 1
    else:
        error()

def returnstmt():
    global iNextToken

    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "return"):
        consumereturn()

        if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "id" or tokenStream[iNextToken] == "intLiteral" or tokenStream[iNextToken] == "boolLiteral" or tokenStream[iNextToken] == "floatLiteral"):

            expression()

            if iNextToken < len(tokenStream) and tokenStream[iNextToken] == ";":
                semicolon()

            else:
                error()

        else:
            error()
    else:
        error()

def consumereturn():

    global iNextToken

    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "return"):
        iNextToken += 1
    else:
        error()

def printstmt():

    global iNextToken

    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "print"):
        consumeprint()

        if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "id" or tokenStream[iNextToken] == "intLiteral" or tokenStream[iNextToken] == "boolLiteral" or tokenStream[iNextToken] == "floatLiteral"):
            expression()

            if iNextToken < len(tokenStream) and tokenStream[iNextToken] == ";":
                semicolon()
            else:
                error()
        else:
            error()
    else:
        error()

def consumeprint():

    global iNextToken

    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "print"):
        iNextToken +=1

    else:
        error()

def ifstatement():

    global iNextToken

    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "if"):
        consumeif()

        if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "("):
            lparen()

            if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "id" or tokenStream[iNextToken] == "intLiteral" or tokenStream[iNextToken] == "boolLiteral" or tokenStream[iNextToken] == "floatLiteral"):

                expression()
                if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == ")"):
                    rparen()
                    statement()

                else:
                    error()
            else:
                error()
        else:
            error()
    else:
        error()

    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "else"):
        elsestmt()
        statement()

def elsestmt():
    global iNextToken

    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "else"):
        iNextToken += 1

    else:
        error()

def consumeif():
    global iNextToken

    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "if"):
        iNextToken += 1
    else:
        error()

def lparen():

    global iNextToken

    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "("):
        iNextToken += 1
    else:
        error()

def rparen():

    global iNextToken

    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == ")"):
        iNextToken +=1
    else:
        error()


def intLiteral():
    global iNextToken

    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "intLiteral":
        iNextToken += 1
    else:
        error()

def boolLiteral():
    global iNextToken

    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "boolLiteral":
        iNextToken += 1
    else:
        error()

def floatLiteral():
    global iNextToken

    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "floatLiteral":
        iNextToken += 1
    else:
        error()

def error():

    if iNextToken < len(tokenStream):
        print("Error: Invalid expression. Error location: <",\
            tokenStream[iNextToken], ",", lexemeStream[iNextToken], ">.")
    else:
        print("Error: Incomplete expression. Expecting more terms.")
    exit()

if __name__ == "__main__":
    main("last.txt")
