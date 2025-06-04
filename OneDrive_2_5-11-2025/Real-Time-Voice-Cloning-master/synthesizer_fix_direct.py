#!/usr/bin/env python3
import os
import sys
import gdown
from pathlib import Path

def main():
    try:
        # Install gdown if not available
        os.system("pip install -q gdown")
        import gdown
    except ImportError:
        print("Failed to install gdown. Please install it manually: pip install gdown")
        return False
    
    # Create models directory if it doesn't exist
    model_dir = Path("saved_models/default")
    model_dir.mkdir(parents=True, exist_ok=True)
    
    # Path to the synthesizer model
    synthesizer_path = model_dir / "synthesizer.pt"
    
    # Remove existing model if it exists
    if synthesizer_path.exists():
        print("Removing existing synthesizer model...")
        os.remove(str(synthesizer_path))
    
    print("Attempting to download synthesizer model...")
    
    # Direct link to the synthesizer model from Google Drive
    url = "https://drive.google.com/uc?id=1EqFMIbvxffxtjiVrtykroF6_mUh-5Z3s"
    
    # Try to download
    try:
        print(f"Downloading to {synthesizer_path}...")
        output = gdown.download(url, str(synthesizer_path), quiet=False)
        
        if output and os.path.exists(str(synthesizer_path)) and os.path.getsize(str(synthesizer_path)) > 10000000:
            print("Synthesizer model downloaded successfully!")
            return True
        else:
            print("Download failed or file is too small.")
            return False
    except Exception as e:
        print(f"Download failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        print("\nAlternative approach: Please download the model manually")
        print("1. Visit: https://github.com/CorentinJ/Real-Time-Voice-Cloning/wiki/Pretrained-models")
        print("2. Download 'synthesizer.pt'")
        print(f"3. Save it to: {os.path.abspath('saved_models/default/synthesizer.pt')}") 