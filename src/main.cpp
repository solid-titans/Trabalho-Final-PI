#include<string>
#include<iostream>
#include"graph/graph.cpp"
int main() {
    
    Graph* g = new Graph();
    g->add_vertex(5);
    g->add_vertex(2);
    g->add_vertex(15);
    g->add_edge(0,1,7);
    g->add_edge(0,2,8);
    g->print();

    return 0;
}