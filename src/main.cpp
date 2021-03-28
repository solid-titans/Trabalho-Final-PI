#include<string>
#include<iostream>
#include"graph/graph.cpp"
#include"image/image.cpp"
int main() {

    Image* test = new Image("thumb.png");

    double ker[] = { 1/16.0, 2/16.0, 1/16.0,
                     2/16.0, 4/16.0, 2/16.0,
                     1/16.0, 2/16.0, 1/16.0};

    test->std_convolve_cyclic(0,3,3,ker,1,1);
    test->std_convolve_cyclic(1,3,3,ker,1,1);
    test->std_convolve_cyclic(2,3,3,ker,1,1);

    test->write("blurred.jpg");
    
    return 0;
}