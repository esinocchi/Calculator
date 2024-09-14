class Node:
    def __init__(self, value):
        self.value = value  
        self.next = None 
    
    def __str__(self):
        return "Node({})".format(self.value) 

    __repr__ = __str__

class Stack:
    def __init__(self):
        self.top = None
    
    def __str__(self):
        temp=self.top
        out=[]
        while temp:
            out.append(str(temp.value))
            temp=temp.next
        out='\n'.join(out)
        return ('Top:{}\nStack:\n{}'.format(self.top,out))

    __repr__=__str__


    def isEmpty(self):
        return self.top == None

    def __len__(self): 
        count = 0
        current = self.top
        while current: # count each node until current is None
            current = current.next
            count += 1
        return count

    def push(self,value):
        new_node = Node(value)
        temp = self.top
        self.top = new_node # new node is now the top
        self.top.next =  temp # next node is previous top

     
    def pop(self):
        if not self.isEmpty():
            output = self.top.value # output is the value of the top if the stack is not empty
            if self.__len__() > 1:
                self.top = self.top.next # if the length of the stack is greater than 1, the top is now equal to the next of the previous top
            else:
                self.top = None
        else:
            output = None
        
        return output
    
    def peek(self):
        if not self.isEmpty():
            return self.top.value # returns top value if stack is not empty
        return None
    
class Calculator:
    def __init__(self):
        self.__expr = None


    @property
    def getExpr(self):
        return self.__expr

    def setExpr(self, new_expr):
        if isinstance(new_expr, str):
            self.__expr=new_expr
        else:
            print('setExpr error: Invalid expression')
            return None

    def _isNumber(self, txt):
        try:
            float(txt)
            return True
        except ValueError:
            return False

    def _getPostfix(self, txt):
            postfixStack = Stack() # method must use postfixStack to compute the postfix expression
            postfix = ''
            signs = '^*+/-'
            precedence = {'^': 3, '*': 2, '/': 2, '+': 1, '-': 1, '(':0, '{':0, '[': 0}
            closing_to_opening = {')': '(', ']': '[', '}': '{'}
            open_parenthesis = list(closing_to_opening.values())

            infix = []
            for cell in txt.split(' '): # initally splits the text by space, then appends to new list
                if cell: # prevents uneeded whitespace
                    infix.append(cell)

            for i, cell in enumerate(infix): # iterate through infix usisng enumerate to track the index, referenced in python documentation
                if not self._isNumber(cell) and cell not in precedence and cell not in closing_to_opening:
                    return None # return None if the cell is not an operator or a closing parenthesis
                if i < len(infix) - 1 and self._isNumber(cell) and self._isNumber(infix[i + 1]):
                    return None # return None if there are two numbers back to back

            if infix[0] in signs:
                return None # return None if the first index is a sign
            
            if infix[-1] in precedence: # returnns none if the last index is an operator - includes opening parenthesis
                return None
            
            bracketstack = Stack() # stack to store parenthesis
            while not bracketstack.isEmpty():
                bracketstack.pop() # while the stack is not empty, pop to ensure the stack is empty
            for cell in infix:
                if cell in open_parenthesis:
                    bracketstack.push(cell) # push open parenthesis into stack
                elif cell in closing_to_opening:
                    if bracketstack.isEmpty() or bracketstack.peek() != closing_to_opening[cell]:
                        return None # if the cell is a closed parenthesis, return None if the stack is empty, or if the top of the stack does not equal the corresponding open parenthesis
                    bracketstack.pop()
            if not bracketstack.isEmpty():
                return None # ensure for each open there is a closed parenthesis

                
            for i in range(len(infix) - 1):
                if not i == len(infix) - 1: # if not last index
                    if (self._isNumber(infix[i]) and infix[i + 1] in open_parenthesis) or infix[i] in closing_to_opening and infix[i + 1] in open_parenthesis:
                        infix.insert(i + 1, '*') # inserts multiplication operator for implied multiplication with parenthesis

            last = ''
            for cell in infix:
        
                if cell in signs and last in signs: # two signs in a row
                    return None
                
                if self._isNumber(cell): # add all numbers to postfix string
                    num = float(cell)
                    postfix += f"{num} "
                    last = cell

                # similar algorithm shown in module video
                elif cell in open_parenthesis: # push open parenthesis in stack
                    postfixStack.push(cell)
                    last = cell

                elif cell in closing_to_opening: # if cell is a closed parenthesis
                    while not postfixStack.isEmpty() and postfixStack.peek() not in open_parenthesis:
                        postfix += postfixStack.pop() + ' ' # pop to postfix while the stack is not empty and the top is not an open parenthesis
                    if not postfixStack.isEmpty() and postfixStack.peek() in open_parenthesis:
                        postfixStack.pop() # just pop when the top is an open parenthesis 

                elif cell in signs: # if the cell is a sign
                    while (not postfixStack.isEmpty()) and postfixStack.peek() not in open_parenthesis and (precedence[postfixStack.peek()] > precedence[cell] or (precedence[postfixStack.peek()] == precedence[cell] and cell != '^')):
                        postfix += postfixStack.pop() + ' ' # pop to postfix while the stack is not empty and the top is not an open parenthesis and the cell is not '^' while following PEMDAS
                    postfixStack.push(cell)  # push the current sign onto the stack
                    last = cell


            while not postfixStack.isEmpty(): 
                if postfixStack.peek() not in open_parenthesis:
                    postfix += postfixStack.pop() + ' ' # pop back to postfix while the stack is not empty and the top is not an open parenthesis
                else:
                    postfixStack.pop()  # pops parenthesis without adding to postfix string
            
            remove_spaces = postfix.split() # addresses edge case when last character is a space
            if remove_spaces[-1] == ' ':
                del remove_spaces[-1] 
            
            postfix = ' '.join(remove_spaces) # join postfix back to string
            return postfix
    
    @property
    def calculate(self):
        if not isinstance(self.__expr,str) or len(self.__expr)<=0:
            print("Argument error in calculate")
            return None

        calcStack = Stack() 
        operators = '*-+/^'
        postfix = self._getPostfix(self.__expr) # use postfix expression to calculate
        if postfix is None:
            return None
        postfix = postfix.split(' ') # split expression by space to analyze each character
        
        num3 = 0
        for item in postfix: # similar algorithm shown in module lecture
            if self._isNumber(item):
                calcStack.push(item) # push item into stack if it as number
            elif item in operators:  
                num1 = float(calcStack.pop())
                num2 = float(calcStack.pop())
                # pop twice from stack if the item is an operation, then perform correct operation
                if item == '*':
                    num3 = num2 * num1
                elif item == '-':
                    num3 = num2 - num1
                elif item == '+':
                    num3 = num2 + num1
                elif item == '^':
                    num3 = num2 ** num1
                else:
                    try:
                        num3 = num2 / num1
                    except ZeroDivisionError: # prevents divide by zero error
                        return None
                calcStack.push(num3) # pushes the result onto the stack
        return calcStack.pop() # pops the last value in the stack
    
    class AdvancedCalculator:

        def __init__(self):
            self.expressions = ''
            self.states = {}

        def setExpression(self, expression):
            self.expressions = expression
            self.states = {}

        def _isVariable(self, word):
            if not word[0].isalpha() or not word: # if the word is an empty string or the first character is non a letter, return False
                return False
            for char in word:
                if not char.isalnum(): # for each character, if the character alphanumeric, return False
                    return False
            return True
        

        def _replaceVariables(self, expr):
            expr = expr.split()
            for i, char in enumerate(expr): #iterates through the splitted expression
                if char.isalnum():
                    if char in self.states:
                        expr[i] = str(self.states[char]) # if the char is alphanumeric and in states, replaces it with the key of the value in states
                    elif not char.isnumeric():
                        return None # if the char is a letter(s) not in states, return None
    
            expr_s = ' '.join(expr) # join the expression back into a string
            return expr_s
        
        
        def calculateExpressions(self):
            self.states = {} 
            calcObj = Calculator()     # method must use calcObj to compute each expression
            new_dict = {}
            expr = self.expressions.split(';')
            copy_expr = expr.copy()
            for i, cell in enumerate(expr): # iterate through expr, splitting by the '=' to seperate the expression
                expr[i] = cell.split('=')
            for i, cell in enumerate(expr):

                if i == 0: # On the first iteration, _replaceVariables is not needed because by defualt states will be empty
                    calcObj.setExpr(cell[1].strip())
                    self.states[cell[0].strip()] = float(calcObj.calculate)
                    new_dict[copy_expr[0]] = self.states.copy() # copy() is used to create a shallow copy of the dictionary, since the dictioanary is mutable

                elif i != len(expr) - 1: # If the iteration is not the first one or the last one
                    expression = self._replaceVariables(cell[1].strip()) # Replace variables
                    if not isinstance(expression, str): # Ensures that the expression is a valid expression
                        self.states = {}
                        return None
                    calcObj.setExpr(expression)
                    self.states[cell[0].strip()] = float(calcObj.calculate) # Updates states
                    new_dict[copy_expr[i]] = self.states.copy()

                else:
                    return_expression = cell[0][7:] # cell[0][7:] represents the expression after 'return ' in the string
                    ans = self._replaceVariables(return_expression)
                    if not isinstance(expression, str):
                        self.states = {}
                        return None
                    calcObj.setExpr(ans)
                    new_dict['_return_'] = float(calcObj.calculate) # hardcodes the key as '_return_' to match doctests
            return new_dict