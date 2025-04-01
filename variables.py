#Define the variables
import math
import random

class exponential:
    def __init__(self, l : float):
        self.l = l
        self.continous = True

    #exponential random variable with lambda l
    def generate(self) -> float:
        ran = random.random()
        return (-math.log(ran)) / self.l

class uniform:
    def __init__(self, a : float, b: float):
        self.a = a
        self.b = b
        self.continous = True

    def generate(self) -> float:
        return self.a + (self.b - self.a) * random.random()

class erlang:
    def __init__(self, l : float, num : int):
        self.l = l
        self.num = num
        self.continous = True

    #erlang variable with lamdba l, number num
    def generate(self) -> float:
        x = exponential(self.l)
        result = 0
        for i in range(0, self.num):
            result += x.generate()
        return result

class bernoulli:
    def __init__(self, p : float):
        self.p = p
        if(p < 0 or p > 1):
            raise ValueError("Probability must be between 0 and 1.")
        self.continous = False

    #bernoulli variable with probability p
    def generate(self) -> float:
        if(random.random() < self.p):
            return 1
        else:
            return 0

class binomial:
    def __init__(self, n: int, p : float):
        self.n = n
        self.p = p
        if(p < 0 or p > 1):
            raise ValueError("Probability must be between 0 and 1.")
        if(type(n) != int):
            raise ValueError("Num must be an int.")
        self.continous = False

    #bernoulli variable with probability p
    def generate(self) -> float:
        result = 0
        ber = bernoulli(self.p)
        for i in range(0, self.n):
            result += ber.generate()
        return result
        
class poisson:
    def __init__(self, l: float):
        self.l = l
        self.continous = False

    #poisson variable with lambda l
    def generate(self) -> float:
        u = random.random()
        p = math.exp(-self.l)
        k = 0
        while u > p:
            k += 1
            p += (self.l**k * math.exp(-self.l)) / math.factorial(k)
        return k

class geometric:
    def __init__(self, p: float):
        self.p = p
        if(p < 0 or p > 1):
            raise ValueError("Probability must be between 0 and 1.")
        self.continous = False

    #geometric variable with probability p
    def generate(self) -> float:
        u = random.random()
        return math.floor(math.log(u) / math.log(1 - self.p)) + 1

class pascal:
    def __init__(self, p: float, l: float):
        self.l = l
        self.p = p
        if(p < 0 or p > 1):
            raise ValueError("Probability must be between 0 and 1.")
        self.continous = False

    #pascal variable with probability p
    def generate(self) -> float:
        g = geometric(self.p)
        result = 0
        for i in range(0, self.l):
            result += g.generate()
        return result

class v_sum:
    #takes in two random variables, and outputs the sum of them
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.continous = a.continous or b.continous

    def generate(self) -> float:
        return self.a.generate() + self.b.generate()

class v_div:
    #takes in two random variables, and outputs the quotient (a/b)
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.continous = a.continous or b.continous

    def generate(self) -> float:
        return self.a.generate() / self.b.generate()

class v_prod:
    #takes in two random variables, and outputs the product
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.continous = a.continous or b.continous

    def generate(self) -> float:
        return self.a.generate() * self.b.generate()

class v_power:
    #takes in a random variable, and outputs that variable to a given power
    def __init__(self, a, b : float):
        self.a = a
        self.b = b
        self.continous = a.continous

    def generate(self) -> float:
        return self.a.generate() ** self.b

class v_const:
    #takes in two random variables, and outputs the variable times a constant
    def __init__(self, a, b : float):
        self.a = a
        self.b = b
        self.continous = a.continous

    def generate(self) -> float:
        return self.a.generate() * self.b


