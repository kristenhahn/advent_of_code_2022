# Advent of Code 20222
# Day 17

class Rock:
    def __init__(
        self,
        shape:str,
        chamber_ymax:int):

        self.shape = shape
        self.chamber_ymax = chamber_ymax

    # dictionary of shapes with height, width, and occupied squares
    # in x-y format. 
    # a = horizontal line
    # b = plus symbol
    # c = backwards L
    # d = vertical line
    # e = square
        self.shape_dict = {
            'a':{'height':1, 'width':4, 'occupied':((0,0),(1,0),(2,0),(3,0),(4,0))},
            'b':{'height':3, 'width':3, 'occupied':((1,0),(0,1),(1,1),(2,1),(1,2))},
            'c':{'height':3, 'width':3, 'occupied':((0,0),(1,0),(2,0),(2,1),(2,2))},
            'd':{'height':4, 'width':1, 'occupied':((0,0),(0,1),(0,2),(0,3),(0,4))},
            'e':{'height':2, 'width':2, 'occupied':((0,0),(1,0),(0,1),(1,1))}
            }

        self.height = self.shape_dict[self.shape]['height']
        self.width = self.shape_dict[self.shape]['width']
        self.shape_item =self.shape_dict[self.shape]
        self.occupied_points = self.shape_item['occupied']
        
        self.start_point = (2, chamber_ymax + 3)

    def print_shape(self):
        for r in reversed(range(self.height)):
            row_text = ''
            for c in range(self.width):
                if (c,r) in self.occupied_points:
                    row_text += '@'
                else:
                    row_text += '.'
            print(row_text)

    # def move_right(self):


                    


class Chamber():
    
    def __init__(
        self,
        width=7,
        max_height=0):

        self.width = width
        self.max_height = max_height

        self.occupied_points = {}

    def print_chamber(self):
        for r in reversed(range(self.max_height+1)):
            row_text = ''
            for c in range(self.width):
                if (c,r) in self.occupied_points:
                    row_text += '@'
                else:
                    row_text += '.'
            print(row_text)
        print('-'*self.width)
        print('')





    

### test printing ###

test_chamber = Chamber()
test_chamber.print_chamber()


test_rock = Rock('a', 0)
test_rock_2 = Rock('b', 0)
test_rock_3 = Rock('c', 0)
test_rock_4 = Rock('d', 0)
test_rock_5 = Rock('e', 0)

test_rock.print_shape()
print('')
test_rock_2.print_shape()
print('')
test_rock_3.print_shape()
print('')
test_rock_4.print_shape()
print('')
test_rock_5.print_shape()
print('')