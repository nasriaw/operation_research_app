"""
Contoh Penggunaan Solver untuk Assignment Problem

File ini menunjukkan cara menggunakan Assignment Solver
"""

from modules.solvers import assignment_problem_solver
import pandas as pd

# ==================== CONTOH 1: ALOKASI PEKERJAAN ====================
print("=" * 70)
print("CONTOH 1: ALOKASI 4 PEKERJA KE 4 TUGAS")
print("=" * 70)

cost_matrix = [
    [10, 19, 8, 15],   # Pekerja 1 ke tugas 1,2,3,4
    [10, 18, 7, 17],   # Pekerja 2
    [13, 16, 9, 14],   # Pekerja 3
    [12, 19, 8, 18]    # Pekerja 4
]

result = assignment_problem_solver(cost_matrix)

print(f"\nStatus: {result['status']}")
print(f"Total Biaya Minimal: {result['total_cost']:.2f} jam")

print("\nAlokasi Optimal:")
print("-" * 50)
total = 0
for (worker, task), cost in zip(result['assignment'], result['assignment_cost']):
    print(f"Pekerja {worker+1} → Tugas {task+1}: {cost:.2f} jam")
    total += cost

print("-" * 50)
print(f"Total: {total:.2f} jam")

# ==================== CONTOH 2: MATCHING DOKTER-PASIEN ====================
print("\n" + "=" * 70)
print("CONTOH 2: MATCHING 5 DOKTER KE 5 PASIEN")
print("=" * 70)

cost_matrix = [
    [5, 8, 12, 9, 11],    # Dokter 1: compatibility score
    [7, 4, 10, 8, 9],     # Dokter 2
    [10, 6, 8, 7, 12],    # Dokter 3
    [8, 9, 7, 6, 10],     # Dokter 4
    [9, 7, 11, 8, 5]      # Dokter 5
]

result = assignment_problem_solver(cost_matrix)

print(f"\nStatus: {result['status']}")
print(f"Total Compatibility Score: {result['total_cost']:.2f}")

print("\nMatching Optimal (Minimal mismatch):")
print("-" * 50)
assignment_list = []
for (doctor, patient), score in zip(result['assignment'], result['assignment_cost']):
    print(f"Dokter {doctor+1} ← → Pasien {patient+1} (Score: {score:.2f})")
    assignment_list.append({
        'Dokter': f"Dr-{doctor+1}",
        'Pasien': f"P-{patient+1}",
        'Score': score
    })

df_assignment = pd.DataFrame(assignment_list)
print("\n")
print(df_assignment.to_string(index=False))

# ==================== CONTOH 3: DELIVERY ROUTE OPTIMIZATION ====================
print("\n" + "=" * 70)
print("CONTOH 3: OPTIMASI RUTE KURIR (6 Kurir ke 6 Zona Pengiriman)")
print("=" * 70)

# Cost = waktu perjalanan (menit)
cost_matrix = [
    [15, 22, 30, 18, 25, 20],   # Kurir 1
    [20, 18, 25, 22, 28, 23],   # Kurir 2
    [25, 28, 20, 30, 22, 21],   # Kurir 3
    [18, 24, 28, 15, 26, 25],   # Kurir 4
    [22, 20, 23, 27, 18, 24],   # Kurir 5
    [19, 25, 22, 24, 23, 16]    # Kurir 6
]

result = assignment_problem_solver(cost_matrix)

print(f"\nStatus: {result['status']}")
print(f"Total Waktu Perjalanan Minimal: {result['total_cost']:.2f} menit")

print("\nAlokasi Rute Optimal:")
print("-" * 50)
assignment_list = []
for (courier, zone), time in zip(result['assignment'], result['assignment_cost']):
    print(f"Kurir {courier+1} → Zona {zone+1}: {time:.0f} menit")
    assignment_list.append({
        'Kurir': f"K-{courier+1}",
        'Zona': f"Z-{zone+1}",
        'Waktu (menit)': int(time)
    })

df_assignment = pd.DataFrame(assignment_list)
print("\n")
print(df_assignment.to_string(index=False))

# ==================== CONTOH 4: TOURNAMENT SEEDING ====================
print("\n" + "=" * 70)
print("CONTOH 4: SEEDING TURNAMEN (Minimasi Pertemuan Rival)")
print("=" * 70)

# Cost = score jika kedua tim bertemu (semakin tinggi semakin buruk matchup)
cost_matrix = [
    [0, 10, 8, 7, 9],      # Tim A (ingin hindari)
    [10, 0, 6, 9, 8],      # Tim B
    [8, 6, 0, 10, 7],      # Tim C
    [7, 9, 10, 0, 6],      # Tim D
    [9, 8, 7, 6, 0]        # Tim E
]

result = assignment_problem_solver(cost_matrix)

print(f"\nStatus: {result['status']}")
print(f"Total 'Badness' Score Minimal: {result['total_cost']:.2f}")

print("\nPairing Optimal (Least controversial):")
print("-" * 50)
for (i, j), score in zip(result['assignment'], result['assignment_cost']):
    teams = ['A', 'B', 'C', 'D', 'E']
    print(f"Tim {teams[i]} vs Tim {teams[j]} (Conflict Score: {score:.0f})")

print("\n" + "=" * 70)
print("Selesai!")
print("=" * 70)
