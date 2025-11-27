import numpy as np
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def reconstruct_fourier(pts, K):
    """指定されたK個のフーリエ成分で曲線を再構成"""
    z = pts[:, 0] + 1j * pts[:, 1]
    N = len(z)
    
    F = np.fft.fft(z)
    freqs = np.fft.fftfreq(N)
    
    amplitudes = np.abs(F)
    indices_sorted = np.argsort(amplitudes)[::-1]
    
    K = min(K, N)
    selected_indices = indices_sorted[:K]
    
    num_output_points = max(N, 200)
    t_new = np.linspace(0, 1, num_output_points, endpoint=False)
    
    z_smooth = np.zeros(num_output_points, dtype=complex)
    for k in selected_indices:
        freq = freqs[k] * N
        z_smooth += (F[k] / N) * np.exp(2j * np.pi * freq * t_new)
    
    return [[pt.real, pt.imag] for pt in z_smooth]


@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    pts = np.array(data['points'])
    K = data.get('K', 10)
    
    print(f"=== フーリエ変換処理開始 ===", flush=True)
    print(f"受信した点の数: {len(pts)}", flush=True)
    print(f"K値: {K}", flush=True)
    
    if pts.shape[0] == 0:
        print("警告: 点が0個です", flush=True)
        return jsonify({'points': []})
    
    if len(pts) < 2:
        print("警告: 点が少なすぎます", flush=True)
        return jsonify({'points': pts.tolist()})
    
    points_reconstructed = reconstruct_fourier(pts, K)
    print(f"=== フーリエ変換処理完了 ===", flush=True)
    
    return jsonify({'points': points_reconstructed})


@app.route('/process_animation', methods=['POST'])
def process_animation():
    """K=2から頂点数まで指数的にサンプリングした複数フレームを生成"""
    data = request.get_json()
    pts = np.array(data['points'])
    num_frames = data.get('numFrames', 30)  # フレーム数
    
    print(f"=== アニメーション生成開始 ===", flush=True)
    print(f"受信した点の数: {len(pts)}", flush=True)
    print(f"フレーム数: {num_frames}", flush=True)
    
    if pts.shape[0] == 0:
        return jsonify({'frames': []})
    
    if len(pts) < 2:
        return jsonify({'frames': [{'K': len(pts), 'points': pts.tolist()}]})
    
    N = len(pts)
    
    # K=2 から N まで指数的にサンプリング
    # 序盤（小さいK）のフレームを多めにするため、累乗を使用
    k_min = 2
    k_max = N
    
    k_values = []
    for i in range(num_frames):
        if num_frames == 1:
            k = k_max
        else:
            # 0から1の範囲で、序盤に密度を持たせる（累乗で調整）
            # t^0.5 を使うと序盤が密になる
            t = i / (num_frames - 1)
            t_adjusted = t ** 0.6  # 0.6乗で序盤を密に
            
            # 対数スケールで分布
            log_k = np.log(k_min) + (np.log(k_max) - np.log(k_min)) * t_adjusted
            k = int(np.round(np.exp(log_k)))
        k = max(k_min, min(k, k_max))  # 範囲内に収める
        if k not in k_values:  # 重複を避ける
            k_values.append(k)
    
    # 念のためソート
    k_values = sorted(set(k_values))
    
    print(f"サンプリングされたK値: {k_values}", flush=True)
    
    frames = []
    for k in k_values:
        points_reconstructed = reconstruct_fourier(pts, k)
        frames.append({
            'K': k,
            'points': points_reconstructed,
            'isFinal': False
        })
    
    # 最後に元の入力画像（全成分）のフレームを追加
    final_points = reconstruct_fourier(pts, N)
    frames.append({
        'K': N,
        'points': final_points,
        'isFinal': True  # 最終フレームのマーカー
    })
    
    print(f"生成されたフレーム数: {len(frames)}", flush=True)
    print(f"=== アニメーション生成完了 ===", flush=True)
    
    return jsonify({'frames': frames, 'totalPoints': N})

if __name__ == '__main__':
    # Docker コンテナ内では 0.0.0.0 で待ち受ける必要があります
    app.run(host='0.0.0.0', debug=True)
