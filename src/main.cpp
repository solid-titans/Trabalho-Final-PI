#include<string>
#include<string.h>
#include<iostream>
#include"graph/graph.cpp"
#include"image/image.cpp"

img THRESHOLD_VALUE = 122;

void graph(int argc, char* argv[]);
void image(int argc, char* argv[]);

int main(int argc, char *argv[]) {

    if(argc < 3) {
        std::cerr << "[ERROR]: Not enough paramaters!\n Input example: .\\a.out grayscale.png 123"<< std::endl;
        return 0;
    }

    if(strcmp(argv[1],"graph") == 0) 
        graph(argc,argv);
    else if(strcmp(argv[1],"image") == 0) 
        image(argc,argv);
    else 
        std::cerr << "[ERROR]: First command not defined"<< std::endl;
    
    return 0;
}

void graph(int argc, char* argv[]) {

}

void image(int argc, char* argv[]) {

    Image* test = new Image(argv[2]);

    for (int i = 0 ; i < strlen(argv[3]); i++) {
        int operation = argv[3][i] - 48;
        
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
                test->grayscale_lum();
                break;
            case 5: 
                test->grayscale_lum();
                break;
            default:  
                std::cerr << "[ERROR]: Not defined operation"<< std::endl;
                break;
        }
    }

    test->write("result.png");
}