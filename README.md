# Type App
A GUI automatically types. Use case, initial server setup with noVNC/QEMU terminal where copy paste is not available.

### How it works
With the  **Auto Switch** function on
You type something into the bottom text box and click the send button.
-  It visually locates the VNC windows coordinate by the image feature provided
-  It clicks left mouse button in the middle of image feature, this switches to the VNC window 
-  It types in the VNC window.
- It changes the mouse cursor back to where it used to be
### Quick start
#### Install dependencies
pip3 install pyautogui wx
#### Run the GUI
Capture a screenshot of a distinguishable feature **inside** the VNC window, an example is provided in the res/kiwi_vnc.png

![window feature](https://raw.githubusercontent.com/Tony607/TypeApp/master/res/kiwi_vnc.png)

Run the App by

```
python3 type_app.py
```
In the App you can choose your image by clicking the **Browse** button, also be sure to check the **Auto Switch** checkbox.

#### To deploy as executable
```
pyinstaller --windowed --clean --icon=icon.ico type_app.py
```
The executable will be generated to folder **TypeApp\dist\type_app\type_app.exe**