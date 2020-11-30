class MachineInstance:
    # constants, built-in settings of processor
    REG_SIZE = 18
    BYTE_SIZE = 9
    INT_MAX = 2 ** REG_SIZE
    MAX_BYTE = 2 ** BYTE_SIZE

    def __init__(self):
        self.stack = []
        self.commands = {'add': self.add,
                         'sub': self.subtracts,
                         'div': self.divide,
                         'mul': self.multiply,
                         'pop': self.pop,
                         'push': self.push,
                         'inv': self.inverse,
                         }
        self.memory = {'IR': '',
                       'PS': '+',
                       'PC': 0,
                       'TC': 0,
                       'R0': 0,
                       'R1': 0,
                       'R2': 0,
                       'R3': 0,
                       }

    def add(self):
        """ Add 3 numbers from the top of the stack and write the result instead of the top of the stack. """
        if len(self.stack) < 3:
            raise MemoryError('The stack contains fewer operands than needed!')
        self.memory['PS'] = '+' if self.stack[-1] + self.stack[-2] + self.stack[-3] >= 0 else '-'
        self.stack[-1] = (self.stack.pop() + self.stack.pop() + self.stack[-1]) % self.INT_MAX
        self.memory['TC'] += 1

    def subtracts(self):
        """
        Pops the top three items from the stack and writes the difference
        of the first by the second divided by the third element.
        """
        if len(self.stack) < 3:
            raise MemoryError('The stack contains fewer operands than needed!')
        self.memory['PS'] = '+' if self.stack[-1] - self.stack[-2] - self.stack[-3] >= 0 else '-'
        self.stack[-1] = (self.stack.pop() - self.stack.pop() - self.stack[-1]) % self.INT_MAX
        self.memory['TC'] += 1

    def divide(self):
        """
        Pops the top three items from the stack and writes the division
        of the first by the second subtracted by the third element.
        """
        if len(self.stack) < 3:
            raise MemoryError('The stack contains fewer operands than needed!')
        if self.stack[-2] == 0:
            raise ValueError('Cannot divide by 0')
        self.memory['PS'] = '+' if (self.stack[-1] // self.stack[-2]) // self.stack[-3] >= 0 else '-'
        self.stack[-1] = ((self.stack.pop() // self.stack.pop()) // self.stack[-1]) % self.INT_MAX
        self.memory['TC'] += 1

    def multiply(self):
        """ Multiplies three upper elements of the stack and write the result instead of the top of the stack. """
        if len(self.stack) < 3:
            raise MemoryError('The stack contains fewer operands than needed!')
        self.memory['PS'] = '+' if self.stack[-1] * self.stack[-2] * self.stack[-3] >= 0 else '-'
        self.stack[-1] = (self.stack.pop() * self.stack.pop() * self.stack[-1]) % self.INT_MAX
        self.memory['TC'] += 1

    def odd_mask(self):
        ans = 0
        for i in range(self.REG_SIZE):
            ans+= 2**i if i%2 == 1 else 0
        return ans

    def even_mask(self):
        ans = 0
        for i in range(self.REG_SIZE):
            ans+= 2**i if i%2 == 0 else 0
        return ans

    def inverse(self):
        """ Custom operation """
        if len(self.stack) < 3:
            raise MemoryError('The stack contains fewer operands than needed!')

        last = self.stack.pop()
        odd_mask = self.stack.pop() ^ self.odd_mask() if self.stack[-1] % 2 == 1 else self.stack.pop() * 0
        even_mask = self.stack.pop() ^ self.even_mask() if self.stack[-1] % 2 == 0 else self.stack.pop() * 0
        self.stack.append(last ^ odd_mask ^ even_mask)
        self.memory['PS'] = '+' if self.stack[-1] >= 0 else '-'
        self.memory['TC'] += 1

    def pop(self, reg_name):
        """ Pops the top element of the stack. """
        self.memory['PS'] = '+' if self.stack[-1] >= 0 else '-'
        if reg_name in self.memory or reg_name[0] != 'R':
            self.memory[reg_name] = self.stack.pop()
        else:
            raise NameError('Register with name ' + reg_name + ' does not exist.')
        self.memory['TC'] += 1

    def push(self, item):
        """ Pushes item into the stack. """
        self.stack.append(self.memory[item] if item in self.memory else item)
        self.memory['PS'] = '+' if self.stack[-1] >= 0 else '-'
        self.memory['TC'] += 1

    def to_bin(self, n):
        s = ''
        for _ in range(self.REG_SIZE):
            s = str(n % 2) + s
            n //= 2
        return s

    def to_byte(self, n):
        s = self.to_bin(n)
        t = s[0:self.BYTE_SIZE]
        for i in range(1, self.REG_SIZE // self.BYTE_SIZE):
            t = t + '|' + s[i * self.BYTE_SIZE:(i + 1) * self.BYTE_SIZE]
        return t

    def load(self, command):
        """ Parses a command """
        self.memory['IR'] = command.strip()
        args = command.split()
        func = self.commands[args[0]]

        val = None
        if len(args) > 1:
            if args[1].isdigit():
                val = int(args[1])
            else:
                val = args[1]
            self.memory['PS'] = '+' if (self.memory[val] if val in self.memory else int(val)) >= 0 else '-'
        self.memory['TC'] += 1
        self.print_state()
        input('')
        try:
            return (func, int(val))
        except:
            return (func, val)

    def execute(self, command):
        """ Executes a command """
        func, val = self.load(command)
        if val == None:
            func()
        else:
            func(val)
        self.memory['PC'] += 1
        self.print_state()
        input('')

    def print_state(self, ):
        print('Memory:')
        for register in self.memory:
            if register[0] == 'R':
                print('\n', register, self.to_bin(self.memory[register]), end='')
            else:
                print(register, self.memory[register], end='\t' if register != 'IR' else '\n')
        print('\nStack:')
        for item in self.stack:
            print(self.to_byte(item))


if __name__ == '__main__':
    stackMachine = MachineInstance()
    with open('in.txt') as Input:
        for line in Input:
            stackMachine.execute(line)
