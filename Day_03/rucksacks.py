# %% [markdown]
# # Advent of Code 2022
# ### Day 3 Part 1
# https://adventofcode.com/2022/day/3

# %%
# Open the file containing the strategy guide
with open('rucksacks.txt', 'r') as f:
    lines = f.readlines()
    lines = [l.replace('\n', '') for l in lines]


# %%
rucksacks = lines.copy()


# %%
# Find the common item found in both halves of a rucksack
def find_common_letter(rucksack):
    
    # compartment holds 1/2 of the letters (items) in the rucksack.
    compartment_quantity = int(len(rucksack)/2)

    # split the compartments
    c1 = rucksack[:compartment_quantity]
    c2 = rucksack[compartment_quantity:]

    # identify the item found in both compartments
    common_letter_set = set(c1).intersection(c2)
    common_letter = list(common_letter_set)[0]

    return common_letter



# %%
#Create a dictionary for letter priority

# a-z character codes are 97-122   
# a-z Priority 1-26

# A-Z haracter codes are 65-90  
# A-Z Priority 27-52

# Add letters to a list in ascending priority order (a to z, then A to Z)
letters = []

#lowercase letters
for c in range(97,123):
    letters.append(chr(c))

#upperrcase letters
for c in range(65,91):
    letters.append(chr(c))

# turn the letter list into a priority dictionary
priority_dict = {}
for v, k in enumerate(letters):
    priority_dict[k] = v+1


# %%
# Create a list of priorities for the common item found in both sides of each rucksack
priority_list = []

for r in rucksacks:
    letter = find_common_letter(r)
    priority = priority_dict[letter]
    priority_list.append(priority)

# %%
# Now just add them all up!
total = sum(priority_list)
print(f"The sum of priorities for the items that showed up in both sides of each ruucksack is {total}")

# %% [markdown]
# 

# %% [markdown]
# ### Part 2
# https://adventofcode.com/2022/day/3#part2

# %%


# total number of groups of three
total_groups = int(len(rucksacks)/3)

# set up a list to contain the group badge prioriy for each group
badge_priority_list = []

# Pop 3 rucksacks off of the list
for g in range(total_groups):
    r1 = rucksacks.pop(0)
    r2 = rucksacks.pop(0)
    r3 = rucksacks.pop(0)

    # find the common letter among the three rucksacks
    l = set(r1).intersection(r2).intersection(r3)
    l = list(l)[0]

    # find the priority for the common letter
    p = priority_dict[l]

    # add the priority for this group to the list of group badge priorities
    badge_priority_list.append(p)


    print(r1)
    print(r2)
    print(r3)
    print(f'letter is {l}')
    print(f'priority is {p}')
    print('\n')
    
   


# %%
# ...and the grand total is.....
badge_priority_total = sum(badge_priority_list)

print(f"The sum of priorities for the badges in each group is {badge_priority_total}")


