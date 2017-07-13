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
    group["tuples"] = [None] * group["n"]
    group["tuples"][0] = get_tuples(**group)

# Recursive backtracking to find solution
# Iterates through each square in each group
# Updates valid tuples for each square

board = np.array([[0] * 9 for i in range(9)])
end = [num_groups, 0]

counter = 0

def solve(cur=[0, 0]):
    # Testing
    global counter
    counter += 1
    if counter % 1000000 == 0:
        print(counter)
        print(board)
    # If solution is found, return True
    if cur == end:
        return True
    # Current group
    g = groups[cur[0]]
    # Row and column of current square to guess
    r, c = g["squares"][cur[1]]
    # Index in groups for next square (groups index, squares index)
    next = cur[:]
    next[1] += 1
    if next[1] == g["n"]:
        next[0] += 1
        next[1] = 0
    # Trying every number from 1-9
    for i in range(1, 10):
        # i already exists in current row or column
        if i in board[r, :] or i in board[:, c]:
            continue
        # Get tuples containing i
        valid_tuples = [t[:] for t in g["tuples"][cur[1]] if i in t]
        # No valid tuples
        if not valid_tuples:
            continue
        # Update g["tuples"] with new valid tuples
        if cur[0] == next[0]:
            # i is removed because it's already used
            for t in valid_tuples:
                t.remove(i)
            g["tuples"][next[1]] = valid_tuples
        # Update board
        board[r, c] = i
        # If solution found, don't continue searching
        if solve(next):
            return True
    # No solutions found here
    board[r, c] = 0
    return False

if solve():
    print(board)
else:
    print("No solutions found")
print(counter)
