#include<string>
#include<iostream>
#include"graph/graph.cpp"
#include"image/image.cpp"
int main() {

    Image* test = new Image("thumb.png");

    test->threshold(70);

    test->write("blurred.jpg");
    
    return 0;
}