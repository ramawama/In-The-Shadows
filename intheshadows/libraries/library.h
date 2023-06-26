#ifndef LIBRARIES_LIBRARY_H
#define LIBRARIES_LIBRARY_H
#include <vector>
#include <iostream>
using namespace std;

struct tile {
    int row;
    int col;
    int tot;
    int dist;
    int heur;

    tile(int row, int col);

    bool operator<(const tile& other) const;
};

bool is_valid(int row, int col, int rows, int cols);

bool not_wall(const vector<vector<char>>& map, int row, int col);

int manhattan_dist(int row, int col, int destRow, int destCol);

extern "C"
char get_next(int x, int y, char* map, int startx, int starty, int endx, int endy);

#endif //LIBRARIES_LIBRARY_H
