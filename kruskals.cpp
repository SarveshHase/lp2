#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

class Solution
{
public:
    // DSU Code
    vector<int> parent;
    vector<int> rank;

    int find(int x)
    {
        if (x == parent[x])
            return x;
        return parent[x] = find(parent[x]);
    }

    void Union(int x, int y)
    {
        int x_parent = find(x);
        int y_parent = find(y);

        if (x_parent == y_parent)
            return;

        if (rank[x_parent] > rank[y_parent])
        {
            parent[y_parent] = x_parent;
        }
        else if (rank[x_parent] < rank[y_parent])
        {
            parent[x_parent] = y_parent;
        }
        else
        {
            parent[x_parent] = y_parent;
            rank[y_parent]++;
        }
    }

    int Kruskal(vector<vector<int>> &vec, vector<pair<int, int>> &mstEdges)
    {
        int sum = 0;
        for (auto &temp : vec)
        {
            int u = temp[0];
            int v = temp[1];
            int wt = temp[2];

            int parent_u = find(u);
            int parent_v = find(v);

            if (parent_u != parent_v)
            {
                Union(u, v);
                sum += wt;
                mstEdges.push_back({u, v}); // Store the edge in MST
            }
        }
        return sum;
    }

    int spanningTree(int V, vector<vector<int>> adj[], vector<pair<int, int>> &mstEdges)
    {
        parent.resize(V);
        rank.resize(V, 0);

        for (int i = 0; i < V; i++)
            parent[i] = i;

        vector<vector<int>> vec;

        for (int i = 0; i < V; i++)
        {
            for (auto &temp : adj[i])
            {
                int u = i;
                int v = temp[0];
                int d = temp[1];
                vec.push_back({u, v, d});
            }
        }

        auto lambda = [&](auto &v1, auto &v2)
        {
            return v1[2] < v2[2];
        };

        sort(begin(vec), end(vec), lambda);

        return Kruskal(vec, mstEdges);
    }
};

int main()
{
    int V = 5; // Number of vertices
    vector<vector<int>> adj[V];

    // Adding edges to the graph (undirected)
    adj[0].push_back({1, 2});
    adj[1].push_back({0, 2});

    adj[0].push_back({3, 6});
    adj[3].push_back({0, 6});

    adj[1].push_back({2, 3});
    adj[2].push_back({1, 3});

    adj[1].push_back({3, 8});
    adj[3].push_back({1, 8});

    adj[1].push_back({4, 5});
    adj[4].push_back({1, 5});

    adj[2].push_back({4, 7});
    adj[4].push_back({2, 7});

    Solution sol;
    vector<pair<int, int>> mstEdges;
    int totalWeight = sol.spanningTree(V, adj, mstEdges);

    cout << "Edges in MST:" << endl;
    for (auto edge : mstEdges)
    {
        cout << edge.first << " - " << edge.second << endl;
    }

    cout << "Total weight of MST: " << totalWeight << endl;

    return 0;
}