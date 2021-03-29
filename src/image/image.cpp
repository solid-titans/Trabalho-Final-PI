#include"image.hpp"
#include <cstring>
#include<iostream>

#define BYTE_BOUND(value) value < 0 ? 0 : (value > 255 ? 255 : value)

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

    Image& Image::threshold(img threshold) {
        for (int32_t i = 0; i < size; i+=channels) {
            int32_t pixel = (data[i]+ data[i+1]+ data[i+2])/3;
            memset(data+i, pixel < threshold ? MIN : MAX, 3);
        }

        return  *this;
    }


    Image& Image::grayscale_avg(){

        // if the image is already in grayscale
            if(channels < 3 ){ 
                std::cerr << "Image is already in grayscale"<< std::endl;

            } else {
                for (int32_t i = 0; i < size; i+=channels) {
                // (r+g+b)/3
                int32_t gray = (data[i]+ data[i+1]+ data[i+2])/3;
                memset(data+i, gray, 3);

                }
            }
            
      return *this;
    }
        
       
    Image& Image::grayscale_lum(){
        // if the image is already in grayscale
            if(channels < 3 ){ 
                std::cerr << "Image is already in grayscale"<< std::endl;;

            } else {
                for (int32_t i = 0; i < size; i+=channels) {
               
                int32_t gray = (0.2126*data[i]+ 0.7152*data[i+1]+ 0.0722*data[i+2]);
                memset(data+i, gray, 3);
                
                }
            }
               
      return *this;
    }

    Image& Image::diffmap(Image& img) {
        int32_t compare_width    = fmin(this->width,img.width);
        int32_t compare_height   = fmin(this->height,img.height);
        int32_t compare_channels = fmin(this->channels,img.channels);

        for(uint32_t i=0; i<compare_height; i++) {
            for(uint32_t j=0; j<compare_width;j++) {
                for(uint8_t k=0; k<compare_channels;k++) {
                    data[(i*width+j)*channels+k] = BYTE_BOUND(abs(data[(i*width+j)*channels+k] - img.data[(i*img.width+j)*img.channels+k]));
                }
            }
        }

        return *this;
    }

    Image& Image::colorMask(float r, float g, float b) {
        if(channels <3) {
            std::cerr << "\e[31[ERROR] Color mask requires at least 3 channels,\n but this image has "<< channels << " channels\e[0m\n"<< std::endl;

        }
        else {
            for(int32_t i =0; i < size; i+=channels) {
                data[i]   *= r;
                data[i+1] *= g;
                data[i+2] *= b;
            }
        }

        return *this;
    }

    Image& Image::std_convolve_clamp_to_0(img channel, uint32_t ker_w, uint32_t ker_h, double ker[], uint32_t cr, uint32_t cc) {
        img new_data[width*height];
        uint64_t center = cr*ker_w + cc;

        for(uint64_t k =channel; k<size; k+=this->channels) {
            double c = 0;
            for(long i = -((long)cr); i <(long)ker_h -cr; i++) {
                long row = ((long)k/this->channels)/width-i;
                if(row < 0 || row > height-1) 
                    continue;
                
                for(long j = -((long)cc);j <(long)ker_w -cc; j++) {
                    long column = ((long)k/this->channels)%width-j;
                    if(column < 0 || column > width-1) 
                        continue;
                    
                    c+= ker[center+i*(long)ker_w+j]*data[(row*width+column)*this->channels+this->channels];
                }
            }
            new_data[k/this->channels] = (img)BYTE_BOUND(round(c));
        }
        for(uint64_t k = channel; k < size; k+=this->channels) {
            data[k] = new_data[k/this->channels];
        }
        return *this;
    }

    Image& Image::std_convolve_clamp_to_border(img channel, uint32_t ker_w, uint32_t ker_h, double ker[], uint32_t cr, uint32_t cc) {
        img new_data[width*height];
        uint64_t center = cr*ker_w + cc;

        for(uint64_t k =channel; k<size; k+=this->channels) {
            double c = 0;
            for(long i = -((long)cr); i <(long)ker_h -cr; i++) {
                long row = ((long)k/this->channels)/width-i;

                if(row < 0 ) 
                    row = 0;
                else if (row > height-1) 
                    row = height-1;

                for(long j = -((long)cc);j <(long)ker_w -cc; j++) {
                    long column = ((long)k/this->channels)%width-j;

                    if(column < 0)
                        column = 0;
                    else if(column > width-1)
                        column = width-1;
                    
                    c+= ker[center+i*(long)ker_w+j]*data[(row*width+column)*this->channels+this->channels];
                }
            }
            new_data[k/this->channels] = (img)BYTE_BOUND(round(c));
        }
        for(uint64_t k = channel; k < size; k+=this->channels) {
            data[k] = new_data[k/this->channels];
        }
        return *this;
    }

    Image& Image::std_convolve_cyclic(img channel, uint32_t ker_w, uint32_t ker_h, double ker[], uint32_t cr, uint32_t cc) {
        img new_data[width*height];
        uint64_t center = cr*ker_w + cc;

        for(uint64_t k =channel; k<size; k+=this->channels) {
            double c = 0;
            for(long i = -((long)cr); i <(long)ker_h -cr; i++) {
                long row = ((long)k/this->channels)/width-i;

                if(row < 0 ) 
                    row = row%height + height;
                else if (row > height-1) 
                    row %= height;

                for(long j = -((long)cc);j <(long)ker_w -cc; j++) {
                    long column = ((long)k/this->channels)%width-j;

                    if(column < 0)
                        column = column%width + width;
                    else if(column > width-1)
                        column %= width;
                    
                    c+= ker[center+i*(long)ker_w+j]*data[(row*width+column)*this->channels+this->channels];
                }
            }
            new_data[k/this->channels] = (img)BYTE_BOUND(round(c));
        }
        for(uint64_t k = channel; k < size; k+=this->channels) {
            data[k] = new_data[k/this->channels];
        }
        return *this;
    }

    