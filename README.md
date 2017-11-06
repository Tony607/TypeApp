# Type App
A GUI automatically types. Use case, initial server setup with noVNC/QEMU terminal where copy paste is not available. Check out the YouTube demo [here](https://www.youtube.com/watch?v=y0-UUlOJvmU).
If you want to dive into the code to learn how it works, I also have a [write up](https://www.dlology.com/blog/how-to-paste-content-to-a-vnc-console-which-does-not-support-copy-and-paste/)

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
Capture and save a screenshot of a distinguishable feature **inside** the VNC window, an example is provided in the res/kiwi_vnc.png

![window feature](https://raw.githubusercontent.com/Tony607/TypeApp/master/res/kiwi_vnc.png)

Captured from this window

![VNC_Browser](https://raw.githubusercontent.com/Tony607/TypeApp/master/res/VNC_Window_demo.png)

I use [PicPick](http://ngwin.com/picpick) on Windows to capture the image.

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