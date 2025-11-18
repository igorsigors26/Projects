from typing import List, Sequence

NumberGrid = Sequence[Sequence[int]]


def find_greatest_product_of_contiguous_integers(
    grid: NumberGrid,
    contiguous_integers: int
) -> int:
    """
    Find the greatest product of `contiguous_integers` adjacent numbers in the same
    direction in a 2D grid.

    Directions considered:
        - Horizontal  (left → right and right → left)
        - Vertical    (top → bottom and bottom → top)
        - Diagonal    (top-left → bottom-right and bottom-right → top-left)
        - Diagonal    (top-right → bottom-left and bottom-left → top-right)

    Args:
        grid: 2D sequence of ints representing the number grid.
        contiguous_integers: Length of each run of adjacent numbers.

    Returns:
        The maximum product found as an int.

    Raises:
        ValueError: If the grid is empty, rows have different lengths,
                    or contiguous_integers < 1.
    """
    if contiguous_integers < 1:
        raise ValueError("contiguous_integers must be >= 1")

    if not grid:
        raise ValueError("Grid must not be empty")

    row_count = len(grid)
    col_count = len(grid[0])

    # Ensure grid is rectangular
    if any(len(row) != col_count for row in grid):
        raise ValueError("All rows in the grid must have the same length")

    k = contiguous_integers
    max_product = None

    # Directions: (dr, dc)
    directions = [
        (0, 1),   # right
        (1, 0),   # down
        (1, 1),   # down-right
        (1, -1),  # down-left
    ]

    for r in range(row_count):
        for c in range(col_count):
            for dr, dc in directions:
                # End cell (r + (k-1)*dr, c + (k-1)*dc) must be inside grid
                end_r = r + (k - 1) * dr
                end_c = c + (k - 1) * dc

                if not (0 <= end_r < row_count and 0 <= end_c < col_count):
                    continue

                product = 1
                for i in range(k):
                    rr = r + i * dr
                    cc = c + i * dc
                    product *= grid[rr][cc]

                if max_product is None or product > max_product:
                    max_product = product

    # If grid is non-empty and k >= 1, we must have found something
    return max_product if max_product is not None else 0


# --- Optional helpers / tests for your submission ---

def count_unique_combinations_of_length_k(grid: NumberGrid, k: int) -> int:
    """
    Counts how many unique combinations of length k exist in the grid
    in the four base directions (right, down, down-right, down-left),
    treating a line and its reverse as the same combination for counting.

    This matches the clarification in the task about not distinguishing
    left→right vs right→left, etc.
    """
    row_count = len(grid)
    col_count = len(grid[0]) if row_count > 0 else 0

    directions = [
        (0, 1),   # right
        (1, 0),   # down
        (1, 1),   # down-right
        (1, -1),  # down-left
    ]

    seen = set()

    for r in range(row_count):
        for c in range(col_count):
            for dr, dc in directions:
                end_r = r + (k - 1) * dr
                end_c = c + (k - 1) * dc

                if not (0 <= end_r < row_count and 0 <= end_c < col_count):
                    continue

                seq = []
                for i in range(k):
                    rr = r + i * dr
                    cc = c + i * dc
                    seq.append(grid[rr][cc])

                # Treat sequence and its reverse as the same combination
                fwd = tuple(seq)
                rev = tuple(reversed(seq))
                canonical = min(fwd, rev)
                seen.add(canonical)

    return len(seen)


if __name__ == "__main__":
    # Sample 10x10 grid from the test
    grid = [
        [8, 2, 22, 97, 38, 15, 0, 40, 0, 75],
        [49, 49, 99, 40, 17, 81, 18, 57, 60, 87],
        [81, 49, 31, 73, 55, 79, 14, 29, 93, 71],
        [52, 70, 95, 23, 4, 60, 11, 42, 69, 24],
        [22, 31, 16, 71, 51, 67, 63, 89, 41, 92],
        [24, 47, 32, 60, 99, 3, 45, 2, 44, 75],
        [32, 98, 81, 28, 64, 23, 67, 10, 26, 38],
        [67, 26, 20, 68, 2, 62, 12, 20, 95, 63],
        [24, 55, 58, 5, 66, 73, 99, 26, 97, 17],
        [21, 36, 23, 9, 75, 0, 76, 44, 20, 45],
    ]

    # Question 1: how many combinations of length 3?
    combos_len_3 = count_unique_combinations_of_length_k(grid, 3)
    print("Unique combinations of length 3:", combos_len_3)  # Expected: 288

    # Question 2: greatest product of 3 adjacent numbers
    max_prod_3 = find_greatest_product_of_contiguous_integers(grid, 3)
    print("Greatest product for length 3:", max_prod_3)  # Expected: 667755
