"""
Contoh Penggunaan Solver untuk Linear Programming

File ini menunjukkan cara menggunakan LP Solver tanpa Streamlit UI
"""

from modules.solvers import linear_programming_solver
from modules.utils import format_number

# ==================== CONTOH 1: PRODUKSI MEBEL ====================
print("=" * 60)
print("CONTOH 1: PRODUKSI MEBEL")
print("=" * 60)

# Problem:
# Maksimalkan keuntungan dari produksi meja dan kursi
# Maximize: 800*x1 + 600*x2
# Subject to:
#   2*x1 + 3*x2 <= 60  (Kayu Jati dalam unit)
#   5*x1 + 3*x2 <= 100 (Jam Kerja)
#   x1, x2 >= 0

result = linear_programming_solver(
    obj_coeffs=[800, 600],
    constraint_matrix=[[2, 3], [5, 3]],
    constraint_bounds=[60, 100],
    constraint_types=['<=', '<='],
    prob_type='MAX'
)

print(f"\nStatus: {result['status']}")
print(f"Optimal Value: Rp {format_number(result['optimal_value'])}")
print(f"\nNilai Variabel Optimal:")
for var, value in result['variables'].items():
    print(f"  {var} = {format_number(value)}")

# ==================== CONTOH 2: DIET PROBLEM ====================
print("\n" + "=" * 60)
print("CONTOH 2: DIET PROBLEM")
print("=" * 60)

# Problem:
# Minimalisir biaya diet dengan nutrisi minimal terpenuhi
# Minimize: 3*x1 + 2.5*x2
# Subject to:
#   5*x1 + 10*x2 >= 50  (Protein minimal 50g)
#   4*x1 + 3*x2 >= 60   (Carbs minimal 60g)
#   x1, x2 >= 0

result = linear_programming_solver(
    obj_coeffs=[3, 2.5],
    constraint_matrix=[[5, 10], [4, 3]],
    constraint_bounds=[50, 60],
    constraint_types=['>=', '>='],
    prob_type='MIN'
)

print(f"\nStatus: {result['status']}")
print(f"Minimal Cost: Rp {format_number(result['optimal_value'])}")
print(f"\nNilai Variabel Optimal:")
for var, value in result['variables'].items():
    print(f"  {var} = {format_number(value)}")

# ==================== CONTOH 3: INVENTORY PROBLEM ====================
print("\n" + "=" * 60)
print("CONTOH 3: INVENTORY OPTIMIZATION")
print("=" * 60)

# Problem dengan 3 variabel dan 3 kendala
# Maximize: 50*x1 + 40*x2 + 60*x3
# Subject to:
#   x1 + x2 + x3 <= 100     (Kapasitas warehouse)
#   2*x1 + x2 + 3*x3 <= 200 (Budget untuk pembelian)
#   x1 + 2*x2 + x3 <= 80    (Ruang display)

result = linear_programming_solver(
    obj_coeffs=[50, 40, 60],
    constraint_matrix=[[1, 1, 1], [2, 1, 3], [1, 2, 1]],
    constraint_bounds=[100, 200, 80],
    constraint_types=['<=', '<=', '<='],
    prob_type='MAX'
)

print(f"\nStatus: {result['status']}")
print(f"Maximum Profit: Rp {format_number(result['optimal_value'])}")
print(f"\nNilai Variabel Optimal:")
for var, value in result['variables'].items():
    print(f"  {var} = {format_number(value)}")

print("\n" + "=" * 60)
print("Selesai!")
print("=" * 60)
