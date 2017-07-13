from __future__ import print_function
import numpy as np
from math import factorial

# Alien KenKen
# https://www.geocaching.com/geocache/GC4V7C9_alien-kenken

# Each function takes in a list of numbers and returns the output of the function applied on them

def clubs(nums):
    ret = 0
    for num in nums:
        ret += num * num
    return ret

def diamonds(nums):
    n = len(nums)
    geometric = 1
    arithmetic = 0
    harmonic = 0
    for num in nums:
        geometric *= num
        arithmetic += num
        harmonic += 1.0 / num
    geometric **= 1.0 / n
    arithmetic /= float(n)
    harmonic = n / harmonic
    return int(n * (geometric + arithmetic + harmonic))

def hearts(nums):
    ret = 0
    for num in nums:
        ret += num ** 3
    return int(ret ** 0.5)

def spades(nums):
    product = 1
    for num in nums:
        product *= num
    return sum(nums) + int(product ** 0.5)

# Increments the list of unordered numbers

def increment(nums):
    for i in range(len(nums) - 1, -1, -1):
        if nums[i] < 9:
            break
    nums[i] += 1
    for i in range(i + 1, len(nums)):
        nums[i] = nums[i - 1]

# Returns a list of all tuples such that:
# Each tuple contains n integers
# The result of the function applied on each tuple is target

def get_tuples(func, n, target, **kwargs):
    cur = [1] * n
    end = [9] * n
    ret = []
    while cur <= end:
        if func(cur) == target:
            ret.append(cur[:])
        increment(cur)
    return ret

# Each element in groups is a group of squares
# Changing the order may increase the speed of solving

groups = [{"func": spades, "n": 5, "target": 104, "squares": [(3, 4), (4, 3), (4, 4), (4, 5), (5, 4)]},
         {"func": diamonds, "n": 2, "target": 13, "squares": [(1, 4), (2, 4)]},
         {"func": hearts, "n": 2, "target": 28, "squares": [(6, 4), (7, 4)]},
         {"func": clubs, "n": 2, "target": 34, "squares": [(4, 1), (4, 2)]},
         {"func": spades, "n": 2, "target": 15, "squares": [(4, 6), (4, 7)]},
         {"func": hearts, "n": 4, "target": 39, "squares": [(2, 2), (2, 3), (3, 2), (3, 3)]},
         {"func": hearts, "n": 4, "target": 20, "squares": [(2, 5), (2, 6), (3, 5), (3, 6)]},
         {"func": spades, "n": 4, "target": 21, "squares": [(5, 2), (5, 3), (6, 2), (6, 3)]},
         {"func": diamonds, "n": 4, "target": 79, "squares": [(5, 5), (5, 6), (6, 5), (6, 6)]},
         {"func": hearts, "n": 5, "target": 36, "squares": [(1, 1), (1, 2), (1, 3), (2, 1), (3, 1)]},
         {"func": hearts, "n": 5, "target": 34, "squares": [(1, 5), (1, 6), (1, 7), (2, 7), (3, 7)]},
         {"func": clubs, "n": 5, "target": 130, "squares": [(5, 1), (6, 1), (7, 1), (7, 2), (7, 3)]},
         {"func": clubs, "n": 5, "target": 91, "squares": [(5, 7), (6, 7), (7, 5), (7, 6), (7, 7)]},
         {"func": diamonds, "n": 3, "target": 29, "squares": [(0, 3), (0, 4), (0, 5)]},
         {"func": spades, "n": 3, "target": 24, "squares": [(8, 3), (8, 4), (8, 5)]},
         {"func": hearts, "n": 3, "target": 9, "squares": [(3, 0), (4, 0), (5, 0)]},
         {"func": hearts, "n": 3, "target": 18, "squares": [(3, 8), (4, 8), (5, 8)]},
         {"func": clubs, "n": 5, "target": 237, "squares": [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)]},
         {"func": diamonds, "n": 5, "target": 72, "squares": [(0, 6), (0, 7), (0, 8), (1, 8), (2, 8)]},
         {"func": diamonds, "n": 5, "target": 84, "squares": [(6, 0), (7, 0), (8, 0), (8, 1), (8, 2)]},
         {"func": hearts, "n": 5, "target": 35, "squares": [(6, 8), (7, 8), (8, 6), (8, 7), (8, 8)]}]
num_groups = len(groups)

for group in groups:
    group["tuples"] = get_tuples(**group)

# Corresponding group for each square
cg = np.array([[None] * 9 for i in range(9)])
for group in groups:
    for coords in group["squares"]:
        cg[coords] = group

# Recursive backtracking to find solution
# Iterates through each square in each group
# Updates valid tuples for each square

board = np.array([[0] * 9 for i in range(9)])

counter = 0
progress = 0
denominator = 1

def solve():
    # Testing
    global counter
    global progress
    global denominator
    counter += 1
    if counter % 1000 == 0:
        print(counter)
        print(progress)
        print(board)

    # Condition for solved
    if 0 not in board.flatten():
        return True
    # Find square with least amount of valid tuples
    r, c = -1, -1
    valid = [0] * 10
    tuple_count = 1000000
    for i in range(9):
        for j in range(9):
            if board[i][j] > 0:
                continue
            cur = []
            cur_count = 0
            for k in range(1, 10):
                # Number is not in row, column, and exists in valid tuples
                if k not in board[i, :] and k not in board[:, j]:
                    for t in cg[i, j]["tuples"]:
                        if k in t:
                            cur_count += 1
                            if k not in cur:
                                cur.append(k)
            if len(cur) < len(valid) or (len(cur) == len(valid) and cur_count < tuple_count):
                valid = cur
                tuple_count = cur_count
                r, c = i, j
    # No solutions
    if len(valid) == 0:
        return False
    # For approximating amount of puzzle searched
    denominator *= tuple_count
    # Guess each valid number
    old_tuples = cg[r, c]["tuples"]
    for num in valid:
        board[r, c] = num
        # Update valid tuples
        cg[r, c]["tuples"] = [t[:] for t in old_tuples if num in t]
        for t in cg[r, c]["tuples"]:
            t.remove(num)
        # Solution found
        if solve():
            return True
        # Approximate amount of puzzle searched
        progress += float(len(cg[r, c]["tuples"])) / denominator
    # None of the numbers worked
    # Reset stuff
    cg[r, c]["tuples"] = old_tuples
    board[r, c] = 0
    denominator /= tuple_count
    progress -= 1.0 / denominator
    return False

if solve():
    print(board)
else:
    print("No solutions found")
print(counter)
