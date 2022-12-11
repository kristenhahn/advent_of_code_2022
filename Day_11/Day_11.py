# Advent of Code 2022
# Day 11, Part 1
# https://adventofcode.com/2022/day/11

class Monkey:
    def __init__(
        self, 
        id:int, 
        items:[], 
        operation:str,
        test_divisor:int, 
        if_true_throw_to:int, 
        if_false_throw_to:int):

        self.id = id
        self.items = items
        self.operation = operation
        self.test_divisor = test_divisor
        self.if_true_throw_to= if_true_throw_to
        self.if_false_throw_to = if_false_throw_to
        self.inspection_count = 0

    def inspect_and_test(self):
        item = self.items[0]
        old = item
        new_worry = eval(self.operation)
        relief_worry = new_worry//3
        self.inspection_count += 1
        return relief_worry%self.test_divisor == 0
        
    def throw_item(self):
        return self.items.pop(0)

    def catch_item(self, i):
        self.items.append(i)


# m0 = Monkey(0,[79,98],'old * old',23,2,3)

with open('test_input.txt') as f:
    data = f.read()
    lines = data.split('\n')
# remove leading spaces
lines = [l.strip() for l in lines]

# build a list of monkeys
monkeys = {}
m = 0

# Parse the lines into monkey attributes
for l in lines:
    monkey_id = 0
    items = []
    if l.startswith('Monkey'):
        words = l.split(' ')
        monkey_id = words[1].split(':')[0]
        monkey_id = int(monkey_id)
        print(monkey_id)
    elif l.startswith('Starting'):
        items = l.split(': ')[1]
        items = items.split(', ')
        items = [int(i) for i in items]
        print(items)
    elif l.startswith('Operation'):
        operation = l.split('= ')[1]
        print(operation)
    elif l.startswith('Test'):
        test = l.split(" by ")[1]
        test = int(test)
        print(test)
    elif l.startswith("If true"):
        true_throw_to = l.split(" monkey ")[1]
        true_throw_to = int(true_throw_to)
        print(true_throw_to)
    elif l.startswith("if false"):
        false_throw_to = l.split(" monkey ")[1]
        false_throw_to = int(false_throw_to)
        print(false_throw_to)
    elif l == '':
        monkey_id += 1
        print(monkey_id)

   


    





    


    


