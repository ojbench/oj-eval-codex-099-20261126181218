"""Compare the executable with an independent disjoint-set reference."""
import random
import subprocess
import sys


def reference(grid):
    rows, columns = len(grid), len(grid[0])
    parent = list(range(rows * columns))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for r in range(rows):
        for c in range(columns):
            if grid[r][c]:
                for nr, nc in ((r + 1, c), (r, c + 1)):
                    if nr < rows and nc < columns and grid[nr][nc]:
                        parent[find(r * columns + c)] = find(nr * columns + nc)
    totals = [0] * (rows * columns)
    for r in range(rows):
        for c in range(columns):
            totals[find(r * columns + c)] += grid[r][c]
    return max(totals)


def main():
    executable = sys.argv[1] if len(sys.argv) > 1 else './build/code'
    cases = [
        [[0, 2, 1, 0], [4, 0, 0, 3], [1, 0, 0, 4], [0, 3, 2, 0]],
        [[0]], [[9]], [[9] * 100 for _ in range(100)],
        [[0] * 100 for _ in range(100)],
        [[9 if (r + c) % 2 else 0 for c in range(100)] for r in range(100)],
        [[1, 2, 0, 9, 9]], [[1], [2], [0], [9], [9]],
    ]
    rng = random.Random(2454)
    for _ in range(500):
        rows, columns = rng.randint(1, 20), rng.randint(1, 20)
        cases.append([[rng.choice([0, 0, 0, 1, 3, 9])
                       for _ in range(columns)] for _ in range(rows)])
    for grid in cases:
        data = f'{len(grid)} {len(grid[0])}\n'
        data += '\n'.join(' '.join(map(str, row)) for row in grid) + '\n'
        result = subprocess.run([executable], input=data, text=True,
                                capture_output=True, check=True, timeout=2)
        assert result.stdout.strip() == str(reference(grid)), (grid, result.stdout)
    print(f'Passed {len(cases)} cases.')


if __name__ == '__main__':
    main()
