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


# Variable to hold the sum of signal strengths
sum_signal_strength = 0

# Find signal strentgh for cycles 60, 100, 140, 180, and 220.
# signal strength = cycle number * x value.
for c in range(20,221,40):

    # if this cycle is in the dictionary:
    if c in cycle_dict.keys():
        x = cycle_dict[c]

    # if this cycle is not in the dictionary,
    # the value hasn't changed since the 
    # most recent recorded cycle.
    else:
        cycle_not_found = True

        # lookup the previous cycle
        lookup_c = c-1

        while cycle_not_found:

            # if previous cycle is in the dictionary,
            # take the x value from that previous cycle.
            if lookup_c in cycle_dict.keys():
                x = cycle_dict[lookup_c]

                # change flag to stop looking backward
                # through the cycles
                cycle_not_found = False

            # if previous cycle is not in the dictionary,
            # keep stepping back by 1 cycle and see
            # if that one is found.
            else:
                lookup_c -= 1

    # signal strength = cycle * x value
    strength = c * x

    # add signal strength to the running total
    sum_signal_strength += strength

# print the final sum of signal strengths
print(sum_signal_strength)

# Part 2:
# https://adventofcode.com/2022/day/10#part2

# for a pixel to be drawn, cycle numnber has to equal x-1, x, or x+1.

# Add the cycles missing from the dictionary

# for c in range(242):
#     if c not in cycle_dict.keys():



# print(cycle_dict)


