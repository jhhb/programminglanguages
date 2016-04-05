__author__ = 'jamesboyle'
import sys
import string

##this program takes a command line argument text file

def main():

    textFile = readFile()

    splitted = textFile #puts the textfile into a string

    myList = splitted.split("\n")   #split by newline which helps us remove comments

    lexemeList, commentList = moveComments(myList)  #moveComments returns a list of Comments and a list of lexemes

    testString = ' '.join(lexemeList)   #separate the parts of our lexemeList by spaces

    stringListToUse = breakUpLine(testString)   #returns us a new string with all of the lexemes space separated
                                                #so we dont have to deal with different kinds of spacing, etc.

    stringListToUse = stringListToUse.split()   #finally split the space separated string into a List

    lastList = fixBlankChars(stringListToUse)   #this makes it so two ' ' denoting a blank char are recognized as
                                                #charLiteral

    parseFile(lastList)  #parseFile goes through and prints every lexeme and matching token


#concatenates blank chars into ''
def fixBlankChars(thisList):


    finalList = []

    for d in range(0, len(thisList)):

        if thisList[d] == "'":
            if thisList[d+1] == "'":
                finalList.append("' '")
        else:
            finalList.append(thisList[d])

    return finalList


#this reads the file in from a directory with one command line argument, i.e., the input text file.
#so to run, CD to the correct working directory, then say python lexical.py [myfile.txt]
def readFile():

    with open(sys.argv[1], "r") as f:
        myFileString = f.read()

    return myFileString

#checks if something is an int by seeing if it is only digits
def isIntLiteral(lexeme):

    isInt = True

    for i in range(0, len(lexeme)):
        if lexeme[i].isdigit() is False:
            isInt = False

    return isInt


#checks if something is Float by seeing if you get two IntLiterals when you split by '.'
def isFloatLiteral(lexeme):

    if "." in lexeme:
        intList = lexeme.split(".")

        if intList[0].isdigit() and intList[1].isdigit() is True and len(intList) is 2:
            return True


    return False

#checks if something is Char Literal by saying if it is not anything else (e.g. not print, return, etc., or any
#of the single characters, it is a char literal.

def isCharLiteral(lexeme):


    printable = string.printable

    for z in range (0, len(printable)):
        temp = "'"+printable[z]+"'"

        if temp == lexeme:
            return True

    if lexeme == "''":
        return True

    return False


#This function goes through a given string and makes it so every token is separated by only a single space.
def breakUpLine(aString):

    stringToSplit = aString

    myString = ''

    for d in range(len(stringToSplit)):

        if stringToSplit[d] == "<" and stringToSplit[d+1] != "=":
                myString = myString + " < "

        elif stringToSplit[d] == ">" and stringToSplit[d+1] != "=":
                myString = myString + " > "

        elif stringToSplit[d] == "=" and stringToSplit[d-1] != "!" and stringToSplit[d-1] != "<" and stringToSplit[d-1] != ">" and stringToSplit[d-1] != "=" and stringToSplit[d+1] != "=":
                myString = myString + " = "

        else:
            myString = myString + stringToSplit[d]

    myString = myString.replace("+", " + ")
    myString = myString.replace("-", " - ")
    myString = myString.replace("==", " == ")
    myString = myString.replace("!=", " != ")
    myString = myString.replace(">=", " >= ")
    myString = myString.replace("<=", " <= ")
    myString = myString.replace("*", " * ")
    myString = myString.replace("/", " / ")
    myString = myString.replace(";", " ; ")
    myString = myString.replace("(", " ( ")
    myString = myString.replace(")", " ) ")
    myString = myString.replace("{", " { ")
    myString = myString.replace("}", " } ")
    myString = myString.replace("[", " [ ")
    myString = myString.replace("]", " ] ")

    return myString

#this function checks if something is an ID by seeing if the first character is alpha and if all others are alnum
def isId(lexeme):

    isId = True

    for i in range (0, len(lexeme)):
        if lexeme[i].isalnum() is False:
            isId = False

    if lexeme[0].isalpha() is False:
        isId = False

    return isId

#this function goes through a file (a list) and removes all comments by finding where there are //, and then
#slicing that string into two, and appending them to different lists.

#moves comments into a separate list
def moveComments(myList):

    commentList = []
    lexemeList = []

    for q in range(0, len(myList)):

        lexemeString = ''
        commentString = ''

        toParse = myList[q]

        alreadyAppended = False

        for r in range(0, len(toParse) -1):

            if toParse[r] == "/":
                if toParse[r+1] == "/":
                    lexemeString = toParse[:r]
                    commentString = toParse[r:]

                    if(lexemeString != ""):
                        lexemeList.append(lexemeString)
                        alreadyAppended = True

                    if(commentString != ""):
                        commentList.append(commentString)


        if alreadyAppended == False:
            lexemeList.append(myList[q])

    return lexemeList, commentList

#this function is a long list of if elifs that prints output according to the specification
def parseFile(wordList):

    for lexeme in wordList:

        if lexeme == "main":
            print("main" + "\t"+ lexeme)

        elif lexeme == "int" or lexeme =="char" or lexeme == "float" or lexeme == "bool":
            print("type" + "\t" + lexeme)

        elif isId(lexeme) is True  and (lexeme != "print" and lexeme != "return" and lexeme != "if"
                                        and lexeme != "else" and lexeme != "while" and lexeme != "true"
                                        and lexeme != "false"):
            print("id" + "\t" + lexeme)

        elif isIntLiteral(lexeme) is True:
            print("intLiteral" + "\t" + lexeme)

        elif isFloatLiteral(lexeme) is True:
            print("floatLiteral" + "\t" + lexeme)

        elif isCharLiteral(lexeme) is True:
            print("charLiteral" + "\t" + lexeme)

        elif lexeme == "true" or lexeme == "false":
            print("boolLiteral" + "\t" + lexeme)

        elif lexeme == "==" or lexeme == "!=":
            print("equOp" + "\t" + lexeme)

        elif lexeme == "<" or lexeme == "<=" or lexeme == ">" or lexeme == ">=":
            print("relOp" + "\t" + lexeme)

        elif lexeme == ("="):
            print("assignOp" + "\t" + lexeme)

        elif lexeme == ("if"):
            print("if" + "\t" + lexeme)

        elif lexeme == ("else"):
            print("else" + "\t" + lexeme)

        elif lexeme == ("while"):
            print("while" + "\t" + lexeme)

        elif lexeme == "+" or lexeme == "-":
            print("addOp" + "\t" + lexeme)

        elif lexeme == "*" or lexeme == "/":
            print("multOp" + "\t" + lexeme)

        elif lexeme == (";"):
            print(";" + "\t" + lexeme)

        elif lexeme == ("("):
            print("(" + "\t" + lexeme)

        elif lexeme == (")"):
            print(")" + "\t" + lexeme)

        elif lexeme == ("{"):
            print("{" + "\t" + lexeme)

        elif lexeme == ("}"):
            print("}" + "\t" + lexeme)

        elif lexeme == ("["):
            print("[" + "\t" + lexeme)

        elif lexeme == ("]"):
            print("]" + "\t" + lexeme)

        #comments go into my commentList at the beginning of the document

        elif lexeme == "return":
            print("return" + "\t" + lexeme)

        elif lexeme == "print":
            print("print" + "\t" + lexeme)

        else:
            print("unknown" + "\t" + lexeme)

if __name__ == "__main__":
    main()