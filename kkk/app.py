from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
from PIL import Image
import io
import base64

app = Flask(__name__)

# 전역 변수 선언
img = np.ones((600, 800, 3), dtype=np.uint8) * 255
penColor = 'black'
penWidth = 5

@app.route('/')
def index():
    return render_template('index.html', pen_color=penColor)

@app.route('/set_pen_color', methods=['POST'])
def set_pen_color():
    global penColor
    try:
        penColor = request.form['color']
    except KeyError:
        return jsonify({'error': 'color parameter missing'}), 400
    return jsonify({'pen_color': penColor})

@app.route('/add_text', methods=['POST'])
def add_text():
    global img
    try:
        text = request.form['text']
        x, y = 100, 100  # 텍스트 위치 설정
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, text, (x, y), font, 1, (0, 0, 0), 2, cv2.LINE_AA)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify({'message': '텍스트가 추가되었습니다.'})

@app.route('/get_canvas_image')
def get_canvas_image():
    global img
    try:
        # 이미지를 PNG 포맷으로 인코딩
        _, buffer = cv2.imencode('.PNG', img)
        img_bytes = buffer.tobytes()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify({'image': img_base64})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
