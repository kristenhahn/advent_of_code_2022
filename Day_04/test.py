import re

def parse_input(input_str):
    pairs = []
    for pair in input_str.splitlines():
        a, b, c, d = map(int, re.findall(r'\d+', pair))
        one = set(range(a, b + 1))
        other = set(range(c, d + 1))
        pairs.append((one, other))
    return pairs



def solve_first(pairs):
    return sum(one >= other or one <= other for one, other in pairs)



def solve_second(pairs):
    return sum(bool(one & other) for one, other in pairs)


if __name__ == '__main__':
    pairs = parse_input(get_input(4, year=2022))
    solve_first(pairs)
    solve_second(pairs)


solve_first(camp_area_ranges.txt)