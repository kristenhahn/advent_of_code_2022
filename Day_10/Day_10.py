# Advent of Code 2022
# Day 10
# https://adventofcode.com/2022/day/10

with open ('input.txt') as f:
    data = f.read()

lines = list(data.split('\n'))
lines = list(filter(None, lines))


# split lines into instructions (noop or addx) and addx values (if present)
lines = [l.split(' ') for l in lines]

# set up a dictionary to contain cycle numbers (period DURING each cycle), 
# and X values for that period:  {<cycle_number>:X}
cycle_dict = {1:1}

# set up variables to track current cycle
# and x value
c = 1
x = 1
for l in lines:
    if l[0] == 'noop':
        # add 1 cycle
        c += 1
        # no change to X
        # record status in the cycle dictionary
        cycle_dict[c] = x
    if l[0] == 'addx':
        # add 2 cycles
        c += 2
        # change X
        change_value = int(l[1])
        x += change_value
        # record status in the cycle dictionary
        cycle_dict[c]=x


# fill in missing cycles in the dictionsary.
cycle_dict_keys = list(cycle_dict.keys())
max_cycle = max(cycle_dict_keys)

# Add a placeholder item 0 so that
# part 2 works.  Need to look for 
# a sprite spanning pixels 0-2, 
# so a 0 key is required in the 
# dictionary.

cycle_dict[0]=0

# fill in the rest of the missing cycles
for c in range(2,max_cycle+1):

    if c not in cycle_dict_keys:

        # if this cycle is not in the dictionary,
        # the value hasn't changed since the 
        # most recent recorded cycle.
        cycle_not_found = True

        # lookup the previous cycle
        lookup_c = c-1

        while cycle_not_found:

            # if previous cycle is in the dictionary,
            # take the x value from that previous cycle.
            if lookup_c in cycle_dict.keys():
                x = cycle_dict[lookup_c]
                # assign the same x value to our missing cycle
                cycle_dict[c] = x

                # change flag to stop looking backward
                # through the cycles
                cycle_not_found = False

            # if previous cycle is not in the dictionary,
            # keep stepping back by 1 cycle and see
            # if that one is found.
            else:
                lookup_c -= 1

# Variable to hold the sum of signal strengths
sum_signal_strength = 0

# Find signal strentgh for cycles 60, 100, 140, 180, and 220.
# signal strength = cycle number * x value.
for c in range(20,221,40):

    # # if this cycle is in the dictionary:
    # if c in cycle_dict.keys():
    x = cycle_dict[c]

    # signal strength = cycle * x value
    strength = c * x

    # add signal strength to the running total
    sum_signal_strength += strength

# print the final sum of signal strengths
print(sum_signal_strength)

# Part 2:
# https://adventofcode.com/2022/day/10#part2

# for a pixel to be drawn, cycle number -1 must equal x-1, x, or x+1.

def print_pixels(range_start, range_end):
    pixels = ''
    for c in range(range_start, range_end):
        x = cycle_dict[c]
        
        # each row of 40 starts over at 0
        c_thisrow = c%40

        if x-1 <= c_thisrow-1 <= x+1:
            pixels = pixels + r'#'
        else:
            pixels = pixels + r'.'
    print(pixels)


print_pixels(1,40)
print_pixels(41,80)
print_pixels(81,120)
print_pixels(121,160)
print_pixels(161,200)
print_pixels(201,240)
