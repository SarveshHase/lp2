#include <iostream>
#include <vector>
#include <string>
#include <queue>
#include <unordered_set>
using namespace std;

// Structure to represent the state of the board for BFS
struct BoardState
{
    int row;
    vector<string> board;
    unordered_set<int> cols;
    unordered_set<int> rightUpperDiag; // row + col diagonals
    unordered_set<int> leftUpperDiag;  // row - col diagonals

    BoardState(int r, vector<string> b,
               unordered_set<int> c,
               unordered_set<int> rd,
               unordered_set<int> ld)
        : row(r), board(b), cols(c), rightUpperDiag(rd), leftUpperDiag(ld) {}
};

class Solution
{
public:
    vector<vector<string>> solveNQueens(int n)
    {
        vector<vector<string>> solutions;
        queue<BoardState> q;

        // Initial state: row=0, empty board, no columns or diagonals used
        vector<string> initialBoard(n, string(n, '.'));
        q.push(BoardState(0, initialBoard,
                          unordered_set<int>(),
                          unordered_set<int>(),
                          unordered_set<int>()));

        while (!q.empty())
        {
            BoardState state = q.front();
            q.pop();

            // If we've placed queens in all rows, we have a solution
            if (state.row >= n)
            {
                solutions.push_back(state.board);
                continue;
            }

            // Try placing a queen in each column of the current row
            for (int col = 0; col < n; col++)
            {
                // Check if position is under attack
                if (state.cols.count(col) ||
                    state.rightUpperDiag.count(state.row + col) ||
                    state.leftUpperDiag.count(state.row - col))
                {
                    continue; // Position under attack
                }

                // Create new board state with this queen placement
                vector<string> newBoard = state.board;
                newBoard[state.row][col] = 'Q';

                // Create new sets with this queen's constraints
                unordered_set<int> newCols = state.cols;
                newCols.insert(col);

                unordered_set<int> newRightDiag = state.rightUpperDiag;
                newRightDiag.insert(state.row + col);

                unordered_set<int> newLeftDiag = state.leftUpperDiag;
                newLeftDiag.insert(state.row - col);

                // Add new state to queue
                q.push(BoardState(state.row + 1, newBoard, newCols, newRightDiag, newLeftDiag));
            }
        }

        return solutions;
    }
};

int main()
{
    int n;
    cout << "Enter the number of queens (N): ";
    cin >> n;

    Solution sol;
    vector<vector<string>> solutions = sol.solveNQueens(n);

    cout << "Number of solutions: " << solutions.size() << endl;

    for (int i = 0; i < solutions.size(); i++)
    {
        cout << "\nSolution " << i + 1 << ":\n";
        for (const string &row : solutions[i])
        {
            for (char c : row)
            {
                cout << c << " ";
            }
            cout << endl;
        }
    }

    return 0;
}