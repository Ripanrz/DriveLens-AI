import gradio as gr
import gdown
import os
import shutil
from deepface import DeepFace

def cari_wajah(foto_referensi, link_drive):
    # 1. Siapkan folder sementara (hapus yang lama jika ada agar server tidak penuh)
    folder_sementara = "./temp_kegiatan"
    if os.path.exists(folder_sementara):
        shutil.rmtree(folder_sementara)
    os.makedirs(folder_sementara)
    
    # 2. Unduh folder dari Google Drive
    try:
        gdown.download_folder(link_drive, output=folder_sementara, quiet=False, use_cookies=False)
    except Exception as e:
        return f"Gagal mengunduh folder Drive. Pastikan link valid dan aksesnya 'Anyone with the link'. Error: {e}", []

    # 3. Proses pencocokan dengan DeepFace
    try:
        hasil_pencarian = DeepFace.find(
            img_path=foto_referensi, 
            db_path=folder_sementara, 
            model_name="Facenet", 
            distance_metric="cosine", 
            enforce_detection=False
        )
        
        df_hasil = hasil_pencarian[0]
        
        if len(df_hasil) == 0:
            return "Pencarian selesai, tapi tidak ada wajah yang cocok ditemukan.", []
            
        # Ambil daftar lokasi file foto yang cocok
        foto_cocok = df_hasil['identity'].tolist()
        pesan = f"✅ Selesai! Ditemukan {len(foto_cocok)} foto Anda."
        
        return pesan, foto_cocok

    except Exception as e:
        return f"Terjadi kesalahan saat memproses AI: {e}", []

# --- CSS KUSTOM UNTUK MEMAKSA SIMETRIS ---
css_kustom = """
.force-row { flex-wrap: nowrap !important; }
"""

# --- MEMBUAT TAMPILAN WEBSITE (UI) DENGAN GRADIO ---
with gr.Blocks(theme=gr.themes.Soft(), css=css_kustom) as web_app:
    gr.Markdown("# 🔍 DriveLens AI - Pencari Wajah Otomatis")
    gr.Markdown("Unggah foto wajah Anda, masukkan link folder Google Drive kegiatan, dan biarkan AI mencari foto Anda!")
    
    # Menggunakan equal_height dan mematikan auto-wrap (force-row)
    with gr.Row(equal_height=True, elem_classes="force-row"):
        
        # --- KOLOM KIRI (INPUT) ---
        with gr.Column(scale=1, min_width=300):
            # height=300 memastikan foto selalu compact dan tidak memanjang ke bawah
            input_foto = gr.Image(type="filepath", label="1. Unggah Foto Wajah Anda (Referensi)", height=300)
            input_link = gr.Textbox(label="2. Link Folder Google Drive (Pastikan aksesnya Public)", placeholder="https://drive.google.com/drive/folders/...")
            tombol_cari = gr.Button("Cari Foto Saya! 🚀", variant="primary")
            
        # --- KOLOM KANAN (OUTPUT) ---
        with gr.Column(scale=1, min_width=300):
            output_teks = gr.Textbox(label="Status Pencarian", interactive=False)
            # height=400 disetel agar batas bawah galeri sejajar dengan batas bawah tombol di kiri
            output_galeri = gr.Gallery(label="Hasil Foto Anda", columns=2, object_fit="contain", height=400)
            
    # Menghubungkan tombol dengan fungsi AI
    tombol_cari.click(
        fn=cari_wajah,
        inputs=[input_foto, input_link],
        outputs=[output_teks, output_galeri]
    )

# Jalankan aplikasi
if __name__ == "__main__":
    web_app.launch()
