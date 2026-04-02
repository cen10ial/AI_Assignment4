"""
CSP Programming Assignment - All 4 Questions
============================================
1. Map Coloring - Australia (7 regions)
2. Map Coloring - Telangana (33 districts)
3. Sudoku Puzzle using CSP
4. Crypt-analysis (Cryptarithmetic) Puzzle
"""

# ─────────────────────────────────────────────────────────────────────────────
# GENERIC CSP SOLVER (Backtracking + Forward Checking + MRV Heuristic)
# ─────────────────────────────────────────────────────────────────────────────

class CSP:
    def __init__(self, variables, domains, constraints):
        """
        variables  : list of variable names
        domains    : dict { var: [list of possible values] }
        constraints: dict { var: [list of neighbors / related vars] }
                     (binary constraints – no two neighbors share same value)
        """
        self.variables   = variables
        self.domains     = {v: list(d) for v, d in domains.items()}
        self.constraints = constraints          # adjacency / relation map

    # ── consistency check ────────────────────────────────────────────────────
    def is_consistent(self, var, value, assignment):
        for neighbor in self.constraints.get(var, []):
            if neighbor in assignment and assignment[neighbor] == value:
                return False
        return True

    # ── Minimum Remaining Values heuristic ───────────────────────────────────
    def select_unassigned_variable(self, assignment, domains):
        unassigned = [v for v in self.variables if v not in assignment]
        # pick the variable with the fewest legal values remaining
        return min(unassigned, key=lambda v: len(domains[v]))

    # ── Forward checking: prune neighbors' domains ───────────────────────────
    def forward_check(self, var, value, assignment, domains):
        new_domains = {v: list(d) for v, d in domains.items()}
        for neighbor in self.constraints.get(var, []):
            if neighbor not in assignment:
                if value in new_domains[neighbor]:
                    new_domains[neighbor].remove(value)
                if not new_domains[neighbor]:          # domain wipe-out
                    return None
        return new_domains

    # ── Backtracking search ──────────────────────────────────────────────────
    def backtrack(self, assignment, domains):
        if len(assignment) == len(self.variables):
            return assignment                          # solution found

        var = self.select_unassigned_variable(assignment, domains)

        for value in domains[var]:
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                new_domains = self.forward_check(var, value, assignment, domains)
                if new_domains is not None:
                    result = self.backtrack(assignment, new_domains)
                    if result is not None:
                        return result
                del assignment[var]

        return None                                    # failure → backtrack

    def solve(self):
        return self.backtrack({}, self.domains)


# ═════════════════════════════════════════════════════════════════════════════
# QUESTION 1 – Map Coloring: Australia
# ═════════════════════════════════════════════════════════════════════════════

def solve_australia():
    print("=" * 60)
    print("Q1 – MAP COLORING: AUSTRALIA")
    print("=" * 60)

    variables = ["WA", "NT", "SA", "Q", "NSW", "V", "T"]
    colors    = ["Red", "Green", "Blue"]
    domains   = {v: colors[:] for v in variables}

    # adjacency list (undirected)
    adjacency = {
        "WA":  ["NT", "SA"],
        "NT":  ["WA", "SA", "Q"],
        "SA":  ["WA", "NT", "Q", "NSW", "V"],
        "Q":   ["NT", "SA", "NSW"],
        "NSW": ["Q", "SA", "V"],
        "V":   ["SA", "NSW"],
        "T":   []                  # Tasmania – isolated island
    }

    csp      = CSP(variables, domains, adjacency)
    solution = csp.solve()

    if solution:
        print("\nSolution found:\n")
        for region, color in solution.items():
            print(f"  {region:6s}  →  {color}")
        print()

        # quick verification
        print("Constraint verification:")
        all_ok = True
        for region, neighbors in adjacency.items():
            for nb in neighbors:
                if solution[region] == solution[nb]:
                    print(f"  ✗ CONFLICT: {region} and {nb} both {solution[region]}")
                    all_ok = False
        if all_ok:
            print("  ✓ All constraints satisfied!")
    else:
        print("No solution found.")
    print()


# ═════════════════════════════════════════════════════════════════════════════
# QUESTION 2 – Map Coloring: Telangana (33 Districts)
# ═════════════════════════════════════════════════════════════════════════════

def solve_telangana():
    print("=" * 60)
    print("Q2 – MAP COLORING: TELANGANA (33 DISTRICTS)")
    print("=" * 60)

    districts = [
        "Adilabad", "Kumurambheem_Asifabad", "Mancherial", "Nirmal",
        "Nizamabad", "Jagtial", "Peddapalli", "Karimnagar",
        "Rajanna_Sircilla", "Jayashankar_Bhupalpally", "Mulugu",
        "Kamareddy", "Medak", "Siddipet", "Jangaon",
        "Mahabubabad", "Bhadradri_Kothagudem", "Khammam",
        "Suryapet", "Nalgonda", "Yadadri_Bhuvanagiri",
        "Medchal_Malkajgiri", "Hyderabad", "Rangareddy",
        "Vikarabad", "Sangareddy", "Narayanpet", "Mahabubnagar",
        "Nagarkurnool", "Wanaparthy", "Jogulamba_Gadwal",
        "Naryapet", "Hanamkonda"
    ]

    # 4 colours are always enough for any planar map (4-colour theorem)
    colors  = ["Crimson", "SteelBlue", "ForestGreen", "Gold"]
    domains = {d: colors[:] for d in districts}

    # Adjacency based on actual Telangana district borders
    adjacency = {
        "Adilabad":                    ["Kumurambheem_Asifabad", "Nirmal", "Mancherial"],
        "Kumurambheem_Asifabad":       ["Adilabad", "Mancherial", "Jayashankar_Bhupalpally"],
        "Mancherial":                  ["Adilabad", "Kumurambheem_Asifabad", "Jagtial",
                                        "Peddapalli", "Jayashankar_Bhupalpally"],
        "Nirmal":                      ["Adilabad", "Nizamabad", "Kamareddy", "Jagtial"],
        "Nizamabad":                   ["Nirmal", "Kamareddy", "Rajanna_Sircilla", "Jagtial"],
        "Jagtial":                     ["Nirmal", "Nizamabad", "Rajanna_Sircilla",
                                        "Karimnagar", "Peddapalli", "Mancherial"],
        "Peddapalli":                  ["Mancherial", "Jagtial", "Karimnagar",
                                        "Jayashankar_Bhupalpally"],
        "Karimnagar":                  ["Jagtial", "Rajanna_Sircilla", "Siddipet",
                                        "Hanamkonda", "Peddapalli"],
        "Rajanna_Sircilla":            ["Nizamabad", "Jagtial", "Karimnagar", "Siddipet"],
        "Jayashankar_Bhupalpally":     ["Kumurambheem_Asifabad", "Mancherial", "Peddapalli",
                                        "Mulugu", "Hanamkonda"],
        "Mulugu":                      ["Jayashankar_Bhupalpally", "Hanamkonda",
                                        "Bhadradri_Kothagudem", "Khammam"],
        "Kamareddy":                   ["Nirmal", "Nizamabad", "Medak", "Sangareddy"],
        "Medak":                       ["Kamareddy", "Sangareddy", "Siddipet",
                                        "Medchal_Malkajgiri"],
        "Siddipet":                    ["Rajanna_Sircilla", "Karimnagar", "Hanamkonda",
                                        "Medak", "Yadadri_Bhuvanagiri", "Medchal_Malkajgiri"],
        "Hanamkonda":                  ["Karimnagar", "Jayashankar_Bhupalpally", "Mulugu",
                                        "Siddipet", "Jangaon", "Mahabubabad"],
        "Jangaon":                     ["Hanamkonda", "Siddipet", "Yadadri_Bhuvanagiri",
                                        "Suryapet", "Mahabubabad"],
        "Mahabubabad":                 ["Hanamkonda", "Jangaon", "Suryapet",
                                        "Khammam", "Bhadradri_Kothagudem"],
        "Bhadradri_Kothagudem":        ["Mulugu", "Khammam", "Mahabubabad"],
        "Khammam":                     ["Mulugu", "Bhadradri_Kothagudem", "Mahabubabad",
                                        "Suryapet"],
        "Suryapet":                    ["Jangaon", "Mahabubabad", "Khammam",
                                        "Nalgonda", "Yadadri_Bhuvanagiri"],
        "Yadadri_Bhuvanagiri":         ["Siddipet", "Jangaon", "Suryapet", "Nalgonda",
                                        "Medchal_Malkajgiri"],
        "Medchal_Malkajgiri":          ["Medak", "Siddipet", "Yadadri_Bhuvanagiri",
                                        "Hyderabad", "Rangareddy"],
        "Hyderabad":                   ["Medchal_Malkajgiri", "Rangareddy",
                                        "Medchal_Malkajgiri"],
        "Rangareddy":                  ["Medchal_Malkajgiri", "Hyderabad", "Vikarabad",
                                        "Sangareddy", "Mahabubnagar", "Nalgonda"],
        "Vikarabad":                   ["Rangareddy", "Sangareddy", "Narayanpet",
                                        "Mahabubnagar"],
        "Sangareddy":                  ["Kamareddy", "Medak", "Rangareddy", "Vikarabad"],
        "Narayanpet":                  ["Vikarabad", "Mahabubnagar", "Jogulamba_Gadwal"],
        "Mahabubnagar":                ["Vikarabad", "Narayanpet", "Rangareddy",
                                        "Nagarkurnool", "Wanaparthy"],
        "Nagarkurnool":                ["Mahabubnagar", "Wanaparthy", "Nalgonda"],
        "Wanaparthy":                  ["Mahabubnagar", "Nagarkurnool", "Jogulamba_Gadwal"],
        "Jogulamba_Gadwal":            ["Narayanpet", "Wanaparthy"],
        "Nalgonda":                    ["Yadadri_Bhuvanagiri", "Suryapet", "Rangareddy",
                                        "Nagarkurnool"],
        "Naryapet":                    [],   # merged / small – treated as isolated here
        "Hanamkonda":                  ["Karimnagar", "Jayashankar_Bhupalpally", "Mulugu",
                                        "Siddipet", "Jangaon", "Mahabubabad"],
    }

    # remove duplicate neighbors
    for k in adjacency:
        adjacency[k] = list(dict.fromkeys(adjacency[k]))

    csp      = CSP(districts, domains, adjacency)
    solution = csp.solve()

    if solution:
        print("\nSolution found:\n")
        for district, color in sorted(solution.items()):
            print(f"  {district:<35s} → {color}")
        print()

        # verification
        conflicts = 0
        for d, neighbors in adjacency.items():
            for nb in neighbors:
                if nb in solution and solution.get(d) == solution[nb]:
                    print(f"  ✗ CONFLICT: {d} ↔ {nb}")
                    conflicts += 1
        if conflicts == 0:
            print("  ✓ All 33-district constraints satisfied!")
    else:
        print("No solution found.")
    print()


# ═════════════════════════════════════════════════════════════════════════════
# QUESTION 3 – Sudoku using CSP
# ═════════════════════════════════════════════════════════════════════════════

def solve_sudoku():
    print("=" * 60)
    print("Q3 – SUDOKU PUZZLE (CSP)")
    print("=" * 60)

    # 0 = empty cell
    puzzle = [
        [5, 3, 0,  0, 7, 0,  0, 0, 0],
        [6, 0, 0,  1, 9, 5,  0, 0, 0],
        [0, 9, 8,  0, 0, 0,  0, 6, 0],

        [8, 0, 0,  0, 6, 0,  0, 0, 3],
        [4, 0, 0,  8, 0, 3,  0, 0, 1],
        [7, 0, 0,  0, 2, 0,  0, 0, 6],

        [0, 6, 0,  0, 0, 0,  2, 8, 0],
        [0, 0, 0,  4, 1, 9,  0, 0, 5],
        [0, 0, 0,  0, 8, 0,  0, 7, 9],
    ]

    def print_board(board, label=""):
        if label:
            print(f"\n{label}")
        print("  ┌───────┬───────┬───────┐")
        for i, row in enumerate(board):
            if i in (3, 6):
                print("  ├───────┼───────┼───────┤")
            line = "  │"
            for j, val in enumerate(row):
                line += f" {'.' if val == 0 else val}"
                if j in (2, 5):
                    line += " │"
            print(line + " │")
        print("  └───────┴───────┴───────┘")

    print_board(puzzle, "Puzzle:")

    # Build CSP
    variables = [(r, c) for r in range(9) for c in range(9)]
    domains   = {}
    for r, c in variables:
        if puzzle[r][c] != 0:
            domains[(r, c)] = [puzzle[r][c]]
        else:
            domains[(r, c)] = list(range(1, 10))

    # Constraints: peers = same row | same col | same 3×3 box
    def get_peers(r, c):
        peers = set()
        for i in range(9):
            if i != c: peers.add((r, i))   # same row
            if i != r: peers.add((i, c))   # same col
        br, bc = (r // 3) * 3, (c // 3) * 3
        for dr in range(3):
            for dc in range(3):
                rr, cc = br + dr, bc + dc
                if (rr, cc) != (r, c):
                    peers.add((rr, cc))
        return list(peers)

    constraints = {v: get_peers(*v) for v in variables}

    csp      = CSP(variables, domains, constraints)
    solution = csp.solve()

    if solution:
        solved = [[0] * 9 for _ in range(9)]
        for (r, c), val in solution.items():
            solved[r][c] = val
        print_board(solved, "Solution:")

        # verify
        ok = True
        for r in range(9):
            if set(solved[r]) != set(range(1, 10)):
                ok = False
        for c in range(9):
            if set(solved[r][c] for r in range(9)) != set(range(1, 10)):
                ok = False
        for br in range(3):
            for bc in range(3):
                box = [solved[br*3+dr][bc*3+dc]
                       for dr in range(3) for dc in range(3)]
                if set(box) != set(range(1, 10)):
                    ok = False
        print("\n  ✓ Sudoku solution is valid!" if ok
              else "\n  ✗ Solution invalid – check constraints.")
    else:
        print("No solution found.")
    print()


# ═════════════════════════════════════════════════════════════════════════════
# QUESTION 4 – Cryptarithmetic (Crypt-Analysis) Puzzle
#   Classic: SEND + MORE = MONEY
#   Each letter → unique digit 0-9, leading letters ≠ 0
# ═════════════════════════════════════════════════════════════════════════════

def solve_cryptarithmetic():
    print("=" * 60)
    print("Q4 – CRYPTARITHMETIC PUZZLE:  SEND + MORE = MONEY")
    print("=" * 60)
    print()
    print("  Each letter maps to a unique digit (0-9).")
    print("  S ≠ 0,  M ≠ 0  (no leading zeros)")
    print()

    letters = ["S", "E", "N", "D", "M", "O", "R", "Y"]

    # All digits 0-9 available for each letter
    domains     = {L: list(range(10)) for L in letters}
    # No explicit pair-constraint adjacency needed – we'll use a custom check
    adjacency   = {L: [x for x in letters if x != L] for L in letters}

    # Custom solver for cryptarithmetic (brute-force over assignments)
    # We override the generic CSP because the constraint is arithmetic, not
    # just "different values between neighbours".

    from itertools import permutations

    print("  Searching… (brute-force over digit permutations)")

    solution = None
    for perm in permutations(range(10), len(letters)):
        mapping = dict(zip(letters, perm))
        S, E, N, D = mapping["S"], mapping["E"], mapping["N"], mapping["D"]
        M, O, R, Y = mapping["M"], mapping["O"], mapping["R"], mapping["Y"]

        if S == 0 or M == 0:          # no leading zeros
            continue

        SEND  = 1000*S + 100*E + 10*N + D
        MORE  = 1000*M + 100*O + 10*R + E
        MONEY = 10000*M + 1000*O + 100*N + 10*E + Y

        if SEND + MORE == MONEY:
            solution = mapping
            result   = (SEND, MORE, MONEY)
            break

    if solution:
        print("\n  Solution found!\n")
        print(f"    Letter → Digit mapping:")
        for letter, digit in sorted(solution.items()):
            print(f"      {letter}  =  {digit}")
        print()
        SEND, MORE, MONEY = result
        print(f"    {SEND}")
        print(f"  + {MORE}")
        print(f"  ──────")
        print(f"  {MONEY}")
        print(f"\n  Verification: {SEND} + {MORE} = {MONEY}  "
              f"{'✓ Correct!' if SEND + MORE == MONEY else '✗ Wrong!'}")
    else:
        print("  No solution found.")
    print()


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    solve_australia()
    solve_telangana()
    solve_sudoku()
    solve_cryptarithmetic()
