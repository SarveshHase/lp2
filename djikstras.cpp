#include <iostream>
#include <vector>
#include <queue>
#include <climits>
#include <algorithm>
#include <utility>

using namespace std;

void dijkstra(vector<vector<pair<int, int>>>& adj, int V, int src, vector<int>& dist, vector<int>& parent) {
    dist.assign(V, INT_MAX);
    parent.assign(V, -1);
    
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> pq;

    dist[src] = 0;
    pq.push({0, src});

    while (!pq.empty()) {
        int u = pq.top().second;
        pq.pop();

        for (auto& edge : adj[u]) {
            int v = edge.first;
            int weight = edge.second;

            if (dist[v] > dist[u] + weight) {
                dist[v] = dist[u] + weight;
                parent[v] = u;
                pq.push({dist[v], v});
            }
        }
    }
}

void printPath(int j, const vector<int>& parent, int src) {
    if (j < 0 || j >= parent.size()) {
        cout << "Invalid node for path printing." << endl;
        return;
    }

    vector<int> path;
    int currentNode = j;

    while (currentNode != -1) {
        path.push_back(currentNode);
        if (currentNode == src) break;
        currentNode = parent[currentNode];
    }
    
    reverse(path.begin(), path.end());

    for (size_t i = 0; i < path.size(); ++i) {
        cout << path[i] << (i == path.size() - 1 ? "" : " -> ");
    }
}

int main() {
    int V, E, src;
    cout << "Enter number of vertices and edges: ";
    cin >> V >> E;
    vector<vector<pair<int, int>>> adj(V);

    cout << "Enter edges (u v weight) --- (vertices are 0-indexed):\n";
    for (int i = 0; i < E; ++i) {
        int u, v, w;
        cin >> u >> v >> w;
        adj[u].push_back({v, w});
        // adj[v].push_back({u, w});
    }

    cout << "Enter source vertex (0-indexed): ";
    cin >> src;

    vector<int> dist(V);
    vector<int> parent(V);

    dijkstra(adj, V, src, dist, parent);

    cout << "\nShortest distances and paths from source node " << src << ":\n";
    for (int i = 0; i < V; ++i) {
        cout << "To Node " << i << ": ";
        if (dist[i] == INT_MAX) {
            cout << "Distance = INF, Path: No path" << endl;
        } else {
            cout << "Distance = " << dist[i] << ", Path: ";
            printPath(i, parent, src);
            cout << endl;
        }
    }
    return 0;
}