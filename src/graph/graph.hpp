#ifndef graph_hpp
#define graph_hpp

#define EMPTY -1

#include <vector>
#include "matrix_cpp/matrix.cpp"

using weight  = int;
using counter = uint16_t;

class Graph {

    private: 
        counter vertices;
        counter edges;

        Matrix<weight>*       graph;
        std::vector<std::vector<counter>> adj;

        bool has_space();

    public:
        
        //
        Graph();
        Graph(counter vertices);
        ~Graph();
        
        //
        bool    add_edge(counter first, counter last, weight weight);
        counter add_vertex(weight value);
        bool    search_vertex(counter id);
        void    add_adj(counter first,counter last);
        
        //
        counter getVerticesNumber();  
        counter getEdgesNumber();
        
        virtual void print();  
};

#endif