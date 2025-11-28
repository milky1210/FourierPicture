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

## How to Use

1. Draw on the left canvas
2. Set the number of Fourier terms (K)
3. Click "Transform" or "Generate Animation"
4. View the reconstructed image on the right canvas

## How It Works

The point sequence is treated as complex numbers $z = x + iy$ and transformed using Discrete Fourier Transform (DFT). Only the top K frequency components (by amplitude) are used for reconstruction. Smaller K values produce more abstract shapes, while larger values approach the original drawing.

For detailed mathematical background, see [Technical Documentation (TECHNICAL.md)](TECHNICAL.md).

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
