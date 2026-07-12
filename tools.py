import os
import shutil
import subprocess

def list_directory(path="."):
    """List contents of a directory"""
    try:
        return os.listdir(path)
    except Exception as e:
        print(f"Error listing directory: {e}")
        return []

def run_system_command(command):
    """Run a safe system command"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        print(f"Error running command: {e}")
        return str(e)
