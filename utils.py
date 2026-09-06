import numpy as np
from PIL import Image
import tensorflow as tf

def preprocess_image(image_path, target_size=(224, 224)):
    """
    Melakukan preprocessing pada gambar input:
    1. Membuka gambar menggunakan library PIL (Pillow).
    2. Mengonversi gambar ke format RGB jika gambarnya berformat grayscale atau RGBA.
    3. Mengubah ukuran gambar (resize) menjadi 224x224 piksel.
    4. Mengubah gambar menjadi array numerik (numpy array).
    5. Menambahkan dimensi batch (batch dimension) agar sesuai dengan input Keras (1, 224, 224, 3).
    """
    # 1 & 2. Load gambar dan pastikan formatnya RGB
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
        
    # 3. Resize gambar
    img = img.resize(target_size)
    
    # 4. Konversi ke numpy array (Skala 0-255 dibiarkan utuh karena sudah dihandle internal oleh model)
    img_array = np.array(img, dtype=np.float32)
    
    # 5. Tambahkan dimensi batch
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

def get_disease_info(class_name):
    """
    Mengambil data penjelasan medis dan solusi penanganan berdasarkan 
    label prediksi penyakit buah kakao.
    """
    info = {
        "Black Pod Rot": {
            "deskripsi": "Busuk Buah Hitam (Black Pod Rot) disebabkan oleh jamur Phytophthora palmivora. Penyakit ini memicu timbulnya bercak cokelat gelap atau kehitaman pada kulit buah, yang biasanya dimulai dari ujung atau pangkal buah. Infeksi ini menyebar dengan sangat cepat, membuat buah membusuk seluruhnya, mengeras, dan akhirnya rusak.",
            "pencegahan": "Lakukan pemangkasan tajuk pohon secara rutin untuk menjaga sirkulasi udara dan mengurangi kelembapan kebun. Terapkan sanitasi kebun dengan membuang buah yang terinfeksi jauh dari area budidaya, serta gunakan fungisida berbahan aktif tembaga secara berkala saat musim penghujan."
        },
        "Healthy": {
            "deskripsi": "Buah Kakao Sehat (Healthy). Buah kakao berada dalam kondisi prima tanpa gejala infeksi jamur maupun kerusakan fisik akibat hama. Kulit buah memiliki permukaan yang bersih dengan warna kuning cerah (jika matang) atau hijau kemerahan (jika masih muda).",
            "pencegahan": "Lanjutkan pemeliharaan kebun yang konsisten seperti pemupukan organik dan kimiawi secara berimbang, penyiangan gulma pengganggu, pemangkasan berkala, serta monitoring teratur agar buah terhindar dari potensi penyakit."
        },
        "Pod Borer": {
            "deskripsi": "Penggerek Buah Kakao (Pod Borer) disebabkan oleh serangan larva ngengat Conopomorpha cramerella. Larva ini merusak bagian dalam buah dengan memakan jaringan kulit bagian dalam, plasenta, dan biji kakao. Akibatnya, buah mengalami kematangan prematur yang tidak merata, berbobot ringan, dan bijinya saling melekat keras.",
            "pencegahan": "Terapkan teknik sarungisasi (membungkus buah muda ukuran 8-10 cm dengan kantong plastik bening), lakukan panen berkala setiap minggu (panen sering) untuk memutus siklus hidup hama, serta bersihkan sisa-sisa kulit buah hasil panen."
        }
    }
    return info.get(class_name, {"deskripsi": "Data tidak ditemukan.", "pencegahan": "Data tidak ditemukan."})