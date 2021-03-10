#include<string>
#include<iostream>
#include"image/image.cpp"

int main() {
    
    Image* test = new Image("r35.jpeg");
    auto tmp = test->get_data();

    for(int i =0; i < test->get_width(); i++) {
        tmp[i] = 0;
    }

    test->write("resultado.png");

    return 0;
}