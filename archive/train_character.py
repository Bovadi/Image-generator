"""
LoRA training script for a BIP Visualized character.

Usage:
    python train_character.py --image path/to/character_sheet.png --character-id south_asian_girl_child

The script will:
1. Crop the character sheet grid into individual panels
2. Upload them to fal.ai
3. Kick off a FLUX LoRA training run
4. Print the resulting LoRA URL to add to characters.py
"""

import argparse
import io
import os
import zipfile
import tempfile
import sys

# Load .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from PIL import Image
except ImportError:
    print("Installing Pillow...")
    os.system("pip install Pillow --quiet")
    from PIL import Image

try:
    import fal_client
except ImportError:
    print("Installing fal-client...")
    os.system("pip install fal-client --quiet")
    import fal_client

from app.characters import CHARACTERS


def crop_grid(image_path: str, cols: int = 4, rows: int = 3) -> list[Image.Image]:
    """Crop a character sheet grid into individual panels."""
    img = Image.open(image_path).convert("RGB")
    w, h = img.size
    panel_w = w // cols
    panel_h = h // rows

    panels = []
    for row in range(rows):
        for col in range(cols):
            left = col * panel_w
            top = row * panel_h
            panel = img.crop((left, top, left + panel_w, top + panel_h))
            panels.append(panel)

    print(f"Cropped {len(panels)} panels from {cols}x{rows} grid ({w}x{h} image)")
    return panels


def build_training_zip(panels: list[Image.Image]) -> bytes:
    """Pack all panels into a zip file in memory."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for i, panel in enumerate(panels):
            img_buf = io.BytesIO()
            panel.save(img_buf, format="PNG")
            zf.writestr(f"character_{i+1:02d}.png", img_buf.getvalue())
    return buf.getvalue()


def train(image_path: str, character_id: str, steps: int = 1000) -> str:
    """Run FLUX LoRA training on fal.ai and return the LoRA URL."""
    fal_key = os.environ.get("FAL_KEY")
    if not fal_key:
        print("ERROR: FAL_KEY environment variable is not set.")
        print("Set it with: export FAL_KEY=your-key-here")
        sys.exit(1)

    if character_id not in CHARACTERS:
        print(f"ERROR: Unknown character_id '{character_id}'")
        print(f"Valid IDs: {list(CHARACTERS.keys())}")
        sys.exit(1)

    character = CHARACTERS[character_id]
    trigger_word = character["trigger_word"]

    print(f"\nCharacter: {character_id}")
    print(f"Trigger word: {trigger_word}")
    print(f"Training steps: {steps}")
    print(f"Estimated cost: ~${steps * 0.0024:.2f}\n")

    # Crop sheet into panels
    panels = crop_grid(image_path)

    # Build zip
    print("Packaging training images...")
    zip_bytes = build_training_zip(panels)

    # Upload zip to fal.ai storage
    print("Uploading to fal.ai storage...")
    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp:
        tmp.write(zip_bytes)
        tmp_path = tmp.name

    try:
        zip_url = fal_client.upload_file(tmp_path)
        print(f"Uploaded: {zip_url}")
    finally:
        os.unlink(tmp_path)

    # Kick off training
    print("\nStarting LoRA training (this takes ~15–20 minutes)...\n")
    result = fal_client.run(
        "fal-ai/flux-lora-fast-training",
        arguments={
            "images_data_url": zip_url,
            "trigger_word": trigger_word,
            "steps": steps,
            "is_style": False,
            "create_masks": True,
        },
    )

    lora_url = result.get("diffusers_lora_file", {}).get("url") or \
               result.get("config_file", {}).get("url") or \
               str(result)

    print("\n" + "="*60)
    print("TRAINING COMPLETE")
    print("="*60)
    print(f"Character ID : {character_id}")
    print(f"Trigger word : {trigger_word}")
    print(f"LoRA URL     : {lora_url}")
    print("="*60)
    print(f"\nUpdate characters.py:")
    print(f'  "{character_id}": {{')
    print(f'      "lora_url": "{lora_url}",')
    print(f'      "trigger_word": "{trigger_word}",')
    print(f'      ...')
    print(f'  }}')

    return lora_url


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a FLUX LoRA for a BIP Visualized character")
    parser.add_argument("--image", required=True, help="Path to the character sheet image (grid of poses)")
    parser.add_argument("--character-id", required=True, help="Character ID from characters.py")
    parser.add_argument("--steps", type=int, default=1000, help="Training steps (default: 1000, ~$2.40)")
    parser.add_argument("--cols", type=int, default=4, help="Number of columns in the character sheet grid")
    parser.add_argument("--rows", type=int, default=3, help="Number of rows in the character sheet grid")
    args = parser.parse_args()

    train(args.image, args.character_id, args.steps)
