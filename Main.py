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

class Sum(AExpr):
    def __init__(self, a1, a2):
        self.AExpr1 = a1
        self.AExpr2 = a2

    def eval(self, state):
        return self.AExpr1.eval(state) + self.AExpr2.eval(state)

class Diff(AExpr):
    def __init__(self, a1, a2):
        self.AExpr1 = a1
        self.AExpr2 = a2

    def eval(self, state):
        return self.AExpr1.eval(state) - self.AExpr2.eval(state)


class Product(AExpr):
    def __init__(self, a1, a2):
        self.AExpr1 = a1
        self.AExpr2 = a2
    def eval(self,state):
        return self.AExpr1.eval(state) * self.AExpr2.eval(state)

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

class Less(BExpr):
    def __init__(self,a1,a2):
        self.AExpr1 = a1
        self.AExpr2 = a2
    def eval(self,state):
        return self.AExpr1.eval(state) < self.AExpr2.eval(state)

class Greater(BExpr):
    def __init__(self,a1,a2):
        self.AExpr1 = a1
        self.AExpr2 = a2
    def eval(self, state):
        return self.AExpr1.eval(state) > self.AExpr2.eval(state)

class And(BExpr):
    def __init__(self,b1,b2):
        self.BExpr1 = b1
        self.BExpr2 = b2
    def eval(self, state):
        return self.BExpr1.eval(state) and self.BExpr2.eval(state)

class Or(BExpr):
    def __init__(self, b1, b2):
        self.BExpr1 = b1
        self.BExpr2 = b2
    def eval(self, state):
        return self.BExpr1.eval(state) or self.BExpr2.eval(state)

class Not(BExpr):
    def __init__(self, b):
        self.BExpr = b

    def eval(self, state):
        return not self.BExpr.eval(state)

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



