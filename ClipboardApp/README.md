# Data Steward Clipboard Manager

## Overview

**Data Steward Clipboard Manager** is a Python-based application designed to automate the process of capturing, processing, and managing 
clipboard content, specifically for handling master IDs and unique identifiers for the Data Steward role. 
The app supports undo/redo functionality, ensures state persistence across sessions, and is packaged as a Windows 
executable.

## Features

- **Automatic Clipboard Monitoring:** Listens to the clipboard for specific content and processes it accordingly.
- **Undo/Redo Functionality:** Supports multiple levels of undo and redo, with states saved in `.json` files for persistence.
- **User-Friendly Interface:** Simple and intuitive user interface built with `Tkinter` and `ttkthemes`.
- **Executable Packaging:** Available as a downloadable & installable Windows application.

## Installation

### Prerequisites

- **Python 3.8+**: Ensure Python is installed on your system.
- **Git**: If you plan to clone the repository.

### Local Installation for IDE

1. **Clone the repository**:

```bash
git clone https://github.com/Drew5040/ClipboardApp.git
cd ClipboardApp
```
2. **Set up a virtual environment:** 
```bash
python -m venv venv
source venv/bin/activate
```
3. **Install dependencies:**
```bash
pip install -r requirements0.txt
```
4. **Run the application:**
```bash
python main.py 
```
5. **Optional-create an executable:**
```bash
pyinstaller --onefile --windowed main.py
```
<br><br>

****Special Note:*** This application was built with the aid of ChatGPT for guidance 

