import parsley
import sys

class AExpr:
    pass

class LiteralInteger(AExpr):
    def __init__(self, n):
        self.value = n

    def eval(self, state):
        return self.value

    def __repr__(self):
        return str(self.value)

class Variable(AExpr):
    def __init__(self,char_name):
        self.var = char_name
    def eval(self, state):
        if not (self.var in state):
            #state[self.var] = 0
            return 0
        else:
            return state[self.var]
    def __repr__(self):
        return self.var

class Sum(AExpr):
    def __init__(self, a1, a2):
        self.AExpr1 = a1
        self.AExpr2 = a2

    def eval(self, state):
        return self.AExpr1.eval(state) + self.AExpr2.eval(state)

    def __repr__(self):
        return "(" + str(self.AExpr1) + '+' + str(self.AExpr2)+")"

class Diff(AExpr):
    def __init__(self, a1, a2):
        self.AExpr1 = a1
        self.AExpr2 = a2

    def eval(self, state):
        return self.AExpr1.eval(state) - self.AExpr2.eval(state)
    def __repr__(self):
        return "(" + str(self.AExpr1) + '-' + str(self.AExpr2) + ")"

class Product(AExpr):
    def __init__(self, a1, a2):
        self.AExpr1 = a1
        self.AExpr2 = a2
    def eval(self,state):
        return self.AExpr1.eval(state) * self.AExpr2.eval(state)

    def __repr__(self):
        return '('+str(self.AExpr1) + '*' + str(self.AExpr2)+')'

class BExpr:
    pass

class LiteralBoolean(BExpr):
    def __init__(self, p):
        if p == 'false':
            self.value = False
        if p == 'true':
            self.value = True
    def eval(self,state):
        return self.value
    def __repr__(self):
        if self.value == False:
            return "false"
        if self.value == True:
            return "true"

class Equals(BExpr):
    def __init__(self,a1,a2):
        self.AExpr1 = a1
        self.AExpr2 = a2
    def eval(self, state):
        return self.AExpr1.eval(state) == self.AExpr2.eval(state)

    def __repr__(self):
        return '(' + str(self.AExpr1) + '=' + str(self.AExpr2)+')'

class Less(BExpr):
    def __init__(self,a1,a2):
        self.AExpr1 = a1
        self.AExpr2 = a2
    def eval(self,state):
        return self.AExpr1.eval(state) < self.AExpr2.eval(state)

    def __repr__(self):
        return '('+str(self.AExpr1) + '<' + str(self.AExpr2)+')'

class Greater(BExpr):
    def __init__(self,a1,a2):
        self.AExpr1 = a1
        self.AExpr2 = a2
    def eval(self, state):
        return self.AExpr1.eval(state) > self.AExpr2.eval(state)
    def __repr__(self):
        return '('+str(self.AExpr1) +'>' + str(self.AExpr2)+')'

class And(BExpr):
    def __init__(self,b1,b2):
        self.BExpr1 = b1
        self.BExpr2 = b2
    def eval(self, state):
        return self.BExpr1.eval(state) and self.BExpr2.eval(state)

    def __repr__(self):
        return '('+ str(self.BExpr1) + '∧' + str(self.BExpr2) + ')'

class Or(BExpr):
    def __init__(self, b1, b2):
        self.BExpr1 = b1
        self.BExpr2 = b2
    def eval(self, state):
        return self.BExpr1.eval(state) or self.BExpr2.eval(state)

    def __repr__(self):
        return '('+str(self.BExpr1) + '∨' + str(self.BExpr2)+')'
class Not(BExpr):
    def __init__(self, b):
        self.BExpr = b

    def eval(self, state):
        return not self.BExpr.eval(state)

    def __repr__(self):
        return '¬' + str(self.BExpr)
class Commands:
    pass

class Skip(Commands):
    def run(self, state):
        return state
    def __repr__(self):
        return "skip"
    def run_small(self,state):
        pass
    def __str__(self):
        return "skip"

class Assign(Commands):
    def __init__(self,var,a):
        self.var = var
        self.value = a
    def run(self, state):
        state[self.var] = self.value.eval(state)
        return state
    def __repr__(self):
        return self.var + " := " + str(self.value)
    def run_small(self,state):
        return Skip(), self.run(state)

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
    def run_small(self,state):
        if self.BExpr.eval(state):
            return self.Command1, state
        else:
            return self.Command2, state
    def __repr__(self):
        return "if " + str(self.BExpr) + " then { " + str(self.Command1) + " } else { " + str(self.Command2) + " }"
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
    def __repr__(self):
        return "while " + str(self.BExpr) + " do { " + str(self.Command) + " }"
    def run_small(self,state):
        if not self.BExpr.eval(state):
            return Skip(), state
        else:
            return Seq(self.Command, self), state
class Seq(Commands):
    def __init__(self, c1, c2):
        self.Command1 = c1
        self.Command2 = c2
    def run(self,state):
        return self.Command2.run(self.Command1.run(state))
    def __repr__(self):
        return str(self.Command1) + ' ; ' + str(self.Command2)
    def run_small(self,state):
        if not (type(self.Command1) == Skip):
            Command1_prime, state_prime = self.Command1.run_small(state)
            return Seq(Command1_prime,self.Command2), state_prime
        else:
            return self.Command2, state

def makeLiteralInteger(x):
    return LiteralInteger(x)
def makeVariable(char):
    return Variable(char)
def makeSum(a1,a2):
    return Sum(a1,a2)
def makeDiff(a1,a2):
    return Diff(a1,a2)
def makeProduct(a1,a2):
    return Product(a1,a2)
def makeAnd(b1,b2):
    return And(b1,b2)
def makeOr(b1,b2):
    return Or(b1,b2)
def makeEquals(a1,a2):
    return Equals(a1,a2)
def makeLess(a1,a2):
    return Less(a1,a2)
def makeGreater(a1,a2):
    return Greater(a1,a2)
def makeNot(b):
    return Not(b)
def makeLiteralBoolean(n):
    return LiteralBoolean(n)
def makeWhile(b,c):
    return While(b,c)
def makeSeq(c1,c2):
    return Seq(c1,c2)
def makeSkip():
    return Skip()
def makeIf(b,c1,c2):
    return If(b,c1,c2)
def makeAssign(var, a):
    return Assign(var, a)
commandParser = parsley.makeGrammar("""
num = <digit+>:ds -> int(ds)
char = <letter+>:ds -> str(ds)
Aparens = '(' ws? AExpr:e ws? ')' -> e
Bparens = '(' ws? BExpr:e ws? ')' -> e
Braces = '{' ws? Seq:e ws? '}' -> e
AExpr = (
        Aparens:a -> a
        |'-' ws? AExpr:a1 -> -a1
        |AExpr:a1 ws? '+' ws? AExpr:a2 -> makeSum(a1,a2)
        |AExpr:a1 ws? '-' ws? AExpr:a2 -> makeDiff(a1,a2)
        |AExpr:a1 ws? '*' ws? AExpr:a2 -> makeProduct(a1,a2)
        |char:n -> makeVariable(n)
        |num:n -> makeLiteralInteger(n)
        
        )
BExpr = (
        Bparens:b -> b
        |BExpr:b1 ws? '∧' ws? BExpr:b2 -> makeAnd(b1,b2)
        |BExpr:b1 ws? '∨' ws? BExpr:b2 -> makeOr(b1,b2)
        |AExpr:a1 ws? '=' ws? AExpr:a2 -> makeEquals(a1,a2)
        |AExpr:a1 ws? '<' ws? AExpr:a2 -> makeLess(a1,a2)
        |AExpr:a1 ws? '>' ws? AExpr:a2 -> makeGreater(a1,a2)
        |'¬' ws? BExpr:b -> makeNot(b)
        |"true":n -> makeLiteralBoolean(n)
        |"false":n -> makeLiteralBoolean(n)
        
        )
Command = (
        Braces:c -> c
        |"while" ws? BExpr:b ws? "do" ws? Command:c -> makeWhile(b,c)
        
        |"skip":n -> makeSkip()
        |char:var ws? ":=" (
                ws? '-' ws? AExpr:n -> makeAssign(var, -n)
                |ws? AExpr:n -> makeAssign(var, n)
                )
        |"if" ws? BExpr:b ws? "then" ws?  Command:c1 ws? "else" ws? Command:c2 -> makeIf(b,c1,c2)
        )
Seq = (Command:c1 ws? ';' ws? Command:c2 -> makeSeq(c1,c2)
        |Command:c1 -> c1
        )
""",{"makeLiteralInteger": makeLiteralInteger,
     "makeVariable": makeVariable,
     "makeSum": makeSum,
     "makeDiff": makeDiff,
     "makeProduct": makeProduct,
     "makeAnd": makeAnd,
     "makeOr": makeOr,
     "makeEquals": makeEquals,
     "makeLess": makeLess,
     "makeGreater": makeGreater,
     "makeNot": makeNot,
     "makeLiteralBoolean": makeLiteralBoolean,
     "makeWhile": makeWhile,
     "makeSeq": makeSeq,
     "makeSkip": makeSkip,
     "makeIf": makeIf,
     "makeAssign": makeAssign

     }
)
def print_dict(d):
    l = sorted(d.keys())
    ret = "{"
    list = []
    for i in l:
        list.append(i + " → " + str(d[i]) )
    ret += ", ".join(list)
    ret += "}"
    return ret

def rerun_small(c, state):
    step = 0
    command = c
    while True:
        if step >= 10000:
            break
        if not (type(command) == Skip):
            command, state = command.run_small(state)
            print("⇒" + str(command) + ", " + print_dict(state))
        else:
            break
        step += 1



a = commandParser('if false then while true do skip else x:=2').Seq()
rerun_small(a, {})


