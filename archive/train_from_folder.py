"""
Train a FLUX LoRA from a folder of individual images.

Usage:
    # For a character LoRA:
    python3 train_from_folder.py --folder ~/Desktop/south_asian_girl_images \
        --trigger BIPCHAR_south_asian_girl --steps 1000

    # For the adult style LoRA:
    python3 train_from_folder.py --folder ~/Desktop/adult_images \
        --trigger BIPADULT --style --steps 1000

After training completes, paste the printed LoRA URL into:
  - characters.py  (for a character LoRA)
  - test_ui.html   (for the adult style LoRA)
"""

import argparse
import io
import os
import sys
import tempfile
import zipfile
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from PIL import Image
except ImportError:
    print("Installing Pillow...")
    os.system("pip3 install Pillow --quiet")
    from PIL import Image

try:
    import fal_client
except ImportError:
    print("Installing fal-client...")
    os.system("pip3 install fal-client --quiet")
    import fal_client


SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def load_images_from_folder(folder: str) -> list[tuple[str, Image.Image]]:
    """Load all supported images from a folder."""
    folder_path = Path(folder).expanduser().resolve()
    if not folder_path.exists():
        print(f"ERROR: Folder not found: {folder_path}")
        sys.exit(1)

    images = []
    for f in sorted(folder_path.iterdir()):
        if f.suffix.lower() in SUPPORTED_EXTENSIONS:
            try:
                img = Image.open(f).convert("RGB")
                images.append((f.name, img))
            except Exception as e:
                print(f"  Skipping {f.name}: {e}")

    print(f"Found {len(images)} images in {folder_path}")
    if len(images) < 5:
        print("WARNING: Fewer than 5 images — training quality will be low. Aim for 15-20.")
    return images


def build_zip(images: list[tuple[str, Image.Image]]) -> bytes:
    """Pack images into a zip."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, img in images:
            img_buf = io.BytesIO()
            # Save as PNG for consistency
            stem = Path(name).stem
            img.save(img_buf, format="PNG")
            zf.writestr(f"{stem}.png", img_buf.getvalue())
    return buf.getvalue()


def train(folder: str, trigger: str, is_style: bool, steps: int) -> str:
    fal_key = os.environ.get("FAL_KEY")
    if not fal_key:
        print("ERROR: FAL_KEY not set.")
        print("Run: export FAL_KEY=your-key-here")
        sys.exit(1)

    print(f"\nTrigger word : {trigger}")
    print(f"Mode         : {'style LoRA' if is_style else 'character LoRA'}")
    print(f"Steps        : {steps}  (~${steps * 0.0024:.2f})\n")

    images = load_images_from_folder(folder)

    print("Packaging images into zip...")
    zip_bytes = build_zip(images)
    print(f"Zip size: {len(zip_bytes) / 1024:.1f} KB, {len(images)} images")

    print("Uploading to fal.ai storage...")
    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp:
        tmp.write(zip_bytes)
        tmp_path = tmp.name

    try:
        zip_url = fal_client.upload_file(tmp_path)
        print(f"Uploaded: {zip_url}")
    finally:
        os.unlink(tmp_path)

    print(f"\nStarting LoRA training — this takes ~15–20 minutes...\n")
    result = fal_client.run(
        "fal-ai/flux-lora-fast-training",
        arguments={
            "images_data_url": zip_url,
            "trigger_word":    trigger,
            "steps":           steps,
            "is_style":        is_style,
            "create_masks":    not is_style,  # masks help for characters, not for style
        },
    )

    lora_url = (
        result.get("diffusers_lora_file", {}).get("url")
        or result.get("config_file", {}).get("url")
        or str(result)
    )

    print("\n" + "=" * 60)
    print("TRAINING COMPLETE")
    print("=" * 60)
    print(f"Trigger word : {trigger}")
    print(f"LoRA URL     : {lora_url}")
    print("=" * 60)

    if is_style:
        print("\nThis is the adult style LoRA.")
        print("Paste the URL into test_ui.html as ADULT_LORA_URL.")
    else:
        print(f"\nPaste this URL into characters.py / characters.rb")
        print(f"under the character with trigger '{trigger}'.")

    return lora_url


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a FLUX LoRA from a folder of images")
    parser.add_argument("--folder",  required=True, help="Path to folder containing training images")
    parser.add_argument("--trigger", required=True, help="Trigger word (e.g. BIPCHAR_south_asian_girl or BIPADULT)")
    parser.add_argument("--steps",   type=int, default=1000, help="Training steps (default: 1000)")
    parser.add_argument("--style",   action="store_true", help="Train as style LoRA (use for adult style, not characters)")
    args = parser.parse_args()

    train(args.folder, args.trigger, args.style, args.steps)
