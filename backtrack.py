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
# Number of corporation with 0 market, 1 market, ...
corporations_with_n_markets = (0, 0, 0, 2, 4, 3, 1, 0, 0, 0, 0)
corporations_with_n_markets = (0, 1, 2, 0, 1)
# Number of markets with 0 corpo, 1 corpo, 2 corpo, ...
markets_with_n_corporations = (0, 0, 0, 1, 6, 2, 1, 0, 0, 0, 0)
markets_with_n_corporations = (0, 1, 2, 0, 1)

# USEFUL CONSTANTS

corporation_count = len(corporations_with_n_markets) - 1
market_count = len(markets_with_n_corporations) - 1
grid_size = corporation_count * market_count
# First dimension (rows): corporation
# Second dimension (columns): market
grid = [0] * grid_size
solutions_count = 0
max_markets_per_corpo = max(
    i for i, nb_markets
    in enumerate(corporations_with_n_markets)
    if nb_markets > 0
) + 1
max_corpos_per_market = max(
    i for i, nb_corpos
    in enumerate(markets_with_n_corporations)
    if nb_corpos > 0
) + 1


class unique_element:
    def __init__(self, value, occurrences):
        self.value = value
        self.occurrences = occurrences


def perm_unique(elements):
    eset = set(elements)
    listunique = [unique_element(i, elements.count(i)) for i in eset]
    u = len(elements)
    return perm_unique_helper(listunique, [0] * u, u - 1)


def perm_unique_helper(listunique, result_list, d):
    if d < 0:
        yield tuple(result_list)
    else:
        for i in listunique:
            if i.occurrences > 0:
                result_list[d] = i.value
                i.occurrences -= 1
                for g in perm_unique_helper(listunique, result_list, d - 1):
                    yield g
                i.occurrences += 1


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
    market_allowed = list(corporations_with_n_markets)
    for corpo in corpos_list(grid):
        nb_markets = sum(corpo)
        if nb_markets >= max_corpos_per_market:
            return False
        if nb_markets == 0 or corporations_with_n_markets[nb_markets] == 0:
            continue
        market_allowed[nb_markets] -= 1
        if market_allowed[nb_markets] < 0:
            return False
    if max(market_allowed) == 0:
        return True
    else:
        return None


def corpo_constraint(grid):
    # 1 corpos à 6
    # 2 corpos à 5
    # 6 corpos à 4 marchés
    # 1 corpo à 3
    corpo_allowed = list(markets_with_n_corporations)

    for market in market_list(grid):
        nb_corpos = sum(market)
        if nb_corpos >= max_markets_per_corpo:
            return False
        if nb_corpos == 0 or markets_with_n_corporations[nb_corpos] == 0:
            continue
        corpo_allowed[nb_corpos] -= 1
        if corpo_allowed[nb_corpos] < 0:
            return False
    if max(corpo_allowed) == 0:
        return True
    else:
        return None


def match_constraint(grid):
    """
    return True if the grid is valid,
    False if invalid
    None if not concluding yet
    """
    constraint = corpo_constraint(grid)
    return constraint


def display_grid(grid):
    global solutions_count
    solutions_count += 1
    print "--------------------------"
    print "## SOLUTION %s" % solutions_count
    for corpo in corpos_list(grid):
        print corpo, sum(corpo)
    print "--------------------------"


def base_grid_generator():
    # Generates all valid grids matching corporation constraints only
    lines = []
    for i, count in enumerate(corporations_with_n_markets):
        for j in range(count):
            line = ([1] * i)
            line.extend([0] * (corporation_count - i))
            lines.append(tuple(line))

    for grid in column_permutator(lines, 0):
        yield grid


def column_permutator(lines_permutation, line_index):
    # We need to permute all columns
    if line_index < corporation_count:
        line = lines_permutation[line_index]

        permutations = list(perm_unique(line))
        # Only run on first half, symetric after
        permutations = permutations[0:len(permutations) / 2 + 1]

        for i, line_variation in enumerate(permutations):
            if line_index < 8:
                print "%s : %s / %s" % (line_index, i, len(permutations))
            new_lines_permutation = list(lines_permutation)
            new_lines_permutation[line_index] = line_variation

            next_columns = column_permutator(
                new_lines_permutation,
                line_index + 1
            )
            for grid in next_columns:
                yield grid
    else:
        grid = []
        for l in lines_permutation:
            grid += l
        yield grid


if __name__ == "__main__":
    for grid in base_grid_generator():
        if match_constraint(grid):
            display_grid(grid)
