import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    pts = np.array(data['points'])
    K = data.get('K', 10)  # デフォルト値は10
    
    if pts.shape[0] == 0:
        return jsonify({'points': []})
    
    # 座標を複素数 z = x + i*y として扱う
    z = pts[:, 0] + 1j * pts[:, 1]
    N = len(z)
    F = np.fft.fft(z)
    
    # 振幅の大きい順に係数を抽出
    indices_sorted = np.argsort(np.abs(F))[::-1]
    K = min(K, N)  # K が点の数を超えないようにする
    selected_indices = indices_sorted[:K]
    
    # 再構成（逆フーリエ変換）
    # 選択された周波数成分のみを使用
    F_filtered = np.zeros(N, dtype=complex)
    for k in selected_indices:
        F_filtered[k] = F[k]
    
    # 逆フーリエ変換で再構成
    z_reconstructed = np.fft.ifft(F_filtered)
    
    # 再構成した複素数から [x, y] の座標リストに変換
    points_reconstructed = [[pt.real, pt.imag] for pt in z_reconstructed]
    return jsonify({'points': points_reconstructed})

if __name__ == '__main__':
    # Docker コンテナ内では 0.0.0.0 で待ち受ける必要があります
    app.run(host='0.0.0.0', debug=True)
