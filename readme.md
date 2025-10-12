##  🌀 swwwcycle 
### custom wallpaper cycler with tray icon for [swww](https://github.com/LGFae/swww)

![demo](./swwwcycle.gif)


### Features

- control wallpaper rotation from tray icon
- set wallpaper directory
- set time for changing wallpaper

### Dependencies

- swww

### Building

- On NixOS
  - `nix build`
  - `nix profile install .`

- with docker (a Dockerfile is provided in this repo), run these commands from the root dir of this repo:
  
  - `docker build -t swwwcycle-builder .`
  - `docker run -v $(pwd):/app swwwcycle-builder`
  
- with pyinstaller:
  - `pyinstaller --onefile --name swwwcycle main.py`

### License

- Inversepolarity License 1.0

[changelog](./changelog)