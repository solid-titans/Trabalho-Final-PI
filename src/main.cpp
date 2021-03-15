#include<string>
#include<iostream>
#include"image/image.cpp"

int main() {
    
    Image* test = new Image("tabela.png");
    auto tmp = test->get_data();

    for(int i =test->get_width(); i < test->get_width()*2; i++) {
        tmp[i] = 0;
    }

    test->write("resultado.png");

    return 0;
}