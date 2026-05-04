"""
Contoh Penggunaan Solver untuk Transportation Problem

File ini menunjukkan cara menggunakan Transportation Solver
"""

from modules.solvers import transportation_problem_solver
import pandas as pd

# ==================== CONTOH 1: DISTRIBUSI BARANG ====================
print("=" * 70)
print("CONTOH 1: DISTRIBUSI BARANG (3 Pabrik ke 3 Toko)")
print("=" * 70)

supply = [100, 150, 120]
demand = [80, 90, 100]
cost_matrix = [
    [4, 6, 8],
    [5, 4, 7],
    [6, 5, 4]
]

result = transportation_problem_solver(supply, demand, cost_matrix)

print(f"\nStatus: {result['status']}")
print(f"Total Cost Minimal: Rp {result['total_cost']}")

# Tampilkan allocation matrix
print("\nMatriks Alokasi (Unit):")
allocation_df = pd.DataFrame(
    result['allocation'],
    columns=[f'Toko {j+1}' for j in range(result['num_destinations'])],
    index=[f'Pabrik {i+1}' for i in range(result['num_sources'])]
)
print(allocation_df)

# Detail supply dan demand
print("\nSupply & Demand:")
print(f"Total Supply: {sum(result['supply'])}")
print(f"Total Demand: {sum(result['demand'])}")

# ==================== CONTOH 2: JARINGAN DISTRIBUSI BESAR ====================
print("\n" + "=" * 70)
print("CONTOH 2: JARINGAN DISTRIBUSI (4 Warehouse ke 5 Toko)")
print("=" * 70)

supply = [150, 200, 180, 170]
demand = [100, 120, 110, 90, 90]
cost_matrix = [
    [2, 3, 4, 5, 6],
    [3, 2, 5, 4, 5],
    [4, 5, 2, 3, 4],
    [5, 4, 3, 2, 3]
]

result = transportation_problem_solver(supply, demand, cost_matrix)

print(f"\nStatus: {result['status']}")
print(f"Total Cost Minimal: Rp {result['total_cost']}")

# Tampilkan allocation matrix
print("\nMatriks Alokasi (Unit):")
allocation_df = pd.DataFrame(
    result['allocation'],
    columns=[f'Toko {j+1}' for j in range(result['num_destinations'])],
    index=[f'Warehouse {i+1}' for i in range(result['num_sources'])]
)
print(allocation_df)

# ==================== CONTOH 3: COAL SUPPLY ====================
print("\n" + "=" * 70)
print("CONTOH 3: SUPPLY BATU BARA (3 Tambang ke 4 Pembangkit Listrik)")
print("=" * 70)

supply = [200, 300, 250]  # Kapasitas tambang (ton)
demand = [150, 200, 180, 220]  # Kebutuhan pembangkit (ton)
cost_matrix = [  # Biaya transportasi per ton
    [15, 18, 22, 25],
    [12, 20, 16, 24],
    [18, 15, 20, 22]
]

result = transportation_problem_solver(supply, demand, cost_matrix)

print(f"\nStatus: {result['status']}")
print(f"Total Biaya Transportasi: Rp {result['total_cost']:.2f}")

# Tampilkan allocation matrix
print("\nMatriks Alokasi (Ton Batu Bara):")
allocation_df = pd.DataFrame(
    result['allocation'],
    columns=[f'Pembangkit {j+1}' for j in range(result['num_destinations'])],
    index=[f'Tambang {i+1}' for i in range(result['num_sources'])]
)
print(allocation_df)

print("\n" + "=" * 70)
print("Selesai!")
print("=" * 70)
