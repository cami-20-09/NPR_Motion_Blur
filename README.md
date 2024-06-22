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
* it is recommended to use the latest Maya version (2024)

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
    * The Nodes with yellow backdrops offer more insights into some self-created
    compounds
Or you can also simply search for the following Nodes in Bifrost:
    * deform
    * multiples
    * multiple_shape
    * shapetrails
    * motiontrail

## Author

Thi Cam Thanh Pham
[@tp054](tp054@hdm-stuttgart.de)


## Acknowledgments

This project was supervised by:
* PROF. JAN ADAMCZYK
* DIPL. ING. JOCHEN BOMM
