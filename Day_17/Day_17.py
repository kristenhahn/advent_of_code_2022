# Advent of Code 20222
# Day 17

class Rock:
    def __init__(
        self,
        shape:str,
        base_point:tuple):
        # chamber_ymax:int,
        # chamber_width=7):

        self.shape = shape
        # self.chamber_ymax = chamber_ymax
        # self.chamber_width = chamber_width

    # dictionary of shapes with height, width, and occupied squares
    # in x-y format. 
    # a = horizontal line
    # b = plus symbol
    # c = backwards L
    # d = vertical line
    # e = square
        self.shape_dict = {
            'a':{'height':1, 'width':4, 'occupied':{(0,0),(1,0),(2,0),(3,0)}},
            'b':{'height':3, 'width':3, 'occupied':{(1,0),(0,1),(1,1),(2,1),(1,2)}},
            'c':{'height':3, 'width':3, 'occupied':{(0,0),(1,0),(2,0),(2,1),(2,2)}},
            'd':{'height':4, 'width':1, 'occupied':{(0,0),(0,1),(0,2),(0,3),(0,4)}},
            'e':{'height':2, 'width':2, 'occupied':{(0,0),(1,0),(0,1),(1,1)}}
            }

        self.height = self.shape_dict[self.shape]['height']
        self.width = self.shape_dict[self.shape]['width']
        self.shape_item =self.shape_dict[self.shape]
        self.occupied_points = self.shape_item['occupied']
        
        # update the occupied points based on the starting point for each
        # newly created shape:
        # x = 2, y = chamber_ymax + 3
        old_points = self.occupied_points.copy()
        self.occupied_points.update([(x+base_point[0],y+base_point[1])for (x,y) in self.occupied_points])
        self.occupied_points.difference_update(old_points)

    def print_shape(self):
        for r in reversed(range(self.height)):
            row_text = ''
            for c in range(self.width):
                if (c,r) in self.occupied_points:
                    row_text += '@'
                else:
                    row_text += '.'
            print(row_text)

    def right_points(self):
        right_points = set()
        right_points.update([(x+1,y) for (x, y) in self.occupied_points])
        return right_points

    def move_right(self):
        new_occupied_points = self.right_points()
        self.occupied_points = self.right_points()

    def left_points(self):
        left_points = set()
        left_points.update([(x-1,y) for (x, y) in self.occupied_points])
        return left_points

    def move_left(self):
        new_occupied_points = self.left_points()
        self.occupied_points = self.left_points()

    def down_points(self):
        down_points = set()
        down_points.update([(x,y-1) for (x, y) in self.occupied_points])
        return down_points

    def move_down(self):
        new_occupied_points = self.down_points()
        self.occupied_points = self.down_points()

    



class Chamber():
    
    def __init__(
        self,
        width=7,
        max_wall_height=-1,
        max_rock_height=-1):

        self.width = width
        self.max_wall_height = max_wall_height
        self.max_rock_height = max_rock_height

        self.occupied_points = {()}

    # Starting point:  
    #   Column -1 = a wall.
    #   Column (width) = a wall.
    #   Row -1 = the floor.

    def build_floor(self):
        floor = [(x, -1) for x in range(-1,self.width+1)]
        self.occupied_points.update(floor)

    # walls
    def add_rows(self,num_rows):
        for n in range(num_rows):
            self.max_wall_height += 1
            walls = [(-1,self.max_wall_height),(self.width,self.max_wall_height)]
            self.occupied_points.update(walls)

    # # initial chamber = floor plus row 0
    # def build_floor(self):
    #     self.add_floor()
    #     self.add_rows(1)

     
    def print_chamber(self):
        for r in reversed(range(-1,self.max_wall_height+1)):
            row_text = ''
            for c in range(-1,self.width+1):
                if (c,r) in self.occupied_points:
                    row_text += '@'
                else:
                    row_text += '.'
            print(row_text)
        print('')

    def add_rock(self, rock_type):
        base_point = (2, self.max_rock_height + 4)
        rock = Rock(rock_type, base_point)

        # build chamber walls to the top of the
        # new rock
        extra_height = rock.height + 3
        self.add_rows(extra_height)

        # record the rock's occupied points in the chamber
        self.occupied_points.update(rock.occupied_points)

        return rock

    def move_rock_right(self, rock:Rock):
        # remove rock points from chamber temporarily
        self.occupied_points.difference_update([p for p in self.occupied_points if p in rock.occupied_points])
        # if the rock moves one space right, see if there are
        # any obstructions
        overlap = self.occupied_points.intersection(rock.right_points())
        if len(overlap) == 0:
            rock.move_right()
            self.occupied_points.update(rock.occupied_points)
        # if there are obstructions, put the rock back where it was.
        else:
            self.occupied_points.update(rock.occupied_points)

    def move_rock_left(self, rock:Rock):
        # remove rock points from chamber temporarily
        self.occupied_points.difference_update([p for p in self.occupied_points if p in rock.occupied_points])
        # if the rock moves one space right, see if there are
        # any obstructions
        overlap = self.occupied_points.intersection(rock.left_points())
        if len(overlap) == 0:
            rock.move_left()
            self.occupied_points.update(rock.occupied_points)
        # if there are obstructions, put the rock back where it was.
        else:
            self.occupied_points.update(rock.occupied_points)
    
    def move_rock_down(self, rock:Rock):
        # remove rock points from chamber temporarily
        self.occupied_points.difference_update([p for p in self.occupied_points if p in rock.occupied_points])
        # if the rock moves one space right, see if there are
        # any obstructions
        overlap = self.occupied_points.intersection(rock.down_points())
        if len(overlap) == 0:
            rock.move_down()
            self.occupied_points.update(rock.occupied_points)
        # if there are obstructions, put the rock back where it was.
        else:
            self.occupied_points.update(rock.occupied_points)    

        










    

### test printing ###

test_chamber = Chamber()
test_chamber.build_floor()

r = test_chamber.add_rock('d')
test_chamber.print_chamber()
test_chamber.move_rock_right(r)
test_chamber.print_chamber()
test_chamber.move_rock_right(r)
test_chamber.print_chamber()
test_chamber.move_rock_left(r)
test_chamber.print_chamber()
test_chamber.move_rock_down(r)
test_chamber.print_chamber()
test_chamber.move_rock_left(r)
test_chamber.print_chamber()
test_chamber.move_rock_left(r)
test_chamber.print_chamber()
test_chamber.move_rock_left(r)
test_chamber.print_chamber()
test_chamber.move_rock_left(r)
test_chamber.print_chamber()
test_chamber.move_rock_down(r)
test_chamber.print_chamber()
test_chamber.move_rock_down(r)
test_chamber.print_chamber()
test_chamber.move_rock_down(r)
test_chamber.print_chamber()
test_chamber.move_rock_down(r)
test_chamber.print_chamber()



# test_rock = Rock('a', 0)
# test_rock_2 = Rock('b', (4,4))
# test_rock_3 = Rock('c', 0)
# test_rock_4 = Rock('d', 0)
# test_rock_5 = Rock('e', 0)

# test_rock.print_shape()
# print('')
# test_rock.move_right()
# print()

# test_rock_2.print_shape()
# print()
# test_rock_2.move_right()
# print()
# test_rock_2.move_right()
# print()
# test_rock_2.move_right()
# print()
# test_rock_2.move_right()
# print()
# test_rock_2.move_right()
# print()
# test_rock_2.move_right()
# print()
# test_rock_2.move_right()
# print()
# test_rock_2.move_right()

# test_rock_2.print_shape()
# print()
# test_rock_2.move_left()
# print()
# test_rock_2.move_left()
# print()
# test_rock_2.move_left()
# print()
# test_rock_2.move_left()
# print()
# test_rock_2.move_left()
# print()
# test_rock_2.move_left()
# print()
# test_rock_2.move_left()
# print()
# test_rock_2.move_left()
# print()
# test_rock_2.move_left()
# print()

# test_rock_2.move_down()
# print()
# test_rock_2.move_down()
# print()
# test_rock_2.move_down()
# print()
# test_rock_2.move_down()
# print()



# test_rock_3.print_shape()
# print('')
# test_rock_4.print_shape()
# print('')
# test_rock_5.print_shape()
# print('')