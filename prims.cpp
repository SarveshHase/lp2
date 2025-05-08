#include <iostream>
#include <vector>
#include <queue>
using namespace std;

class Solution
{
    struct T
    {
        int wt;
        int node;
        int parent;
    };

    struct cmp
    {
        bool operator()(const T &a, const T &b)
        {
            return a.wt > b.wt;
        }
    };

public:
    // Function to find sum of weights of edges of the Minimum Spanning Tree.
    int spanningTree(int V, vector<vector<int>> adj[])
    {
        int sum = 0;
        priority_queue<T, vector<T>, cmp> pq;

        vector<bool> inMST(V, false);
        vector<int> parentStore(V, -1);

        pq.push({0, 0, -1});

        while (!pq.empty())
        {
            T t = pq.top();
            pq.pop();

            int wt = t.wt;
            int node = t.node;
            int parent = t.parent;

            if (inMST[node])
                continue;

            inMST[node] = true;
            parentStore[node] = parent;
            sum += wt;

            for (auto &v : adj[node])
            {
                int nbr = v[0];
                int w = v[1];

                if (!inMST[nbr])
                {
                    pq.push({w, nbr, node});
                }
            }
        }

        // Print the MST edges
        cout << "Edges in MST:" << endl;
        for (int i = 1; i < V; i++)
        {
            cout << parentStore[i] << " - " << i << endl;
        }

        return sum;
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
    int totalWeight = sol.spanningTree(V, adj);

    cout << "Total weight of MST: " << totalWeight << endl;

    return 0;
}