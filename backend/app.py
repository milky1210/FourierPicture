import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    pts = np.array(data['points'])
    if pts.shape[0] == 0:
        return jsonify({'points': []})
    
    # 座標を複素数 z = x + i*y として扱う
    z = pts[:, 0] + 1j * pts[:, 1]
    N = len(z)
    F = np.fft.fft(z)
    
    # 振幅の大きい順に係数を抽出
    indices_sorted = np.argsort(np.abs(F))[::-1]
    K = 10  # 上位 K 個の係数を使用（必要に応じて調整）
    selected_indices = indices_sorted[:K]
    
    # 時間軸（0〜1の範囲で N 個のサンプル）
    t = np.linspace(0, 1, N, endpoint=False)
    z_reconstructed = np.zeros(N, dtype=complex)
    freqs = np.fft.fftfreq(N)
    for k in selected_indices:
        z_reconstructed += (F[k] / N) * np.exp(2j * np.pi * freqs[k] * t)
    
    # 再構成した複素数から [x, y] の座標リストに変換
    points_reconstructed = [[pt.real, pt.imag] for pt in z_reconstructed]
    return jsonify({'points': points_reconstructed})

if __name__ == '__main__':
    # Docker コンテナ内では 0.0.0.0 で待ち受ける必要があります
    app.run(host='0.0.0.0', debug=True)
