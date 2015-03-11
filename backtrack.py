# -*- coding: utf-8 -*-
import random

# First dimension (rows): corporation
# Second dimension (columns): market
grid = [
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10
]
solutions_count = 0


def cell_to_corpo_market(cell):
    return (cell / 10, cell % 10)


base_allowed = [0, 0, 0, 2, 4, 3, 1, 0, 0, 0, 0]


def market_constraint(grid):
    # 1 marché à 6
    # 3 marchés à 5 corpos
    # 4 marchés à 4 corpos
    # 2 marchés à 3
    allowed = [0, 0, 0, 2, 4, 3, 1]
    for corpo in grid:
        nb_markets = sum(corpo)
        if nb_markets >= len(allowed):
            return False
        if nb_markets == 0 or base_allowed[nb_markets] == 0:
            continue
        allowed[nb_markets] -= 1
        if allowed[nb_markets] < 0:
            return False
    if sum(allowed) == 0:
        return True
    else:
        return None


def match_constraint(grid):
    """
    return True if the grid is valid
    """
    return market_constraint(grid)


def backtracker(grid, cell):
    if cell > 99:
        return

    id_corpo, id_market = cell_to_corpo_market(cell)
    grid[id_corpo][id_market] = 1

    is_match = match_constraint(grid)
    # display_grid(grid)
    # print is_match
    # print "###"
    # print
    if is_match:
        # We're done
        display_grid(grid)
        grid[id_corpo][id_market] = 0
        return True
    elif is_match is None:
        # Not enough data yet, try adding more 1
        if backtracker(grid, cell + 1):
            # There was a solution, let's now see if there is another one
            # with a 0 on this cell
            grid[id_corpo][id_market] = 0
            backtracker(grid, cell + 1)
            # But anyway, we have to return True cause we had a solution
            return True
    else:
        # Won't work, let's try something else
        grid[id_corpo][id_market] = 0
        return backtracker(grid, cell + 1)


def display_grid(grid):
    global solutions_count
    solutions_count += 1
    print "--------------------------"
    print "## SOLUTION %s" % solutions_count
    for corpo in grid:
        print corpo
    print "--------------------------"


backtracker(grid, 0)
