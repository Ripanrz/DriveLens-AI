# 🔍 DriveLens AI - Pencari Wajah Otomatis Terintegrasi Google Drive

[![Live Demo on Hugging Face](https://img.shields.io/badge/Live%20Demo-%F0%9F%A4%97%20Hugging%20Face-blue?style=for-the-badge)](https://huggingface.co/spaces/Ripanrz/drivelens-ai)

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![DeepFace](https://img.shields.io/badge/Model-Facenet_&_DeepFace-orange)
![Computer Vision](https://img.shields.io/badge/Library-OpenCV-green)
![Gradio](https://img.shields.io/badge/UI-Gradio-lightgrey)
![Hugging Face](https://img.shields.io/badge/Deployment-Hugging_Face_Spaces-purple)

**Pernahkah Anda merasa lelah men-scroll ratusan hingga ribuan foto dokumentasi acara di Google Drive hanya untuk mencari di mana foto Anda berada?** **DriveLens AI** dibangun khusus untuk memecahkan masalah tersebut. Proyek ini mengotomatisasi proses pencarian foto wajah kita di antara tumpukan dokumentasi acara yang masif. Menggunakan pendekatan **Computer Vision** dan **One-Shot Learning**, sistem ini mengekstrak representasi fitur wajah (*embeddings*) dari satu foto referensi pengguna, lalu mengukur tingkat kemiripannya dengan seluruh gambar di dalam folder Drive tujuan dalam hitungan detik.

---

## 📸 Tampilan Dashboard

> *Aplikasi web interaktif dengan antarmuka yang bersih, di-deploy secara live di ekosistem Hugging Face.*

![Tampilan Dashboard](DriveLensAI/Dashboard_PencarianWajah.png)

---

## 🚀 Fitur Utama

* **Zero-Shot Face Matching**: Tidak memerlukan proses *training* model dari awal. Cukup unggah 1 foto referensi (Ground Truth), AI akan langsung mendeteksi dan mencari wajah Anda di tumpukan ratusan foto kegiatan.
* **Integrasi Cloud Langsung**: Menggunakan utilitas `gdown` untuk menarik data dari folder publik Google Drive secara otomatis di latar belakang tanpa membebani memori lokal pengguna.
* **Arsitektur Model Andal**: Memanfaatkan model **Facenet** untuk ekstraksi fitur (*embedding*) dan metrik perhitungan **Cosine Similarity** guna memastikan tingkat akurasi pencocokan yang tinggi.
* **Manajemen Ruang Penyimpanan Cerdas (Auto-Cleanup)**: Sistem *backend* dirancang untuk secara otomatis membuat dan menghapus direktori sementara (temporary folder) setiap kali satu sesi pencarian selesai, mencegah terjadinya *server overload* atau *storage full*.

---

## 🔁 Arsitektur Sistem (Data Pipeline)

```mermaid
graph LR
    A[Input UI] -->|Foto Referensi & URL Drive| B(Data Ingestion)
    B -->|gdown Download| C{Face Detection & Embedding}
    C -->|Model Facenet| D[Similarity Measurement]
    D -->|Cosine Distance Threshold| E(Filtering & Matching)
    E -->|Render UI| F[Tampilkan Galeri Foto]
    F -->|System Cleanup| G[Hapus Direktori Sementara]
