def isComplete(assignment):
    for row in assignment:
        for val in row:
            if val == 0 or val == 10:
                return False
    return True


def next_unassigned_variable_MRV(assignment, domains):
    min_domain_size = float('inf')
    selected_var = None

    for i in range(9):
        for j in range(9):
            if assignment[i][j] == 0 or assignment[i][j] == 10:
                domain_size = len(domains[i][j])
                if domain_size < min_domain_size:
                    min_domain_size = domain_size
                    selected_var = (i, j)

    return selected_var

def Domain(var, assignment):
    i, j = var
    domain = []
    if assignment[i][j] == 10:
        domain = [2, 4, 6, 8]
    else:
        if assignment[i][j] == 0:
            domain = [1, 3, 5, 7, 9]
    return domain


def consistent(assignment, var, value):
    i, j = var
    is_even = value % 2 == 0

    for k in range(9):
        if assignment[i][k] == value or assignment[k][j] == value:
            return False

    start_row, start_col = 3 * (i // 3), 3 * (j // 3)
    for x in range(3):
        for y in range(3):
            if (start_row + x != i or start_col + y != j) and assignment[start_row + x][start_col + y] == value:
                return False

    if is_even and assignment[i][j] != 10:
        return False
    if not is_even and assignment[i][j] == 10:
        return False

    return True

def update_domains_FC(domains, var, value):
    i, j = var
    updated_domains = [row[:] for row in domains]

    for k in range(9):
        if k != j and value in updated_domains[i][k]:
            updated_domains[i][k].remove(value)
        if k != i and value in updated_domains[k][j]:
            updated_domains[k][j].remove(value)

    start_row, start_col = 3 * (i // 3), 3 * (j // 3)
    for x in range(3):
        for y in range(3):
            if (start_row + x != i or start_col + y != j) and value in updated_domains[start_row + x][start_col + y]:
                updated_domains[start_row + x][start_col + y].remove(value)

    print(f"Updated domains for cell ({i}, {j}): {updated_domains[i][j]}")

    return updated_domains

def BKT_with_FC(assignment, domains):
    if isComplete(assignment):
        return assignment

    var = next_unassigned_variable_MRV(assignment, domains)
    if var is None:
        return assignment

    i, j = var
    for value in Domain(var, assignment):
        if consistent(assignment, var, value):
            new_assignment = [row[:] for row in assignment]
            new_assignment[i][j] = value
            new_domains = update_domains_FC(domains, var, value)
            result = BKT_with_FC(new_assignment, new_domains)
            if result is not None:
                return result

    return None

if __name__ == '__main__':
    assignment = [
        [0, 10, 10, 3, 0, 0, 10, 10, 0],
        [0, 8, 1, 10, 6, 10, 7, 0, 3],
        [0, 3, 10, 0, 10, 5, 4, 10, 1],
        [0, 0, 3, 10, 10, 10, 0, 6, 0],
        [8, 0, 10, 0, 9, 10, 0, 5, 10],
        [10, 6, 9, 0, 0, 0, 10, 0, 2],
        [10, 10, 10, 5, 0, 1, 10, 3, 0],
        [2, 0, 0, 6, 0, 0, 0, 10, 10],
        [0, 0, 0, 10, 10, 4, 1, 0, 10]
    ]

    domains = [[Domain((i, j), assignment) for j in range(9)] for i in range(9)]

    result = BKT_with_FC(assignment, domains)
    if result is not None:
        print("Soluția pentru Sudoku cu numere pare:")
        for row in result:
            print(row)
    else:
        print("Nu există o soluție posibilă.")
