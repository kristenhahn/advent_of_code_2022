# Advent of Code 2022
# Day 12 
# https://adventofcode.com/2022/day/12


import pandas as pd
import copy

##########
# Import data
##########


with open('test_input.txt') as f:
    data = f.read()

# split input into lines
lines = data.split('\n')
# remove blank lines
lines = list(filter(None, lines))
# separate lines into lists of individual letters
lines = [[l for l in line] for line in lines]


##########
# dictionary to convert letters to heights
##########

letter_ht_dict = {}

# lowercase letters
for chr_code in range(97,123):
    letter = chr(chr_code)
    # set starting height as 0, arbitrary just for convenience
    height = chr_code-97
    # add lowercase letters to the dictionary
    letter_ht_dict[letter] = height

# # Start and End points - S and E
# letter_ht_dict['S'] = 0
# letter_ht_dict['E'] = 25


##########
# Grid dictionary: Convert row-column positions 
# in the grid to heights
##########

# crate dataframe of letters
df = pd.DataFrame(lines)

# convert lowercase letters to numbers. Leave uppercase (S and E) as they are.
def lower_letter_to_height(letter):
    if letter.islower():
        return letter_ht_dict[letter]
    else:
        return letter

# convert lowercase letters in dataframe to heights
df = df.applymap(lower_letter_to_height)

# find max index (row) and column:
max_index = max(df.index)
max_col = max(df.columns)


##########
# Strategy for mapping out routes
##########

# Route dictionary:
# {id: [status, [(index, col),(index, col)...]}
#       status options:
#           in progress = valid steps left to take
#           dead end = completed path ending in a dead end
#           complete = complete path to the endpoint
#       (row, col) pairs indicate points along the path in order
#
# For each point on the path:
#   Identify all adjacent points
#   Ignore points already visited on this path
#   Ignore points with height > current point height + 1

# If no points are left to move to, status = de

# if one point is available to move to, move to it.

# If multiple points are left to move to:

#   Copy the entire path to a new dictionary id and continue 
#   it to one available adjacent point.

#   Repeat the step above if there are more than 2 available points,
#   each time choosing a different adjacent point to move to.

#   On the original path, move to the last available direction 
#   and continue on.

#   Once a path is complete (dead end or completed path), return to 
#   an incomplete path and keep going.
# When all possible paths are completed, measure the complete paths
#  to find the shortest.
# Choose one 

##########
# Functions
##########

# Find start and end points:
def find_point(letter:str):
    for c in df.columns:
        if any(df[c]==letter):
            index_filter = df[c]==letter
            i = df.loc[index_filter,c].index[0]
            return(i, c)



def list_adjacent(p:tuple):
    '''list adjacent points to a given
    point in the format (<index>,<column>)'''

    i = p[0]
    c = p[1]
    points = []

    # if not top row
    if i >0:
        above = (i-1,c)
        points.append(above)

    # if not bottom row
    if i < max_index:
        below = (i+1,c)
        points.append(below)

    # if not far left column
    if c > 0:
        left = (i, c-1)
        points.append(left)

    # if not far right colun
    if c < max_col:
        right = (i, c+1)
        points.append(right)

    return points


def is_valid_step(route_id:int, point:tuple):
    '''Given a route id from the route dictionary
    and a point adjacent to the last point on the route,
    return True if the points is a valid option for
    the route to continue on.'''

    # test point(the point being tested to see if it is
    # a valid path): index and column
    pi, pc = point[0], point[1]
    # height of the test point
    ph = df.loc[pi, pc]


    # route
    r = rte_dict[route_id]
    # route points so far
    rp = r['points']
    # last route point
    lp = rp[-1]
    # last route point index and column
    lpi, lpc = lp[0], lp[1]
    # height of the last point on the route
    lph = df.loc[lpi,lpc]

 
    # Has this point alreay been included on this route?
    if point in rp:
        return False

    # Is this point adjacent to the last point on the route?
            # not strictly necessary as long as only adjacent points 
            # are being run through this function, but keeping 
            # it just in case something changes later
    if point not in list_adjacent(lp):
        return False

    # Is this point's height a max of one higher than the 
    # last point on the route?
    elif ph > lph + 1:
        return False
    
    else:
        return True

def list_valid_next_steps(route_id:int):
    '''Given a route id, this function returns
    a list of valid next steps along that route,
    if any.'''

    route = rte_dict[route_id]

    valid_steps = []

    # if route is already done, don't look for more steps.
    if route['status']=='in progress':
        
        last_point = route['points'][-1]
        adjacent_points = list_adjacent(last_point)

        for p in adjacent_points:
            # if valid steps are found, add to the list
            if is_valid_step(route_id, p):
                valid_steps.append(p)


    return valid_steps


def step(route_id:int):
    '''Take the next step along a given route'''

    global ep

    route = rte_dict[route_id]

    steps = list_valid_next_steps(route_id)

    # if there are no more valid steps available:
    if len(steps) == 0:
        # if end of route, mark complete.
        if route['points'][-1]==ep:
            route['status'] = 'complete'
        # if not end of route, mark dead end
        else:
            route['status']='dead end'

    # if there is only one valid step:
    elif len(steps) == 1:
        next_step = steps[0]
        # add step to the route
        route['points'].append(next_step)
        # check for end of route
        if next_step == (ep):
            route['status']='complete'

    # if there are multiple valid steps:       
    else:
        while len(steps)>1:
            # pick off one valid step at a time
            next_step = steps.pop()
            # make a new copy of the route so 
            # all possible routes can continue separately
            next_route_id = max(rte_dict)+1
            rte_dict[next_route_id]=copy.deepcopy(route)
            rte_dict[next_route_id]['status']='in progress'
            rte_dict[next_route_id]['points'].append(next_step)
            # check for end of route
            if next_step == (ep):
                rte_dict[next_route_id]['status']='complete'
                
        # once the list of valid steps is down to one
        next_step = steps[0]
        # add step to the route
        route['points'].append(next_step)
        # check for end of route
        if next_step == (ep):
            route['status']='complete'

def get_incomplete_route_ids():
    ids = []
    # find the first incomplete route
    for k,v in rte_dict.items():
        if v['status']=='in progress':
            ids.append(k)
            return ids

##########
# Prepare to run routes
##########

# identify start point
sp = find_point('S')
# identify end point
ep = find_point('E')
# convert start and end points from letters
# to values so they work with height formulas
# from now on
df.loc[sp[0],sp[1]]=0
df.loc[ep[0],ep[1]]=25

# set up route dictionary with the start point of the first route,
# flag that route as in progress.
rte_dict = {0:{'status':'in progress', 'points':[sp]}}


#########
# Run routes
##########


id_list = get_incomplete_route_ids()

while len(id_list) > 0:

    # pick the first incomplete route
    r = id_list[0]

    # step through the route until it ends (no longer 'in progress' status)
    while rte_dict[r]['status'] == 'in progress':
        step(r)

    # recalculate the incomplete routes list
    id_list = get_incomplete_route_ids()
    if id_list == None:
        break
    

   

##########
# Find the shortest complete route
##########

complete_route_ids = [r for r in rte_dict if rte_dict[r]['status']=='complete']

complete_route_point_count = [len(rte_dict[r]['points']) for r in complete_route_ids]

complete_route_step_count = [c-1 for c in complete_route_point_count]

min_route = min(complete_route_step_count)

print(min_route)



# rte_dict = {0:{'status':'complete', 'points':[(a,b)]}, 1:{'status':'in progress','points':[(2,3)]}}


# print(get_first_incomplete_route_id)


