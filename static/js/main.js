document.addEventListener('DOMContentLoaded', function () {
    const dropArea = document.getElementById('dropArea');
    const fileInput = document.getElementById('fileInput');
    const previewContainer = document.getElementById('previewContainer');
    const imagePreview = document.getElementById('imagePreview');
    const fileName = document.getElementById('fileName');
    const predictionForm = document.getElementById('predictionForm');
    const loadingOverlay = document.getElementById('loadingOverlay');

    // Memicu jendela dialog pemilih file
    window.triggerFileInput = function () {
        fileInput.click();
    };

    if (fileInput) {
        fileInput.addEventListener('change', function () {
            validateAndPreviewFiles(this.files);
        });
    }

    // Mengelola Event Drag and Drop
    if (dropArea) {
        ['dragenter', 'dragover'].forEach(eventName => {
            dropArea.addEventListener(eventName, (e) => {
                e.preventDefault();
                dropArea.classList.add('dragover');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, (e) => {
                e.preventDefault();
                dropArea.classList.remove('dragover');
            }, false);
        });

        dropArea.addEventListener('drop', (e) => {
            e.preventDefault();
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files; // Sinkronkan ke input form
                validateAndPreviewFiles(files);
            }
        }, false);
    }

    // Fungsi Validasi Tipe File & Memunculkan Pratinjau (Preview)
    function validateAndPreviewFiles(files) {
        if (files.length > 0) {
            const file = files[0];
            const allowedTypes = ['image/jpeg', 'image/png', 'image/jpg'];

            // 1. Validasi Ekstensi File
            if (!allowedTypes.includes(file.type)) {
                alert('Format salah! Mohon pilih file gambar berformat JPG, JPEG, atau PNG.');
                resetFileSelection();
                return;
            }

            // 2. Validasi Ukuran Maksimum File (5MB)
            if (file.size > 5 * 1024 * 1024) {
                alert('Ukuran file terlalu besar! Batas maksimum adalah 5MB.');
                resetFileSelection();
                return;
            }

            // 3. Render Pratinjau menggunakan FileReader
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onloadend = function () {
                imagePreview.src = reader.result;
                fileName.textContent = file.name;
                previewContainer.style.display = 'block';
            };
        }
    }

    // Fungsi Menghapus Pilihan Gambar
    window.resetFileSelection = function () {
        if (fileInput) fileInput.value = '';
        if (imagePreview) imagePreview.src = '';
        if (fileName) fileName.textContent = '';
        if (previewContainer) previewContainer.style.display = 'none';
    };

    // Memunculkan Loading Spinner full screen ketika tombol "Prediksi Sekarang" ditekan
    if (predictionForm) {
        predictionForm.addEventListener('submit', function () {
            if (fileInput.files.length > 0 && loadingOverlay) {
                loadingOverlay.style.display = 'flex';
            }
        });
    }
});