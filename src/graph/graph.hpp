#ifndef graph_hpp
#define graph_hpp

#define EMPTY -1

#include <vector>
#include "vertex.hpp"
#include "matrix_cpp/matrix.cpp"

using weight = int8_t;
using counter= uint16_t;

class Graph {

    private: 
        counter vertices;
        counter edges;

        Matrix<weight>* all_vertices;

        bool has_space();

    public:
        
        //
        Graph();
        Graph(counter vertices);
        
        //
        bool add_edge(counter first, counter last, weight weight);
        counter add_vertex(weight value);
        bool search_vertex(counter id);
        
        //
        counter getVerticesNumber();  
        counter getEdgesNumber();
        
        virtual void print();  
};

#endif