# 技術資料: フーリエ変換による曲線の抽象化

## 1. 離散フーリエ変換 (DFT) の基礎

### 1.1 定義

$N$ 個の点列 $\{z_n\}_{n=0}^{N-1}$ に対する離散フーリエ変換は以下で定義される：

$$
F_k = \sum_{n=0}^{N-1} z_n \cdot e^{-\frac{2\pi i k n}{N}} \quad (k = 0, 1, \ldots, N-1)
$$

逆変換は：

$$
z_n = \frac{1}{N} \sum_{k=0}^{N-1} F_k \cdot e^{\frac{2\pi i k n}{N}}
$$

### 1.2 周波数の解釈

各 $F_k$ は周波数 $f_k$ に対応する複素振幅を表す：

$$
f_k = \begin{cases}
\frac{k}{N} & (k < \frac{N}{2}) \\
\frac{k - N}{N} & (k \geq \frac{N}{2})
\end{cases}
$$

- $|F_k|$: 振幅（その周波数成分の「強さ」）
- $\arg(F_k)$: 位相（その周波数成分の「開始位置」）

---

## 2. 2次元曲線のフーリエ表現

### 2.1 複素数としての座標

2次元平面上の点列 $\{(x_n, y_n)\}$ を複素数列として表現：

$$
z_n = x_n + i y_n
$$

### 2.2 曲線の再構成

連続パラメータ $t \in [0, 1)$ を用いて、滑らかな曲線を再構成：

$$
z(t) = \frac{1}{N} \sum_{k \in S} F_k \cdot e^{2\pi i f_k N t}
$$

ここで $S$ は選択された周波数成分のインデックス集合。

### 2.3 K成分での近似

振幅 $|F_k|$ の大きい順に上位 $K$ 個を選択：

$$
S_K = \underset{|S|=K}{\arg\max} \sum_{k \in S} |F_k|
$$

再構成曲線：

$$
\tilde{z}_K(t) = \frac{1}{N} \sum_{k \in S_K} F_k \cdot e^{2\pi i f_k N t}
$$

**性質**:
- $K = N$ のとき $\tilde{z}_N(t) = z(t)$（完全復元）
- $K$ が小さいほど高周波成分が失われ、曲線が滑らかになる

---

## 3. 3次元拡張（複数ストローク対応）

### 3.1 問題設定

複数ストロークを扱うため、ペンの状態（描画中/移動中）を第3軸として追加：

$$
\mathbf{p}_n = (x_n, y_n, \text{pen}_n)
$$

ここで：
- $\text{pen}_n = 1$: 描画中（線を引く）
- $\text{pen}_n = 0$: 移動中（線を引かない）

### 3.2 各軸独立のDFT

3つの実数値信号を独立にフーリエ変換：

$$
\begin{aligned}
F_k^{(x)} &= \sum_{n=0}^{N-1} x_n \cdot e^{-\frac{2\pi i k n}{N}} \\
F_k^{(y)} &= \sum_{n=0}^{N-1} y_n \cdot e^{-\frac{2\pi i k n}{N}} \\
F_k^{(\text{pen})} &= \sum_{n=0}^{N-1} \text{pen}_n \cdot e^{-\frac{2\pi i k n}{N}}
\end{aligned}
$$

### 3.3 統合された振幅

周波数成分の重要度を3軸の振幅の和で評価：

$$
A_k = |F_k^{(x)}| + |F_k^{(y)}| + |F_k^{(\text{pen})}|
$$

上位 $K$ 個を選択：

$$
S_K = \{k_1, k_2, \ldots, k_K\} \quad \text{where} \quad A_{k_1} \geq A_{k_2} \geq \cdots \geq A_{k_K}
$$

### 3.4 3次元再構成

$$
\begin{aligned}
\tilde{x}(t) &= \frac{1}{N} \sum_{k \in S_K} \text{Re}\left( F_k^{(x)} \cdot e^{2\pi i f_k N t} \right) \\
\tilde{y}(t) &= \frac{1}{N} \sum_{k \in S_K} \text{Re}\left( F_k^{(y)} \cdot e^{2\pi i f_k N t} \right) \\
\widetilde{\text{pen}}(t) &= \text{clamp}\left( \frac{1}{N} \sum_{k \in S_K} \text{Re}\left( F_k^{(\text{pen})} \cdot e^{2\pi i f_k N t} \right), 0, 1 \right)
\end{aligned}
$$

### 3.5 描画時の閾値処理

連続的なペン値を離散的な描画判定に変換：

$$
\text{draw}(t) = \begin{cases}
\text{true} & (\widetilde{\text{pen}}(t) \geq \theta) \\
\text{false} & (\widetilde{\text{pen}}(t) < \theta)
\end{cases}
$$

本実装では閾値 $\theta = 0.5$ を使用。

さらに、閾値以上の場合は透明度を線形マッピング：

$$
\alpha(t) = \frac{\widetilde{\text{pen}}(t) - \theta}{1 - \theta}
$$

---

## 4. アニメーションのK値サンプリング

### 4.1 指数的サンプリング

$K = 2$ から $K = N$ まで指数的に増加させる：

$$
K_i = \text{round}\left( \exp\left( \log(2) + (\log(N) - \log(2)) \cdot t_i^{0.6} \right) \right)
$$

ここで $t_i = \frac{i}{M-1}$ （$M$ はフレーム数）。

### 4.2 累乗調整の理由

$t^{0.6}$ の累乗を適用することで：
- 序盤（小さい $K$）: フレームが密集 → 抽象的な形の変化を詳しく見せる
- 終盤（大きい $K$）: フレームが疎 → ほぼ完成形なので省略

---

## 5. 計算量

| 処理 | 計算量 |
|------|--------|
| DFT | $O(N^2)$ |
| 振幅ソート | $O(N \log N)$ |
| 再構成（$M$点） | $O(K \cdot M)$ |

※ 本実装では簡易実装のためDFTを使用。FFT ($O(N \log N)$) への置き換えで高速化可能。

---

## 6. 参考文献

- Cooley, J. W., & Tukey, J. W. (1965). "An algorithm for the machine calculation of complex Fourier series"
- 3Blue1Brown. "But what is the Fourier Transform? A visual introduction" (YouTube)
