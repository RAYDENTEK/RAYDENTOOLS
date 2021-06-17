RAYDENTOOLS
by Rayden

A collection of tools that improve workflow between Blender and Unity & Unreal (primarily Unity)

Main aspect is working with hierarchies. For this, a custom parent / unparent routine is introduced, which allows keeping local transform values on parented objects (just like in unity)
This way, upon importing (with the help of https://github.com/EdyJ/blender-to-unity-fbx-exporter to fix the coordinate system) all the transform values are identical between both blender & unity (for entire fbx object tree). This is not standard behaviour, thus the custom parenting is key for this.
Unreal unfortunately currently does not import fbx hierarchies well from blender, so I am forced to merge the object (unreal import settings)

Other features are workflow improvement operators, put into pie menus. Blender is fast, but keymaps are all over the keyboard. Well mapped pie menus make it even faster and work less daunting, from having to move your hand a lot.
This personal toolkit will be updated once evolved as I'm working with it. Hopefully, if you are picking up blender scripting to customize it to your needs, this can be a helpful resource too.

Works with Blender 2.93.1+
Zip the Raydentools folder & install as any other blender addon
Auto Keymaps are not included yet. Manual keymaps are suggested.
Copy the startup file (scene) and userprefs files from "CONFIG" folder to:
C:\Users\ [YOUR USER NAME] \AppData\Roaming\Blender Foundation\Blender\2.93\config
Link some HDRI maps into World & World_Render environment shaders to have them light the scene

Version 1 - Essential Tools 
- 

Origin Actions
(keymap to Shift+A)
- Toggle Origin Editing
- Origin to Cursor (Location Only)
- Origin to Selection (Location Only)

Cursor Actions
(keymap to Shift+S)
- Set Cursor to Active
- Cursor Rotation from Parent
- Set Cursor Rotation to Active
- Reset Cursor Rotation
- Set Cursor Rotation from View

Manipulation Modes
(keymap to Shift+D)
- Active Element mode
- Cursor mode
- Local mode
- Global mode
- Normal mode
- Custom mode (auto-adapts to selected element)
(these adjust both rotation and position of "action centers")

Selections
(keymap to Shift+W)
- Join
- Separate
- Split
- Merge
- Select / Deselect All
- Inverse selection
- Select material
- Select linked

Utility Actions
(keymap to Shift+F)
- Parent (Custom parent routine to keep local transform values on object as in Unity)
- Unparent
- Merge hierarchy
- Set Normals ()

View Options
(keymap to Shift+V)
- Toggle All Overlays
- Toggle View Mode (switches between material preview & rendering modes and 'World' and 'World_Render' environments)
- Toggle Edge Lengths
- Toggle Face Orientation
- Toggle Bounding Box (show bounding box of active object)
- Toggle Forward Vector (black axis to indicate forward vector in Unity & Unreal)
- Toggle Center Axes (xyz axes to indicate orientation of active object without gizmos displayed)
- Hide hierarchy (hide object with all hierarchy)

