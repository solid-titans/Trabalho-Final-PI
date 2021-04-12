#include<string>
#include<string.h>
#include<iostream>
#include"graph/graph.cpp"
#include"image/image.cpp"

img THRESHOLD_VALUE = 122;

int main(int argc, char *argv[]) {

    if(argc < 3) {
        std::cerr << "[ERROR]: Not enough paramaters!\n Input example: .\\a.out grayscale.png 123"<< std::endl;
        return 0;
    }

    Image* test = new Image(argv[1]);

    for (int i = 0 ; i < strlen(argv[2]); i++) {
        int operation = argv[2][i] - 48;
        
        switch(operation) {
            case 0:
                test->threshold_grayscale(THRESHOLD_VALUE);
                break;
            case 1:
                test->invert();
                break;
            case 2:
                test->grayscale_avg();
                break;
            case 3:
                test->grayscale_lum();
                break;
            case 4:
                
                break;
            case 5: 

                break;
            default:  
                std::cerr << "[ERROR]: Not defined operation"<< std::endl;
                break;
        }
    }
    
    test->threshold_grayscale(122);

    test->write("threshold.jpg");

    test->invert();

    test->write("threshold_inverted.jpg");
    
    return 0;
}