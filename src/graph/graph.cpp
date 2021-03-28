#include "graph.hpp"
#include<iostream>
#include <bits/stdc++.h>
/*
* Implementing the graph class
*  v0.1
*/

    // Start the graph with the 'min' size of Matrix
    Graph::Graph() {

        //Starting the matrix with EMPTY value
        weight default_value = EMPTY;
        this->graph          = new Matrix<weight>(default_value);

        this->vertices = 0;
        this->edges    = 0;
    }

    // Start the graph matrix with a set size
    Graph::Graph(counter v) {

        //Starting the matrix with EMPTY value
        weight default_value = EMPTY;
        this->graph          = new Matrix<weight>(default_value);
        
        this->vertices = 0;
        this->edges    = 0;
    } 

    Graph::~Graph() {
        free(this->graph);
    }

    //Return the number of vertices the graph has
    counter Graph::getVerticesNumber() {
        return this->vertices;
    }

    //Return the number of edges the graph has
    counter Graph::getEdgesNumber() {
        return this->edges;
    }

    // Add a new Vertex to the graph and return its id if it is successful
    counter Graph::add_vertex(weight value) {
        counter result = -1;
        counter pos    = this->vertices;

        has_space();

        this->graph->insert(value,pos,pos);
        result = this->vertices;
        this->vertices++;

        std::vector<counter> it;
        this->adj.push_back(it);
        
        return result;
    }

    // Checks if the graph matrix have space, if does not, expand the matrix
    bool Graph::has_space(){
        bool result = false;

        if(this->vertices == this->graph->get_number_of_columns()) {
            this->graph->expand_matrix(1,EMPTY);
            result = true;
        }

        return result;
    }

    // Add a new Edge to the graph and return if its successfully
    bool Graph::add_edge(counter first, counter last, weight value) {
        bool result = false;

        if(search_vertex(first) && search_vertex(last)) {
            this->graph->insert(value,first,last);
            this->graph->insert(value,last,first);
            result = true;
            this->edges++;

            add_adj(first, last);
            add_adj(last, first);
        }

        return result;
    }

    // Checks if the vertex exist
    bool Graph::search_vertex(counter id) {
        bool resp = false;

        if (this->graph->get(id,id) != EMPTY) 
            resp = true;
        
        return resp;
    }

    void Graph::add_adj(counter first, counter last) {
        auto it = this->adj.at(first);
        it.push_back(last);

        std::replace(this->adj.begin(), this->adj.end(), this->adj.at(first), it);
    }

    void Graph::print() {

        std::cout << "Number of vertices: " << this->vertices << std::endl;
        std::cout << "Number of edges   : " << this->edges << std::endl; 

        std::cout << "\nAdj:\n"; 

        for(int i = 0; i < adj.size(); i++) {
            std::vector<counter> it = this->adj.at(i);
            std::vector<counter> :: iterator v;
            std::cout << "v[" << i << "] :"; 
            for(v = it.begin(); v != it.end() ;++v) {
                std::cout << ' ' << *v; 
            }
            std::cout << '\n'; 
        }
        std::cout << '\n'; 

        this->graph->print(); 
    }