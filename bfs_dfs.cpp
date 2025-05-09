#include <iostream>
#include <vector>
#include <queue>
#include <stack>
using namespace std;

class Graph {
private:
    int V;
    vector<vector<int>> adj;

public:
    Graph(int V) {
      this->V = V;
      adj.resize(V);
    }

    void addEdge(int v, int w) {
        adj[v].push_back(w);
        adj[w].push_back(v);
    }

    void DFS(int v, vector<bool>& visited) {
        visited[v] = true;
        cout << v << " ";

        for(int neighbor : adj[v]) {
            if(!visited[neighbor]) {
                DFS(neighbor, visited);
            }
        }
        return;
    } 

    void BFSRecursiveUtil(queue<int>& q, vector<bool>& visited) {
        if(q.empty()) return; // base condition

        int curr = q.front();
        q.pop();
        cout << curr << " ";

        for(int neighbor : adj[curr]) {
            if (!visited[neighbor]) {
                visited[neighbor] = true;
                q.push(neighbor);
            }
        }

        BFSRecursiveUtil(q, visited);
    }

    void BFS(int start, vector<bool>& visited) {
        queue<int> q;
        visited[start] = true;
        q.push(start);
        BFSRecursiveUtil(q, visited);
    }

    void DFSIterative(int start) {
        vector<bool> visited(V, false);
        stack<int> s;
        s.push(start);
    
        while(!s.empty()) {
            int vertex = s.top();
            s.pop();
    
            if(!visited[vertex]) {
                cout << vertex << " ";
                visited[vertex] = true;
            }
    
            for(int neighbor : adj[vertex]) {
                if(!visited[neighbor]) {
                    s.push(neighbor);
                }
            }
        }
    }
    
    void BFSIterative(int start) {
        vector<bool> visited(V, false);
        queue<int> q;
        q.push(start);
        visited[start] = true;
    
        while(!q.empty()) {
            int vertex = q.front();
            q.pop();
            cout << vertex << " ";
            for(auto neighbor : adj[vertex]) {
                if(!visited[neighbor]) {
                    visited[neighbor] = true;
                    q.push(neighbor);
                }
            }
        }
    }
};

int main() {
    int V, E;
    cout << "Enter number of vertices: ";
    cin >> V;
    cout << "Enter number of edges: ";
    cin >> E;

    Graph g(V);
    cout << "Enter edges (u v):\n";
    for (int i = 0; i < E; i++) {
        int u, v;
        cin >> u >> v;
        g.addEdge(u, v);
    }

    int start;
    cout << "Enter starting vertex: ";
    cin >> start;

    cout << "\nDFS starting from vertex " << start << ":\n";
    vector<bool> visitedDFS(V, false);
    g.DFS(start, visitedDFS);

    cout << "\n\nBFS starting from vertex " << start << ":\n";
    vector<bool> visitedBFS(V, false);
    g.BFS(start, visitedBFS);

    cout << "\n\nBFS Iterative starting from vertex " << start << ":\n";
    g.BFSIterative(start);

    cout << "\n\nDFS Iterative starting from vertex " << start << ":\n";
    g.DFSIterative(start);

    cout << endl;
    return 0;
}