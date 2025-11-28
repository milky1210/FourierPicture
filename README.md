# FourierPicture

A web app that transforms doodles into abstract art using Fourier transforms.

👉 **[Try the Demo](https://milky1210.github.io/FourierPicture/)**

![Screenshot](image/README/1764253760039.png)

## Features

| Feature | Description |
|---------|-------------|
| 🎨 Multi-stroke | Draw multiple lines to create a single image |
| 🔄 Fourier Transform | Reconstruct with specified number of terms (K) |
| 🎬 Animation | Visualize reconstruction from K=2 to full resolution |
| 📹 Video Export | Save as WebM format |
| 📱 Mobile Support | Touch-enabled |
| 🔗 QR Sharing | Create shareable QR cards with embedded decoder |

## How to Use

1. Draw on the left canvas
2. Set the number of Fourier terms (K)
3. Click "Transform" or "Generate Animation"
4. View the reconstructed image on the right canvas
5. Click "Create QR Card" to generate a shareable artifact card with QR code

## How It Works

The point sequence is treated as complex numbers $z = x + iy$ and transformed using Discrete Fourier Transform (DFT). Only the top K frequency components (by amplitude) are used for reconstruction. Smaller K values produce more abstract shapes, while larger values approach the original drawing.

For detailed mathematical background, see [Technical Documentation (TECHNICAL.md)](TECHNICAL.md).

### QR Code Format

The generated QR code contains both the restoration method **and** the coefficient data, making it self-documenting:

**QR Data Structure:**
```
[ASCII Decoder Header] + [Binary Coefficient Data]
```

**Embedded Decoder Instructions:**
```
[UNIVERSAL DECODER: FOURIER STROKE]
Formula: v(t)=Sum(Re(F[k]*exp(i*2*pi*k*t)))
Range: t=0.0...1.0
Target: X,Y,Pen axes independently
Draw: Plot(x(t),y(t)) where pen(t)>0.5
Data: [binary coefficients]
```

This means:
- The QR code is **self-contained** – you don't need external documentation to decode it
- Even if this repository disappears, the QR itself contains the restoration formula
- The formula works for any implementation (Python, JavaScript, etc.)

**Data Encoding:**
- Compact binary format for coefficients (~60% size reduction vs JSON)
- ASCII metadata (~180 bytes) for universality
- Supports 3D multi-stroke and 2D single-stroke modes
- Backward compatible with older URL formats

## Run Locally

```bash
git clone https://github.com/milky1210/FourierPicture.git
```

Simply open `docs/index.html` in your browser.

## Publication Info

- **First Published**: 2025-11-27 (See [git history](https://github.com/milky1210/FourierPicture/commits/main) for precise timestamp)
- **Author**: [milky1210](https://github.com/milky1210)

## License

MIT License

---

[日本語版 README](README.ja.md)
