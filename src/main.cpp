#include<string>
#include<iostream>
#include"graph/graph.cpp"
#include"image/image.cpp"
int main() {

    Image* test = new Image("guara.jpg");

    test->threshold(122);

    test->write("threshold.jpg");

    test->invert();

    test->write("threshold_inverted.jpg");
    
    return 0;
}