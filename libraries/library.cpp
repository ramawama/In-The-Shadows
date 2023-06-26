#include "library.h"
#include "limits.h"

#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <cmath>

using namespace std;

tile::tile(int row, int col) : row(row), col(col), tot(0), dist(0), heur(0) {}

bool tile::operator<(const tile& other) const {
    return tot > other.tot;
}

bool is_valid(int row, int col, int rows, int cols) {
    return (row >= 0 && row < rows && col >= 0 && col < cols);
}

bool not_wall(char* map, int row, int col, int rows, int cols) {
    return (map[((row*cols) + col) * 4] != 'w');
}

int manhattan_dist(int row, int col, int destRow, int destCol) {
    return abs(row - destRow) + abs(col - destCol);
}

extern "C" {
char get_next(int x, int y, char *map, int startx, int starty, int endx, int endy) {
    int rows = y;
    int cols = x;
    vector<int> moveRows = {-1, 1, 0, 0};
    vector<int> moveCols = {0, 0, -1, 1};

    vector < vector < pair < int, int>>> parents(rows, vector < pair < int, int >> (cols, {-1, -1}));
    priority_queue <tile> nearbyTiles;

    vector <vector<int>> costs(rows, vector<int>(cols, INT_MAX));
    int start_row = startx;
    int start_col = starty;
    int end_row = endx;
    int end_col = endy;
    tile start_tile(start_row, start_col);
    start_tile.dist = 0;
    start_tile.heur = manhattan_dist(start_row, start_col, end_row, end_col);
    start_tile.tot = start_tile.dist + start_tile.heur;
    nearbyTiles.push(start_tile);
    costs[start_row][start_col] = 0;

    while (!nearbyTiles.empty()) {
        tile current_tile = nearbyTiles.top();
        nearbyTiles.pop();

        int row = current_tile.row;
        int col = current_tile.col;
        if (row == end_row && col == end_col) {
            vector <pair<int, int>> path;
            while (row != -1 && col != -1) {
                path.push_back({row, col});
                pair<int, int> parent_tile = parents[row][col];
                row = parent_tile.first;
                col = parent_tile.second;
            }
            reverse(path.begin(), path.end());
            int row_diff = path[1].first - start_row;
            int col_diff = path[1].second - start_col;
            if (row_diff > 0) {
                for (int i = 0; i < path.size(); i++) {
                    cout << "RIGHT" << endl;
                    cout << path[i].first << ' ' << path[i].second << endl;
                }
                return 'R';
            } else if (row_diff < 0) {
                cout << "LEFT" << endl;
                for (int i = 0; i < path.size(); i++) {
                    cout << path[i].first << ' ' << path[i].second << endl;
                }
                return 'L';
            } else if (col_diff > 0) {
                cout << "DOWN" << endl;
                for (int i = 0; i < path.size(); i++) {
                    cout << path[i].first << ' ' << path[i].second << endl;
                }
                return 'D';
            } else if (col_diff < 0) {
                cout << "UP" << endl;
                for (int i = 0; i < path.size(); i++) {
                    cout << path[i].first << ' ' << path[i].second << endl;
                }
                return 'U';
            }
        }

        for (int i = 0; i < 4; i++) {
            int new_row = row + moveRows[i];
            int new_col = col + moveCols[i];
            if (is_valid(new_row, new_col, rows, cols) && not_wall(map, new_row, new_col, rows, cols)) {
                int new_dist = current_tile.dist + 1;

                if (new_dist < costs[new_row][new_col]) {
                    costs[new_row][new_col] = new_dist;

                    int new_manhattan = manhattan_dist(new_row, new_col, end_row, end_col);

                    tile neighbor(new_row, new_col);
                    neighbor.dist = new_dist;
                    neighbor.heur = new_manhattan;
                    neighbor.tot = new_dist + new_manhattan;

                    nearbyTiles.push(neighbor);
                    parents[new_row][new_col] = {row, col};
                }
            }
        }
    }
    return 'z';
}
}
