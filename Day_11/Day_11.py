# Advent of Code 2022
# Day 11, Part 1
# https://adventofcode.com/2022/day/11


##########
# Set up a Monkey class
##########

class Monkey:
    def __init__(
        self, 
        id:int, 
        items:list, 
        operation:str,
        test_divisor:int, 
        true_throw_to:int, 
        false_throw_to:int):

        self.id = id
        self.items = items
        self.operation = operation
        self.test_divisor = test_divisor
        self.true_throw_to= true_throw_to
        self.false_throw_to = false_throw_to
        self.inspection_count = 0
        self.test_result = 0

    def inspect_and_test(self):

        # consider the first item
        item = self.items[0]

        # set the old variable so the operation can be evaluated
        old = item

        # perform operation to get new worry level
        new_worry = eval(self.operation)

        relief_worry = new_worry//3
        # relief_worry = new_worry%self.test_divisor

        # update worry value of the item
        self.items[0] = relief_worry

        # keep count of how many items monkey inspected
        self.inspection_count += 1

        # test results
        return relief_worry%self.test_divisor == 0


    # part 2 version:  worry not divided by 3
    def inspect_and_test_part_2(self):
        global lcm

        # consider the first item
        item = self.items[0]

        # set the old variable so the operation can be evaluated
        old = item

        # perform operation to get new worry level
        new_worry = eval(self.operation)

        # remainder of relief worry divided by
        # least common multiple of all monkeys' 
        # test divisors
        relief_worry = new_worry%lcm
       
        # update worry value of the item
        self.items[0] = relief_worry

        # keep count of how many items monkey inspected
        self.inspection_count += 1

        # test results
        return relief_worry%self.test_divisor == 0
        
    def throw_item(self):
        return self.items.pop(0)

    def catch_item(self, i):
        self.items.append(i)
    
    # for troubleshooting
    def print_monkey(self):
        print(f'id: {self.id}')
        print(f'items: {self.items}')
        print(f'operation: {self.operation}')
        print(f'test_divisor: {self.test_divisor}')
        print(f'true_throw_to: {self.true_throw_to}')
        print(f'false_throw_to: {self.false_throw_to}')
        print(f'inspection_count: {self.inspection_count}')
        print('\n')



##########
# Parse input and generate Monkeys
##########

def generate_monkeys(input):
    with open(input) as f:
        data = f.read()
        lines = data.split('\n')
    # remove leading spaces
    lines = [l.strip() for l in lines]

    # build a dictionary of monkeys
    monkeys = {}
    m = 0

    # Parse the lines into monkey attributes
    monkey_id = 0
    for l in lines:
        if l.startswith('Monkey'):
            words = l.split(' ')
            monkey_id = words[1].split(':')[0]
            monkey_id = int(monkey_id)
            
        elif l.startswith('Starting'):
            items = l.split(': ')[1]
            items = items.split(', ')
            items = [int(i) for i in items]
           
        elif l.startswith('Operation'):
            operation = l.split('= ')[1]
          
        elif l.startswith('Test'):
            test_divisor = l.split(" by ")[1]
            test_divisor = int(test_divisor)
           
        elif l.startswith("If true"):
            true_throw_to = l.split(" monkey ")[1]
            true_throw_to = int(true_throw_to)
        
        elif l.startswith("If false"):
            false_throw_to = l.split(" monkey ")[1]
            false_throw_to = int(false_throw_to)
           
        elif l == '':
            # create monkey using the values collected above
            monkey = Monkey(monkey_id,
                items,
                operation, 
                test_divisor, 
                true_throw_to, 
                false_throw_to)

            # add monkey to the monkey dictionary
            monkeys[monkey_id] = monkey

            # increment the ID to start the next monkey
            monkey_id += 1

    return monkeys     


###########
# Function to have monkeys play one round
##########


def monkey_round(monkeys):

    # loop through each monkey in order
    for m in monkeys:
        player = monkeys[m]
        item_count = len(player.items)
        # loop through items in the monkey's posession'

        for i in range(item_count):

            # test and insepct items
            test_result = player.inspect_and_test()
          
            # decide which monkey to throw item to
            if test_result == True:
                catcher_id= player.true_throw_to
            else:
                catcher_id  = player.false_throw_to

            # catcher monkey
            catcher = monkeys[catcher_id]

            # player throws
            thrown_item = player.throw_item()

            # catcher catches
            catcher.catch_item(thrown_item)
       

def monkey_round_part_2(monkeys):
    # loop through each monkey in order
    for m in monkeys:
        player = monkeys[m]
        item_count = len(player.items)

        # loop through items in the monkey's posessions
        for i in range(item_count):

            # test and insepct items
            test_result = player.inspect_and_test_part_2()

            # decide which monkey to throw item to
            if test_result == True:
                catcher_id= player.true_throw_to
            else:
                catcher_id  = player.false_throw_to

            # catcher monkey
            catcher = monkeys[catcher_id]

            # player throws
            thrown_item = player.throw_item()

            # catcher catches
            catcher.catch_item(thrown_item)
          


# Run multiple rounds

monkeys = generate_monkeys('input.txt')

# Had to look for help on this strategy for identifying least
# common denominator in Part 2 - thanks to 
# https://www.reddit.com/user/sky_badger/ :
# https://replit.com/@skybadger/AOC2022-Day11#main.py


lcm = 1
divisors = [monkeys[m].test_divisor for m in monkeys]
for div in divisors:
    lcm *= div

# # Part 1:
# for r in range(20):
#     monkey_round(monkeys)


# Part 2:
for r in range(10000):
    monkey_round_part_2(monkeys)

##########
# calculate monkey business
##########


# list how many times each monkey inspected an item
inspection_frequencies = [monkeys[m].inspection_count for m in monkeys]


# sort high to low
inspection_frequencies.sort(reverse=True)
# print(inspection_frequencies)


# multiply the top 2 highest 
monkey_business = inspection_frequencies[0] * inspection_frequencies[1]

print(monkey_business)




  
        





    


    


