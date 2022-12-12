
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

# print(letter_ht_dict)

##########
# Convert letters to heights
##########

print(lines)


##########
# Grid dictionary converting row-column positions in the grid to heights
##########


# grid = {}

# # loop through lines (rows)
# for l in lines:
#     # loop through items in each line (columns)
#     for i in lines[l]:
#         # add item to dictionary, key = (<row>,<column>)
#         # grid[(l,i)] = 









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



print(df)

