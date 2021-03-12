# Fragkathoulas Christos
# 4196
# cs04196
# Panagiotis Katsantas
# 3390
# cs03390

import sys

#=============================================================
#                   Lektikos Analyths
#=============================================================
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

#        numbers letters  +-            */           {}()[]       ,;         :        <        >        =           #      " \n\t\r"  #.
states = [[dig,   idk,    addOperator, mulOperator, groupSymbol, delimiter, asgn,    smaller, larger,  relOp,      rem,     start,   stop],  # start 0
          [dig,   number, number,      number,      number,      number,    number,  number,  number,  number,     number,  number,  stop],  # dig 1
          [idk,   idk,    keyIden,     keyIden,     keyIden,     keyIden,   keyIden, keyIden, keyIden, keyIden,    keyIden, keyIden, stop],  # idk 2
          [error, idk,    error,       error,       groupSymbol, error,     error,   error,   error,   assignment, error,   asgnStop,stop],  # asgn 3
          [relOp, relOp,  relOp,       relOp,       relOp,       relOp,     relOp,   error,   relOp,   relOp,      error,   relOp,   stop],  # smaller 4
          [relOp, relOp,  relOp,       relOp,       relOp,       relOp,     relOp,   relOp,   relOp,   relOp,      error,   relOp,   stop],  # larger 5
          [rem,   rem,    rem,         rem,         rem,         rem,       rem,     rem,     rem,     rem,        start,   rem,     rem]    # rem 6
          ]


#------------Variables-----------
file_counters = [0, 1, 1, False, 1]  # code_file_counter, row, col, 
word, token, variables, ins, inouts, temp, elseflag, whileflag, var_counter = "","", list(), list(), list(), "", 0, 0, 0
strict_words = ["program","declare","if","else","while","switchcase","incase","case","default","not","and","or",
                "procedure","call","return","in","inout","input","print","function"]
#----------------------------------

def advance(char, file_counters):
    file_counters[0] += 1  # code_file_counter
    file_counters[2] += 1  # col
    file_counters[4] += 1  # temporary column. It take the value '1' when file_counters[2]=1 (this happens when char = '\n' and lexer reads next char)
    if(file_counters[2] == 1):
        file_counters[4] = 2

    if((char == "\n") and (char != '\t') and (char != '\r') and (char != '')):
        file_counters[2] = 0  # col
        file_counters[1] += 1  # row
        file_counters[4] += 1

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
            elif(char == '#'): 
                comment_counter += 1
                next_state = 10
            elif(char in "."):
                next_state = 12
                if(comment_counter != 1):
                    if(file.read(200) not in " "):
                        print("Code / Comments after '.' character is/are not acceptable. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                        ",column: " +(str(file_counters[4] -1)))
                        file.close()
                        sys.exit()
                    else:
                        print("System exited successfully!")
                        file.close()
                        sys.exit()
            else:
                if(comment_counter != 1):
                    print("Invalid character: "+ char +". Error at line: "+str(int((file_counters[1] + 1) / 2))+
                    ",column: " +(str(file_counters[4] -1)))           #invalid char is not in last_word. so... -1
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

        if((state == keyIden) or (state == number) or (state == asgnStop) or ((state == relOp) and (last_word[-1] != '=') and (last_word != "<>"))): #final states.
            file_counters[0] -= 1
            file_counters[2] -= 1
            if(file_counters[2] < 0):
                file_counters[2] = 0
            file_counters[4] -= 1
            if(last_word[-1] == '\n'):
                file_counters[1] -= 1
            if((not last_word[-1].isalpha()) and (not last_word[-1].isdigit()) or (state == relOp)):
                last_word = last_word[:-1]

        


        if(state == keyIden):  # keywordIdentifier
            if(len(last_word) > 30):
                print("Cimple's keywords must be under 30 characters. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(last_word))))
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
            elif(last_word == '}'):
                return last_word, "endtk"
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
                print("Number out of bounds (-4.294.967.297 ,4.294.967.295). Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
                file.close()
                sys.exit()
            else:
                return last_word, "numbertk"
        elif(state == stop):
                return last_word, "stoptk"
        else:
            return last_word, "errortk"
    else:
        print("System exited successfully!")
        file.close()
        sys.exit()

#==================================================================
#           Start of Syntaktikos Analyths
#==================================================================

#============ PROGRAM =================
def program(file_counters):
    global word,token
    program_name = ""
    if(token == "programtk"):
        word, token = lexer(file_counters)
        print(word+" "+token)
        if(token == "keywordtk"):
            program_name = word
            word, token = lexer(file_counters)
            print(word+" "+token)
            block(file_counters,program_name)
        else:
            if(word in strict_words):
                print("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as program name.'Strict words' like '"+word+"' are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            elif(token == "numbertk"):
                print("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as program name. Numbers are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            else:
                print("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as program name. Symbols like '"+word+"' are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
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
def block(file_counters,program_name):
    global word,token,temp

    declarations(file_counters)
    subprograms(file_counters)
    if(program_name != ""):
        genquad("begin_block",program_name,"","")
    statements(file_counters)
    if(program_name != ""):
        genquad("halt","","","")
        genquad("end_block",program_name,"","")
#============ BLOCK ================

#============ DECLARATIONS ================  
def declarations(file_counters):
    global word,token,temp


    while(token == "declaretk"):
        word, token = lexer(file_counters)
        print(word+" "+token)
        varlist(file_counters)
        
        if(word != ';'):
            print("Syntax Error. Keyword ';' was expected at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))) +" in order to finish the declarations of variables")
            file.close()
            sys.exit()
        if(word == ';'):
            word, token = lexer(file_counters)
            print(word+" "+token)
#============ DECLARATIONS ================  

#============ VARLIST =====================
def varlist(file_counters):
    global word,token,variables
    count_vars, count_commas = 0, 0

    if(token == "keywordtk"):
        count_vars += 1
        variables.append(word)
        word, token = lexer(file_counters)
        print(word+" "+token)
        if((word != ',') and (word != ';')):
            print("Keyword ',' was expected at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))) +" in order to declare more than one variables")
            file.close()
            sys.exit()
    else:
        illegal_variables()

    while(word == ','):
        count_commas += 1
        word, token = lexer(file_counters)
        print(word+" "+token)
        if(token == "keywordtk"):
            variables.append(word)
            word, token = lexer(file_counters)
            print(word+" "+token)
            if(word == ';'):
                break
            elif(word != ','):
                print("Keyword ',' was expected at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))) +" in order to declare more than one variables")
                file.close()
                sys.exit()
            else:
                continue
        else:
            illegal_variables()

#============ VARLIST ====================

#============ SUBPROGRAMS ================  

def subprograms(file_counters):
    global word, token
    sub = True
    while(sub):
        sub = subprogram(file_counters)
        
#============ SUBPROGRAMS ================  

#============ SUBPROGRAM ================= 
def subprogram(file_counters):
    global word, token,temp
    id = ""
    if(token == "functiontk"):
        word, token = lexer(file_counters)
        print(word+" "+token)
        if(token == "keywordtk"):
            id = word
            word, token = lexer(file_counters)
            print(word+" "+token)
            if(word == '('):
                word, token = lexer(file_counters)
                print(word+" "+token)
                formalparlist(file_counters)
                if(word == ')'):
                    word, token = lexer(file_counters)
                    print(word+" "+token)
                    temp = "subprograms"   #connects subprogram with statements

                    genquad("begin_block",id,"","")
                    block(file_counters,"")
                    genquad("end_block",id,"","")

                    temp = ""
                    return True
                else:
                    print("Syntax Error. Keyword ')' expected here in order to finish function's parameteres list. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                    ",column: " +(str(file_counters[4] - len(word))))
                    file.close()
                    sys.exit()  
            else:
                print("Syntax Error. Keyword '(' expected here in order to start function's parameteres list. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
                file.close()
                sys.exit()  
        else:
            illegal_function_names("function")
    elif(token == "proceduretk"):
        word, token = lexer(file_counters)
        print(word+" "+token)
        if(token == "keywordtk"):
            id = word
            word, token = lexer(file_counters)
            print(word+" "+token)
            if(word == '('):
                word, token = lexer(file_counters)
                print(word+" "+token)
                formalparlist(file_counters)
                if(word == ')'):
                    word, token = lexer(file_counters)
                    print(word+" "+token)
                    temp = "subprograms"    #connects subprogram with statements


                    genquad("begin_block",id,"","")
                    block(file_counters,"")
                    genquad("end_block",id,"","")

                    temp = ""
                    return True
                else:
                    print("Syntax Error. Keyword ')' expected here in order to finish procedure's parameteres list. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                    ",column: " +(str(file_counters[4] - len(word))))
                    file.close()
                    sys.exit()  
            else:
                print("Syntax Error. Keyword '(' expected here in order to start procedure's parameteres list. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
                file.close()
                sys.exit()
        else:
            illegal_function_names("procedure")
    else:
        return False
#============ SUBPROGRAM ===================

#============ FORMALPARLIST ================

def formalparlist(file_counters):
    global word, token
    flag = token
    if((token == "intk") or (token == "inouttk")):
        word, token = lexer(file_counters)
        print(word+" "+token)
        formalparitem(file_counters, flag)

        while(word == ','):
            word, token = lexer(file_counters)
            print(word+" "+token)
            formalparitem(file_counters,flag)
            if(word != ')'):
                if(word != ','):
                    print("Keyword ',' was expected at line: "+str(int((file_counters[1] + 1) / 2))+
                    ",column: " +(str(file_counters[4] - len(word))) +" in order to add more parameters")
                    file.close()
                    sys.exit()
#============ FORMALPARLIST ================

#============ FORMALPARITEM ================
def formalparitem(file_counters,flag):
    global word, token
    if(flag == "intk"):
        if(token == "keywordtk"):
            ins.append(word)
            word, token = lexer(file_counters)
            print(word+" "+token)
        else:
            print("Only keywords like ([a..z] or [a..z][A..Z] or [a..z][A..Z][0..9]) are allowed as function parameters. Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
            file.close()
            sys.exit()
    elif(flag == "inouttk"):
        if(token == "keywordtk"):
            wordreference = [str(word)]
            inouts.append(wordreference)
            word, token = lexer(file_counters)
            print(word+" "+token)
        else:
            if(word in strict_words):
                print("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as variable names.'Strict words' like '"+word+"' are not acceptable here. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            elif(token == "numbertk"):
                print("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as variable names. Numbers are not acceptable here. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            else:
                print("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as variable names. Symbols like '"+word+"' are not acceptable here. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            file.close()
            sys.exit()
#============ FORMALPARITEM ================

#============ STATEMENTS ===================   
def statements(file_counters):
    global word, token, temp, elseflag
    forreturn = ""

    if(token == "begintk"):
        word, token = lexer(file_counters)
        print(word+" "+token)

        forreturn = forreturn +" "+ statement(file_counters)


        while(word == ';'):
            word, token = lexer(file_counters)
            print(word+" "+token)
            forreturn = forreturn +" "+ statement(file_counters)


            if(token != "endtk"):
                if(word != ';'):
                    print("Keyword ';' was expected at line: "+str(int((file_counters[1] + 1) / 2))+
                    ",column: " +(str(file_counters[4] - len(word))) +" in order to add one more statement")
                    file.close()
                    sys.exit()
        
        if(token == "endtk"):
            word, token = lexer(file_counters)
            print(word+" "+token)

            if(token == "declaretk"):
                print("Syntax Error. Wrong program structure! The valid structure for the program is 1.declarations (if any)\n\
2. functions (if any) and 3. statements (if any). Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
                file.close()
                sys.exit()

        else:
            print("Keyword '}' expected here in order to finish statement/s. Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
            file.close()
            sys.exit()
        
    else:   #///////// one statement //////////

        forreturn = forreturn +" "+ statement(file_counters)
        
        if(word != ';'):
            print("Syntax error. Keyword ';' was expected at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))) +" in order to finish with the statements")
            file.close()
            sys.exit()
        
        if(((word == ';') and (elseflag > 0))):
            pass
        else:
            word, token = lexer(file_counters)
            print(word+" "+token)

        elseflag -= 1
        if(elseflag < 0):
            elseflag = 0

        if((temp != "subprograms") and ((token == "functiontk") or (token == "proceduretk"))):
            print("Syntax Error. Wrong program structure! The valid structure for the program is 1.declarations (if any)\n\
2. functions (if any) and 3. statements (if any). Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
            file.close()
            sys.exit()
        elif(token == "declaretk"):
            print("Syntax Error. Wrong program structure! The valid structure for the program is 1.declarations (if any)\n\
2. functions (if any) and 3. statements (if any). Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
            file.close()
            sys.exit()


    return forreturn
#============ STATEMENTS ==================  

#============ STATEMENT ===================   
def statement(file_counters):
    global word,token
    forreturn = ""

    if(token == "keywordtk"):
        forreturn = forreturn +" "+ asgnStat(file_counters)
    elif(token == "iftk"):
        word, token = lexer(file_counters)
        print(word+" "+token)
        forreturn = forreturn +" "+ ifStat(file_counters)
    elif(token == "whiletk"):
        word, token = lexer(file_counters)
        print(word+" "+token)
        forreturn = forreturn +" "+ whileStat(file_counters)
    elif(token == "switchcasetk"):
        word, token = lexer(file_counters)
        print(word+" "+token)
        forreturn = forreturn +" "+ switchcaseStat(file_counters)
    elif(token == "forcasetk"):
        print("edwwwwwwww")
        word, token = lexer(file_counters)
        print(word+" "+token)
        forreturn = forreturn +" "+ forcaseStat(file_counters)
    elif(token == "incasetk"):
        word, token = lexer(file_counters)
        print(word+" "+token)
        forreturn = forreturn +" "+ incaseStat(file_counters)
    elif(token =="calltk"):
        word, token = lexer(file_counters)
        print(word+" "+token)
        forreturn = forreturn +" "+ callStat(file_counters)
    elif(token == "returntk"):
        word, token = lexer(file_counters)
        print(word+" "+token)
        forreturn = forreturn +" "+ returnStat(file_counters)
    elif(token == "inputtk"):
        word, token = lexer(file_counters)
        print(word+" "+token)
        forreturn = forreturn +" "+ inputStat(file_counters)
    elif(token == "printtk"):
        word, token = lexer(file_counters)
        print(word+" "+token)
        forreturn = forreturn +" "+ printStat(file_counters)
    elif(word in strict_words and (word != "function" and word!="procedure" and word != "declare")):
        print("Statements can not start with 'Strict words' like '"+word+"'. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
        file.close()
        sys.exit()
    elif(token == "numbertk"):
        print("Syntax Error. Statements can not start with a number. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
        file.close()
        sys.exit()
    elif(word in "():=+-*/[]<=>=<>"):
        print("Syntax Error. Statements can not start with symbols like '"+word+"'. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
        file.close()
        sys.exit()

    print(forreturn)
    return forreturn
#============ STATEMENT ===================   

#============ ASGNSTAT ===================
def asgnStat(file_counters):
    global word, token
    forreturn = ""

    if(token == "keywordtk"):
        forreturn = forreturn +" "+ word

        word, token = lexer(file_counters)
        print(word+" "+token)

        if(token == "asignementtk"):
            forreturn = forreturn +" "+ word

            word, token = lexer(file_counters)
            print(word+" "+token)
            forreturn = forreturn +" "+ expression(file_counters)
        else:
            if(word in strict_words):
                print("Keyword ':=' excpected here. 'Strict words' like '"+word+"' are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            elif(token == "numbertk"):
                print("Keyword ':=' excpected here. Numbers are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            elif(token == "keywordtk"):
                print("':=' excpected here. Keyword '"+word+"' is not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            else:
                print("Keyword ':=' excpected here. Symbols like '"+word+"' are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            file.close()
            sys.exit()
    else:
        if(word in strict_words):
            print("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as variable names.'Strict words' like '"+word+"' are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
        elif(token == "numbertk"):
            print("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as variable names. Numbers are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
        else:
            print("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as variable names. Symbols like '"+word+"' are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
        file.close()
        sys.exit()

    return forreturn
#============ ASGNSTAT ===================

#============ IFSTAT ===================
def ifStat(file_counters):
    global word, token
    forreturn = ""

    if(word == '('):
        forreturn = forreturn +" "+ word

        word, token = lexer(file_counters)
        print(word+" "+token)

        forreturn = forreturn +" "+ condition(file_counters)

        if(word == ')'):
            forreturn = forreturn +" "+ word
            
            word, token = lexer(file_counters)
            print(word+" "+token)

            forreturn = forreturn +" "+ statements(file_counters)
            print(word+" "+token)
            forreturn = forreturn +" "+ elsepart(file_counters)
        else:
            print("Syntax Error. Keyword ')' expected here in order to finish return condition. Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
            file.close()
            sys.exit()
    else:
        print("Syntax Error. Keyword '(' expected here in order to start if condition. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
        file.close()
        sys.exit()
    
    
    return forreturn
#============ IFSTAT ===================

#============ ELSEPART ===================
def elsepart(file_counters):
    global word, token, elseflag
    forreturn = ""

    if(token == "elsetk"):
        word, token = lexer(file_counters)
        print(word+" "+token)
        elseflag += 1
        forreturn = forreturn +" "+ statements(file_counters)# 8a epistrefei epomeno
        
    
    return forreturn
#============ ELSEPART ===================

#============ WHILESTAT ===================
def whileStat(file_counters):
    global word, token, whileflag
    forreturn = ""

    if(word == '('):
        forreturn = forreturn +" "+ word

        word, token = lexer(file_counters)
        print(word+" "+token)

        forreturn = forreturn +" "+ condition(file_counters)

        if(word == ')'):
            forreturn = forreturn +" "+ word
            
            word, token = lexer(file_counters)
            print(word+" "+token)

            whileflag += 1
            forreturn = forreturn +" "+ statements(file_counters)
        else:
            print("Syntax Error. Keyword ')' expected here in order to finish while condition. Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
            file.close()
            sys.exit()
    else:
        print("Syntax Error. Keyword '(' expected here in order to start while condition. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
        file.close()
        sys.exit()
    
    
    return forreturn
#============ WHILESTAT ===================

#============ SWITCHCASESTAT ===================
def switchcaseStat(file_counters):
    global word, token
    forreturn = ""

    if(token != "casetk"):
        print("Syntax Error. Keyword 'case' excpected here in order to start switchcase statement. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
        file.close()
        sys.exit()

    while(token == "casetk"):
        word, token = lexer(file_counters)
        print(word+" "+token)

        if(word == '('):
            forreturn = forreturn +" "+ word

            word, token = lexer(file_counters)
            print(word+" "+token)

            forreturn = forreturn +" "+ condition(file_counters)

            if(word == ')'):
                forreturn = forreturn +" "+ word
                
                word, token = lexer(file_counters)
                print(word+" "+token)

                forreturn = forreturn +" "+ statements(file_counters)
            else:
                print("Syntax Error. Keyword ')' expected here in order to finish case condition. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
                file.close()
                sys.exit()

            
        else:
            print("Syntax Error. Keyword '(' expected here in order to start case condition. Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
            file.close()
            sys.exit()
    
    if(token == "defaulttk"):
        word, token = lexer(file_counters)
        print(word+" "+token)

        forreturn = forreturn +" "+ statements(file_counters)
    else:
        print("Syntax Error. Keyword 'case' excpected here in order to finish switchcase statement. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
        file.close()
        sys.exit()
    
    return forreturn
#============ SWITCHCASESTAT ===================

#============ FORCASESTAT ===================
def forcaseStat(file_counters):
    global word, token
    forreturn = ""

    if(token != "casetk"):
        print("Syntax Error. Keyword 'case' excpected here in order to start forcase statement. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
        file.close()
        sys.exit()

    while(token == "casetk"):
        word, token = lexer(file_counters)
        print(word+" "+token)

        if(word == '('):
            forreturn = forreturn +" "+ word

            word, token = lexer(file_counters)
            print(word+" "+token)

            forreturn = forreturn +" "+ condition(file_counters)

            if(word == ')'):
                forreturn = forreturn +" "+ word
                
                word, token = lexer(file_counters)
                print(word+" "+token)

                forreturn = forreturn +" "+ statements(file_counters)

            else:
                print("Syntax Error. Keyword ')' expected here in order to finish case condition. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
                file.close()
                sys.exit()
        else:
            print("Syntax Error. Keyword '(' expected here in order to start case condition. Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
            file.close()
            sys.exit()

    if(token == "defaulttk"):
        word, token = lexer(file_counters)
        print(word+" "+token)

        forreturn = forreturn +" "+ statements(file_counters)
    else:
        print("Syntax Error. Keyword 'case' excpected here in order to finish forcase statement. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
        file.close()
        sys.exit()
    
    return forreturn
#============ FORCASESTAT ===================   

#============ INCASESTAT ===================
def incaseStat(file_counters):
    global word, token
    forreturn = ""

    if(token != "casetk"):
        print("Syntax Error. Keyword 'case' excpected here in order to start forcase statement. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
        file.close()
        sys.exit()

    while(token == "casetk"):
        word, token = lexer(file_counters)
        print(word+" "+token)

        if(word == '('):
            forreturn = forreturn +" "+ word

            word, token = lexer(file_counters)
            print(word+" "+token)

            forreturn = forreturn +" "+ condition(file_counters)

            if(word == ')'):
                forreturn = forreturn +" "+ word
                
                word, token = lexer(file_counters)
                print(word+" "+token)

                forreturn = forreturn +" "+ statements(file_counters)

            else:
                print("Syntax Error. Keyword ')' expected here in order to finish case condition. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
                file.close()
                sys.exit()
        else:
            print("Syntax Error. Keyword '(' expected here in order to start case condition. Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
            file.close()
            sys.exit()
    
    return forreturn
#============ INCASESTAT ===================

#============ CALLSTAT ====================== 
def callStat(file_counters):
    global word, token
    forreturn = ""


    if(token == "keywordtk"):
        word, token = lexer(file_counters)
        print(word+" "+token)

        if(word == '('):
            forreturn = forreturn +" "+ word

            word, token = lexer(file_counters)
            print(word+" "+token)

            forreturn = forreturn +" "+ actualparlist(file_counters)

            if(word == ')'):
                forreturn = forreturn +" "+ word
                
                word, token = lexer(file_counters)
                print(word+" "+token)

            else:
                print("Syntax Error. Keyword ')' expected here. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
                file.close()
                sys.exit()
        else:
            print("Syntax Error. Keyword '(' expected here. Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
            file.close()
            sys.exit()
    else:
        if(word in strict_words):
            print("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as function/procedure names.'Strict words' like '"+word+"' are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
        elif(token == "numbertk"):
            print("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as function/procedure names. Numbers are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
        else:
            print("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as function/procedure names. Symbols like '"+word+"' are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
        file.close()
        sys.exit()
    
    return forreturn
#============ CALLSTAT ======================

#============ RETURNSTAT ===================  
def returnStat(file_counters):
    global word,token
    
    forreturn = ""

    if(word == '('):
        forreturn = forreturn +" "+ word
        word, token = lexer(file_counters)
        print(word+" "+token)

        forreturn = forreturn +" "+ expression(file_counters)       

        if(word == ')'):
            forreturn = forreturn +" "+ word
            word, token = lexer(file_counters)
            print(word+" "+token)
        else:
            print("Syntax Error. Keyword ')' expected here in order to finish return statement. Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
            file.close()
            sys.exit()
    else:
        print("Syntax Error. Keyword '(' expected here in order to start return statement. Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
        file.close()
        sys.exit()

    return forreturn
#============ RETURNSTAT ======================

#============ INPUTSTAT =======================
def inputStat(file_counters):
    global word, token
    forreturn = ""

    if(word == '('):
        forreturn = forreturn +" "+ word

        word, token = lexer(file_counters)
        print(word+" "+token)

        if(token == "keywordtk"):
            forreturn = forreturn +" "+ word

            word, token = lexer(file_counters)
            print(word+" "+token)

            if(word == ')'):
                forreturn = forreturn +" "+ word
                
                word, token = lexer(file_counters)
                print(word+" "+token)

            else:
                print("Syntax Error. Keyword ')' expected here in order to finish input statement. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
                file.close()
                sys.exit()
        else:
            if(word in strict_words):
                print("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as variables.'Strict words' like '"+word+"' are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            elif(token == "numbertk"):
                print("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as variables. Numbers are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            else:
                print("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as variables. Symbols like '"+word+"' are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            file.close()
            sys.exit()
    else:
        print("Syntax Error. Keyword '(' expected here in order to start input statement. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
        file.close()
        sys.exit()
    
    return forreturn
#============ INPUTSTAT ======================

#============ PRINTSTAT ======================
def printStat(file_counters):
    global word, token
    forreturn = ""

    if(word == '('):
        forreturn = forreturn +" "+ word

        word, token = lexer(file_counters)
        print(word+" "+token)

        forreturn = forreturn +" "+ expression(file_counters)

        if(word == ')'):
            forreturn = forreturn +" "+ word
            
            word, token = lexer(file_counters)
            print(word+" "+token)
        else:
            print("Syntax Error. Keyword ')' expected here in order to finish print statement. Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
            file.close()
            sys.exit()
    else:
        print("Syntax Error. Keyword '(' expected here in order to start print statement. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
        file.close()
        sys.exit()
    
    return forreturn
#============ PRINTSTAT ======================

#============ ACTUALPARLIST ===================
def actualparlist(file_counters):
    global word, token
    forreturn = ""
    flag = token
    insout, commas = 0, 0

    if((token == "intk") or (token == "inouttk")):
        insout += 1
        forreturn = forreturn +" "+ word
        word, token = lexer(file_counters)
        print(word+" "+token)

        forreturn = forreturn +" "+ actualparitem(file_counters,flag,insout,commas)

        if(word != ','):
            if((token == "intk") or (token == "inouttk")):
                
                print("Syntax Error. Keyword ',' was expected at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))) +" in order to add more parameters")
                file.close()
                sys.exit()
        while(word == ','):
            commas += 1
            forreturn = forreturn +" "+ word
            word, token = lexer(file_counters)
            flag = token
            forreturn = forreturn +" "+ word
            
            forreturn = forreturn +" "+ actualparitem(file_counters,flag,insout,commas)
            if(word == ')'):
                break
            elif(word != ','):
                print("Syntax Error. Keyword ',' was expected at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))) +" in order to add more parameters")
                file.close()
                sys.exit()
    
    return forreturn
#============ ACTUALPARLIST ===================

#============ ACTUALPARITEM ===================
def actualparitem(file_counters,flag,insout,commas):
    global word, token
    forreturn = ""
    listappend = ""

    if(flag == "intk"):
        if(insout <= commas):
            word, token = lexer(file_counters)
            print(word+" "+token)

        forreturn = forreturn +" "+ expression(file_counters)
        listappend = listToString(forreturn)
        ins.append(listappend)

    elif(flag == "inouttk"):

        if(insout <= commas):
            word, token = lexer(file_counters)
            print(word+" "+token)
            
        if(token == "keywordtk"):
            forreturn = forreturn +" "+ word
            word, token = lexer(file_counters)
            print(word+" "+token)

        else:
            print("Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as procedure parameters. Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
            file.close()
            sys.exit()
    else:
        print("Syntax Error. Keyword 'in/inout' was expected at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))) +" in order to add more parameters")
        file.close()
        sys.exit()
    return forreturn
#============ ACTUALPARITEM ===================

#============ CONDITION =======================
def condition(file_counters):
    global word,token
    forreturn = ""

    forreturn = forreturn +" "+ boolterm(file_counters)

    while(token == "ortk"):
        forreturn = forreturn +" "+ word

        word, token = lexer(file_counters)
        print(word+" "+token)
        
        forreturn = forreturn +" "+ boolterm(file_counters)
            
    return forreturn
#============ CONDITION =======================

#============ BOOLTERM =======================
def boolterm(file_counters):
    global word,token
    forreturn = ""

    forreturn = forreturn +" "+ boolfactor(file_counters)

    while(token == "andtk"):
        forreturn = forreturn +" "+ word

        word, token = lexer(file_counters)
        print(word+" "+token)
        
        forreturn = forreturn +" "+ boolfactor(file_counters)
            
    return forreturn
#============ BOOLTERM =======================

#============ BOOLFACTOR =======================
def boolfactor(file_counters):
    global word,token
    forreturn = ""

    if(token == "nottk"):
        forreturn = forreturn +" "+ word

        word, token = lexer(file_counters)
        print(word+" "+token)

        if(word == '['):
            forreturn = forreturn +" "+ word

            word, token = lexer(file_counters)
            print(word+" "+token)
            forreturn = forreturn +" "+ condition(file_counters)

            if(word == ']'):
                forreturn = forreturn +" "+ word

                word, token = lexer(file_counters)
                print(word+" "+token)

            else:
                if(word in strict_words):
                    print("Syntax Error. Keyword ']' excpected here. 'Strict words' like '"+word+"' are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                    ",column: " +(str(file_counters[4] - len(word))))
                elif(token == "numbertk"):
                    print("Syntax Error. Keyword ']' excpected here. Numbers are not acceptable heree.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                    ",column: " +(str(file_counters[4] - len(word))))
                elif(token == "keywordtk"):
                    print("Syntax Error. Keyword ']' excpected here. Keyword are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                    ",column: " +(str(file_counters[4] - len(word))))
                else:
                    print("Syntax Error. Keyword ']' excpected here. Symbols like '"+word+"' are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                    ",column: " +(str(file_counters[4] - len(word))))
                file.close()
                sys.exit()
        else:
            if(word in strict_words):
                print("Syntax Error. Keyword '[' excpected here. 'Strict words' like '"+word+"' are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            elif(token == "numbertk"):
                print("Syntax Error. Keyword '[' excpected here. Numbers are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            elif(token == "keywordtk"):
                print("Syntax Error. Keyword '[' excpected here. Keyword are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            else:
                print("Syntax Error. Keyword '[' excpected here. Symbols like '"+word+"' are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            file.close()
            sys.exit()

    elif(word == '['):
        forreturn = forreturn +" "+ word

        word, token = lexer(file_counters)
        print(word+" "+token)
        forreturn = forreturn +" "+ condition(file_counters)

        if(word == ']'):
                forreturn = forreturn +" "+ word

                word, token = lexer(file_counters)
                print(word+" "+token)

        else:
            if(word in strict_words):
                print("Syntax Error. Keyword ']' excpected here. 'Strict words' like '"+word+"' are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            elif(token == "numbertk"):
                print("Syntax Error. Keyword ']' excpected here. Numbers are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            elif(token == "keywordtk"):
                print("Syntax Error. Keyword ']' excpected here. Keyword are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            else:
                print("Syntax Error. Keyword ']' excpected here. Symbols like '"+word+"' are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            file.close()
            sys.exit()
    #expression
    else:

        forreturn = forreturn +" "+ expression(file_counters)

        if(token == "relOperatortk"):
            forreturn = forreturn +" "+ word

            word, token = lexer(file_counters)
            print(word+" "+token)

            forreturn = forreturn +" "+ expression(file_counters)
        else:
            if(word in strict_words):
                print("Syntax Error. Operator '= | <= | >= | > | < | <>' excpected here. 'Strict words' like '"+word+"' are not acceptable here. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            elif(token == "numbertk"):
                print("Syntax Error. Operator '= | <= | >= | > | < | <>' excpected here. Numbers are not acceptable here. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            elif(token == "keywordtk"):
                print("Syntax Error. Operator '= | <= | >= | > | < | <>' excpected here. Keyword are not acceptable here. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            else:
                print("Syntax Error. Operator '= | <= | >= | > | < | <>' excpected here. Symbols like '"+word+"' are not acceptable here. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            file.close()
            sys.exit()

    return forreturn
#============ BOOLFACTOR =======================

#============ EXPRESION =======================
def expression(file_counters):
    global word,token

    forreturn = ""

    forreturn = forreturn +" "+ optionalSign(file_counters)
    forreturn = forreturn +" "+ term(file_counters)

    while(token == "addOperatortk"):

        forreturn = forreturn +" "+ word
        
        word, token = lexer(file_counters)
        print(word+" "+token)

        forreturn = forreturn +" "+ term(file_counters)


    return forreturn
#============ EXPRESION =================== 

#============ TERM ======================== 
def term(file_counters):
    global word,token

    forreturn = ""

    forreturn = forreturn +" "+ factor(file_counters)
    
    while(token == "mulOperatortk"):
        forreturn = forreturn +" "+ word

        word, token = lexer(file_counters)
        print(word+" "+token)

        forreturn = forreturn +" "+ factor(file_counters)
    
    return forreturn

#============ TERM ===================== 

#============ FACTOR =================== 
def factor(file_counters):
    global word,token
    forreturn = ""

    if(token == "numbertk"):
        forreturn = forreturn +" "+ word
        word, token = lexer(file_counters)
        print(word+" "+token)
    
    elif(word == '('):
        forreturn = forreturn +" "+ word
        word, token = lexer(file_counters)
        print(word+" "+token)

        forreturn = forreturn +" "+ expression(file_counters)
        
        if(word == ')'):
            forreturn = forreturn +" "+ word
            word, token = lexer(file_counters)
            print(word+" "+token)
        else:
            print("Syntax Error. Keyword ')' expected here in order to finish expresion. Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
            file.close()
            sys.exit()
    
    elif(token == "keywordtk"): 
        forreturn = forreturn +" "+ word
        word, token = lexer(file_counters)
        print(word+" "+token)
        forreturn = forreturn +" "+ idtail(file_counters)

    #Errors below
    elif(word in strict_words):
        print("Syntax Error. Strict words' like '"+word+"' are not acceptable as factors. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
        file.close()
        sys.exit()
    elif(word in ")[]}{:=+-/<=>=*"):        
        print("Syntax Error. Symbols like '"+word+"' are not acceptable here. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
        file.close()
        sys.exit()
    if(forreturn == []):
        print("Syntax Error. Statement can not be none. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
        file.close()
        sys.exit()
    else:   
        return forreturn
#============ FACTOR ===================    

#============ IDTAIL ===================
def idtail(file_counters):
    global word,token
    forreturn = ""
    
    if((token == "intk") or (token =="inouttk")):
        print("Syntax Error. Keyword '(' expected here. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
        file.close()
        sys.exit()
    elif(word in strict_words):
        print("100. Strict words' like '"+word+"' are not acceptable as factors. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
        file.close()
        sys.exit()
    elif(word == '('):
        forreturn = forreturn +" "+ word
        word, token = lexer(file_counters)
        print(word+" "+token)

        forreturn = forreturn +" "+ actualparlist(file_counters)

        if(word == ')'):
            forreturn = forreturn +" "+ word
            word, token = lexer(file_counters)
            print(word+" "+token)
            return forreturn
        else:
            print("Syntax Error. Keyword ')' expected here. Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
            file.close()
            sys.exit()

    return forreturn
#============ IDTAIL =========================

#============ OPTIONALSIGN ===================
def optionalSign(file_counters):
    global word, token
    forreturn = ""

    if(token == "addOperatortk"):
    	forreturn = forreturn +" "+ word
    	word, token = lexer(file_counters)
    	print(word+" "+token)
    	return forreturn
    return ""
#============ OPTIONALSIGN ===================


# Function to convert lists to strings
def listToString(s):
	# initialize an empty string 
	str1 = "" 
	# traverse in the string 
	for ele in s: 
		str1 += ele 
	# return string 
	return str1 


#======================================================================
#                   Error Handler Methods
#======================================================================

# Illegal variable names for VarList method
def illegal_variables():
    global word,token,variables
    if(word in strict_words):
        print("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as variable names. 'Strict words' like '"+word+"' are not acceptable as variable names.Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
    elif(token == "numbertk"):
        print("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as variable names. Numbers are not acceptable as variable names.Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
    else:
        print("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as variable names. Symbols like '"+word+"' are not acceptable as variable names.Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
    file.close()
    sys.exit()

# Illegal function names for Subprogram method
def illegal_function_names(functionOrProcedure):
    global word,token,variables
    
    if(word in strict_words):
        print("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as variable names.'Strict words' like '"+word+"' are not acceptable as "+functionOrProcedure+" names. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
    elif(token == "numbertk"):
        print("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as variable names. Numbers are not acceptable as "+functionOrProcedure+" names. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
    else:
        print("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as variable names. Symbols like '"+word+"' are not acceptable as "+functionOrProcedure+" names. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
    file.close()
    sys.exit()
#======================================================================
#                   Error Handler Methods
#======================================================================

#======================================================================
#                   End of Syntaktikos Analyths
#======================================================================


#======================================================================
#                   Endiamesos Kwdikas
#======================================================================
quads = 0

quadList = [][3]

def nextquad():
    global quads
    quads += 1
    return quads

def genquad(op,x,y,z):
    quad = [op,x,y,z]
    return quad

def newtemp():
    global var_counter
    var = "T_"
    var = var + str(var_counter)
    return var

def emptylist():
    emptylist = list()
    return emptylist

def makelist(x):
    tmp_list = list()
    tmp_list.append(x)
    return tmp_list

def merge(list1, list2):
    for x in list2:
        list1.append(x)
    release_list(list2)
    return list1

# delete list from memory
def release_list(a):
    del a[:]
    del a

def backpatch(list, z):
    global quadList
    for ptr in list:
        quadList[ptr][3] = z
















#==================== MAIN ============================================
if(len(sys.argv) < 2):
    sys.exit("Error: No file given!")
elif(len(sys.argv) > 2):
    sys.exit("More than one files given!")
else:
    file = open(sys.argv[1], "r")

word, token = lexer(file_counters)
print(word+" "+token)
program(file_counters)