#!/usr/bin/env python3
import os
import sys
import requests
import subprocess
from pathlib import Path
import urllib.request

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"
    
    session = requests.Session()
    response = session.get(URL, params={'id': id, 'confirm': 't'}, stream=True)
    
    # Get the token for large files
    token = None
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            token = value
            break
    
    if token:
        response = session.get(URL, params={'id': id, 'confirm': token}, stream=True)
    
    # Save the file
    with open(destination, 'wb') as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)

def download_from_alternative_source(destination):
    """Try to download from a mirror source"""
    # Alternative URLs - these are just examples and may not work
    alt_urls = [
        "https://github.com/CorentinJ/Real-Time-Voice-Cloning/releases/download/v1.0/synthesizer.pt",
        "https://huggingface.co/CorentinJ/Real-Time-Voice-Cloning/resolve/main/synthesizer.pt"
    ]
    
    for url in alt_urls:
        try:
            print(f"Trying to download from: {url}")
            urllib.request.urlretrieve(url, destination)
            return True
        except Exception as e:
            print(f"Failed: {e}")
    
    return False

def main():
    # Create models directory if it doesn't exist
    model_dir = Path("saved_models/default")
    model_dir.mkdir(parents=True, exist_ok=True)
    
    # Path to the synthesizer model
    synthesizer_path = model_dir / "synthesizer.pt"
    
    # Remove existing model if it exists
    if synthesizer_path.exists():
        print("Removing existing synthesizer model...")
        synthesizer_path.unlink()
    
    print("Attempting to download synthesizer model...")
    
    # Try direct Google Drive download
    try:
        # Google Drive ID for the synthesizer model
        file_id = "1EqFMIbvxffxtjiVrtykroF6_mUh-5Z3s"
        print("Downloading from Google Drive...")
        download_file_from_google_drive(file_id, str(synthesizer_path))
        
        if synthesizer_path.exists() and synthesizer_path.stat().st_size > 10000000:  # Check if file is reasonably sized
            print("Synthesizer model downloaded successfully!")
            return True
    except Exception as e:
        print(f"Google Drive download failed: {e}")
    
    # Try wget as alternative
    try:
        print("Trying with wget...")
        subprocess.run([
            'wget', 
            '--no-check-certificate',
            'https://drive.google.com/uc?export=download&id=1EqFMIbvxffxtjiVrtykroF6_mUh-5Z3s&confirm=t',
            '-O', 
            str(synthesizer_path)
        ])
        
        if synthesizer_path.exists() and synthesizer_path.stat().st_size > 10000000:
            print("Synthesizer model downloaded successfully with wget!")
            return True
    except Exception as e:
        print(f"wget download failed: {e}")
    
    # Try alternative sources
    if download_from_alternative_source(str(synthesizer_path)):
        print("Synthesizer model downloaded from alternative source!")
        return True
    
    print("All download attempts failed. Please download the model manually.")
    print("You can download it from the project's wiki page and place it in:")
    print(f"  {synthesizer_path}")
    return False

if __name__ == "__main__":
    main() 