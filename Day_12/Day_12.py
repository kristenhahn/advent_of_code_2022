# Advent of Code 2022
# Day 12 
# https://adventofcode.com/2022/day/12


import pandas as pd
import copy

##########
# Import data
##########


with open('input.txt') as f:
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
# Strategy for mapping out every possible route
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

# If no points are left to move to, status = dead end

# if one point is available to move to, move to it, status = in progress

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



def list_valid_next_steps(route_id:int):
    '''list valid next steps from the last point in a route,
    in the format (<index>,<column>)'''

    route = rte_dict[route_id]
    route_points = route['points']
    # last point in route so far
    lp = route_points[-1]
    # last point index
    lpi = lp[0]
    # last point column
    lpc = lp[1]
    # last point height
    lph = df.loc[lpi, lpc]

    # Find the points adjacent to the last
    # point in the route
    adjacent_points = []

    # if not top row
    if lpi >0:
        above = (lpi-1,lpc)
        adjacent_points.append(above)

    # if not bottom row
    if lpi < max_index:
        below = (lpi+1,lpc)
        adjacent_points.append(below)

    # if not far left column
    if lpc > 0:
        left = (lpi, lpc-1)
        adjacent_points.append(left)

    # if not far right colun
    if lpc < max_col:
        right = (lpi, lpc+1)
        adjacent_points.append(right)

    # Check each adjacent point 
    # to see if it is a valid next step.
    # Create a list of valid next steps
    valid_steps = []
  
    for ap in adjacent_points:
        api, apc = ap[0], ap[1]
        # height of the adjacent point
        aph = df.loc[api, apc]

        # Has adjacent point already been included
        # in this route? If so, don't put it on the list.
        if ap in route_points:
            pass

        # Is adjacent point too high?  (height 
        # more than last point height + 1)?
        elif aph > (lph + 1):
            pass
        
        # if neither of the previos conditions
        # is true, this is a valid point. Add it
        # to the list.
        else:
            valid_steps.append(ap)

    return valid_steps


def step(route_id:int):
    '''Take the next step along a given route'''

    global ep

    route = rte_dict[route_id]

    valid_steps = list_valid_next_steps(route_id)

    # if there are no more valid steps available:
    if len(valid_steps) == 0 or valid_steps == None:
        # if end of route, mark complete.
        if route['points'][-1]==ep:
            route['status'] = 'complete'
        # if not end of route, mark dead end
        else:
            route['status']='dead end'

    # if there is only one valid step:
    elif len(valid_steps) == 1:
        next_step = valid_steps[0]
        # add step to the route
        route['points'].append(next_step)
        # check for end of route
        if next_step == (ep):
            route['status'] = 'complete'
        else:
            route['status'] = 'in progress'

    # if there are multiple valid steps:       
    else:
        while len(valid_steps)>1:
            # pick off one valid step at a time
            next_step = valid_steps.pop()
            # make a new copy of the route so 
            # all possible routes can continue separately
            next_route_id = max(rte_dict)+1
            rte_dict[next_route_id]=copy.deepcopy(route)
            # add step to the copied route
            rte_dict[next_route_id]['points'].append(next_step)
            # check copied to see if it has ended
            if next_step == ep:
                rte_dict[next_route_id]['status'] = 'complete'
            else:
                rte_dict[next_route_id]['status'] = 'in progress'
         
        # once the list of valid steps is down to one
        next_step = valid_steps[0]
        # add step to the route
        route['points'].append(next_step)
        # check for end of route
        if next_step == (ep):
            route['status'] = 'complete'
        else:
            route['status'] = 'in progress'

def get_incomplete_route_ids():
    incomplete_ids = []
    # find the first incomplete route
    for k,v in rte_dict.items():
        if v['status']=='in progress':
            incomplete_ids.append(k)
    return incomplete_ids

def get_complete_route_ids():
    complete_ids = []
    # find the first complete route
    for k,v in rte_dict.items():
        if v['status']=='complete':
            complete_ids.append(k)
    return complete_ids

def get_dead_end_route_ids():
    dead_end_ids = []
    # find the first dead end route
    for k,v in rte_dict.items():
        if v['status']=='dead end':
            dead_end_ids.append(k)
    return dead_end_ids


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


# id_list = get_incomplete_route_ids()

# while len(id_list) > 0:

#     # pick the first incomplete route
#     r = id_list[0]

#     # step through the route until it ends (no longer 'in progress' status)
#     while rte_dict[r]['status'] == 'in progress':
#         step(r)

#     # recalculate the incomplete routes list
#     id_list = get_incomplete_route_ids()
#     if id_list == None:
#         break



incomplete_id_list = get_incomplete_route_ids()

keep_mapping = True
while keep_mapping == True:

    # pick the first incomplete route
    rid = incomplete_id_list[0]
    print(f"Now working on route {rid}")

    # step through the route until it ends (no longer 'in progress' status)
    route_status = rte_dict[rid]['status']
    while route_status == 'in progress':
        step(rid)
        route_status = rte_dict[rid]['status']


    # check incomplete ID list again to see if there are more
    incomplete_id_list = get_incomplete_route_ids()
    # print(f'Incomplete routes: {incomplete_id_list}')

    # complete_id_list = get_complete_route_ids()
    # print(f'Complete routes: {complete_id_list}')

    # dead_end_id_list = get_dead_end_route_ids()
    # print(f'Dead end routes: {dead_end_id_list}\n')

    # check for complete routes and stop mapping
    # if there are no more.
    if incomplete_id_list == None:
        keep_mapping = False
    elif len(incomplete_id_list) == 0:
        keep_mapping = False
    else:
        keep_mapping = True
    

    # # recalculate the incomplete routes list
    # # id_list = get_incomplete_route_ids()
    # if id_list == None:
    #     break
    

   
##########
# Find the shortest complete route
##########

complete_route_ids = get_complete_route_ids()

complete_route_point_count = [len(rte_dict[r]['points']) for r in complete_route_ids]

complete_route_step_count = [c-1 for c in complete_route_point_count]

min_route = min(complete_route_step_count)

print(min_route)

# print(rte_dict)
# print(get_dead_end_route_ids())

