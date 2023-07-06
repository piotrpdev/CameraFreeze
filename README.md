![Example](./.github/img/example.mp4)

# Camera Freeze

Freeze a virtual camera using a hotkey. Made specifically to freeze a webcam during video calls on Linux.

## Requirements

- [Python 3](https://www.python.org/downloads/)
- [v4l2loopback](https://github.com/umlaeute/v4l2loopback) (and a virtual camera)

## Installation

> **Note:** This project uses the [`keyboard`](https://pypi.org/project/keyboard/) package which requires root privileges to work.

### Ensure pip exists (if not already installed)

```bash
sudo venv/bin/python -m ensurepip
```

### Install dependencies

```bash
sudo venv/bin/python -m pip install -r requirements.txt
```

## Usage

### Run with default settings

> **Note:** This will use `/dev/video0` as the virtual camera and '#' as the hotkey.

```bash
sudo venv/bin/python camera_freeze.py
```

### See available options

```bash
sudo venv/bin/python camera_freeze.py -h
```

