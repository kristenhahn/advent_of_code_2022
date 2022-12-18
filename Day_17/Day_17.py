# Advent of Code 20222
# Day 17

class Rock:
    def __init__(
        self,
        shape:str,
        base_point:tuple):

        self.shape = shape
        self.base_point = base_point

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
            'd':{'height':4, 'width':1, 'occupied':{(0,0),(0,1),(0,2),(0,3)}},
            'e':{'height':2, 'width':2, 'occupied':{(0,0),(1,0),(0,1),(1,1)}}
            }

        self.height = self.shape_dict[self.shape]['height']
        self.width = self.shape_dict[self.shape]['width']
        self.shape_item =self.shape_dict[self.shape]
        self.occupied_points = self.shape_item['occupied']
        self.max_y = self.base_point[1] + self.height - 1
        
        # update the occupied points based on the starting point for each
        # newly created shape:
        # x = 2, y = chamber_ymax + 3. This method seems clunky - is 
        # there a better way?
        old_points = self.occupied_points.copy()
        self.occupied_points.update([(x+base_point[0],y+base_point[1])for (x,y) in self.occupied_points])
        self.occupied_points.difference_update(old_points)


    def update_max_y(self):
        self.max_y = self.base_point[1] + self.height - 1
        return self.max_y

    # def print_shape(self):
    #     for r in reversed(range(self.height)):
    #         row_text = ''
    #         for c in range(self.width):
    #             if (c,r) in self.occupied_points:
    #                 row_text += '@'
    #             else:
    #                 row_text += '.'
    #         print(row_text)

    def right_points(self):
        right_points = set()
        right_points.update([(x+1,y) for (x, y) in self.occupied_points])
        return right_points

    def move_right(self):
        self.occupied_points = self.right_points()
        self.base_point = (self.base_point[0]+1, self.base_point[1])
  
    def left_points(self):
        left_points = set()
        left_points.update([(x-1,y) for (x, y) in self.occupied_points])
        return left_points

    def move_left(self):
        self.occupied_points = self.left_points()
        self.base_point = (self.base_point[0]-1, self.base_point[1])

    def down_points(self):
        down_points = set()
        down_points.update([(x,y-1) for (x, y) in self.occupied_points])
        return down_points

    def move_down(self):
        self.occupied_points = self.down_points()
        self.base_point = (self.base_point[0], self.base_point[1]-1)
        # self.max_y = self.max_y - 1

    
class Chamber():
    
    def __init__(
        self,
        width=7):

        self.width = width
        self.max_wall_height = -1

        self.occupied_points = set()

        self.max_rock_y = -1

    # Starting point:  
    #   Column -1 = a wall.
    #   Column (width) = a wall.
    #   Row -1 = the floor.

    def build_floor(self):
        floor = [(x, -1) for x in range(-1,self.width+1)]
        self.occupied_points.update(floor)
        self.max_rock_y = -1

    # walls
    def add_rows(self,num_rows):
        for n in range(num_rows):
            self.max_wall_height += 1
            walls = [(-1,self.max_wall_height),(self.width,self.max_wall_height)]
            self.occupied_points.update(walls)
     
    def print_chamber(self):
        for r in reversed(range(-1,self.max_wall_height+1)):
            row_text = ''
            for c in range(-1,self.width+1):
                if (c,r) in self.occupied_points:
                    row_text += '@'
                else:
                    row_text += '.'
            print(f'{r} {row_text}')
        print('')

    def print_chamber_slice(self, min_y, max_y):
        for r in reversed(range(min_y,max_y)):
            row_text = ''
            for c in range(-1,self.width+1):
                if (c,r) in self.occupied_points:
                    row_text += '@'
                else:
                    row_text += '.'
            print(row_text)
        print('')
        
    def add_rock(self, rock_type):
        base_point = (2, self.max_rock_y + 4)
        rock = Rock(rock_type, base_point)

        # build chamber walls to the top of the
        # new rock
        extra_height = rock.base_point[1]+rock.height - self.max_wall_height
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
        # if the rock moves one space down, see if there are
        # any obstructions
        overlap = self.occupied_points.intersection(rock.down_points())
        if len(overlap) == 0:
            rock.move_down()
            self.occupied_points.update(rock.occupied_points)
        # if there are obstructions, put the rock back where it was.
        else:
            self.occupied_points.update(rock.occupied_points)
            rock_y = rock.update_max_y()
            if self.max_rock_y < rock_y:
                self.max_rock_y = rock_y
            return ('rock bottom')

    def find_effective_floor(self):
        # Added for Part 2
        # If 3 adjacent rows cover all columns, then 
        # none of the available shapes can get past them.
        # Look for this condition and remove all
        # of the occupied points below it.

        # check the top 3 rows.

        for y in reversed(range(2,self.max_rock_y)):

            r1 = y
            r2 = r1 - 1
            r3 = r1 - 2
    
            occupied_cols = [p[0] for p in self.occupied_points if p[1]in(r1,r2,r3)]
            occupied_cols = set(occupied_cols)
            # if all columns are occupied, delete all of the occupied points
            # below these rows.
            if len(occupied_cols) == self.width + 2:
                # print(f'{len(self.occupied_points)} occupied points.')
                # print(f'r3 is {r3}')
                lower_points = [(x,y) for (x,y) in self.occupied_points if y < r3]
                # print(f'{len(lower_points)} lower points.')
                self.occupied_points.difference_update(lower_points)
                return r3
            else:
                return None
                # print(f'Now there are {len(self.occupied_points)} occupied points.')
                # self.print_chamber()

                

###########       
# Run game
###########

with open('input.txt') as f:
    data = f.read()

# remove blanks and separate into list of left-right instructions
inst = data.strip()
inst = list(inst)

rock_order = ['a', 'b', 'c', 'd', 'e']

# Set up a new chamber
chamber = Chamber()
chamber.build_floor()
# chamber.print_chamber()

fallen_rocks = 0

max_rock_height = 0

while fallen_rocks < 2000:

    # get the next rock type to fall and add it to the back of the list
    rock_type = rock_order.pop(0)
    rock_order.append(rock_type)

    # A new rock appears
    rock = chamber.add_rock(rock_type)

    ## Test print as needed ##
    # print_max_y = rock.update_max_y() + 5
    # print_min_y = max(-1,print_max_y - 12)
    # print('A new rock appears')
    # chamber.print_chamber_slice(print_min_y, print_max_y)
    # print()

    turn_end = False

    while turn_end == False:

        # get the next instruction and add it to the back of the list
        push = inst.pop(0)
        inst.append(push)

        # jets push the rock
        if push == "<":
            chamber.move_rock_left(rock)
        elif push == ">":
            chamber.move_rock_right(rock)
        else:  print("Error, invalid gas jet instruction")

        ## Test print as needed ##
        # print(f'\n push {push}')
        # print_max_y = rock.update_max_y() + 5
        # print_min_y = max(-1,print_max_y - 12)
        # chamber.print_chamber_slice(print_min_y, print_max_y)
        # print()

        # Rock falls one level
        move = chamber.move_rock_down(rock)
        if move == 'rock bottom':
            turn_end = True
            floor = chamber.find_effective_floor()
            if floor != None:
                print(f'new floor is row {floor}')
                print(f'floor change is {old_floor - floor}')
                print(f'{fallen_rocks} rocks have fallen.')
                print(f'rock height = {chamber.max_rock_y}\n')
            fallen_rocks += 1
            # print(f'{fallen_rocks} rocks have fallen.')

        ## Test print as needed
        # print('Rock falls')
        # print_max_y = rock.update_max_y() + 5
        # print_min_y = max(-1,print_max_y - 12)
        # chamber.print_chamber_slice(print_min_y, print_max_y)
        # print()

print(f'Total rock height = {chamber.max_rock_y+1}')


##########
# Part 2
##########

# Define a new "false" chamber bottom and trim it to that point?
# What are the conditions for that?  Obviously a complete
# filled row would do it - any other ways?

# If a group of adjacent rows covers all 7 columns with overlaps,
# then the bottom of these is the new effective chamber bottom.


