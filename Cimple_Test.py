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
word, token, variables, temp, elseflag, whileflag, var_counter,program_name,function_names,var,counter_blocks = "","", list(), "", 0, 0, 0, "",[],"",0
main_framelenght, main_start_quad = -1, -1
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
                        file.close()
                        sys.exit("Code / Comments after '.' character is/are not acceptable. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                        ",column: " +(str(file_counters[4] -1)))
                    else:
                        print("System exited successfully!")
                        ##########Code exits#########
            else:
                if(comment_counter != 1):         
                    file.close()
                    sys.exit("Invalid character: "+ char +". Error at line: "+str(int((file_counters[1] + 1) / 2))+      #invalid char is not in last_word. so... -1
                    ",column: " +(str(file_counters[4] -1)))
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
                file.close()
                sys.exit("Cimple's keywords must be under 30 characters. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(last_word))))
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
                file.close()
                sys.exit("Number out of bounds (-4.294.967.297 ,4.294.967.295). Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            else:
                return last_word, "numbertk"
        elif(state == stop):
                return last_word, "stoptk"
        else:
            return last_word, "errortk"
    else:
        file.close()
        sys.exit("System exited successfully!")

#==================================================================
#           Start of Syntaktikos Analyths
#==================================================================

#============ PROGRAM =================
def program(file_counters):
    global word,token,program_name

    if(token == "programtk"):
        word, token = lexer(file_counters)
        print(word+" "+token)
        
        if(token == "keywordtk"):
            program_name = word + "_"
            word, token = lexer(file_counters)
            print(word+" "+token)
            block(file_counters,program_name)
        else:
            file.close()
            if(word in strict_words):
                sys.exit("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as program name.'Strict words' like '"+word+"' are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            elif(token == "numbertk"):
                sys.exit("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as program name. Numbers are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            else:
                sys.exit("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as program name. Symbols like '"+word+"' are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            
    else:
        file.close()
        sys.exit("Keyword 'program' was expected in order to start the program.Although '"+word+"' found.\nError at line: "+str(file_counters[1])+
            ",column: " +(str(file_counters[4] - len(word))))  
#============ PROGRAM  ====================

#============ BLOCK ================
def block(file_counters,name):
    global word,token,temp,quadList,program_name, quads, objects_list,main_obj,counter_blocks,main_start_quad,main_framelenght

    counter_blocks += 1

    declarations(file_counters)
    subprograms(file_counters)

    nextquad()
    if('_' in name):    
        quadList.append(genquad(quads,"begin_block",name[:-1],"",""))
        main_start_quad = quads + 1
    else:
        quadList.append(genquad(quads,"begin_block",name,"",""))
        main_obj.pinakas_symvolwn[main_obj.scope-1][-1].set_start_quad(quads+1)

    statements(file_counters)
    if(name == program_name):
        nextquad()
        quadList.append(genquad(quads,"halt","","",""))

    nextquad()
    if('_' in name):
        name = name[:-1]
        main_framelenght = main_obj.offsets[0] + 4
    quadList.append(genquad(quads,"end_block",name,"",""))

    counter_blocks -= 1
   
    if(len(main_obj.offsets) >= 2):
        objects_list[len(objects_list) -1].set_framelength(main_obj.offsets[len(objects_list)-1] + 4)
        

    main_obj.print()
    main_obj.remove_scope()
    del objects_list[-1]
#============ BLOCK ================

#============ DECLARATIONS ================  
def declarations(file_counters):
    global word,token,temp


    while(token == "declaretk"):
        word, token = lexer(file_counters)
        print(word+" "+token)
        varlist(file_counters)
        
        if(word != ';'):
            file.close()
            sys.exit("Syntax Error. Keyword ';' was expected at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))) +" in order to finish the declarations of variables")
        if(word == ';'):
            word, token = lexer(file_counters)
            print(word+" "+token)
#============ DECLARATIONS ================  

#============ VARLIST =====================
def varlist(file_counters):
    global word,token,variables,main_obj
    count_vars, count_commas = 0, 0

    if(token == "keywordtk"):

        i = main_obj.Search(word,main_obj.scope)
        if (i != -1):
            file.close()
            sys.exit("Variable name '"+word+"' already in use. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
        
        main_obj.change_offset()
        var = Variable(word, main_obj.offsets[main_obj.scope])
        main_obj.append(var)

        count_vars += 1
        variables.append(word)
        addVars(word)
        word, token = lexer(file_counters)
        print(word+" "+token)
        if((word != ',') and (word != ';')):
            file.close()
            sys.exit("Keyword ',' was expected at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))) +" in order to declare more than one variables")
    else:
        illegal_variables()

    while(word == ','):
        count_commas += 1
        word, token = lexer(file_counters)
        print(word+" "+token)
        if(token == "keywordtk"):

            i = main_obj.Search(word,main_obj.scope)
            if (i != -1):
                file.close()
                sys.exit("Variable name '"+word+"' already in use. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))

            main_obj.change_offset()
            var = Variable(word, main_obj.offsets[main_obj.scope])
            main_obj.append(var)

            word, token = lexer(file_counters)
            print(word+" "+token)
            if(word == ';'):
                break
            elif(word != ','):
                file.close()
                sys.exit("Keyword ',' was expected at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))) +" in order to declare more than one variables")
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
    global word, token,temp,quadList,objects_list,main_obj
    id = ""
    if(token == "functiontk"):
        word, token = lexer(file_counters)
        print(word+" "+token)
        if(token == "keywordtk"):

            i = main_obj.Search(word)
            if i!=-1:
                file.close()
                sys.exit("Function name '"+word+"' already in use. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))  

            id = word
            function_names.append(id)

            function_obj = Function(id)
            objects_list.append(function_obj)

            main_obj.append(function_obj)
            main_obj.add_scope()


            word, token = lexer(file_counters)
            print(word+" "+token)

            if(word == '('):
                word, token = lexer(file_counters)
                print(word+" "+token)
                formalparlist(file_counters, function_obj)
            
                if(word == ')'):
                    word, token = lexer(file_counters)
                    print(word+" "+token)
                    temp = "subprograms"   #connects subprogram with statements
            
                    block(file_counters,id)

                    temp = ""
                    return True
                else:
                    file.close()
                    sys.exit("Syntax Error. Keyword ')' expected here in order to finish function's parameteres list. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                    ",column: " +(str(file_counters[4] - len(word))))  
            else:
                file.close()
                sys.exit("Syntax Error. Keyword '(' expected here in order to start function's parameteres list. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))  
        else:
            illegal_function_names("function")
    elif(token == "proceduretk"):
        word, token = lexer(file_counters)
        print(word+" "+token)
        if(token == "keywordtk"):

            i = main_obj.Search(word)
            if i!=-1:
                file.close()
                sys.exit("Procedure name '"+word+"' already in use. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))

            id = word
            function_names.append(id)

            function_obj = Function(id)
            objects_list.append(function_obj)

            main_obj.append(function_obj)
            main_obj.add_scope()
            
            word, token = lexer(file_counters)
            print(word+" "+token)
            if(word == '('):
                word, token = lexer(file_counters)
                print(word+" "+token)
                formalparlist(file_counters, function_obj)
        
                if(word == ')'):
                    word, token = lexer(file_counters)
                    print(word+" "+token)
                    temp = "subprograms"    #connects subprogram with statements


                    block(file_counters,id)

                    temp = ""
                    return True
                else:
                    file.close()
                    sys.exit("Syntax Error. Keyword ')' expected here in order to finish procedure's parameteres list. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                    ",column: " +(str(file_counters[4] - len(word))))  
            else:
                file.close()
                sys.exit("Syntax Error. Keyword '(' expected here in order to start procedure's parameteres list. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
        else:
            illegal_function_names("procedure")
    else:
        return False
#============ SUBPROGRAM ===================

#============ FORMALPARLIST ================

def formalparlist(file_counters, function_obj):
    global word, token
    if((token == "intk") or (token == "inouttk")):
        formalparitem(file_counters, function_obj)

        while(word == ','):
            word, token = lexer(file_counters)
            print(word+" "+token)
            formalparitem(file_counters, function_obj)
            if(word != ')'):
                if(word != ','):
                    file.close()
                    sys.exit("Keyword ',' was expected at line: "+str(int((file_counters[1] + 1) / 2))+
                    ",column: " +(str(file_counters[4] - len(word))) +" in order to add more parameters")
#============ FORMALPARLIST ================

#============ FORMALPARITEM ================
def formalparitem(file_counters, function_obj):
    global word, token,quadList, quads, main_obj
    if(token == "intk"):

        arg = Argument("in")
        function_obj.add_argument(arg)

        word, token = lexer(file_counters)
        print(word+" "+token)
        if(token == "keywordtk"):              
          
            main_obj.change_offset()
            ##par = Parameter(word,"CV",main_obj.offsets[len(main_obj.offsets)-1])
            par = Parameter(word,"CV",main_obj.offsets[main_obj.scope])
            main_obj.append(par)

            word, token = lexer(file_counters)
            print(word+" "+token)
        else:
            file.close()
            sys.exit("Syntax Error. Only keywords like ([a..z] or [a..z][A..Z] or [a..z][A..Z][0..9]) are allowed as function parameters. Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
    elif(token == "inouttk"):

        arg = Argument("inout")
        function_obj.add_argument(arg)

        word, token = lexer(file_counters)
        print(word+" "+token)
        if(token == "keywordtk"):
                        
            main_obj.change_offset()
            par = Parameter(word,"REF",main_obj.offsets[main_obj.scope])
            main_obj.append(par)

            word, token = lexer(file_counters)
            print(word+" "+token)
        else:
            file.close()
            if(word in strict_words):
                sys.exit("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as variable names.'Strict words' like '"+word+"' are not acceptable here. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            elif(token == "numbertk"):
                sys.exit("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as variable names. Numbers are not acceptable here. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            else:
                sys.exit("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as variable names. Symbols like '"+word+"' are not acceptable here. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
    else:
        file.close()
        sys.exit("Syntax Error. Keyword 'in' or 'inout' was expected here. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
#============ FORMALPARITEM ================

#============ STATEMENTS ===================   
def statements(file_counters):
    global word, token, temp, elseflag,counter_blocks

    if(token == "begintk"):
        word, token = lexer(file_counters)
        print(word+" "+token)

        statement(file_counters)


        while(word == ';'):
            word, token = lexer(file_counters)
            print(word+" "+token)
            statement(file_counters)


            if(token != "endtk"):
                if(word != ';'):
                    file.close()
                    sys.exit("Syntax Error. Keyword ';' was expected at line: "+str(int((file_counters[1] + 1) / 2))+
                    ",column: " +(str(file_counters[4] - len(word))) +" in order to add one more statement")
        
        if(token == "endtk"):
            word, token = lexer(file_counters)
            print(word+" "+token)

            if(token == "declaretk"):
                file.close()
                sys.exit("Syntax Error. Wrong program structure! The valid structure for the program is 1.declarations (if any)\n\
2. functions (if any) and 3. statements (if any). Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))

        else:
            file.close()
            if(token == "declaretk"):
                sys.exit("Syntax Error. Wrong program structure! The valid structure for the program is 1.declarations (if any)\n\
2. functions (if any) and 3. statements (if any). Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
            else:
                sys.exit("Syntax Error. Keyword '}' expected here in order to finish statement/s. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
        
    else:   #///////// one statement //////////

        statement(file_counters)
        
        if(word != ';'):
            file.close()
            sys.exit("Syntax error. Keyword ';' was expected at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))) +" in order to finish with the statements")
        
        word, token = lexer(file_counters)
        print(word+" "+token)
        '''if(((word == ';') and (elseflag > 0))):
            pass
        else:
            word, token = lexer(file_counters)
            print(word+" "+token)

        elseflag -= 1
        if(elseflag < 0):
            elseflag = 0'''

        if((temp != "subprograms") and (counter_blocks ==0) and ((token == "functiontk") or (token == "proceduretk"))):
            file.close()
            sys.exit("Syntax Error. Wrong program structure! The valid structure for the program is 1.declarations (if any)\n\
2. functions (if any) and 3. statements (if any). Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
        elif(token == "declaretk"):
            file.close()
            sys.exit("Syntax Error. Wrong program structure! The valid structure for the program is 1.declarations (if any)\n\
2. functions (if any) and 3. statements (if any). Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
#============ STATEMENTS ==================  

#============ STATEMENT ===================   
def statement(file_counters):
    global word,token

    if(token == "keywordtk"):
        asgnStat(file_counters)
    elif(token == "iftk"):
        word, token = lexer(file_counters)
        print(word+" "+token)
        ifStat(file_counters)
    elif(token == "whiletk"):
        word, token = lexer(file_counters)
        print(word+" "+token)
        whileStat(file_counters)
    elif(token == "switchcasetk"):
        word, token = lexer(file_counters)
        print(word+" "+token)
        switchcaseStat(file_counters)
    elif(token == "forcasetk"):
        word, token = lexer(file_counters)
        print(word+" "+token)
        forcaseStat(file_counters)
    elif(token == "incasetk"):
        word, token = lexer(file_counters)
        print(word+" "+token)
        incaseStat(file_counters)
    elif(token =="calltk"):
        word, token = lexer(file_counters)
        print(word+" "+token)
        callStat(file_counters)
    elif(token == "returntk"):
        word, token = lexer(file_counters)
        print(word+" "+token)
        returnStat(file_counters)
    elif(token == "inputtk"):
        word, token = lexer(file_counters)
        print(word+" "+token)
        inputStat(file_counters)
    elif(token == "printtk"):
        word, token = lexer(file_counters)
        print(word+" "+token)
        printStat(file_counters)
    elif(word in strict_words and (word != "function" and word!="procedure" and word != "declare")):
        file.close()
        sys.exit("Syntax Error. Statements can not start with 'Strict words' like '"+word+"'. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
    elif(token == "numbertk"):
        file.close()
        sys.exit("Syntax Error. Statements can not start with a number. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
    elif(word in "():=+-*/[]<=>=<>"):
        file.close()
        sys.exit("Syntax Error. Statements can not start with symbols like '"+word+"'. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
#============ STATEMENT ===================   

#============ ASGNSTAT ===================
def asgnStat(file_counters):
    global word, token,quadList,quads

    if(token == "keywordtk"):
        z = word

        word, token = lexer(file_counters)
        print(word+" "+token)

        if(token == "asignementtk"):
            word, token = lexer(file_counters)
            print(word+" "+token)

            exp = expression(file_counters)

            nextquad()
            quadList.append(genquad(quads,":=",exp,"",z))

        else:
            file.close()
            if(word in strict_words):
                sys.exit("Syntax Error. Keyword ':=' excpected here. 'Strict words' like '"+word+"' are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            elif(token == "numbertk"):
                sys.exitt("Syntax Error. Keyword ':=' excpected here. Numbers are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            elif(token == "keywordtk"):
                sys.exit("Syntax Error. ':=' excpected here. Keyword '"+word+"' is not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            else:
                sys.exit("Syntax Error. Keyword ':=' excpected here. Symbols like '"+word+"' are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
    else:
        file.close()
        if(word in strict_words):
            sys.exit("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as variable names.'Strict words' like '"+word+"' are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
        elif(token == "numbertk"):
            sys.exit("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as variable names. Numbers are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
        else:
            sys.exit("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as variable names. Symbols like '"+word+"' are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
#============ ASGNSTAT ===================

#============ IFSTAT ===================
def ifStat(file_counters):
    global word, token,quadList,quads

    if(word == '('):

        word, token = lexer(file_counters)
        print(word+" "+token)

        B = condition(file_counters)

        Btrue = B[0]
        Bfalse = B[1]

        if(word == ')'):
            
            word, token = lexer(file_counters)
            print(word+" "+token)

            backpatch(Btrue,quads + 1)
            statements(file_counters)
            ifList = makelist(nextquad())
            quadList.append(genquad(quads,"jump","","",""))
            backpatch(Bfalse,quads + 1)

            print(word+" "+token)
            elsepart(file_counters)
            backpatch(ifList,quads + 1)
        else:
            file.close()
            sys.exit("Syntax Error. Keyword ')' expected here in order to finish return condition. Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
    else:
        file.close()
        sys.exit("Syntax Error. Keyword '(' expected here in order to start if condition. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
#============ IFSTAT ===================

#============ ELSEPART ===================
def elsepart(file_counters):
    global word, token, elseflag

    if(token == "elsetk"):
        word, token = lexer(file_counters)
        print(word+" "+token)
        #elseflag += 1
        statements(file_counters)# 8a epistrefei epomeno
#============ ELSEPART ===================

#============ WHILESTAT ===================
def whileStat(file_counters):
    global word, token, whileflag,quadList, quads

    if(word == '('):

        word, token = lexer(file_counters)
        print(word+" "+token)

        Bquad = quads+1
        B = condition(file_counters)

        Btrue = B[0]
        Bfalse = B[1]

        if(word == ')'):
            word, token = lexer(file_counters)
            print(word+" "+token)

            whileflag += 1

            backpatch(Btrue,quads + 1)
            statements(file_counters)
            nextquad()
            quadList.append(genquad(quads,"jump","","",Bquad))
            backpatch(Bfalse,quads + 1)
            
        else:
            file.close()
            sys.exit("Syntax Error. Keyword ')' expected here in order to finish while condition. Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
    else:
        file.close()
        sys.exit("Syntax Error. Keyword '(' expected here in order to start while condition. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
#============ WHILESTAT ===================

#============ SWITCHCASESTAT ===================
def switchcaseStat(file_counters):
    global word, token, quadList, quads

    exitlist = emptylist()
    
    if(token != "casetk"):
        file.close()
        sys.exit("Syntax Error. Keyword 'case' excpected here in order to start switchcase statement. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))

    while(token == "casetk"):
        word, token = lexer(file_counters)
        print(word+" "+token)

        if(word == '('):

            word, token = lexer(file_counters)
            print(word+" "+token)

            C = condition(file_counters)
            CondTrue = C[0]
            CondFalse = C[1]

            if(word == ')'):
                
                word, token = lexer(file_counters)
                print(word+" "+token)

                backpatch(CondTrue,quads + 1)
                statements(file_counters)

                e = makelist(nextquad())
                quadList.append(genquad(quads,"jump","","",""))
                merge(exitlist,e)
                backpatch(CondFalse,quads + 1)
            else:
                file.close()
                sys.exit("Syntax Error. Keyword ')' expected here in order to finish case condition. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))

        else:
            file.close()
            sys.exit("Syntax Error. Keyword '(' expected here in order to start case condition. Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
    
    if(token == "defaulttk"):
        word, token = lexer(file_counters)
        print(word+" "+token)

        statements(file_counters)
        backpatch(exitlist,quads + 1)
    else:
        file.close()
        sys.exit("Syntax Error. Keyword 'case' excpected here in order to finish switchcase statement. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
#============ SWITCHCASESTAT ===================

#============ FORCASESTAT ===================
def forcaseStat(file_counters):
    global word, token, quadList, quads

    if(token != "casetk"):
        file.close()
        sys.exit("Syntax Error. Keyword 'case' excpected here in order to start forcase statement. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))

    p1Quad = quads + 1

    while(token == "casetk"):
        word, token = lexer(file_counters)
        print(word+" "+token)

        if(word == '('):
            word, token = lexer(file_counters)
            print(word+" "+token)

            C = condition(file_counters)

            if(word == ')'):
                word, token = lexer(file_counters)
                print(word+" "+token)

                CondTrue = C[0]
                CondFalse = C[1]
                
                backpatch(CondTrue,quads + 1)

                statements(file_counters)

                quadList.append(genquad(quads,"jump","","",p1Quad))
                backpatch(CondFalse,quads + 1)
            else:
                file.close()
                sys.exit("Syntax Error. Keyword ')' expected here in order to finish case condition. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
        else:
            file.close()
            sys.exit("Syntax Error. Keyword '(' expected here in order to start case condition. Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))

    if(token == "defaulttk"):
        word, token = lexer(file_counters)
        print(word+" "+token)

        statements(file_counters)
    else:
        file.close()
        sys.exit("Syntax Error. Keyword 'case' excpected here in order to finish forcase statement. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
#============ FORCASESTAT ===================   

#============ INCASESTAT ===================
def incaseStat(file_counters):
    global word, token, quadList, quads,main_obj

    if(token != "casetk"):
        file.close()
        sys.exit("Syntax Error. Keyword 'case' excpected here in order to start forcase statement. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))

    w = newtemp()
    p1Quad = nextquad()
    quadList.append(genquad(quads,":=","1","",w))

    main_obj.change_offset()
    temp_var_obj = Temp_Variable(w,main_obj.offsets[main_obj.scope])
    main_obj.append(temp_var_obj)

    while(token == "casetk"):
        word, token = lexer(file_counters)
        print(word+" "+token)

        if(word == '('):

            word, token = lexer(file_counters)
            print(word+" "+token)

            C = condition(file_counters)

            if(word == ')'):                
                word, token = lexer(file_counters)
                print(word+" "+token)

                CondTrue = C[0]
                CondFalse = C[1]
                
                backpatch(CondTrue,nextquad())
                genquad(quads,":=","0","",w)

                statements(file_counters)

                backpatch(CondFalse,quads + 1)

            else:
                file.close()
                sys.exit("Syntax Error. Keyword ')' expected here in order to finish case condition. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
        else:
            file.close()
            sys.exit("Syntax Error. Keyword '(' expected here in order to start case condition. Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))

    quadList.append(genquad(nextquad(),":=",w,"0",p1Quad))
#============ INCASESTAT ===================

#============ CALLSTAT ====================== 
def callStat(file_counters):
    global word, token

    if(token == "keywordtk"):
        id = word
        word, token = lexer(file_counters)
        print(word+" "+token)

        if(word == '('):
            word, token = lexer(file_counters)
            print(word+" "+token)

            parameters = list()   
            parameters.append('......')  #used for the actualparlist in order to not bind memory for temp_var
            actualparlist(file_counters,id,parameters)

            if(word == ')'):
                
                word, token = lexer(file_counters)
                print(word+" "+token)

            else:
                file.close()
                sys.exit("Syntax Error. Keyword ')' expected here. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
        else:
            file.close()
            sys.exit("Syntax Error. Keyword '(' expected here. Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
    else:
        file.close()
        if(word in strict_words):
            sys.exit("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as function/procedure names.'Strict words' like '"+word+"' are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
        elif(token == "numbertk"):
            sys.exit("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as function/procedure names. Numbers are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
        else:
            sys.exit("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as function/procedure names. Symbols like '"+word+"' are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word)))) 
#============ CALLSTAT ======================

#============ RETURNSTAT ===================  
def returnStat(file_counters):
    global word,token,quadList, quads

    if(word == '('):
        word, token = lexer(file_counters)
        print(word+" "+token)

        e = expression(file_counters)

        nextquad()
        quadList.append(genquad(quads,"retv",e,"",""))


        if(word == ')'):
            word, token = lexer(file_counters)
            print(word+" "+token)
        else:
            file.close()
            sys.exit("Syntax Error. Keyword ')' expected here in order to finish return statement. Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
    else:
        file.close()
        sys.exit("Syntax Error. Keyword '(' expected here in order to start return statement. Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
#============ RETURNSTAT ======================

#============ INPUTSTAT =======================
def inputStat(file_counters):
    global word, token,quadList,quads

    if(word == '('):
        word, token = lexer(file_counters)
        print(word+" "+token)

        if(token == "keywordtk"):
            nextquad()
            quadList.append(genquad(quads,"inp",word,"",""))

            word, token = lexer(file_counters)
            print(word+" "+token)

            if(word == ')'):
                word, token = lexer(file_counters)
                print(word+" "+token)

            else:
                file.close()
                sys.exit("Syntax Error. Keyword ')' expected here in order to finish input statement. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
        else:
            file.close()
            if(word in strict_words):
                sys.exit("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as variables.'Strict words' like '"+word+"' are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            elif(token == "numbertk"):
                sys.exit("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as variables. Numbers are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            else:
                sys.exit("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as variables. Symbols like '"+word+"' are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
    
    else:
        file.close()
        sys.exit("Syntax Error. Keyword '(' expected here in order to start input statement. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
#============ INPUTSTAT ======================

#============ PRINTSTAT ======================
def printStat(file_counters):
    global word, token, quadList, quads

    if(word == '('):
        word, token = lexer(file_counters)
        print(word+" "+token)

        e = expression(file_counters)

        nextquad()
        quadList.append(genquad(quads,"out",e,"",""))

        if(word == ')'):
            
            word, token = lexer(file_counters)
            print(word+" "+token)
        else:
            file.close()
            sys.exit("Syntax Error. Keyword ')' expected here in order to finish print statement. Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
    else:
        file.close()
        sys.exit("Syntax Error. Keyword '(' expected here in order to start print statement. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
#============ PRINTSTAT ======================

#============ ACTUALPARLIST ===================
def actualparlist(file_counters,function_name,parameters):
    global word, token,quadList, quads, main_obj
    flag = token
    insout, commas = 0, 0
    ret = ""
    caller = True

    if parameters != []:
        caller = False

    if((token == "intk") or (token == "inouttk")):
        insout += 1
        word, token = lexer(file_counters)
        print(word+" "+token)

        ret = actualparitem(file_counters,flag,insout,commas,parameters)

        if(word != ','):
            if((token == "intk") or (token == "inouttk")):
                file.close()
                sys.exit("Syntax Error. Keyword ',' was expected at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))) +" in order to add more parameters")
        while(word == ','):
            commas += 1
            word, token = lexer(file_counters)
            flag = token
            
            ret += actualparitem(file_counters,flag,insout,commas,parameters)
            if(word == ')'):
                break
            elif(word != ','):
                file.close()
                sys.exit("Syntax Error. Keyword ',' was expected at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))) +" in order to add more parameters") 

        if(function_name in function_names):
            w = newtemp()

            if caller == True:
                main_obj.change_offset()
                temp_var_obj = Temp_Variable(w,main_obj.offsets[main_obj.scope])
                main_obj.append(temp_var_obj) 

            parameters.append(["par",w,"RET"])
            parameters.append(["call",function_name,""])

            ret = w
        
    return ret
#============ ACTUALPARLIST ===================

#============ ACTUALPARITEM ===================
def actualparitem(file_counters,flag,insout,commas,parameters):
    global word, token,quadList, quads
    listappend = ""
    e = ""

    if(flag == "intk"):
        if(insout <= commas):
            word, token = lexer(file_counters)
            print(word+" "+token)

        e = expression(file_counters)

        parameters.append(["par",e,"CV"])

    elif(flag == "inouttk"):

        if(insout <= commas):
            word, token = lexer(file_counters)
            print(word+" "+token)
            
        if(token == "keywordtk"):
            e = word
            word, token = lexer(file_counters)
            print(word+" "+token)

            parameters.append(["par",e,"REF"])

        else:
            file.close()
            sys.exit("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as procedure parameters. Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
    else:
        file.close()
        sys.exit("Syntax Error. Keyword 'in/inout' was expected at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))) +" in order to add more parameters")
    return e
#============ ACTUALPARITEM ===================

#============ CONDITION =======================
def condition(file_counters):
    global word,token,quads
    
    Q_list = boolterm(file_counters)
    Q_list_true = Q_list[0]
    Q_list_false = Q_list[1]

    while(token == "ortk"):
        word, token = lexer(file_counters)
        print(word+" "+token)

        backpatch(Q_list[1],quads + 1)
        Q_list = boolterm(file_counters)
        Q_list_true = merge(Q_list_true, Q_list[0])
        Q_list_false = Q_list[1]
        
    tmp = list()
    tmp.append(Q_list_true)
    tmp.append(Q_list_false)
        
    release_list(Q_list)
    return tmp
#============ CONDITION =======================

#============ BOOLTERM =======================
def boolterm(file_counters):
    global word,token,quads

    Q_list = boolfactor(file_counters)
    Q_list_true = Q_list[0]
    Q_list_false = Q_list[1]


    while(token == "andtk"):
        word, token = lexer(file_counters)
        print(word+" "+token)
        
        backpatch(Q_list[0],quads + 1)
        Q_list = boolfactor(file_counters)
        Q_list_false = merge(Q_list_false, Q_list[1])
        Q_list_true = Q_list[0]
    
    tmp = list()
    tmp.append(Q_list_true)
    tmp.append(Q_list_false)
        
    release_list(Q_list)
    return tmp
#============ BOOLTERM =======================

#============ BOOLFACTOR =======================
def boolfactor(file_counters):
    global word,token, quadList, quads

    if(token == "nottk"):
        word, token = lexer(file_counters)
        print(word+" "+token)

        if(word == '['):
            word, token = lexer(file_counters)
            print(word+" "+token)
            c = condition(file_counters)
            
            tmp = c[0]
            c[0] = c[1]
            c[1] = tmp

            if(word == ']'):
                word, token = lexer(file_counters)
                print(word+" "+token)

                return c
            else:
                file.close()
                if(word in strict_words):
                    sys.exit("Syntax Error. Keyword ']' excpected here. 'Strict words' like '"+word+"' are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                    ",column: " +(str(file_counters[4] - len(word))))
                elif(token == "numbertk"):
                    sys.exit("Syntax Error. Keyword ']' excpected here. Numbers are not acceptable heree.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                    ",column: " +(str(file_counters[4] - len(word))))
                elif(token == "keywordtk"):
                    sys.exit("Syntax Error. Keyword ']' excpected here. Keyword are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                    ",column: " +(str(file_counters[4] - len(word))))
                else:
                    sys.exit("Syntax Error. Keyword ']' excpected here. Symbols like '"+word+"' are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                    ",column: " +(str(file_counters[4] - len(word))))
        else:
            file.close()
            if(word in strict_words):
                sys.exit("Syntax Error. Keyword '[' excpected here. 'Strict words' like '"+word+"' are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            elif(token == "numbertk"):
                sys.exit("Syntax Error. Keyword '[' excpected here. Numbers are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            elif(token == "keywordtk"):
                sys.exit("Syntax Error. Keyword '[' excpected here. Keyword are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            else:
                sys.exit("Syntax Error. Keyword '[' excpected here. Symbols like '"+word+"' are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))

    elif(word == '['):
        word, token = lexer(file_counters)
        print(word+" "+token)
        c = condition(file_counters)

        if(word == ']'):
            word, token = lexer(file_counters)
            print(word+" "+token)
            return c
        else:
            file.close()
            if(word in strict_words):
                sys.exit("Syntax Error. Keyword ']' excpected here. 'Strict words' like '"+word+"' are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            elif(token == "numbertk"):
                sys.exit("Syntax Error. Keyword ']' excpected here. Numbers are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            elif(token == "keywordtk"):
                sys.exit("Syntax Error. Keyword ']' excpected here. Keyword are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            else:
                sys.exit("Syntax Error. Keyword ']' excpected here. Symbols like '"+word+"' are not acceptable here.Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
    #expression
    else:
        
        e1 = expression(file_counters)
        

        if(token == "relOperatortk"):
            op = word
            word, token = lexer(file_counters)
            print(word+" "+token)

            e2 = expression(file_counters)

            R_true = makelist(nextquad())
            quadList.append(genquad(quads,op,e1,e2,""))
            R_false = makelist(nextquad())
            quadList.append(genquad(quads,"jump","","",""))

            tmp = list()
            tmp.append(R_true)
            tmp.append(R_false)
            return tmp
        else:
            file.close()
            if(word in strict_words):
                sys.exit("Syntax Error. Operator '= | <= | >= | > | < | <>' excpected here. 'Strict words' like '"+word+"' are not acceptable here. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            elif(token == "numbertk"):
                sys.exit("Syntax Error. Operator '= | <= | >= | > | < | <>' excpected here. Numbers are not acceptable here. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            elif(token == "keywordtk"):
                sys.exit("Syntax Error. Operator '= | <= | >= | > | < | <>' excpected here. Keyword are not acceptable here. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
            else:
                sys.exit("Syntax Error. Operator '= | <= | >= | > | < | <>' excpected here. Symbols like '"+word+"' are not acceptable here. Error at line: "+str(int((file_counters[1] + 1) / 2))+
                ",column: " +(str(file_counters[4] - len(word))))
#============ BOOLFACTOR =======================

#============ EXPRESION =======================
def expression(file_counters):
    global word,token, quadList, quads,main_obj

    optionalSign(file_counters)


    t1 = term(file_counters)

    while(token == "addOperatortk"):
        op = word
        
        word, token = lexer(file_counters)
        print(word+" "+token)

        t2 = term(file_counters)

        w = newtemp()
        nextquad()
        quadList.append(genquad(quads,op,t1,t2,w))      #endiamesou
        t1 = w

        main_obj.change_offset()
        temp_var_obj = Temp_Variable(w,main_obj.offsets[main_obj.scope])
        main_obj.append(temp_var_obj)

    return t1  
#============ EXPRESION =================== 

#============ TERM ======================== 
def term(file_counters):
    global word,token, quadList, quads, main_obj

    f1 = factor(file_counters)
    
    while(token == "mulOperatortk"):
        mul = word

        word, token = lexer(file_counters)
        print(word+" "+token)

        f2 = factor(file_counters)
        w = newtemp()
        nextquad()
        quadList.append(genquad(quads,mul,f1,f2,w))
        f1 = w

        main_obj.change_offset()
        temp_var_obj = Temp_Variable(w,main_obj.offsets[main_obj.scope])
        main_obj.append(temp_var_obj)

    return f1

#============ TERM ===================== 

#============ FACTOR =================== 
def factor(file_counters):
    global word,token
    ret = ""

    if(token == "numbertk"):
        ret = word
        word, token = lexer(file_counters)
        print(word+" "+token)
       
    
    elif(word == '('):
        word, token = lexer(file_counters)
        print(word+" "+token)

        ret = expression(file_counters)
        
        
        if(word == ')'):
            word, token = lexer(file_counters)
            print(word+" "+token)

        else:
            file.close()
            sys.exit("Syntax Error. Keyword ')' expected here in order to finish expresion. Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))
    
    elif(token == "keywordtk"): 

        i = main_obj.Search(word)
        if i==-1:
            file.close()
            sys.exit("Keyword '"+word+"' unidentified. Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word)))) 


        ret = word
        word, token = lexer(file_counters)
        print(word+" "+token)
        e = idtail(file_counters,ret)
        if(e != ""):
            ret = e

    #Errors below
    elif(word in strict_words):
        file.close()
        sys.exit("Syntax Error. Strict words' like '"+word+"' are not acceptable as factors. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
    elif(word in ")[]}{:=+-/<=>=*"):
        file.close()
        sys.exit("Syntax Error. Symbols like '"+word+"' are not acceptable here. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
        
    if(ret == ""):
        file.close()
        sys.exit("Syntax Error. Statement can not be none. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
        
    return ret
#============ FACTOR ===================    

#============ IDTAIL ===================
def idtail(file_counters,function_name):
    global word,token
    ret = ""
    
    if((token == "intk") or (token =="inouttk")):
        file.close()
        sys.exit("Syntax Error. Keyword '(' expected here. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
    elif(word in strict_words):
        file.close()
        sys.exit("Syntax Error. Strict words' like '"+word+"' are not acceptable as factors. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
    elif(word == '('):
        word, token = lexer(file_counters)
        print(word+" "+token) 

    
        parameters = list()

        ret = actualparlist(file_counters,function_name,parameters)

        if(word == ')'):
            word, token = lexer(file_counters)
            print(word+" "+token)

            #print(parameters)
            for q in parameters:

                nextquad()
                quadList.append(genquad(quads,q[0],q[1],q[2],""))
        
        else:
            file.close()
            sys.exit("Syntax Error. Keyword ')' expected here. Error at line: "+str(int((file_counters[1] + 1) / 2))+
            ",column: " +(str(file_counters[4] - len(word))))

    return ret
#============ IDTAIL =========================

#============ OPTIONALSIGN ===================
def optionalSign(file_counters):
    global word, token

    if(token == "addOperatortk"):
    	word, token = lexer(file_counters)
    	print(word+" "+token)
#============ OPTIONALSIGN ===================


#======================================================================
#                   Error Handler Methods
#======================================================================

# Illegal variable names for VarList method
def illegal_variables():
    global word,token,variables
    file.close()
    if(word in strict_words):
        sys.exit("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as variable names. 'Strict words' like '"+word+"' are not acceptable as variable names.Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
    elif(token == "numbertk"):
        sys.exit("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as variable names. Numbers are not acceptable as variable names.Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
    else:
        sys.exit("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as variable names. Symbols like '"+word+"' are not acceptable as variable names.Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))

# Illegal function names for Subprogram method
def illegal_function_names(functionOrProcedure):
    global word,token,variables
    
    file.close()
    if(word in strict_words):
        sys.exit("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as variable names.'Strict words' like '"+word+"' are not acceptable as "+functionOrProcedure+" names. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
    elif(token == "numbertk"):
        sys.exit("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as variable names. Numbers are not acceptable as "+functionOrProcedure+" names. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
    else:
        sys.exit("Syntax Error. Only keywords like ([a-zA-Z][a-zA-Z0-9]*) are allowed as variable names. Symbols like '"+word+"' are not acceptable as "+functionOrProcedure+" names. Error at line: "+str(int((file_counters[1] + 1) / 2))+
        ",column: " +(str(file_counters[4] - len(word))))
#======================================================================
#                   Error Handler Methods
#======================================================================

#======================================================================
#                   End of Syntaktikos Analyths
#======================================================================


#======================================================================
#                   Endiamesos Kwdikas
#======================================================================
quads = -1

quadList = list()

def nextquad():
    global quads
    quads += 1
    return quads

def genquad(index,op,x,y,z):
    quad = [index,op,x,y,z]
    return quad

def newtemp():
    global var_counter
    var = "T_"
    var = var + str(var_counter)
    var_counter += 1
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
    for ptr_quad in list:
        quadList[ptr_quad][4] = z

def addVars(temp):
    global var

    if var != "":
        var += ","+str(temp)
    else:
        var += ""+str(temp)

def write_quads_to_file():
    global quadList

    with open("quadList.txt","w") as filehandle:
        for quad in quadList:
            filehandle.write('%s\n' %quad)


def endiamesos_kwdikas():
    global quadList, function_names,var_counter

    if function_names == []:  
        for v in range(0,var_counter):
            va = "T_"+str(v)
            addVars(va)

        with open("endiamesos.c","w") as filehandle:
            filehandle.write("int main()\n{\n")
            filehandle.write("\tint %s;\n" %var)
            for quad in quadList:
                if quad[0] == 0:
                    filehandle.write('\tL_0:\n')
                    continue
                if ":=" in quad:
                    filehandle.write('\tL_%s: %s = %s;\t//%s\n' %(quad[0],quad[4],quad[2],quad[1:]))
                    continue
                if ("+" in quad) or ("-" in quad) or ("*" in quad) or ("/" in quad):
                    filehandle.write('\tL_%s: %s = %s %s %s;\t//%s\n' %(quad[0],quad[4],quad[2],quad[1],quad[3],quad[1:]))
                    continue
                if ("<" in quad) or (">" in quad) or ("<>" in quad) or ("<=" in quad)  or ("=" in quad) or (">=" in quad):
                    filehandle.write('\tL_%s: if(%s %s %s) goto L_%s;\t//%s\n' %(quad[0],quad[2],quad[1],quad[3],quad[4],quad[1:]))
                    continue
                if "jump" in quad:
                    filehandle.write('\tL_%s: goto L_%s;\t//%s\n' %(quad[0],quad[4],quad[1:]))
                    continue
                if "halt" in quad:
                    filehandle.write('\tL_%s: {} \n' %quad[0])
                    continue
            filehandle.write("}")

#======================================================================
#                   End of Endiamesos Kwdikas
#======================================================================

#======================================================================
#                   Pinakas Symvolwn
#======================================================================

class ps:
    pinakas_symvolwn = [[]]
    scope = 0
    offset = 0
    offsets = []

    def __init__(self):
        self.pinakas_symvolwn[0].append("0")
        self.offsets.append(8)

    def append(self,record):
        self.pinakas_symvolwn[self.scope].append(record)
    
    def change_offset(self):
        self.offsets[self.scope] += 4
    
    def add_scope(self):
        self.scope += 1
        self.offsets.append(8)
        self.pinakas_symvolwn.append([str(self.scope)])

    def remove_scope(self):
        del self.pinakas_symvolwn[self.scope]
        del self.offsets[self.scope]
        self.scope -= 1

    def print(self):
        for row in self.pinakas_symvolwn:
            k = row[0]
            for j in range(1,len(row)):
                k += " ["+ row[j].get()+"] "
            print(k)    

    def Search(self,name,scope=-1):
        if scope != -1:
            row = self.pinakas_symvolwn[scope]
            for i in range(1,len(row)):
                if name == row[i].getName():
                    return row[i].getName()
            #print("Entity '"+name+"' not found")
            return -1
        else:   
            for row in self.pinakas_symvolwn:
                for j in range(1,len(row)):
                    print(row[j].getName()+ " "+ name)
                    if name == row[j].getName():
                        return row[j].getName()
            #print("Entity '"+name+"' not found")
            return -1

class Variable:
    name = ""
    offset = 0

    def __init__(self,name,offset):
        self.name = name
        self.offset = offset

    def getName(self):
        return self.name

    def get(self):
        return(self.name+" "+ str(self.offset))
    

class Function:
    name = ""
    list_argument = []
    framelength = 0
    start_quad = -1

    def __init__(self,name):
        self.name = name
        self.list_argument = []
        self.framelength = 0
        self.start_quad = -1

    def set_start_quad(self,start_quad):
        self.start_quad = start_quad
        
    def set_framelength(self,framelength):
        self.framelength = framelength
    
    def add_argument(self,argument):
        self.list_argument.append(argument.get())

    def getName(self):
        return self.name

    def get(self):
        if self.list_argument == []:
             return(self.name)
        else:
            listToStr = ', '.join([str(elem) for elem in self.list_argument])
            return(self.name+" "+ str(self.start_quad)+" {"+listToStr+"} "+ str(self.framelength))

class Parameter:
    name = ""
    parMode = ""
    offset = 0

    def __init__(self, name, parMode, offset):
        self.name = name
        self.parMode = parMode
        self.offset = offset
    
    def getName(self):
        return self.name 
    
    def get(self):
        return (self.name+" "+self.parMode+" "+str(self.offset))
    
class Temp_Variable:
    name = ""
    offset = 0

    def __init__(self, name, offset):
        self.name = name
        self.offset = offset

    def getName(self):
        return self.name
    
    def get(self):
        return (self.name+" "+str(self.offset))
    
class Argument:
    name = ""

    def __init__(self,name):
        self.name = name

    def get(self):
        return (self.name+" ")

#==================== MAIN ============================================
if(len(sys.argv) < 2):
    sys.exit("Error: No file given!")
elif(len(sys.argv) > 2):
    sys.exit("More than one files given!")
else:
    file = open(sys.argv[1], "r")


word, token = lexer(file_counters)
print(word+" "+token)

main_obj = ps()
objects_list = list()
objects_list.append(main_obj)

program(file_counters)
print(quadList)

write_quads_to_file()
endiamesos_kwdikas()

print()
main_obj.print()

print(str(main_start_quad) +" "+ str(main_framelenght))