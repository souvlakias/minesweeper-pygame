# minesweeper-pygame
- A simple minesweeper game made with pygame, that I made for fun some a while ago and decided to share it here.
- The game has 3 levels of difficulty: easy, medium and hard.
- Run with `python3 minesweeper.py`
- If you want to compile it to an executable, you can use `pyinstaller`:
  - `pip install pyinstaller`
  - `pyinstaller -F --noconsole --add-data="img:img" minesweeper.py`
  - Also make sure to uncomment the 2 lines that are commented in the code: 
  ```python 
    import sys,os
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        os.chdir(sys._MEIPASS)
    ```