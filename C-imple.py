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


digits = ["0"]


file_counters = [0, 0, 0]  # code_file_counter, row, col
error_messages = {1: "Characters ", 2: " asasa"}


def advance(char, file_counters):
    if char in '\n':
        file_counters[2] = 0  # col
        file_counters[1] += 1  # row
    else:
        file_counters[2] += 1  # col
    file_counters[0] += 1  # code_file_counter


def lexer(file_counters):
    # global code_file_counter
    last_word = []
    error = 0

    while(1):
        # global code_file_counter
        file.seek(file_counters[0])
        char = file.read(1)  # read by character
        # print(type(char))
        # print(len(last_word))
        file_counters[0] = file_counters[0] + 1
        advance(char, file_counters)
        if char in ' \n\t\r':
            break
        elif len(last_word) >= 30:
            error = 1
            break
        elif ((len(last_word) == 0) and char.isdigit()):
            error = 2
            break
        else:
            last_word.append(char)
            print(last_word)
            print(file_counters[0])

    # print(last_word)
    return last_word, error


file = load_file()
for i in range(0, 10):
    word, error = lexer(file_counters)
    if error != 0:
        break
