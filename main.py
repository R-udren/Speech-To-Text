import json
import os
import queue

import sounddevice as sd
import vosk
from rich.console import Console
from rich.prompt import Prompt

q = queue.Queue()
console = Console()
prompt = Prompt()


def format_size(size):
    units = ["B", "KB", "MB", "GB", "TB"]
    index = 0
    while size > 1024:
        size /= 1024
        index += 1
    return f"{size:.2f} {units[index]}"


def folder_size(path):
    total_size = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return format_size(total_size)


def get_vosk_model():
    models_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "models")

    if not os.path.exists(models_path):
        console.print(
            "Please download the model from https://alphacephei.com/vosk/models and unpack in the 'models' folder.")
        exit(1)

    models = os.listdir(models_path)
    models = [model for model in models if os.path.isdir(os.path.join(models_path, model))]

    console.print("[green]Available models:")
    for index, name in enumerate(models, start=1):
        size = folder_size(os.path.join(models_path, name))
        console.print(f"{index}. [yellow]{name} [/yellow]({size})")
    choices = [str(i) for i in range(1, len(models) + 1)]
    model_index = int(prompt.ask("Select model", choices=choices, show_choices=False)) - 1
    model_name = models[model_index]
    model_path = os.path.join(models_path, model_name)

    try:
        model = vosk.Model(model_path)
        return model, model_name
    except Exception as e:
        console.print(f"[red]Error: {e}\n")
        return get_vosk_model()


def callback(indata, frames, time, status):
    if status:
        console.print(status)
    q.put(bytes(indata))


def main():
    model, model_name = get_vosk_model()

    microphone, speaker = sd.default.device
    samplerate = sd.query_devices(microphone, 'input')['default_samplerate']

    console.print(f"\n[green]Current settings:")
    console.print(f"[cyan]Using microphone[/cyan]: {sd.query_devices(microphone, 'input')['name']} ({samplerate} Hz)")
    console.print(f"[cyan]Using speaker[/cyan]: {sd.query_devices(speaker, 'output')['name']}")

    console.print(f"[cyan]Using vosk model[/cyan]: {model_name}")

    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=microphone, dtype='int16',
                           channels=1, callback=callback):
        console.print("\nListening...")
        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                text = json.loads(rec.Result())['text']
                if text:
                    console.print(f"{text}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[red]Exiting...")
        exit(0)
    except Exception as e:
        console.print_exception()
        console.print(f"Error: {e}")
        exit(1)
