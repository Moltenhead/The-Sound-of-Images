# The Sound of Images
Trying to produce sounds, based on images

![alttext][blowingmind]

## How to use :
1. verify you posess a Python3 version active on your OS - if not [install one](https://www.python.org/downloads/release/python-372/)
2. download/clone this repository
3. execute `python setup.py install` from the application root to install dependencies
4. add images you want to test within `.\img` from application root
5. execute `python __main__.py`
6. select image to play and select size option
7. listen

### Don't over do it :
This is not yet optimized, depending on your processor 100 pixels are processed within approximately one second. So if you don't want to wait the following ice age answer `yes` at the shrinking question prompt.
Also each pixel is played as a more or less 0.2 seconds sound right now. So multiply by your image pixel number and you will know for how long you'll get beeped.

## Working On :
* User interface
   
## Features Needed:
* Pattern recognition
* Registering same-ish adjacent pixels as a longer note - instead of singular (will improve execution)
* More user options
* Pattern usage for better composition
* Displaying home key and chords progression
<br/>
<hr/>

### ressources and references:
* [sRGB to XYZ](http://www.ryanjuckett.com/programming/rgb-color-space-conversion/) HOWTO from Ryan Juckett + what the converter will get based on
* [XYZ to Wavelength in nm](https://www.waveformlighting.com/files/color_matching_functions.txt) values
* [Concept discovery](https://www.youtube.com/watch?v=JiNKlhspdKg&t=1799s) MASTERCLASS from Adam Neely
* [Color to pitch diagram](https://www.flutopedia.com/img/ColorOfSound_Nextdrum_lg.jpg)


[blowingmind]: https://github.com/Moltenhead/The-Sound-of-Images/blob/master/blowing_mind.gif "blowing mind gif"
