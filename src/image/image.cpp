#include"image.hpp"
#include <cstring>
#include<iostream>

    Image::Image(std::string filename) {
        if(read(filename)) {
            std::cout << "Read " << filename << std::endl;
            size = this->width*this->height*this->channels;
        } else { 
            std::cout << "Failed to read " << filename << std::endl;
        }
    }

    Image::Image(int w, int h, int c) : width(w), height(h), channels(c) {
        size = width*height*channels;
        data = new img[size];
    }

    Image::Image(const Image& img) : width(img.width), height(img.height), channels(img.channels) {
        memcpy(data, img.data, img.size); //memcpy = memory copy(copy the contents of an array to another)
    }

    Image::~Image() {
        stbi_image_free(data);
    }

    int Image::get_height() {
        return this->height * this->channels;
    }

    int Image::get_width() {
        return this->width * this->channels;
    }

    img* Image::get_data() {
        return this->data;
    }

    bool Image::read(std::string filename) {

        auto cstr = filename.c_str(); // convert std::string into a const char*

        data = stbi_load(cstr, &width, &height, &channels, 0);

        return data != NULL;
    }

    bool Image::write(std::string filename, int quality) {
        ImageType type = getFileType(filename);
        int success;
        switch(type) {
            case PNG:
                success = stbi_write_png(filename.c_str(), this->width, this->height, this->channels, data, this->width*this->channels);
                break;
            case JPG:
                success = stbi_write_jpg(filename.c_str(), this->width, this->height, this->channels, data,quality);
                break;
            case TGA:  
                success = stbi_write_tga(filename.c_str(), this->width, this->height, this->channels, data);
                break; 
            case BMP:  
                success = stbi_write_bmp(filename.c_str(), this->width, this->height, this->channels, data);
                break;  
            default:
                std::cout << "Error! Something went wrong!" << std::endl;
                break;
        }
        return success != 0;
    }

    ImageType Image::getFileType(std::string filename) {
        
        if(filename.find(".") > filename.size()) {
            std::cout << "Erro!" <<std::endl;
            return NOT_IDENTIFIED;
        }

        auto extension = filename.substr(filename.find("."), filename.size() -1);

        if(extension.compare(".png") == 0) {
            return PNG;
        }
        else if(extension.compare(".jpg") == 0) {
            return JPG;
        }
        else if(extension.compare(".bmp") == 0) {
            return BMP;
        }
        else if(extension.compare(".tga") == 0) {
            return TGA;
        }

        return NOT_IDENTIFIED;
    }


    Image& Image::grayscale_avg(){

        // if the image is already in grayscale
            if(channels < 3 ){ 
                std::cerr << "Image is already in grayscale"<< std::endl;;

            } else {
                for (int i = 0; i < size; i+=channels) {
                // (r+g+b)/3
                int gray = (data[i]+ data[i+1]+ data[i+2])/3;
                memset(data+i, gray, 3);
                
                }
            }

    }
        
       
    Image& Image::grayscale_lum(){

            
    }

    