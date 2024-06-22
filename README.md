# Stylized Motion Blur Tool

This animation tool allows you to generate different types of stylized motion blur 

## Description

The current prototype can generate five diffrent motion blur types using Bifrost:
* Smearframes
* Multiples
* Multiple Shapes
* Shape Trails
* Motion Trails

## Getting Started

### Dependencies

* the Bifrost Plug-In needs to be loaded
* you need to use the latest Maya version (2024)

### Installing

* Put the json files in the giving compounds folder in the compounds directory of your Maya Application.

1. You can find the folder here:

    C:\Users\*username*\Autodesk\Bifrost\Compounds (Windows) 
    $HOME/Autodesk/Bifrost/Compounds (MacOS) 
    $HOME/Autodesk/Bifrost/Compounds (Linux)

2. Put the "motiontrails" folder in your sourceimages directory of your current Maya project

3. Put the “Stylized_MotionBlur” folder into your Maya’s user scripts directory. 

    You can either put it in your general Maya scripts directory:
    * C:\*username*\Documents\maya\scripts (windows) 
    * $HOME/Library/Preferences/Autodesk/maya/scripts (MacOS) 
    * $HOME/maya/scripts (Linux)

    Or in your specific Maya version scripts directory: 
    * C:\*username*\documents\maya\*version*\scripts (Windows) 
    * $HOME/Library/Preferences/Autodesk/maya/*version*/scripts (MacOS) 
    * $HOME/maya/scripts/*version*/scripts (Linux)

### Executing program

restart Maya and write the following command into your script editor and hit run:

    from Stylized_MotionBlur import Main_UI
    Main_UI.apply()

### Notes

If you want to take a look into the generated Bifrost Graphs you can find them in the DNT
groups in Maya’s Outliner after generating your desired Motion Blur. 

* Right-Click the Bifrost Object and select Open in Bifrost
* Inside the Bifrost Graph double-click the Motion Blur Node to look inside
* The Nodes with yellow backdrops offer more insights into some self-created compounds
    
Or you can also simply search for the following Nodes in Bifrost:

* deform
* multiples
* multiple_shape
* shapetrails
* motiontrail

## Example Results
![2](https://github.com/cami-20-09/NPR_Motion_Blur/assets/83505396/0b6935b6-e90b-403f-b9ef-fde7dd57dfd2)
![4](https://github.com/cami-20-09/NPR_Motion_Blur/assets/83505396/182c7326-b481-4b25-8aeb-8c9199629f27)
![6](https://github.com/cami-20-09/NPR_Motion_Blur/assets/83505396/2443d119-c01e-4d4a-b428-031ea222b2e5)



## Image Sources
Motiontrails Img.3:https://pngtree.com/element/down?id=OTE3NDk2NA==&type=1&time=1718123702&token=ZDFmYzhhM2VjNDQyMjc4NGM2MzhlZjkyZDI5ZjRiNTE=&t=0

Motiontrails Img.4:https://www.vecteezy.com/png/10313281-ink-brush-stroke?autodl_token=a0ad24ad48eac48da2ee168ac43c7346ba59eac152a6a1fb9dc7293b8f180e3cdf0d175e4279854035b9534a0caa4e5354aee3dbdcd519626978a145d90e3c52

## Author

Thi Cam Thanh Pham
[@tp054](tp054@hdm-stuttgart.de)


## Acknowledgments

This project was supervised by:
* PROF. JAN ADAMCZYK
* DIPL. ING. JOCHEN BOMM
