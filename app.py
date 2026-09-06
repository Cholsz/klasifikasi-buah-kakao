import os

# =====================================================================
# 1. PEMBUNGKAM LOG TENSORFLOW (Agar terminal Anda bersih dan rapi)
# =====================================================================
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Mematikan log info dan warning TF
import logging
logging.getLogger('tensorflow').setLevel(logging.ERROR)

# Menghentikan pesan peringatan dari pustaka internal
try:
    import absl.logging
    absl.logging.set_verbosity(absl.logging.ERROR)
except ImportError:
    pass
# =====================================================================

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import tensorflow as tf
import numpy as np
from utils import preprocess_image, get_disease_info

app = Flask(__name__)
app.secret_key = "skripsi_kakao_secret_key" 

# Konfigurasi folder upload gambar dari user
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # Batas maksimal ukuran file (5MB)

# Membuat folder uploads secara otomatis jika belum ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Memuat model CNN (.keras)
# Baris ini mencari file 'best_model.keras' di dalam folder 'model'
MODEL_PATH = os.path.join('best_models', 'best_dengan_augmentasi.keras')
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("\n" + "="*50)
    print("=== [SUKSES] Model CNN Berhasil Dimuat Ke Memori ===")
    print("="*50 + "\n")
except Exception as e:
    print("\n" + "="*50)
    print(f"=== [ERROR] Gagal Memuat Model! Detail: {str(e)} ===")
    print("=== Silakan cek apakah file 'model/best_model.keras' sudah ada. ===")
    print("="*50 + "\n")
    model = None

# Daftar nama kelas sesuai dengan hasil training model Anda
CLASS_NAMES = ['Black Pod Rot', 'Healthy', 'Pod Borer']

def allowed_file(filename):
    """Memeriksa apakah format gambar yang diupload sudah sesuai (PNG/JPG/JPEG)"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['GET', 'POST'])
def detect():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Gagal memproses, file tidak ditemukan.')
            return redirect(request.url)
            
        file = request.files['file']
        
        if file.filename == '':
            flash('Anda belum memilih file gambar.')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            # Menyimpan gambar yang diupload ke static/uploads/
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            if model is None:
                flash('Sistem gagal memprediksi karena model .keras tidak terbaca di folder model/.')
                return redirect(request.url)
            
            # 1. Preprocessing gambar menggunakan fungsi di utils.py
            processed_img = preprocess_image(filepath)
            
            # 2. Melakukan prediksi secara diam-diam (verbose=0 agar terminal bersih)
            predictions = model.predict(processed_img, verbose=0)[0]
            
            # 3. Mengambil kelas dengan probabilitas tertinggi
            predicted_class_idx = np.argmax(predictions)
            predicted_class = CLASS_NAMES[predicted_class_idx]
            confidence = float(predictions[predicted_class_idx]) * 100
            
            # 4. Mengumpulkan probabilitas ketiga kelas untuk grafik di halaman hasil
            all_predictions = []
            for idx, class_name in enumerate(CLASS_NAMES):
                all_predictions.append({
                    'class_name': class_name,
                    'probability': round(float(predictions[idx]) * 100, 2)
                })
                
            # 5. Mengambil info deskripsi penyakit & cara penanganannya
            info = get_disease_info(predicted_class)
            
            # Mengirimkan hasil ke result.html
            return render_template(
                'result.html',
                image_path=filepath,
                predicted_class=predicted_class,
                confidence=round(confidence, 2),
                all_predictions=all_predictions,
                description=info['deskripsi'],
                prevention=info['pencegahan']
            )
        else:
            flash('Format file salah! Gunakan format JPG, JPEG, atau PNG.')
            return redirect(request.url)
            
    return render_template('detect.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/guide')
def guide():
    return render_template('guide.html')

if __name__ == '__main__':
    # Jalankan server Flask lokal
    app.run(debug=True, port=5000)