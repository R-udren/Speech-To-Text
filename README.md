# Speech To Text - Speech Recognition

## Description

This is simple speech recognition program using python. It uses Offline [VOSK](https://alphacephei.com/vosk/) trained
models to recognize speech.

## Requirements

- Windows 10/11 (Not tested on other OS)
- Python 3.6 or higher
- [Vosk model](https://alphacephei.com/vosk/models) (Download and extract it to `models` folder)
- Other dependencies are in `requirements.txt` file

## Installation

1. Clone this repository

```bash
git clone https://github.com/R-udren/Speech-To-Text.git
```

2. Change directory to `Speech-To-Text`

```bash
cd Speech-To-Text
```

3. Create virtual environment

```bash
python -m venv venv
```

4. Activate virtual environment

```bash
venv\Scripts\activate.bat
```

5. Install requirements using:

```bash
pip install -r requirements.txt
```

6. Download Vosk model from [here](https://alphacephei.com/vosk/models) and extract it to `models` folder

## Usage

### Manual Usage

1. Activate virtual environment
   `venv\Scripts\activate.bat`
2. Run `main.py`
   `python main.py`
3. Follow the instructions in the program
4. Press `Ctrl + C` to stop the program

### Batch Script Usage

1. Create shortcut of `run.bat` file **(Optional)**
2. Run `run.bat` file or shortcut

## Author

- Github: [R-udren](https://github.com/R-udren)
- Discord: rovert777

## License

[MIT](https://choosealicense.com/licenses/mit/)
