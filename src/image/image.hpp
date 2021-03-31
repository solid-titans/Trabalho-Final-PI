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

#define MIN 0
#define MAX 255

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
        //OBS: the 'quality' variable is only used in writing .jpg images
        //for specifing the compression ( 0 - 100 ) 
        bool write(std::string filename, int quality = 100);

        ImageType getFileType(std::string filename);
        
        //  Filters

        /** Turn a image into a binary format
         *  
         */
        Image& threshold(img threshold);

        /** Turn a image into a binary format
         *  
         */
        Image& invert();
        
        /** grayscale Averaging
         * The values of r + g + b will be changed after that divided by 3
         */
        Image& grayscale_avg();
        

        /** Grayscale Luminance
         * Can best maintain the illumination of an image
         */
        Image& grayscale_lum();

        /** Color mask
         * Activate/deactive certain color channels of an image
         */
        Image& colorMask(float r, float g, float b);

        Image& diffmap(Image& img);

        //Basic convulution effects

        //Apply a convulution to the center
        Image& std_convolve_clamp_to_0(img channel, uint32_t ker_w, uint32_t ker_h, double* ker, uint32_t cr, uint32_t cc);
        //Apply a convulution to the border
        Image& std_convolve_clamp_to_border(img channel, uint32_t ker_w, uint32_t ker_h, double* ker, uint32_t cr, uint32_t cc);
        //Apply convulution in a cyclic manner
        Image& std_convolve_cyclic(img channel, uint32_t ker_w, uint32_t ker_h, double* ker, uint32_t cr, uint32_t cc);
};

#endif
