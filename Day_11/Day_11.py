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







    


    


