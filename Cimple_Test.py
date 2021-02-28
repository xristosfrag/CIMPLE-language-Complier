# Fragkathoulas Christos
# 4196
# cs04196
# Panagiotis Katsantas
# 3390
# cs03390

import sys

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


#------------Variables-----------
file_counters = [0, 1, 1, False, 1]  # code_file_counter, row, col
file = load_file()
word, token, variables = "","", list()
strict_words = ["program","declare","if","else","while","switchcase","incase","case","default","not","and","or",
                "procedure","call","return","in","inout","input","print","function"]
#----------------------------------

def advance(char, file_counters):
    file_counters[0] += 1  # code_file_counter
    file_counters[2] += 1  # col
    file_counters[4] += 1  # temporary column. It take the value '1' when file_counters[2]=1 (this happens when char = '\n' and lexer reads next char)
    if(file_counters[2] == 1):
        #tmp = file_counters[2]
        file_counters[4] = 2
    if(char == '\n'):
        file_counters[2] = 0  # col
        file_counters[1] += 1  # row
        file_counters[4] += 1
        
    print("row = "+str(file_counters[1]))
    print("col = "+str(file_counters[2])+" coltmp: "+str(file_counters[4]))

def lexer(file_counters):
    last_word = ""
    if(file_counters[3] != True):
        comment_counter = 0
        state = start
        while((state != number) and (state != keyIden) and (state != addOperator) and (state != mulOperator) and
            (state != groupSymbol) and (state != delimiter) and (state != asgnStop) and (state != assignment) and 
            (state != relOp) and (state != error) and (state != stop)):
            file.seek(file_counters[0])
            char = file.read(1)
            advance(char, file_counters)
            next_state = 0
            if(char in " \n\t\r"):
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
                    file_counters[3] = True
            else:
                print("Invalid character: "+ char)
                file.close()
                sys.exit()
            last_word += char
            state = states[state][next_state]
            
            if(comment_counter == 2): #end of comments
                last_word = ""
                comment_counter = 0
            
            # delete white characters
            if((state == start) and (next_state == 11)):
                last_word = ""

        #------------------- end of automato --------------#

        if((state == keyIden) or (state == number) or (state == asgnStop)): #final states.
            file_counters[0] -= 1
            file_counters[2] -= 1
            if(file_counters[2] < 0):
                file_counters[2] = 0
            file_counters[4] -= 1
            if(last_word[-1] == '\n'):
                print("it goes back")
                file_counters[1] -= 1
            if((not last_word[-1].isalpha()) and (not last_word[-1].isdigit())):
                last_word = last_word[:-1]
            
            print("!row = "+str(file_counters[1]))
            print("!col = "+str(file_counters[2]))


        if(state == keyIden):  # keywordIdentifier
            if(len(last_word) >= 30):
                print("Cimple's keywords must be under 30 characters.")
                file.close()
                sys.exit()
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
            if(last_word == '{'):
                return last_word, "begintk"
            return last_word, "groupSymboltk"
        elif(state == delimiter):
            return last_word, "delimitertk"
        elif(state == assignment):
            return last_word, "asignementtk"
        elif(state == asgnStop):
            return last_word, "asgntk"
        elif(state == relOp):
            return last_word, "relOperatortk"
        elif(last_word.isdigit()):
            if((int(last_word) < -4294967297) or (int(last_word) > 4294967295)):
                print("Number out of bounds (-4.294.967.297 ,4.294.967.295)")
                file.close()
                sys.exit()
            else:
                return last_word, "numbertk"
        else:
                return last_word, "endtk"
    else:
        if(file.read(200) not in " "):
            print("Code after '.' Character is not acceptable.")
            file.close()
            sys.exit()
        else:
            print("System exited successfully!")
            file.close()
            sys.exit()

#==================================================================
#   Syntax Analysis
#==================================================================

#============ PROGRAM =================
def program():
    global word,token
    if(token == "programtk"):
        word, token = lexer(file_counters)
        print(word+" "+token)
        if(token == "keywordtk"):
            word, token = lexer(file_counters)
            print(word+" "+token)
            block()
        else:
            print("Program name expected. Although '"+word+"' found.\nError at line: "+str(file_counters[1])+
            ",column: " +(str(file_counters[4] - len(word))))
            file.close()
            sys.exit()
    else:
        print("Keyword 'program' was expected in order to start the program.Although '"+word+"' found.\nError at line: "+str(file_counters[1])+
            ",column: " +(str(file_counters[4] - len(word))))
        file.close()
        sys.exit()
#============ PROGRAM  ====================

#============ BLOCK ================
def block():
    global word,token
    declarations()
    print(variables)
    #subprograms()
    statements()
#============ BLOCK ================

#============ STATEMENTS ================   
def statements():
    global word,token
    if(token == "begintk"):
        word, token = lexer(file_counters)
        print(word+" "+token)
        #sequence()
        if(token == "endtk"):
            word, token = lexer(file_counters)
            print(word+" "+token)
        else:
            print("Keyword '.' was expected in order to end program. Although '"+word+"' found.\nError at line: "+str(file_counters[1])+
            ",column: " +(str(file_counters[4] - len(word))))
            file.close()
            sys.exit()
    else:
        print("Keyword '{' was expected. Although '"+word+"' found.\nError at line: "+str(file_counters[1])+
            ",column: " +(str(file_counters[4] - len(word))))
        file.close()
        sys.exit()
#============ STATEMENTS ================  

#============ DECLARATIONS ================  
def declarations():
    global word,token
    if(token == "declaretk"):
        word, token = lexer(file_counters)
        print(word+" "+token)
        varlist()
        
        if(word != ';'):
            print("Keyword ';' was expected at line: "+str(file_counters[1])+
            ",column: " +(str(file_counters[4] - len(word))) +" in order to finish the declarations of variables")
            file.close()
            sys.exit()
    else:
        if(token == "numbertk"):
            print("Numbers are only acceptable in function block or main block.\nError at line: "+str(file_counters[1])+
            ",column: " +(str(file_counters[4] - len(word))))

        elif(token == "keywordtk"):
            print("Keywords are unacceptable at this point of code. Error at line: "+str(file_counters[1])+
            ",column: " +(str(file_counters[4] - len(word))))
        elif(word in strict_words[:-1]):
            print("'Strict words' except from (declare) are not acceptable in function block or main block.\nError at line: "
            +str(file_counters[1]) + ",column: " +(str(file_counters[4] - len(word))))
            
        elif((token == "addOperatortk") or (token == "mulOperatortk") or (token == "groupSymboltk") or (token == "asgntk")
            or (token == "asignementtk") or (token == "smallertk") or (token == "largertk") or (token == "relOperatortk")):
            print("Symbols like '"+word+"' are only acceptable in function block or main block.\nError at line: "+str(file_counters[1])+
            ",column: " +(str(file_counters[4] - len(word))))
            
        elif((word == ';') or (word == ',')):
            print("Symbol "+word+" is unacceptable at this point of code. Error at line: "+str(file_counters[1])+
            ",column: " +(str(file_counters[4] - len(word))))

        file.close()
        sys.exit()

# declare x,y;
#============ DECLARATIONS ================  

#============ VARLIST ================
def varlist():
    global word,token,variables

    if(token == "keywordtk"):
        variables.append(word)
        word, token = lexer(file_counters)
        print(word+" "+token)
        if((word != ',') and (word != ';')):
            print("Keyword ',' was expected at line: "+str(file_counters[1])+
            ",column: " +(str(file_counters[4] - len(word))) +" in order to declare more than one variables")
            file.close()
            sys.exit()
    else:
        illegal_variables()

    while(word == ','):
        word, token = lexer(file_counters)
        print(word+" "+token)
        if(token == "keywordtk"):
            variables.append(word)
            word, token = lexer(file_counters)
            print(word+" "+token)
            if(word == ';'):
                break
            elif(word != ','):
                print("Keyword ',' was expected at line: "+str(file_counters[1])+
                ",column: " +(str(file_counters[4] - len(word))) +" in order to declare more than one variables")
                file.close()
                sys.exit()
            else:
                continue
        else:
            illegal_variables()

#============ VARLIST ================


# Illegal variable names for VarList method
def illegal_variables():
    global word,token,variables
    if(word in strict_words):
        print("'Strict words'like '"+word+"' are not acceptable as variable names.Error at line: "+str(file_counters[1])+
        ",column: " +(str(file_counters[4] - len(word))))
    elif(token == "numbertk"):
        print("Numbers are not acceptable as variable names.Error at line: "+str(file_counters[1])+
        ",column: " +(str(file_counters[4] - len(word))))
    else:
        print("Symbols like '"+word+"' are not acceptable as variable names.Error at line: "+str(file_counters[1])+
        ",column: " +(str(file_counters[4] - len(word))))
    file.close()
    sys.exit()


#==================== MAIN ================
word, token = lexer(file_counters)
print(word+" "+token)
program()