# Batch QR generator (requires Pillow; `pip install qrcode[pil]` for better quality)
# Usage:
#   python tools/generate_qr.py urls.txt out/
import sys, os
from PIL import Image, ImageDraw
try:
    import qrcode
except ImportError:
    qrcode = None

def make_qr(data, box=10, border=4):
    if qrcode:
        qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=box, border=border)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
        return img
    img = Image.new("RGB", (256,256), "white")
    d = ImageDraw.Draw(img)
    d.text((10,10), "QR lib not installed", fill="black")
    return img

def main():
    if len(sys.argv) < 3:
        print("Usage: python tools/generate_qr.py urls.txt out/")
        sys.exit(1)
    infile, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    for line in open(infile, "r", encoding="utf-8"):
        line=line.strip()
        if not line:
            continue
        label, url = (line.split(",",1)+["qr"])[:2] if "," in line else ("qr", line)
        if url == "qr":
            url = label
            label = "qr"
        fname = f"{label.replace(' ','-').lower()}.png"
        img = make_qr(url, box=10, border=2)
        img.save(os.path.join(outdir, fname), "PNG")
        print("wrote", fname)

if __name__ == "__main__":
    main()
