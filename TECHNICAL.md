# Technical Documentation: Curve Abstraction via Fourier Transform

## 1. Discrete Fourier Transform (DFT) Basics

### 1.1 Definition

The Discrete Fourier Transform of a sequence of $N$ points $\{z_n\}_{n=0}^{N-1}$ is defined as:

$$
F_k = \sum_{n=0}^{N-1} z_n \cdot e^{-\frac{2\pi i k n}{N}} \quad (k = 0, 1, \ldots, N-1)
$$

The inverse transform is:

$$
z_n = \frac{1}{N} \sum_{k=0}^{N-1} F_k \cdot e^{\frac{2\pi i k n}{N}}
$$

### 1.2 Frequency Interpretation

Each $F_k$ represents the complex amplitude corresponding to frequency $f_k$:

$$
f_k = \begin{cases}
\frac{k}{N} & (k < \frac{N}{2}) \\
\frac{k - N}{N} & (k \geq \frac{N}{2})
\end{cases}
$$

- $|F_k|$: Amplitude (the "strength" of that frequency component)
- $\arg(F_k)$: Phase (the "starting position" of that frequency component)

---

## 2. Fourier Representation of 2D Curves

### 2.1 Coordinates as Complex Numbers

A sequence of points $\{(x_n, y_n)\}$ in the 2D plane is represented as complex numbers:

$$
z_n = x_n + i y_n
$$

### 2.2 Curve Reconstruction

Using a continuous parameter $t \in [0, 1)$, we reconstruct a smooth curve:

$$
z(t) = \frac{1}{N} \sum_{k \in S} F_k \cdot e^{2\pi i f_k N t}
$$

where $S$ is the set of selected frequency component indices.

### 2.3 K-Component Approximation

Select the top $K$ components by amplitude $|F_k|$:

$$
S_K = \underset{|S|=K}{\arg\max} \sum_{k \in S} |F_k|
$$

Reconstructed curve:

$$
\tilde{z}_K(t) = \frac{1}{N} \sum_{k \in S_K} F_k \cdot e^{2\pi i f_k N t}
$$

**Properties**:
- When $K = N$: $\tilde{z}_N(t) = z(t)$ (perfect reconstruction)
- Smaller $K$ loses high-frequency components, resulting in smoother curves

---

## 3. 3D Extension (Multi-Stroke Support)

### 3.1 Problem Setting

To handle multiple strokes, we add pen state (drawing/moving) as a third axis:

$$
\mathbf{p}_n = (x_n, y_n, \text{pen}_n)
$$

where:
- $\text{pen}_n = 1$: Drawing (pen down)
- $\text{pen}_n = 0$: Moving (pen up)

### 3.2 Independent DFT for Each Axis

Three real-valued signals are transformed independently:

$$
\begin{aligned}
F_k^{(x)} &= \sum_{n=0}^{N-1} x_n \cdot e^{-\frac{2\pi i k n}{N}} \\
F_k^{(y)} &= \sum_{n=0}^{N-1} y_n \cdot e^{-\frac{2\pi i k n}{N}} \\
F_k^{(\text{pen})} &= \sum_{n=0}^{N-1} \text{pen}_n \cdot e^{-\frac{2\pi i k n}{N}}
\end{aligned}
$$

### 3.3 Combined Amplitude

The importance of each frequency component is evaluated by the sum of amplitudes across all three axes:

$$
A_k = |F_k^{(x)}| + |F_k^{(y)}| + |F_k^{(\text{pen})}|
$$

Select the top $K$:

$$
S_K = \{k_1, k_2, \ldots, k_K\} \quad \text{where} \quad A_{k_1} \geq A_{k_2} \geq \cdots \geq A_{k_K}
$$

### 3.4 3D Reconstruction

$$
\begin{aligned}
\tilde{x}(t) &= \frac{1}{N} \sum_{k \in S_K} \text{Re}\left( F_k^{(x)} \cdot e^{2\pi i f_k N t} \right) \\
\tilde{y}(t) &= \frac{1}{N} \sum_{k \in S_K} \text{Re}\left( F_k^{(y)} \cdot e^{2\pi i f_k N t} \right) \\
\widetilde{\text{pen}}(t) &= \text{clamp}\left( \frac{1}{N} \sum_{k \in S_K} \text{Re}\left( F_k^{(\text{pen})} \cdot e^{2\pi i f_k N t} \right), 0, 1 \right)
\end{aligned}
$$

### 3.5 Threshold Processing for Rendering

Convert continuous pen values to discrete draw decisions:

$$
\text{draw}(t) = \begin{cases}
\text{true} & (\widetilde{\text{pen}}(t) \geq \theta) \\
\text{false} & (\widetilde{\text{pen}}(t) < \theta)
\end{cases}
$$

This implementation uses threshold $\theta = 0.5$.

Additionally, for values above the threshold, opacity is linearly mapped:

$$
\alpha(t) = \frac{\widetilde{\text{pen}}(t) - \theta}{1 - \theta}
$$

---

## 4. Animation K-Value Sampling

### 4.1 Exponential Sampling

K values are increased exponentially from $K = 2$ to $K = N$:

$$
K_i = \text{round}\left( \exp\left( \log(2) + (\log(N) - \log(2)) \cdot t_i^{0.6} \right) \right)
$$

where $t_i = \frac{i}{M-1}$ ($M$ is the number of frames).

### 4.2 Rationale for Power Adjustment

Applying the $t^{0.6}$ power results in:
- Early frames (small $K$): Dense sampling → Shows detailed changes in abstract shapes
- Later frames (large $K$): Sparse sampling → Nearly complete, so fewer frames needed

---

## 5. Computational Complexity

| Operation | Complexity |
|-----------|------------|
| DFT | $O(N^2)$ |
| Amplitude Sort | $O(N \log N)$ |
| Reconstruction ($M$ points) | $O(K \cdot M)$ |

※ This implementation uses DFT for simplicity. Replacing with FFT ($O(N \log N)$) would improve performance.

---

## 6. References

- Cooley, J. W., & Tukey, J. W. (1965). "An algorithm for the machine calculation of complex Fourier series"
- 3Blue1Brown. "But what is the Fourier Transform? A visual introduction" (YouTube)

---

[日本語版 技術資料](TECHNICAL.ja.md)
