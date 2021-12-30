# Fruit Ninja VR (using webcam) 🍉

Fruit Ninja in **pygame** using pose motion tracking in **MediaPipe**.

### How to Play:

Copy this GitHub repository, and run [fruit_ninja.py](scripts/fruit_ninja.py) with Python 3.

Press the `Esc` key to exit.

### Gameplay:
![fruit ninja](https://user-images.githubusercontent.com/76597978/146680831-99c0f914-2de2-42e8-bf02-091144159612.gif)

### Features:
- **Fruits**:
  -   Pineapple 🍍
  -   Watermelon 🍉
  -   Kiwi 🥝
  -   Orange 🍊
  -   Bomb 💣
-   Black knife trail cuts anything it touches (cut several fruits at the same time)
-   Start menu (hands up before playing to avoid accidentally starting)
-   Preview webcam video while playing by changing the `SHOW_WEBCAM` setting in [fruit_ninja.py](https://github.com/mmbaguette/Fruit-Ninja-VR/blob/main/scripts/fruit_ninja.py)

### Dependences:
```
pip install pygame
pip install opencv-python
pip install mediapipe
```

![alt text](https://github.com/mmbaguette/Fruit-Ninja-VR/blob/main/preview/fruit%20ninja.jpg?raw=true)

### Pyinstaller (package game into executable)

Package your *own* file with your *own* game settings like higher resolution (sacrifice performance). I used this command to package the app into a pyinstaller executable. Place the app inside the working directory with the over dependencies like `images`.
`
pyinstaller -w --onefile --paths="PYTHON_PATH\Python39\Lib\site-packages\cv2" --collect-data mediapipe --add-data "PYTHON_PATH\Python39\Lib\site-packages\mediapipe;mediapipe" -i "images/icon.ico" scripts/fruit_ninja.py
`
Install pyinstaller if you haven't already:
```
pip install pyinstaller
```