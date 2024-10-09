# Cara Menjalankan Projek submission

## Deskripsi
Proyek ini bertujuan untuk menganalisis data pada Bike Sharing Dataset. Tujuan akhirnya adalah untuk menghasilkan wawasan dan informasi yang berguna dari data yang dianalisis.
Salah satunya adalah clustering yang menghitung data berdasarkan sebaran kelompok. 

## Struktur Direktori
/data: Direktori ini berisi data yang digunakan dalam proyek, dalam format .csv
/dashboard: Direktori ini berisi dashboard.py yang digunakan untuk membuat dashboard hasil analisis data.
notebook.ipynb: File ini yang digunakan untuk melakukan analisis dataset.

## Setup Environtment - Shell/Terminal
```markdown
pip install -r requirements.txt
```

## Untuk menjalankan notebook.ipnyb
Anda harus memasukan file yang ada di folder data terlebih dahulu ke dalam google notebook

## Cara menjalankan program dashboard
Masuk ke dalam direktori /dashboard dan jalankan streamlit

```markdown
cd submission/dashboard/
streamlit run dashboard.py
```