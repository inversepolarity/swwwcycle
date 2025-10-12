FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    libqt6widgets6 \
    qt6-base-dev \
    libgl1-mesa-glx \
    libgl1-mesa-dev \
    libglib2.0-0 \
    libxkbcommon-x11-0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-xinerama0 \
    libxcb-xfixes0 \
    libxcb-shape0 \
    libegl1 \
    patchelf \
    binutils \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install pyside6 pyinstaller

WORKDIR /app
COPY main.py .
COPY swwwcycle.spec .

CMD ["pyinstaller", "--clean", "swwwcycle.spec"]