#include <iostream>
#include <vector>
#include <string>
#include <unordered_set>
using namespace std;

class Solution {
    vector<vector<string>> ans;
    unordered_set<int> cols, rightUpperDiag, leftUpperDiag;
    
    void solve(vector<string> &board, int row, int n) {
        if(row >= n) {
            ans.push_back(board);
            return;
        }

        for(int col=0; col<n; col++) {
            if(cols.count(col) || rightUpperDiag.count(row+col) || leftUpperDiag.count(row-col)) {
                continue;
            }

            cols.insert(col);
            rightUpperDiag.insert(row+col);
            leftUpperDiag.insert(row-col);
            board[row][col] = 'Q';

            solve(board, row+1, n);

            cols.erase(col);
            rightUpperDiag.erase(row+col);
            leftUpperDiag.erase(row-col);
            board[row][col] = '.';
        }
    }
public:
    vector<vector<string>> solveNQueens(int n) {
        vector<string> board(n, string(n, '.'));
        solve(board, 0, n);
        return ans;
    }
};

int main() {
    int n;
    cout << "Enter the number of queens (N): ";
    cin >> n;

    Solution sol;
    vector<vector<string>> solutions = sol.solveNQueens(n);

    cout << "Number of solutions: " << solutions.size() << endl;
    for(int i=0; i<solutions.size(); i++) {
        cout << "\nSolution " << i+1 << ":\n";
        for(const string &row : solutions[i]) {
            for(char c : row) {
                cout << c << " ";
            }
            cout << endl;
        }
    }

    return 0;
}