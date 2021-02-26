# Fragkathoulas Christos
# 4196
# cs04196
# Panagiotis Katsantas
# 3390
# cs03390

import os


########################
# Lektikos Analyths
########################


def load_file():
    while True:
        try:
            file = open(input("Please type your C-imple file: "), "r")
            return file
        except:
            print("Error: File does not appear to exist. Try again")

start = 0
dig = 1
number = -1
idk = 2
keyIden = -2 # keywordIdentifier
addOperator = -3
mulOperator = -4
groupSymbol = -5
delimiter = -6
asgn = 3
assignment = -7
asgnStop = -8
smaller = 4
larger = 5
relOp = -9 # relOperator
rem = 6
error = -10
stop = -11

#        numbers letters  +-            */           {}()[]       ,;         :        <        >        =           #    " \n\t\r"  #.
states = [[dig,   idk,    addOperator, mulOperator, groupSymbol, delimiter, asgn,    smaller, larger,  relOp,      rem,   start,   stop],  # state 0
          [dig,   number, number,      number,      number,      number,    number,  number,  number,  number,     error, number,  stop],  # state 1
          [idk,   idk,    keyIden,     keyIden,     keyIden,     keyIden,   keyIden, keyIden, keyIden, keyIden,    error, keyIden, stop],  # state 2
          [error, idk,    error,       error,       groupSymbol, error,     error,   error,   error,   assignment, error, asgnStop,stop],  # state 3
          [relOp, relOp,  relOp,       relOp,       relOp,       relOp,     relOp,   error,   relOp,   relOp,      error, relOp,   stop],  # smaller 4
          [relOp, relOp,  relOp,       relOp,       relOp,       relOp,     relOp,   relOp,   relOp,   relOp,      error, relOp,   stop],  # larger 5
          [rem,   rem,    rem,         rem,         rem,         rem,       rem,     rem,     rem,     rem,        start, rem,     rem]    # rem 6
          ]

# !!!!!!!!!! check for double comment !!!!!!

def error_handler(error):
    errors = {"error 30":"Cimple's keywords must be under 30 characters.",
            "error number":"Number out of bounds (-4.294.967.297 ,4.294.967.295)",
            "error Inv Char":"Invalid character: ",
            "error after dot":"Code after '.' character is not acceptable."}


def advance(char, file_counters):
    if char in '\n':
        file_counters[2] = 0  # col
        file_counters[1] += 1  # row
    else:
        file_counters[2] += 1  # col
    file_counters[0] += 1  # code_file_counter


def lexer(file_counters):
    last_word = ""
    comment_counter = 0
    state = start
    while((state != number) and (state != keyIden) and (state != addOperator) and (state != mulOperator) and
          (state != groupSymbol) and (state != delimiter) and (state != asgnStop) and (state != assignment) and 
          (state != relOp) and (state != error) and (state != stop)):
        file.seek(file_counters[0])
        char = file.read(1)
        if (char == ''):
            return last_word, "eof"
        advance(char, file_counters)
        next_state = 0
        if(char in " \n\t\r"):
            print("here")
            next_state = 11
        elif(char.isdigit()):
            next_state = 0
        elif(char.isalpha()):
            next_state = 1
        elif((char == '+') or (char == '-')):
            next_state = 2
        elif((char == '*') or (char == '/')):
            next_state = 3
        elif((char == '{') or (char == '}') or (char == '(') or (char == ')') or (char == '[') or (char == ']')):
            next_state = 4
        elif((char == ',') or (char == ';')):
            next_state = 5
        elif(char == ':'):
            next_state = 6
        elif(char == '<'):
            next_state = 7
        elif(char == '>'):
            next_state = 8
        elif(char == '='):
            next_state = 9
        elif(char == '#'):  # kdkdkd. # askjfdj#
            comment_counter += 1
            next_state = 10
        elif(char in "."):
            next_state = 12
            if(comment_counter != 1):
                last_word += char
                state = states[state][next_state]
                break
        else:
            return last_word, "error Inv Char"

        last_word += char
        state = states[state][next_state]

        print(last_word + " file_counter: " + str(file_counters[0]) + " state: "+ str(state))
        
        if(comment_counter == 2):
            last_word = ""
            comment_counter = 0
        
        if((state == start) and (next_state == 11)):
            last_word = ""

    #------------------- end of automato --------------#

    if((state == keyIden) or (state == number) or (state == asgnStop)):
        file_counters[0] -= 1
        last_word = last_word[:-1]

    #print(last_word + " file_counter: " + str(file_counters[0]) + " state: "+ str(state))

    if(state == keyIden):  # keywordIdentifier
        if(len(last_word) >= 30):
            return last_word, "error 30"
        if(last_word == "program"):
            return last_word, "programtk"
        elif(last_word == "declare"):
            return last_word, "declaretk"
        elif(last_word == "if"):
            return last_word, "iftk"
        elif(last_word == "else"):
            return last_word, "elsetk"
        elif(last_word == "while"):
            return last_word, "whiletk"
        elif(last_word == "switchcase"):
            return last_word, "switchcasetk"
        elif(last_word == "forcase"):
            return last_word, "forcasetk"
        elif(last_word == "incase"):
            return last_word, "incasetk"
        elif(last_word == "case"):
            return last_word, "casetk"
        elif(last_word == "default"):
            return last_word, "defaulttk"
        elif(last_word == "not"):
            return last_word, "nottk"
        elif(last_word == "and"):
            return last_word, "andtk"
        elif(last_word == "or"):
            return last_word, "ortk"
        elif(last_word == "function"):
            return last_word, "functiontk"
        elif(last_word == "procedure"):
            return last_word, "proceduretk"
        elif(last_word == "call"):
            return last_word, "calltk"
        elif(last_word == "return"):
            return last_word, "returntk"
        elif(last_word == "in"):
            return last_word, "intk"
        elif(last_word == "inout"):
            return last_word, "inouttk"
        elif(last_word == "input"):
            return last_word, "inputtk"
        elif(last_word == "print"):
            return last_word, "printtk"
        else:
            return last_word, "keywordtk" # oxi desmevmenes lekseis
    elif(state == addOperator):
        return last_word, "addOperatortk"
    elif(state == mulOperator):
        return last_word, "mulOperatortk"
    elif(state == groupSymbol):
        return last_word, "groupSymboltk"
    elif(state == delimiter):
        return last_word, "delimitertk"
    elif(state == assignment):
        return last_word, "asignementtk"
    elif(state == relOp):
        return last_word, "relOperatortk"
    elif(last_word.isdigit()):
        if((int(last_word) < -4294967297) or (int(last_word) > 4294967295)):
            return last_word, "error number"
        else:
            return last_word, "numbertk"
    else:
        #print("dot" + last_word)
        #if(file.read(200) != None):
           # print("error")
           # return "","error after dot"
        #else:
        #print("last_word_" + last_word)
        eop = True
        print(eop)
        return last_word, "endtk"


file_counters = [0, 1, 0]  # code_file_counter, row, col
file = load_file()
word, tk = lexer(file_counters)
eop = False
if(tk != "endtk"):
     eop = True
while((tk != "endtk") and (tk != "eof")):
    print("------------------------------------------------ "+ word)
    word, tk = lexer(file_counters)
    if(tk != "endtk"):
        eop = True
print("------------------------------------------------ "+ word + tk)
    #print(word + " file_counter: " + str(file_counters[0]) + " state: "+ str(tk))
word, tk = lexer(file_counters)
print("tk " + tk)
print(eop)
#if((eop) and (tk != "endtk")):
#    print("error")
#    error_handler("error after dot")
