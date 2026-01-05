# Analisis data Air Quality China
## 📌 Deskripsi Proyek
Proyek ini adalah **Air Quality Analysis Dashboard** berbasis **Streamlit** untuk menganalisis data kualitas udara (PM2.5) dari beberapa stasiun pengukuran.  
Dashboard memungkinkan pengguna untuk:  
- Memilih stasiun pengukuran tertentu.  
- Melihat **tren bulanan PM2.5** per stasiun.  
- Mengidentifikasi **bulan dan jam dengan kualitas udara terburuk**.  
- Menampilkan **metrik penting** seperti PM2.5, CO, DEWP, dan WSPM pada jam terburuk.  
- Memberikan **insight singkat** mengenai pola polusi udara.

## 📂 Dataset
- File: `main_data.csv`  
- Kolom penting:
  - `station` : Nama stasiun  
  - `year`, `month`, `day`, `hour` : Waktu pengukuran  
  - `PM2.5`, `CO`, `DEWP`, `WSPM` : Data kualitas udara
Data ini sudah dibersihkan dan siap untuk dianalisis.

## ⚙️ Cara Menjalankan
1. Install dependencies:  
```bash
pip install -r requirements.txt
```
2. Jalankan aplikasi
```bash
streamlit run app.py
```
3. Gunakan sidebar untuk memilih stasiun.
4. Dashboard menampilkan Tren bulanan PM2.5, Grafik PM2.5 per jam di bulan terburuk, Metrik jam terburuk (PM2.5, CO, DEWP, WSPM), dan Insight singkat terkait polusi.
