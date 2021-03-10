#ifndef image_h
#define image_h

#include<stdint.h>
#include<cstddef>
#include<string>
#include<cstdio>
#include<cstring>

#define STB_IMAGE_WRITE_IMPLEMENTATION
#define STB_IMAGE_IMPLEMENTATION
#include "stb_image_write.h"
#include "stb_image.h"

using img=uint8_t;

enum ImageType {
    PNG, 
    JPG,
    BMP,
    TGA,
    NOT_IDENTIFIED,
};

class Image {

    private:
        img* data = NULL;
        size_t size = 0;
        int width;
        int height;
        int channels; //how many colours values per pixel; 3 = RGB , 4 = RGBA

    public: 

        //Constructor 1: Reads a file from a path
        Image(std::string filename);
        //Constructor 2: Create an image based on the width, height, and number of channels
        Image(int width, int height, int channels);
        //Constructor 3: Create an image with another image
        Image(const Image& img);
        //Deconstructor: Release memory (free)
        ~Image();

        int get_width();
        int get_height();
        img* get_data();
        //Read a file an returns a bool, if it was a success
        bool read(std::string filename);
        //Writes a file with the name 'filename'
        bool write(std::string filename, int quality = 100);

        ImageType getFileType(std::string filename);
};

#endif