#include<string>
#include<string.h>
#include<iostream>
#include"image.cpp"

img THRESHOLD_VALUE = 122;

void image(int argc, char* argv[]);

int main(int argc, char *argv[]) {

    if(argc < 3) {
        std::cerr << "[ERROR]: Not enough paramaters!\n Input example: .\\a.out grayscale.png 123"<< std::endl;
        return 0;
    }

    image(argc,argv);
    
    return 0;
}

void image(int argc, char* argv[]) {

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
                test->grayscale_lum();
                break;
            case 5: 
                test->grayscale_lum();
                break;
            case 6:
                test->erosion(1);
                break;
            case 7:
                test->dilation(1);
                break;
            case 8:
            {
                char buffer[4107] = {0};
                size_t len = 0;
                test->decodeMessage(buffer, &len);
                std::cout << "Message : " << buffer << std::endl;
            }
                break;
            default:  
                std::cerr << "[ERROR]: Not defined operation"<< std::endl;
                break;
        }
    }

    test->write("result.png");
}
