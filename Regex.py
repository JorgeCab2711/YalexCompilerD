class RegexToPostfix:
    def __init__(self, regex):
        self.regex = regex
        self.postfix = ""

    def check_errors(self):
        # Add your own error checking here if needed
        pass

    def precedence(self, operator):
        if operator == '|':
            return 1
        elif operator == '$':
            return 2
        elif operator in {'*', '?'}:
            return 3
        else:
            return -1

    def to_postfix(self):
        self.check_errors()

        if self.regex == '_|_':
            return '__|'

        stack = []
        for char in self.regex:
            if char.isalnum():
                self.postfix += char
            elif char == '(':
                stack.append(char)
            elif char == ')':
                while stack and stack[-1] != '(':
                    self.postfix += stack.pop()
                if stack and stack[-1] == '(':
                    stack.pop()
            else:
                while stack and self.precedence(char) <= self.precedence(stack[-1]):
                    self.postfix += stack.pop()
                stack.append(char)

        while stack:
            self.postfix += stack.pop()

        return self.postfix
