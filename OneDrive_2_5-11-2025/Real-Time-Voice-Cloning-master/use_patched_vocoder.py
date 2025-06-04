#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess
from pathlib import Path
import urllib.request

def patch_vocoder():
    """
    Replace the original fatchord_version.py with our patched version
    """
    original_file = Path("vocoder/models/fatchord_version.py")
    patched_file = Path("vocoder/models/fatchord_version_patched.py")
    backup_file = Path("vocoder/models/fatchord_version.py.bak")
    
    # Check if patched file exists
    if not patched_file.exists():
        print("Error: Patched file not found!")
        return False
    
    # Create backup if not already existing
    if not backup_file.exists() and original_file.exists():
        print("Creating backup of original file...")
        shutil.copy2(original_file, backup_file)
    
    # Copy patched file to replace the original
    print("Replacing vocoder with patched version...")
    shutil.copy2(patched_file, original_file)
    
    print("Vocoder patched successfully!")
    return True

def redownload_model(model_name, url):
    """
    Force redownload a model
    """
    model_dir = Path("saved_models/default")
    model_dir.mkdir(parents=True, exist_ok=True)
    
    model_path = model_dir / f"{model_name}.pt"
    
    # Remove existing model if it exists
    if model_path.exists():
        print(f"Removing existing {model_name} model...")
        model_path.unlink()
    
    print(f"Downloading {model_name} model...")
    try:
        # Try using wget which handles Google Drive better
        subprocess.run(['wget', '--no-check-certificate', url, '-O', str(model_path)])
        if model_path.exists() and model_path.stat().st_size > 0:
            print(f"{model_name} model downloaded successfully!")
            return True
    except:
        # Fall back to urllib
        try:
            urllib.request.urlretrieve(url, str(model_path))
            if model_path.exists() and model_path.stat().st_size > 0:
                print(f"{model_name} model downloaded successfully!")
                return True
        except Exception as e:
            print(f"Error downloading {model_name} model: {e}")
    
    return False

if __name__ == "__main__":
    # Model URLs
    encoder_url = "https://drive.google.com/uc?export=download&id=1q8mEGwCkFy23KZsinbuvdKAQLqNKbYf1"
    synthesizer_url = "https://drive.google.com/uc?export=download&id=1EqFMIbvxffxtjiVrtykroF6_mUh-5Z3s&confirm=t"
    vocoder_url = "https://drive.google.com/uc?export=download&id=1cf2NO6FtI0jDuy8AV3Xgn6leO6dHjIgu"
    
    # Ask if user wants to redownload models
    redownload = input("Do you want to redownload the models? (y/n): ").lower() == 'y'
    
    if redownload:
        print("Redownloading models...")
        redownload_model("encoder", encoder_url)
        redownload_model("synthesizer", synthesizer_url)
        redownload_model("vocoder", vocoder_url)
    
    # Patch the vocoder
    success = patch_vocoder()
    
    if success:
        print("You can now run the demo with: python demo_toolbox.py --cpu") 