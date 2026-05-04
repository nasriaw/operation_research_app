# Quick Start Guide - Aplikasi Python Untuk Masalah Operation Research

## ⚡ Quick Start (5 Menit)

### Step 1: Clone/Download Repository
```bash
cd python_solver_app
```

### Step 2: Install Dependencies (Linux/Mac)
```bash
chmod +x run.sh
./run.sh
```

### Step 2: Install Dependencies (Windows)
```bash
run.bat
```

### Step 3: Akses Aplikasi
Buka browser dan kunjungi: **http://localhost:8501**

---

## 🎯 Panduan Penggunaan Per Solver

### Linear Programming

**Kasus:** Produksi Mebel

Seorang pengusaha mebel ingin memaksimalkan keuntungan dari produksi meja dan kursi.

**Input:**
```
Maksimalkan: 800 * Meja + 600 * Kursi

Kendala:
- Kayu Jati: 2 * Meja + 3 * Kursi ≤ 60 unit
- Jam Kerja: 5 * Meja + 3 * Kursi ≤ 100 jam
- Meja ≥ 0, Kursi ≥ 0
```

**Steps:**
1. Pilih "Linear Programming"
2. Tipe: Maksimasi
3. Variabel: 2 (Meja, Kursi)
4. Kendala: 2
5. Input koefisien: [800, 600]
6. Constraint 1: [2, 3] ≤ 60
7. Constraint 2: [5, 3] ≤ 100
8. Click "Selesaikan"

**Hasil Diharapkan:**
```
Optimal Value: ~4400
Meja: ~20 unit
Kursi: ~6.67 unit
```

---

### Transportation Problem

**Kasus:** Distribusi Barang dari 3 Pabrik ke 3 Toko

**Input:**
```
Supply (Pabrik):
- Pabrik 1: 100 unit
- Pabrik 2: 150 unit
- Pabrik 3: 120 unit

Demand (Toko):
- Toko A: 80 unit
- Toko B: 90 unit
- Toko C: 100 unit

Cost Matrix (Biaya per unit):
         Toko A  Toko B  Toko C
Pabrik 1:  4      6       8
Pabrik 2:  5      4       7
Pabrik 3:  6      5       4
```

**Steps:**
1. Pilih "Transportation Problem"
2. Sumber: 3, Tujuan: 3
3. Input Supply: [100, 150, 120]
4. Input Cost Matrix
5. Input Demand: [80, 90, 100]
6. Click "Selesaikan"

**Output:**
- Allocation matrix menunjukkan berapa unit dikirim
- Total cost minimal

---

### Assignment Problem

**Kasus:** 4 Pekerja ke 4 Tugas

**Input:**
```
Cost Matrix (jam kerja yang dibutuhkan):
        Tugas 1  Tugas 2  Tugas 3  Tugas 4
Worker 1:  10      19       8       15
Worker 2:  10      18       7       17
Worker 3:  13      16       9       14
Worker 4:  12      19       8       18
```

**Steps:**
1. Pilih "Assignment Problem"
2. Size: 4x4
3. Input Cost Matrix
4. Click "Selesaikan"

**Hasil:**
```
Worker 1 → Task 3: 8 jam
Worker 2 → Task 1: 10 jam
Worker 3 → Task 4: 14 jam
Worker 4 → Task 2: 19 jam
Total: 51 jam
```

---

## 📊 Tips & Tricks

### 1. Validasi Data Sebelum Submit
- Total Supply = Total Demand (untuk Transportation)
- Matrix bersifat square (untuk Assignment)
- Tidak ada nilai negatif

### 2. Interpretasi Hasil
- **Status**: Optimal = solusi terbaik ditemukan
- **Optimal Value**: Nilai objektif fungsi (max/min)
- **Variables**: Nilai setiap variabel keputusan

### 3. Export Hasil
Klik tombol download untuk export ke Excel/CSV

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| App tidak jalan | Pastikan Python 3.8+ installed |
| Dependencies error | Run `pip install -r requirements.txt` |
| Port 8501 sudah dipakai | `streamlit run main.py --server.port 8502` |
| Hasil Infeasible | Check constraint, mungkin ada konflik |
| Slow performance | Kurangi ukuran problem |

---

## 📚 Rumus & Algoritma

### Linear Programming (Simplex Method)
Minimize: c^T * x
Subject to: A*x ≤ b, x ≥ 0

### Transportation (Vogel's Approximation)
Minimize: Σ (cost[i][j] * x[i][j])
Supply = Demand

### Assignment (Hungarian Algorithm)
Minimize: Σ cost[i][pi(i)]
One-to-one matching

---

## 🔗 Useful Resources

- [PuLP Documentation](https://coin-or.github.io/pulp/)
- [SciPy Optimize](https://docs.scipy.org/doc/scipy/reference/optimize.html)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Operation Research](https://en.wikipedia.org/wiki/Operations_research)

---

## ⚙️ Configuration

### Mengubah Port Default
Edit di `main.py` atau run dengan:
```bash
streamlit run main.py --server.port 8502
```

### Mengubah Theme
Tambahkan `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f8f9fa"
textColor = "#000000"
font = "sans serif"
```

---

## 💡 Contoh Skenario Real-World

### 1. Plant Production Optimization
Maksimalkan profit dari produksi multi-produk dengan keterbatasan resources

### 2. Supply Chain Network
Minimalisir total transportation cost dari warehouse ke retail store

### 3. Workforce Scheduling
Assign worker ke shift dengan mempertimbangkan skill dan availability

### 4. Network Routing
Find optimal route dari data center ke users dengan minimum latency

---

## 📞 Support

- 📧 Email: support@orsolver.local
- 🐛 Issues: Report di platform development
- 📖 Documentation: Lihat folder `/docs`

---

**Happy Solving! 🎉**
