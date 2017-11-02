# Type App
A GUI automatically types. Use case, initial server setup with noVNC/QEMU terminal where copy paste is not available.
### Quick start
#### Install dependencies
pip3 install pyautogui wx
#### Run the GUI
```
python3 type_app.py
```

#### To deploy as executable
```
pyinstaller --windowed --clean --icon=icon.ico type_app.py
```
The executable will be generated to folder **TypeApp\dist\type_app\type_app.exe**