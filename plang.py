import sys


class Plang:
    def __init__(self, src):
        self.src = src
        self.line = 0
        self.feed = self.tokens()
        self.curr = None
        self.stack = []


    def error(self, msg):
        raise ValueError(f'{self.line}: {msg}')


    def tokens(self):
        for l in self.src.strip().split('\n'):
            self.line += 1
            
            for t in l.strip().split(' '):
                if t == 'print':
                    yield (t, )
                elif t.isnumeric():
                    yield ('num', int(t))
                else:
                    self.error(f'Syntax Error: Invalid token {t}')
            yield('\n', )

    
    def proceed(self):
        try:
            t = next(self.feed)
        except StopIteration:
            t = None
        
        return t


    def eat(sel, t):
        if self.curr is not None:
            raise RuntimeError('Can only parse one token at a time')
        
        self.curr = t

    
    def parse_e(self):
        t = self.proceed()

        if t[0] != 'num':
            self.eat(t)
            return False

        self.push(t[1])
        return True


    def parse_ps(self):
        t = self.proceed()

        if t[0] != 'print':
            self.eat(t)
            return False

        if not self.parse_e():
            self.error('Expected expression')

        val = self.pop()
        print(val)
        
        return True


    def parse_s(self):
        if not self.parse_ps():
            self.error('Expected print statement')
        
        t = self.proceed()
        if t[0] != '\n':
            self.error('Expected EOL')

        return True


    def parse_p(self):
        if not self.parse_s():
            self.error('Expected statement')
        
        t = self.proceed()
        while t is not None:
            self.eat(t)
            if not self.parse_s():
                self.error('Expected statement')
            t = self.proceed()
        
        return True


    def compile(self):
        try:
            return self.parse_p()
        except ValueError as e:
            print(str(e))
            return False


    def push(self, cmd): 
        self.stack.append(cmd)


    def pop(self):
        return self.stack.pop()


if __name__ == '__main__':
    with open(sys.argv[1], 'rt') as f:
        src = f.read()
    
    prog = Plang(src)
    prog.compile()