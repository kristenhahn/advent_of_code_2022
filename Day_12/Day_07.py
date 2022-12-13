import pandas as pd

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
#           ip = in progress)
#           de = completed path ending in a dead end)
#           cp = complete path to the endpoint
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
# Start mapping routes
##########

# Find start and end points:
def find_point(letter:str):
    for c in df.columns:
        if any(df[c]==letter):
            index_filter = df[c]==letter
            i = df.loc[index_filter,c].index[0]
            return(i, c)


# list adjacent points given the index and column of a point
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










# start point
sp = find_point('S')
# end point
ep = find_point('E')

# set up route dictionary
rte_dict = {}
# route id
i = 1






