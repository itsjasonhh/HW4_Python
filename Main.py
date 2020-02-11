import parsley

class AExpr:
    pass

class LiteralInteger(AExpr):
    def __init__(self, n):
        self.value = n

    def eval(self, state):
        return self.value

    def __str__(self):
        return str(self.value)

class Variable(AExpr):
    def __init__(self,char_name):
        self.var = char_name
    def eval(self, state):
        if not (self.var in state):
            return None
        else:
            return state[self.var]
    def __str__(self):
        return self.var

class Sum(AExpr):
    def __init__(self, a1, a2):
        self.AExpr1 = a1
        self.AExpr2 = a2

    def eval(self, state):
        return self.AExpr1.eval(state) + self.AExpr2.eval(state)

    def __str__(self):
        return self.AExpr1 + '+' + self.AExpr2

class Diff(AExpr):
    def __init__(self, a1, a2):
        self.AExpr1 = a1
        self.AExpr2 = a2

    def eval(self, state):
        return self.AExpr1.eval(state) - self.AExpr2.eval(state)
    def __str__(self):
        return self.Aexpr1 + '-' + self.AExpr2

class Product(AExpr):
    def __init__(self, a1, a2):
        self.AExpr1 = a1
        self.AExpr2 = a2
    def eval(self,state):
        return self.AExpr1.eval(state) * self.AExpr2.eval(state)

    def __str__(self):
        return self.AExpr1 + '*' + self.AExpr2

class BExpr:
    pass

class LiteralBoolean(BExpr):
    def __init__(self, p):
        self.value = p
    def eval(self,state):
        return self.value
    def __str__(self):
        return str(self.value)

class Equals(BExpr):
    def __init__(self,a1,a2):
        self.AExpr1 = a1
        self.AExpr2 = a2
    def eval(self, state):
        return self.AExpr1.eval(state) == self.AExpr2.eval(state)

    def __str__(self):
        return self.AExpr1 + '=' + self.AExpr2

class Less(BExpr):
    def __init__(self,a1,a2):
        self.AExpr1 = a1
        self.AExpr2 = a2
    def eval(self,state):
        return self.AExpr1.eval(state) < self.AExpr2.eval(state)

    def __str__(self):
        return self.AExpr1 + '<' + self.AExpr2

class Greater(BExpr):
    def __init__(self,a1,a2):
        self.AExpr1 = a1
        self.AExpr2 = a2
    def eval(self, state):
        return self.AExpr1.eval(state) > self.AExpr2.eval(state)
    def __str__(self):
        return self.AExpr1 +'>' + self.AExpr2

class And(BExpr):
    def __init__(self,b1,b2):
        self.BExpr1 = b1
        self.BExpr2 = b2
    def eval(self, state):
        return self.BExpr1.eval(state) and self.BExpr2.eval(state)

    def __str__(self):
        return self.BExpr1 + '∧' + self.BExpr2

class Or(BExpr):
    def __init__(self, b1, b2):
        self.BExpr1 = b1
        self.BExpr2 = b2
    def eval(self, state):
        return self.BExpr1.eval(state) or self.BExpr2.eval(state)

    def __str__(self):
        return self.BExpr1 + '∨' + self.BExpr2
class Not(BExpr):
    def __init__(self, b):
        self.BExpr = b

    def eval(self, state):
        return not self.BExpr.eval(state)

    def __str__(self):
        return '¬' + self.BExpr
class Commands:
    pass

class Skip(Commands):
    def run(self, state):
        return state

class Assign(Commands):
    def __init__(self,var,a):
        self.var = var
        self.value = a
    def run(self, state):
        state[self.var] = self.value
        return state

class If(Commands):
    def __init__(self,b,c1,c2):
        self.BExpr = b
        self.Command1 = c1
        self.Command2 = c2
    def run(self,state):
        if self.BExpr.eval(state):
            return self.Command1.run(state)
        else:
            return self.Command2.run(state)
class While(Commands):
    def __init__(self, b, c):
        self.BExpr = b
        self.Command = c
    def run(self,state):
        if self.BExpr.eval(state):
            new_state = self.Command.run(state)
            return self.run(new_state)
        else:
            return state

class Seq(Commands):
    def __init__(self, c1, c2):
        self.Command1 = c1
        self.Command2 = c2
    def run(self,state):
        return self.Command2.run(self.Command1.run(state))

commandParser = parsley.makeGrammar("""
num = <digit+>:ds -> int(ds)
char = <letter+>:ds -> str(ds)
AExpr = (
        '-' AExpr:a1 -> -a1
        |AExpr:a1 '+' AExpr:a2 -> a1, a2, '+'
        |AExpr:a1 '-' AExpr:a2 -> a1, a2, '-'
        |AExpr:a1 '*' AExpr:a2 -> a1, a2, '*'
        |char:n -> n
        |num:n -> n
        )
BExpr = (
        BExpr:b1 '∧' BExpr:b2 -> b1, b2
        |BExpr:b1 '∨' BExpr:b2 -> b1, b2
        |AExpr:a1 '=' AExpr:a2 -> a1, a2
        |AExpr:a1 '<' AExpr:a2 -> a1, a2
        |AExpr:a1 '>' AExpr:a2 -> a1, a2
        |'¬'BExpr:b -> b
        |"true":n -> n
        |"false":n -> n
        )
Command = (
        "while" BExpr:b "do" Command:c -> b, c
        |Command:c1 ';' Command:c2 -> c1, c2
        |"skip":n -> n
        |char:var ":=" (
                '-' num:n -> var, -n
                |num:n -> var, n)
        |"if" BExpr:b "then" Command:c1 "else" Command:c2 -> b, c1, c2
        )
""",{}
)
print(commandParser('x:=-10').Command())




