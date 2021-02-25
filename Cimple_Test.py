# Fragkathoulas Christos
# 4196
# cs04196


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
keywordIdentifier = -2
addOperator = -3
mulOperator = -4
groupSymbol = -5
delimiter = -6
asgn = 3
assignment = -7
smaller = 4
larger = 5
relOperator = -8
rem = 6
error = -9

#       numbers letters  +-                */            {}()[]       ,;         :       <        >       =            #     " \n\t\r"
states = [[dig,   idk,    addOperator,      mulOperator,  groupSymbol, delimiter, asgn,   smaller, larger, relOperator, rem, start],  # state 0
          [dig,   number, number,           number,       number,      number,
              number, number,  number, number,      error, number],  # state 1
          [idk,   idk,    keywordIdentifier, keywordIdentifier, keywordIdentifier, keywordIdentifier,
              keywordIdentifier, keywordIdentifier, keywordIdentifier, keywordIdentifier, error, keywordIdentifier],  # state 2
          [error, idk,  error,            error,        groupSymbol,  error,
              error,  error,   error,  assignment, error, start],  # state 3
          [relOperator, relOperator,  relOperator, relOperator, relOperator, relOperator,
              relOperator, error, relOperator, relOperator, error, relOperator],  # smaller 4
          [relOperator, relOperator, relOperator, relOperator, relOperator, relOperator,
              relOperator, relOperator, relOperator, relOperator, error, relOperator],  # larger 5
          [rem,   rem,    rem,              rem,          rem,        rem,
              rem,     rem,     rem,    rem,        start, rem]  # rem 6
          ]


def advance(char, file_counters):
    if char in '\n':
        file_counters[2] = 0  # col
        file_counters[1] += 1  # row
    else:
        file_counters[2] += 1  # col
    file_counters[0] += 1  # code_file_counter


def lexer(file_counters):
    last_word = ""
    state = start
    while((state != number) and (state != keywordIdentifier) and (state != addOperator) and (state != mulOperator) and
          (state != groupSymbol) and (state != delimiter) and (state != assignment) and (state != relOperator) and (state != error)):
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
            next_state = 10
        last_word += char

        state = states[state][next_state]
        print(last_word + " " + str(state))

    if(state == keywordIdentifier):
        file_counters[0] -= 1
        last_word = last_word[:-1]

    if(state == keywordIdentifier):
        if(last_word == "program "):
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
    elif(last_word.isdigit()):
        print("here")
        return last_word, "numbertk"
    else:
        return "None", state


file_counters = [0, 0, 0]  # code_file_counter, row, col
file = load_file()
for i in range(0, 10):
    word, tk = lexer(file_counters)
    #print(word + " " + str(tk))
