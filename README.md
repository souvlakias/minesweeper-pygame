# minesweeper-pygame
- A simple minesweeper game made with pygame, that I made for fun a while ago and decided to share it here.
- The game has 3 levels of difficulty: Beginner, Intermediate and Expert.
- Run with `python minesweeper.py`
- If you want to compile it to an executable, you can use `pyinstaller`:
  - `pip install pyinstaller`
  - `pyinstaller -F --noconsole --add-data="img:img" minesweeper.py`