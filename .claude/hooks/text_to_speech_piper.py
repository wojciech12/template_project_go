#!/usr/bin/env python3
"""
Simplified Text-to-Speech script using Piper binary with ffplay audio playback.

Usage:
    python text_to_speech_piper.py "Hello, world!"
    echo "Hello, world!" | python text_to_speech_piper.py
"""

import os
import sys
import subprocess
import argparse
import tempfile
import shutil
from pathlib import Path


def get_piper_home():
    """Get the Piper home directory from environment variable."""
    piper_home = os.environ.get("PIPER_HOME")
    if not piper_home:
        raise EnvironmentError("PIPER_HOME environment variable is not set")

    piper_path = Path(piper_home)
    if not piper_path.exists():
        raise FileNotFoundError(f"Piper home directory not found: {piper_home}")

    return piper_path


def find_piper_binary(piper_home):
    """Find the Piper binary in the Piper home directory."""
    binary_path = piper_home / "piper"

    if not binary_path.exists():
        for subdir in ["bin", "piper"]:
            alt_path = piper_home / subdir / "piper"
            if alt_path.exists():
                binary_path = alt_path
                break
        else:
            raise FileNotFoundError(f"Piper binary not found in {piper_home}")

    if not os.access(binary_path, os.X_OK):
        raise PermissionError(f"Piper binary is not executable: {binary_path}")

    return binary_path


def find_default_model(piper_home):
    """Find a default model to use for TTS."""
    models_dir = piper_home / "models"

    if not models_dir.exists():
        raise FileNotFoundError(f"Models directory not found: {models_dir}")

    preferred_models = [
        "en_US-libritts_r-high.onnx",
        "en_US-libritts_r-medium.onnx",
        "en_US-lessac-medium.onnx",
        "en_US-ljspeech-medium.onnx",
    ]

    for model_name in preferred_models:
        model_path = models_dir / model_name
        if model_path.exists():
            return model_path

    onnx_models = list(models_dir.glob("*.onnx"))
    if onnx_models:
        return onnx_models[0]

    raise FileNotFoundError(f"No ONNX models found in {models_dir}")


def play_wav_file(wav_file):
    """Play a WAV file using ffplay."""
    if not shutil.which("ffplay"):
        print(
            "Warning: ffplay not found. Install ffmpeg to play audio.", file=sys.stderr
        )
        return False

    try:
        subprocess.run(
            ["ffplay", "-nodisp", "-autoexit", str(wav_file)],
            check=True,
            capture_output=True,
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error playing audio with ffplay: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Unexpected error playing audio: {e}", file=sys.stderr)
        return False


def run_piper_tts(text, piper_binary, model_path, output_file=None, play_audio=True):
    """Run Piper TTS with the given text and parameters."""
    temp_file = None
    actual_output_file = output_file

    if play_audio and not output_file:
        temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        actual_output_file = temp_file.name
        temp_file.close()

    cmd = [str(piper_binary), "--model", str(model_path)]

    if actual_output_file:
        cmd.extend(["--output_file", str(actual_output_file)])

    try:
        subprocess.run(cmd, input=text, text=True, capture_output=True, check=True)

        if play_audio and actual_output_file:
            play_wav_file(actual_output_file)

        if temp_file:
            try:
                os.unlink(temp_file.name)
            except OSError:
                pass

        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running Piper: {e}", file=sys.stderr)
        if temp_file:
            try:
                os.unlink(temp_file.name)
            except OSError:
                pass
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate speech from text using Piper TTS"
    )

    parser.add_argument(
        "text",
        nargs="?",
        help="Text to convert to speech (if not provided, reads from stdin)",
    )

    parser.add_argument(
        "--model",
        help="Path to ONNX model file (relative to PIPER_HOME/models or absolute path)",
    )

    parser.add_argument(
        "--output",
        help="Output audio file path (if not specified, plays audio directly)",
    )

    parser.add_argument(
        "--no-play", action="store_true", help="Don't play audio after generation"
    )

    args = parser.parse_args()

    try:
        piper_home = get_piper_home()
        piper_binary = find_piper_binary(piper_home)

        if args.text:
            text = args.text
        else:
            text = sys.stdin.read().strip()

        if not text:
            print("No text provided", file=sys.stderr)
            return 1

        if args.model:
            if os.path.isabs(args.model):
                model_path = Path(args.model)
            else:
                model_path = piper_home / "models" / args.model
        else:
            model_path = find_default_model(piper_home)

        if not model_path.exists():
            print(f"Model not found: {model_path}", file=sys.stderr)
            return 1

        play_audio = not args.no_play
        success = run_piper_tts(text, piper_binary, model_path, args.output, play_audio)

        return 0 if success else 1

    except (EnvironmentError, FileNotFoundError, PermissionError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 1


if __name__ == "__main__":
    sys.exit(main())
