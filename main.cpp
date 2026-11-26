#include <algorithm>
#include <iostream>
#include <utility>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int rows, columns;
    if (!(std::cin >> rows >> columns)) {
        return 0;
    }
    std::vector<std::vector<int>> lake(rows, std::vector<int>(columns));
    for (auto& row : lake) {
        for (int& fish : row) {
            std::cin >> fish;
        }
    }

    constexpr int dr[] = {-1, 1, 0, 0};
    constexpr int dc[] = {0, 0, -1, 1};
    std::vector<std::pair<int, int>> pending;
    int best = 0;
    for (int row = 0; row < rows; ++row) {
        for (int column = 0; column < columns; ++column) {
            if (lake[row][column] == 0) {
                continue;
            }
            int total = lake[row][column];
            lake[row][column] = 0;
            pending.emplace_back(row, column);
            while (!pending.empty()) {
                const auto [r, c] = pending.back();
                pending.pop_back();
                for (int direction = 0; direction < 4; ++direction) {
                    const int nr = r + dr[direction];
                    const int nc = c + dc[direction];
                    if (nr < 0 || nr >= rows || nc < 0 || nc >= columns ||
                        lake[nr][nc] == 0) {
                        continue;
                    }
                    // Clear on discovery so every cell is counted exactly once.
                    total += lake[nr][nc];
                    lake[nr][nc] = 0;
                    pending.emplace_back(nr, nc);
                }
            }
            best = std::max(best, total);
        }
    }
    std::cout << best << '\n';
}
