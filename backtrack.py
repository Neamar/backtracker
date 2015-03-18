# -*- coding: utf-8 -*-

# CONSTRAINTS
# 1 corpo dans 6 marchés
# 3 corpos dans 5
# 4 corpos dans 4
# 2 corpos dans 3

# 1 marché dans 6 corpo
# 2 marchés dans 5
# 6 marchés dans 4
# 1 marchés dans 3 corpo

# Toutes les corpos ont minimum 1 marché en commun,
# pas plus que 2 sauf la corpo qui a 6
# qui a trois liens avec les corpos à 5

# # PROBLEM DEFINITION
corporation_count = 10
market_count = 10
# Number of corporation with 0 market, 1 market, ...
base_market_allowed = (0, 0, 0, 2, 4, 3, 1, 0, 0, 0, 0)
# Number of markets with 0 corpo, 1 corpo, 2 corpo, ...
base_corpo_allowed = (0, 0, 0, 1, 6, 2, 1, 0, 0, 0, 0)

# USEFUL CONSTANTS
grid_size = corporation_count * market_count
# First dimension (rows): corporation
# Second dimension (columns): market
grid = [0] * grid_size
solutions_count = 0
max_markets_per_corpo = max(
    i for i, nb_markets
    in enumerate(base_market_allowed)
    if nb_markets > 0
) + 1
max_corpos_per_market = max(
    i for i, nb_markets
    in enumerate(base_market_allowed)
    if nb_markets > 0
) + 1


def corpos_list(grid):
    return (grid[i:i+market_count] for i in range(0, grid_size, market_count))


def market_list(grid):
    return (
        grid[i:grid_size:corporation_count]
        for i in range(0, corporation_count)
    )


def market_constraint(grid):
    # 1 marché à 6
    # 3 marchés à 5 corpos
    # 4 marchés à 4 corpos
    # 2 marchés à 3
    market_allowed = list(base_market_allowed)
    for corpo in corpos_list(grid):
        nb_markets = sum(corpo)
        if nb_markets >= max_corpos_per_market:
            return False
        if nb_markets == 0 or base_market_allowed[nb_markets] == 0:
            continue
        market_allowed[nb_markets] -= 1
        if market_allowed[nb_markets] < 0:
            return False
    if sum(market_allowed) == 0:
        return True
    else:
        return None


def corpo_constraint(grid):
    # 1 corpos à 6
    # 2 corpos à 5
    # 6 corpos à 4 marchés
    # 1 corpo à 3
    corpo_allowed = list(base_corpo_allowed)
    for market in market_list(grid):
        nb_corpos = sum(market)
        if nb_corpos >= max_markets_per_corpo:
            return False
        if nb_corpos == 0 or base_corpo_allowed[nb_corpos] == 0:
            continue
        corpo_allowed[nb_corpos] -= 1
        if corpo_allowed[nb_corpos] < 0:
            return False
    if sum(corpo_allowed) == 0:
        return True
    else:
        return None


def match_constraint(grid):
    """
    return True if the grid is valid,
    False if invalid
    None if not concluding yet
    """
    constraints = (market_constraint(grid),)
    if False in constraints:
        return False
    if None in constraints:
        return None
    return True


def backtracker(grid, cell):
    if cell > grid_size - 1:
        return

    grid[cell] = 1

    is_match = match_constraint(grid)
    # display_grid(grid)
    # print is_match
    # print "###"
    # print
    if is_match:
        # We're done
        display_grid(grid)
        grid[cell] = 0
        return True
    elif is_match is None:
        # Not enough data yet, try adding more 1
        if backtracker(grid, cell + 1):
            # There was a solution, let's now see if there is another one
            # with a 0 on this cell
            grid[cell] = 0
            backtracker(grid, cell + 1)
            # But anyway, we have to return True cause we had a solution
            return True
        else:
            grid[cell] = 0
            return backtracker(grid, cell + 1)
    else:
        # Won't work, let's try something else
        grid[cell] = 0
        return backtracker(grid, cell + 1)


def display_grid(grid):
    global solutions_count
    solutions_count += 1
    print "--------------------------"
    print "## SOLUTION %s" % solutions_count
    for corpo in corpos_list(grid):
        print corpo, sum(corpo)
    print "--------------------------"


backtracker(grid, 0)
