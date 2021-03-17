#include "graph.hpp"
#include<string>
#include<iostream>
/*
* Implementing the graph class
*  v0.1
*/

    // Start the graph with the 'min' size of Matrix
    Graph::Graph() {
        this->all_vertices = new Matrix<weight>();
        this->all_vertices->fill(EMPTY);

        this->vertices = 0;
        this->edges    = 0;
    }

    // Start the graph with a set size
    Graph::Graph(counter v) {
        this->all_vertices = new Matrix<weight>(v);
        this->all_vertices->fill(EMPTY);

        this->vertices = 0;
        this->edges    = 0;
    } 

    Graph::~Graph() {
        free(this->all_vertices);
        free(this->adj);
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

        this->all_vertices->insert(value,pos,pos);
        result = this->vertices;
        this->vertices++;
        
        return result;
    }

    // Checks if the matrix have space, if does not, expand the matrix
    bool Graph::has_space(){
        bool result = false;

        if(this->vertices == this->all_vertices->get_number_of_columns()) {
            this->all_vertices->expand_matrix(1);
            result = true;
        }

        return result;
    }

    // Add a new Edge to the graph and return if its successfully
    bool Graph::add_edge(counter first, counter last, weight value) {
        bool result = false;

        if(search_vertex(first) && search_vertex(last)) {
            this->all_vertices->insert(value,first,last);
            this->all_vertices->insert(value,last,first);
            result = true;
            this->edges++;
        }

        return result;
    }

    // Checks if the vertex exist
    bool Graph::search_vertex(counter id) {
        bool resp = false;

        if (id < this->all_vertices->get_number_of_columns() && id >= 0) 
            resp = true;
        
        return resp;
    }

    void Graph::print() {

        std::cout << "Number of vertices: " << this->vertices;
        std::cout << "Number of edges   : " << this->edges; 

        this->all_vertices->print(); 
    }