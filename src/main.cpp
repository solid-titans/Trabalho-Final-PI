#include<string>
#include<iostream>
#include"graph/graph.cpp"
#include"image/image.cpp"
int main() {

    Image* test = new Image("teste.png");

    test->threshold(122);

    test->write("blurred.jpg");
    
    return 0;
}