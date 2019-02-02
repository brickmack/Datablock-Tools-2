# Datablock-Tools-2
Updated version of Datablock Tools for Blender https://blenderartists.org/forum/showthread.php?320593-Datablock-Tools Which is apparently no longer being maintained.

Datablock Tools provides an easy way to remove duplicated material or UV image datablocks ("image.png.001", etc), typically created when copy-pasting objects. This reduces memory footprint and also makes editing materials a lot easier.

## Usage
All datablock tools can be found under Object -> Datablock Tools.

* **Clean Images Datablocks:** Removes duplicated UV images from selected objects. If an original image is found ("image.png" instead of "image.png.001"), all duplicate instances will be replaced with the original. Otherwise, one instance is renamed to removed the .xxx suffix

* **Clean Materials Datablocks:** Removes duplicated materials from selected objects. If an original material is found ("material.png" instead of "material.png.001"), all duplicate instances will be replaced with the original. Otherwise, one instance is renamed to removed the .xxx suffix

* **Remove All Materials Datablocks:** Removes all materials from selected objects.

* **Set As Instance:** Converts all *selected* objects into instances of the *active* object. Any change to the geometry or materials of a single instance will affect all instances of the object.

## Changelog

### 2.1

* Fixed fatal bug with image datablock clean on objects with incomplete unwrapping

* If image datablock has no "original" version (without .xxx suffix), rename it to become that

* Image datablock cleaner now uses regex search, like the material cleaner

* Support image/material names with multiple periods, preserves image extensions

* Code styling and commenting improvements for future maintainability

* Text and layout tweaks

* Tool to remove all materials from an object

### 2.0

* First version by Mackenzie Crawford, taking over as de facto developer of apparently orphaned project

* Update for Blender 2.78 onwards

* Switch to regex-based datablock name comparisons

* In absence of a "virgin" material (not image yet) datablock, rename one of the existing duplicates instead of leaving all duplicates unchanged

* Restructure program and translate comments to English for better maintainability in the future

### 1.0, 1.1

* Original release by Vitor Balbio. See BlenderArtists thread [here](https://blenderartists.org/t/datablock-tool/595316) and deprecated Blender Wiki page [here](https://archive.blender.org/wiki/index.php/Extensions:2.6/Py/Scripts/3D_interaction/Datablock_Tools/)