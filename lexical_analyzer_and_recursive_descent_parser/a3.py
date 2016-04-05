__author__ = 'jamesboyle'

import sys

#Global var
iNextToken = 0 #Next token index
tokenStream = []
lexemeStream = []
symTable = {} #empty dictionary/hash-map

execute = True
callingFunction = ''
elseExecute = False
alreadyExecuted = False

def main(inputFileName):
    global tokenStream, lexemeStream, iNextToken
    tokenStream = []
    lexemeStream = []
    iNextToken = 0
    symTable = {}

    #Process the input file and build lists of tokens and lexemes
    inputFileObj = open(inputFileName, "r")
    bigStr = inputFileObj.read()
    bigList = bigStr.split() #bigList is a list of tokens and lexemes (alternating)
    tokenStream = bigList[0: :2] #List of tokens sliced from bigList (even elements)
    lexemeStream = bigList[1: :2] #List of lexemes


    program() #Start at the start symbol Program
    if iNextToken < len(tokenStream): #had to stop early
        error()

def program():
    global iNextToken
    if tokenStream[iNextToken] == 'type':
        iNextToken+=1
        if tokenStream[iNextToken] == 'main':
            iNextToken+=1
            if tokenStream[iNextToken] == "(":
                iNextToken+=1
                if tokenStream[iNextToken] == ")":
                    iNextToken+=1
                    if tokenStream[iNextToken] == "{":
                        iNextToken+=1
                        declarations()
                        statements()
                        if tokenStream[iNextToken] == "}":
                            iNextToken+=1

def declarations():
    while iNextToken < len(tokenStream) and \
          tokenStream[iNextToken] == 'type':
        declaration()

def declaration():
    global iNextToken, symTable

    if tokenStream[iNextToken] == 'type': #redundant
        iNextToken += 1
        if tokenStream[iNextToken] == 'id':
            varName = lexemeStream[iNextToken]
            varType = lexemeStream[iNextToken - 1]
            #Make a new dictionary entry: key = varName, value = [varType, initialValue]
            if varName in symTable:
                declarationError(varName)
            else:
                symTable[varName] = [varType, None] ##put the name of the variable in the table with an associated Type
                iNextToken += 1
                if tokenStream[iNextToken] == ';':
                    iNextToken += 1
                    return
    error()

def statements():
    while iNextToken < len(tokenStream) and (tokenStream[iNextToken] == 'print' or tokenStream[iNextToken] == 'id' or
    tokenStream[iNextToken] == 'while' or tokenStream[iNextToken] == 'if' or tokenStream[iNextToken] == 'return'):
        statement()

def printStatement():
    global iNextToken, symTable, execute


    if tokenStream[iNextToken] == 'print':
        iNextToken += 1

        printReturn = expr()


        if execute is True:# and callingFunction == 'if':
            print(printReturn)

        if tokenStream[iNextToken] == ";":
            iNextToken+=1

def assignmentStatement():
    global iNextToken, symTable

    if tokenStream[iNextToken] == 'id':
        varName = lexemeStream[iNextToken] #for use later
        if varName not in symTable:                         #if not exists(symTable[lexemeStream[iNextToken]]): #var not declared?
            declarationError(lexemeStream[iNextToken])
        iNextToken += 1
        if tokenStream[iNextToken] == 'assignOp':   #change back to =
            iNextToken += 1
            assignmentReturn = expr()
            if tokenStream[iNextToken] == ';':
                iNextToken += 1

                if execute == True:
                    if symTable[varName][0] == "int":
                        if type(assignmentReturn) is int:
                            symTable[varName][1] = assignmentReturn
                        else:
                            typeError(varName)
                    elif symTable[varName][0] == "float":
                        if type(assignmentReturn) is not bool:
                            symTable[varName][1] = assignmentReturn
                        else:
                            typeError(varName)

                    elif symTable[varName][0] == "bool":
                        if type(assignmentReturn) is bool:
                            symTable[varName][1] = assignmentReturn
                        else:
                            typeError(varName)

def ifStatement():
    global iNextToken, execute, elseExecute, alreadyExecuted

    if tokenStream[iNextToken] == 'if':
        iNextToken += 1
        if tokenStream[iNextToken] == '(':
            iNextToken +=1
            if tokenStream[iNextToken] == 'id' or tokenStream[iNextToken] == 'intLiteral' or tokenStream[iNextToken] == 'boolLiteral' or tokenStream[iNextToken] == 'floatLiteral' or tokenStream[iNextToken] =='(':
                ifReturn = expr()
                if(ifReturn == True):
                    execute = True

                else:
                    execute = False

                if tokenStream[iNextToken] == ')':
                    iNextToken +=1
                    statement()
                    execute = True

                    if tokenStream[iNextToken] == "else":
                        if execute == True:
                            execute = False
                        iNextToken +=1
                        statement()
def whileStatement():
    global iNextToken

    if tokenStream[iNextToken] == 'while':
        iNextToken += 1
        if tokenStream[iNextToken] == '(':
            iNextToken +=1
            whileCounter = iNextToken
            secondCounter = 0

            if tokenStream[iNextToken] == ('id' or 'intLiteral' or 'boolLiteral' or 'floatLiteral' or '('):


                while(expr() is True):

                    if tokenStream[iNextToken] == ')':
                        iNextToken+=1   ##consume token
                        statements()
                        secondCounter = iNextToken
                        iNextToken = whileCounter

                iNextToken = secondCounter



def returnStatement():
    global iNextToken

    if tokenStream[iNextToken] == 'return':
        iNextToken+=1

        if tokenStream[iNextToken] == 'id' or tokenStream[iNextToken] =='intLiteral' or tokenStream[iNextToken] == 'boolLiteral' or tokenStream[iNextToken] == 'floatLiteral' or tokenStream[iNextToken] =='(': #or 'intLiteral' or 'boolLiteral' or 'floatLiteral' or '('):
            returnReturn = expr()
            if tokenStream[iNextToken] == ';':
                iNextToken +=1

def statement():
    global iNextToken, symTable

    if tokenStream[iNextToken] == 'print':
        printStatement()

    #Assignment
    elif tokenStream[iNextToken] == 'id':
        assignmentStatement()
#IF
    elif tokenStream[iNextToken] == 'if':
        ifStatement()

#While
    elif tokenStream[iNextToken] == 'while':
        whileStatement()

#RETURN
    elif tokenStream[iNextToken] == 'return':
        returnStatement()

def printValue(varName):
    print(varName, "=", symTable[varName][1],"\n")

def exists(varName):
    return symTable.has_key(varName)

def expr():
    global iNextToken

    conjunctionReturn = conjunction()

    while iNextToken < len(tokenStream) and tokenStream[iNextToken] == "||":
        iNextToken +=1

        b = conjunction()

        if type(conjunctionReturn) == bool and type(b) == bool:
            conjunctionReturn = conjunctionReturn or b
        else:
            error()

    return conjunctionReturn

def conjunction():

    global iNextToken
    equalityReturn = equality()

    while iNextToken < len(tokenStream) and tokenStream[iNextToken] == "&&":
        iNextToken +=1

        b = equality()

        if equalityReturn == (True or False) and b == (True or False):
            equalityReturn = equalityReturn or b
        else:
            error()

    return equalityReturn

def equality():

    global iNextToken

    returnValue = 0

    relationReturn = relation()

    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "equOp"):
        myEquOp = lexemeStream[iNextToken]

        iNextToken+=1

        v = relation()

        if( type(relationReturn) is int or float and type(v) is int or float):
            if(myEquOp == "!="):
                if relationReturn != v:
                    returnValue = True
                else:
                    returnValue = False
            elif(myEquOp == "=="):
                if relationReturn == v:
                    returnValue = True
                else:
                    returnValue = False

        elif(type(relationReturn) is bool and type(v) is bool):
            if(myEquOp == "!="):
                if relationReturn != v:
                    returnValue = True
                else:
                    returnValue = False
            elif(myEquOp == "=="):
                if relationReturn == v:
                    returnValue = True
                else:
                    returnValue = False

        else:
            error()

    if type(returnValue) is bool:
        return returnValue
    else:
        return relationReturn


def relation():
    global iNextToken

    additionReturn = addition()

    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "relOp"):
        myRelOp = lexemeStream[iNextToken]
        iNextToken+=1
        if type(additionReturn) is bool:
            error()
        v = addition()
        if type(v) is bool:
            error()
        if myRelOp == "<":
            if additionReturn < v:
                additionReturn = True
            else:
                additionReturn = False

        elif myRelOp == "<=":
            if additionReturn <= v:
                additionReturn = True
            else:
                additionReturn = False
        elif myRelOp == ">":
            if additionReturn > v:
                additionReturn = True
            else:
                additionReturn = False

        elif myRelOp == ">=":
            if additionReturn >= v:
                additionReturn = True
            else:
                additionReturn = False

    return additionReturn

def addition():

    global iNextToken

    termReturn = term()

    while iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "addOp"):

        myAddOp = lexemeStream[iNextToken]

        iNextToken +=1

        if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "id" or tokenStream[iNextToken] == "intLiteral" or tokenStream[iNextToken] == "boolLiteral"
        or tokenStream[iNextToken] == "floatLiteral" or tokenStream[iNextToken] == '('):
            v = term()

            if v == (True or False):
                error()
        else:
            error()

        if myAddOp == "+":
            termReturn = termReturn + v
        elif myAddOp == "-":
            termReturn = termReturn - v

    return termReturn;


def term():
    global iNextToken
    factorReturn = factor()


    while iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "multOp"):
        exponent = 1 if lexemeStream[iNextToken] == "*" else -1

        iNextToken +=1

        if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "id" or tokenStream[iNextToken] == "intLiteral" or tokenStream[iNextToken] == "boolLiteral"
        or tokenStream[iNextToken] == "floatLiteral" or tokenStream[iNextToken] == "("):

            v = factor()

            if v == (True or False):
                error()
        else:
            error()
        factorReturn = factorReturn * v ** exponent
    return factorReturn

def factor():
    global iNextToken

    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == 'intLiteral':
        iNextToken += 1
        return int(lexemeStream[iNextToken-1])
        ##return the int value
    elif iNextToken < len(tokenStream) and tokenStream[iNextToken] == 'boolLiteral':
        iNextToken +=1
        if lexemeStream[iNextToken-1] == 'true':
            return True
        else:
            return False
    elif iNextToken < len(tokenStream) and tokenStream[iNextToken] == 'floatLiteral':
        iNextToken +=1
        return float(lexemeStream[iNextToken-1])

    elif iNextToken < len(tokenStream) and tokenStream[iNextToken] == 'id':
        iNextToken +=1
        varName = lexemeStream[iNextToken-1]
        if varName not in symTable:
            declarationError(lexemeStream[iNextToken-1])
        else:
            return symTable[lexemeStream[iNextToken-1]][1]
    elif iNextToken < len(tokenStream) and tokenStream[iNextToken] == '(':
        iNextToken +=1
        expressionReturn = expr()
        if iNextToken < len(tokenStream) and tokenStream[iNextToken] == ')':
            iNextToken+=1
            return expressionReturn
    else:
        error()

def typeError(varName):

    print("ERROR: Incompatible Type With", symTable[varName][0])
    exit()

def error():
    if iNextToken < len(tokenStream):
        print ("Error: Invalid expression. Error location: <",\
            tokenStream[iNextToken], ",", lexemeStream[iNextToken], ">.")
    else:
        print("Error: Incomplete expression. Expecting more terms.")
    exit()

def declarationError(varName):
    print("ERROR: Unknown variable", varName)
    exit()

def duplicateError(varName):
    print("ERROR: Variable already declared", varName)
    exit()

if __name__ == "__main__":
    main("file.txt")