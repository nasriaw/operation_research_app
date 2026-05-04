# Aplikasi Python Untuk Masalah Operation Research

Aplikasi web interaktif untuk menyelesaikan berbagai masalah Operation Research menggunakan Python dan Streamlit.

## 🎯 Fitur Utama

### 1. Linear Programming Solver
- Menyelesaikan masalah LP (Maksimasi/Minimasi)
- Support input manual atau upload file
- Visualisasi hasil optimal dengan grafik
- Analisis variabel keputusan

### 2. Integer Programming Solver
- Optimasi dengan variabel bilangan bulat (0-1 atau integer)
- Support binary dan integer variables
- Branch and bound algorithm
- Visualisasi solusi optimal

### 3. Transportation Problem Solver
- Optimasi distribusi dari sumber ke tujuan
- Biaya minimal dengan kendala supply-demand
- Visualisasi heatmap alokasi
- Detail supply dan demand

### 4. Assignment Problem Solver
- Alokasi optimal sumber daya ke tugas
- Hungarian Algorithm untuk solusi optimal
- Visualisasi cost distribution
- Detail assignment untuk setiap pekerja-tugas

### 5. Shortest Path Problem Solver
- Menemukan rute terpendek dalam jaringan
- Support berbagai jenis graf
- Dijkstra Algorithm
- Visualisasi path

### 6. Teori Antrian (Queue Theory)
- Analisis sistem antrian M/M/1 dan M/M/c
- Perhitungan utilization factor, waiting time
- Probabilitas sistem kosong
- Optimasi pelayanan

### 7. Simulasi Monte Carlo
- Simulasi probabilistik untuk analisis risiko
- Support berbagai distribusi (normal, uniform, exponential)
- Confidence interval calculation
- Statistical analysis

### 8. Klasifikasi (Classification)
- Algoritma machine learning untuk klasifikasi
- Support Logistic Regression, SVM, Random Forest, KNN
- Evaluasi model dengan accuracy, precision, recall
- Confusion matrix analysis

### 9. Klaster (Clustering)
- Algoritma clustering untuk pengelompokan data
- Support K-Means, Hierarchical, DBSCAN
- Evaluasi dengan silhouette score
- Visualisasi cluster

## 🛠️ Teknologi yang Digunakan

- **Python 3.8+** - Bahasa pemrograman utama
- **Streamlit** - Framework UI web interaktif
- **PuLP** - Solver untuk linear programming
- **SciPy** - Computasi ilmiah (optimization, linear algebra)
- **Pandas** - Manipulasi dan analisis data
- **NumPy** - Operasi array dan numerik
- **Plotly** - Visualisasi data interaktif
- **Matplotlib** - Visualisasi grafik
- **Scikit-learn** - Machine learning algorithms

## 📋 Struktur Folder

```
python_solver_app/
├── main.py                  # Entry point aplikasi
├── requirements.txt         # Dependencies
├── README.md               # Dokumentasi ini
└── modules/
    ├── __init__.py
    ├── solvers.py          # Implementasi solver
    └── utils.py            # Utility functions
```

## 🚀 Cara Menggunakan

### 1. Instalasi Dependencies

```bash
cd python_solver_app
pip install -r requirements.txt
```

### 2. Menjalankan Aplikasi

```bash
streamlit run main.py
```

Aplikasi akan membuka di browser pada `http://localhost:8501`

### 3. Menggunakan Solver

#### Linear Programming
1. Pilih "Linear Programming" dari sidebar
2. Tentukan jumlah variabel dan kendala
3. Input koefisien fungsi objektif
4. Input koefisien kendala dan RHS
5. Klik "Selesaikan"

#### Transportation Problem
1. Pilih "Transportation Problem" dari sidebar
2. Input jumlah sumber dan tujuan
3. Input supply untuk setiap sumber
4. Input cost matrix
5. Input demand untuk setiap tujuan
6. Klik "Selesaikan"

#### Assignment Problem
1. Pilih "Assignment Problem" dari sidebar
2. Tentukan ukuran problem (n×n)
3. Input cost matrix
4. Klik "Selesaikan"

## 📊 Output dan Hasil

Setiap solver menghasilkan:
- ✅ Status optimasi
- 📈 Nilai optimal
- 📊 Detail variabel/alokasi
- 📉 Visualisasi grafik
- 📥 Option untuk export hasil

## 💡 Contoh Kasus

### Linear Programming - Produksi Mebel
```
Maksimalkan: 800x₁ + 600x₂
Kendala:
  2x₁ + 3x₂ ≤ 60 (Kayu Jati)
  5x₁ + 3x₂ ≤ 100 (Jam Kerja)
  x₁, x₂ ≥ 0
```

### Transportation Problem - Distribusi Barang
```
Supply: [100, 150, 120]
Demand: [80, 90, 100]
Minimize total cost dengan matriks biaya yang diberikan
```

### Assignment Problem - Alokasi Pekerjaan
```
Assign 4 pekerja ke 4 tugas
Minimize total biaya assignment
```

## 🔧 Pengembangan Lebih Lanjut

Fitur yang dapat ditambahkan:
- [ ] Integer Programming
- [ ] Network Flow Problem
- [ ] Goal Programming
- [ ] Quadratic Programming
- [ ] Export ke format lain (PDF, JSON)
- [ ] Database untuk menyimpan hasil
- [ ] Multi-language support
- [ ] API REST
- [ ] Import dari Excel template

## 📚 Referensi

- Linear Programming: Simplex Method, Interior Point Method
- Transportation: Vogel's Approximation Method (VAM), Stepping Stone
- Assignment: Hungarian Algorithm (Kuhn-Munkres)
- Shortest Path: Dijkstra Algorithm, Bellman-Ford Algorithm

## 🐛 Troubleshooting

### Error: Module not found
```bash
pip install -r requirements.txt
```

### Error: Streamlit not responding
- Pastikan port 8501 tidak terpakai
- Coba dengan port berbeda: `streamlit run main.py --server.port 8502`

### Hasil Infeasible
- Cek constraint, mungkin ada konflik antar kendala
- Pastikan supply = demand untuk transportation problem

## 📝 License

Aplikasi ini dikembangkan untuk tujuan pendidikan dan penelitian.

## 👨‍💻 Developer

Dikembangkan sebagai alat bantu pembelajaran Operation Research dengan Python.

---

**Versi:** 1.0.0  
**Last Updated:** 2026  
**Status:** Active Development
