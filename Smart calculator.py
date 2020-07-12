from string import ascii_letters
from collections import deque

def calculate(action, symbol, res):
    if action == '+':
        calculation = res + int(symbol)
    else:
        calculation = res - int(symbol)
    return  calculation

def define_action(sign):
    plus = sign.count('+')
    minus = sign.count('-')
    if minus % 2 == 0:
        return  '+'
    else:
        return '- '

def calculate_expression(input_string):
    input_string = input_string.strip()
    res = 0
    number = ''
    sign = ''
    action = ''
    space = False
    error = False
    it_is_sign = False
    for symbol in input_string:
        if symbol.isdigit():
            if space and not it_is_sign:
                error = True
                return ('Invalid expression')
            number += symbol
            space = False
            it_is_sign = False

        elif (symbol == '+'
              or symbol == '-'):
            it_is_sign = True
            if number != '':
                if sign == '':
                    action = 'addition'
                    res = calculate(action, number, res)
                    number = ''
                else:
                    action = define_action(sign)
                    sign = ''
                    res = calculate(action, number, res)
                    number = ''
            sign += symbol
        elif symbol == ' ':
            space = True

    if not error:
        action = define_action(sign)
        try:
            res = calculate(action, number, res)
        except ValueError:
            return ('Invalid expression')
        else:
            return (res)

def replace_variable(expression):
    new_input = ''
    i = 0
    alpha = False
    digit = False
    while i < len(expression):
        if expression[i] in ascii_letters:
            if digit:
                return 'Invalid assignment'

            search = expression[i]
            alpha = True
            for j in range(i + 1, len(expression)):
                if expression[j] in ascii_letters:
                    search += expression[j]
                    i += 1
                elif expression[j].isdigit():
                    return 'Invalid assignment'
                else:
                    break
            try:
                new_input += str(my_variables[search])
                alpha = False
            except KeyError:
                return 'Unknown variable'
        elif expression[i].isdigit() and alpha:
            return 'Invalid assignment'
        elif expression[i].isdigit():
            digit = True
            new_input += expression[i]
        elif expression[i] == ' ':
            alpha = False
            digit = False
            new_input += expression[i]
        else:
            new_input += expression[i]
        i += 1

    return new_input

def calculate_variable(input_string):
    variable = ''
    equal_sign = False
    postfix = ''

    alpha = False
    if input_string.find('=') == -1\
        and (input_string.find('+') != -1
        or input_string.find('-') != -1
        or input_string.find('*') != -1
        or input_string.find('/') != -1):
        new_input = replace_variable(input_string)
        if new_input == 'Unknown variable':
            return new_input
        else:
            # number = calculate_expression(new_input)
            # return number
            return new_input

    for symbol in input_string:
        if symbol.isalpha():
            variable += symbol
            alpha = True
        elif symbol.isdigit() and alpha:
            return 'Invalid identifier'

        elif symbol == '=':
            equal_sign = True
            ind = input_string.find(symbol)
            expression = input_string[ind + 1:]
            new_input = replace_variable(expression)
            if new_input == 'Unknown variable'\
                    or new_input =='Invalid assignment':
                return new_input
            else:
                number = calculate_expression(new_input)
                break
        elif symbol == ' ':
            alpha = False

    if not equal_sign:
        try:
            print(my_variables[variable])
        except KeyError:
            return 'Unknown variable'
    else:

        my_variables[variable] = number


def to_postfix(input_string):
    sign_dict = {'+' : 1, '-' : 1, '*' :  2, '/' : 2, ')' : 2, '(' : 2}
    my_queue = deque()
    input_string = input_string.strip()
    postfix = ''
    sign = False
    first_number = False
    number = False
    for symbol in input_string:
        if sign:
            postfix += " "
            sign = False
        # Add operands (numbers and variables) to the result (postfix notation) as they arrive.
        if symbol not in sign_dict:
            first_number = True
            number = True
            postfix += symbol
        # unary minus operator
        elif (symbol == '+' or symbol == '-')\
            and not first_number:
            number = False
            postfix += symbol
        # If the incoming element is a left parenthesis, push it on the stack.
        elif symbol =='(':
            number = False
            my_queue.append(symbol)
        # If the incoming element is a right parenthesis, pop the stack and add operators to the result
        # until you see a left parenthesis. Discard the pair of parentheses.
        elif symbol == ')':
            number = False
            last_stack = my_queue[-1]
            while last_stack != '(':
                postfix += " "
                postfix += my_queue.pop()
                try:
                    last_stack = my_queue[-1]
                except IndexError:
                    break
            try:
                my_queue.pop()  # discard left parentheses
            except IndexError:
                return 'Invalid expression'
        # If the stack is empty or contains a left parenthesis on top, push the incoming operator on the stack.
        elif len(my_queue) == 0\
                or my_queue[-1] == '(':
            number = False
            my_queue.append(symbol)
            sign = True
        else:
            last_stack = my_queue[-1]
            if last_stack == symbol and not number:
                if symbol == '*' or symbol == '/':
                    return "Invalid expression"
                else:
                    my_queue[-1] = define_action(last_stack + symbol)
            elif sign_dict[last_stack] < sign_dict[symbol]:
                my_queue.append(symbol)
            else:
                while len(my_queue)\
                    and sign_dict[last_stack] >= sign_dict[symbol]:
                    postfix += " "
                    postfix += my_queue.pop()

                    try:
                        last_stack = my_queue[-1]
                    except IndexError:
                        break
                my_queue.append(symbol)
            sign = True

    while len(my_queue):
        postfix += " "
        postfix += my_queue.pop()

    return postfix

def perform_action(first, second, action):
    if action == '+':
        return first + second
    elif action == '-':
        return second - first
    elif action == '*':
        return second * first
    elif action == '/':
        return second / first

def postfix_to_answer(input_string):
    my_list = list(input_string.split())
    res_queue = deque()

    for item in my_list:
        # If the incoming element is a number, push it into the stack (the whole number, not a single digit!).
        try:
            item = int(item)
            res_queue.append(item)
        #  If the incoming element is an operator, then pop twice to get two numbers
        #  and perform the operation; push the result on the stack.
        except ValueError:
            first_number = res_queue.pop()
            second_number = res_queue.pop()
            res = perform_action(int(first_number), int(second_number), item)
            res_queue.append(res)

    #  When the expression ends, the number on the top of the stack is a final result.
    return res_queue[-1]


my_variables = {}
while True:
    input_string = input()
    if input_string.startswith('/'):
        if  input_string == '/exit':
            print('Bye!')
            break
        elif input_string == '/help':
            print('The program can calculate with "+", "-", "*", "/", "()"')
            continue
        elif input_string[0] == '/':
            print('Unknown command')
    elif not input_string:
        continue
    elif input_string.count('=') > 1:
        print('Invalid assignment')
    elif input_string.isalpha() \
             or input_string.find('=') != -1\
                or any(True for i in input_string if i in ascii_letters):
        new_input = calculate_variable(input_string)
        if new_input != None:
            try:
                rpn = to_postfix(new_input)
                # print(rpn)
                try:
                    res = postfix_to_answer(rpn)
                    print(res)
                except:
                    print(rpn)

            except:
                print(new_input)


    elif (input_string.find('+') != -1
        or input_string.find('-') != -1
        or input_string.find('*') != -1
        or input_string.find('/') != -1
            or input_string.isdigit()):
            rpn = to_postfix(input_string)
            if rpn.find('(') != -1\
                or rpn.find(')') != -1:
                print('Invalid expression')
            else:
                # print(rpn)
                try:
                    res = postfix_to_answer(rpn)
                    print(res)
                except:
                    print(rpn)
            # res = calculate_expression(input_string)
            # print(res)







