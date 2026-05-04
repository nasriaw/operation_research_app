# Dokumentasi API - Aplikasi Python Untuk Masalah Operation Research

## Overview

Module `solvers.py` menyediakan fungsi-fungsi untuk menyelesaikan berbagai masalah Operation Research.

## API Reference

### Linear Programming Solver

```python
from modules.solvers import linear_programming_solver

result = linear_programming_solver(
    obj_coeffs=[5, 4],
    constraint_matrix=[[2, 3], [5, 3]],
    constraint_bounds=[60, 100],
    constraint_types=['<=', '<='],
    prob_type='MAX'
)
```

**Parameters:**
- `obj_coeffs` (list): Koefisien fungsi objektif
- `constraint_matrix` (list of lists): Matriks kendala (m × n)
- `constraint_bounds` (list): RHS dari setiap kendala
- `constraint_types` (list): Tipe kendala ('<=', '=', '>=')
- `prob_type` (str): 'MAX' untuk maksimasi, 'MIN' untuk minimasi

**Returns:**
```python
{
    'status': 'Optimal',
    'optimal_value': 4400.0,
    'variables': {'x1': 20.0, 'x2': 6.67},
    'problem_type': 'MAX',
    'num_variables': 2,
    'num_constraints': 2
}
```

---

### Transportation Problem Solver

```python
from modules.solvers import transportation_problem_solver

result = transportation_problem_solver(
    supply=[100, 150, 120],
    demand=[80, 90, 100],
    cost_matrix=[
        [4, 6, 8],
        [5, 4, 7],
        [6, 5, 4]
    ]
)
```

**Parameters:**
- `supply` (list): Supply di setiap sumber
- `demand` (list): Demand di setiap tujuan
- `cost_matrix` (list of lists): Matriks biaya transportasi

**Returns:**
```python
{
    'status': 'Optimal',
    'total_cost': 1045.0,
    'allocation': [[80, 0, 20], [0, 90, 60], [0, 0, 120]],
    'num_sources': 3,
    'num_destinations': 3,
    'supply': [100, 150, 120],
    'demand': [80, 90, 100]
}
```

---

### Assignment Problem Solver

```python
from modules.solvers import assignment_problem_solver

result = assignment_problem_solver(
    cost_matrix=[
        [10, 19, 8, 15],
        [10, 18, 7, 17],
        [13, 16, 9, 14],
        [12, 19, 8, 18]
    ]
)
```

**Parameters:**
- `cost_matrix` (list of lists): Matriks biaya (n × n)

**Returns:**
```python
{
    'status': 'Optimal',
    'total_cost': 35.0,
    'assignment': [[0, 2], [1, 0], [2, 3], [3, 1]],
    'assignment_cost': [8.0, 10.0, 14.0, 19.0],
    'matrix_size': 4
}
```

---

### Shortest Path Solver

```python
from modules.solvers import shortest_path_solver

graph = {
    'A': [('B', 4), ('C', 2)],
    'B': [('C', 1), ('D', 5)],
    'C': [('D', 8), ('E', 10)],
    'D': [('E', 2)],
    'E': []
}

result = shortest_path_solver(
    graph=graph,
    start='A',
    end='E'
)
```

**Parameters:**
- `graph` (dict): Adjacency list representation
- `start`: Node awal
- `end`: Node tujuan

**Returns:**
```python
{
    'status': 'Found',
    'path': ['A', 'C', 'D', 'E'],
    'distance': 12.0,
    'start': 'A',
    'end': 'E'
}
```

---

## Utility Functions

### Display Results

```python
from modules.utils import display_results

display_results(result, 'Linear Programming')
```

### Export Results

```python
from modules.utils import export_results

# Export to Excel
excel_data = export_results(result, 'excel')

# Export to CSV
csv_data = export_results(result, 'csv')

# Export to JSON
json_data = export_results(result, 'json')
```

### Validate Input

```python
from modules.utils import validate_input

is_valid, message = validate_input(
    supply=[100, 150],
    demand=[80, 170],
    cost_matrix=[[5, 4], [6, 3]]
)

if is_valid:
    print("✓ Input valid")
else:
    print(f"Error: {message}")
```

---

## Error Handling

Setiap solver dapat throw exception. Tangani dengan try-except:

```python
try:
    result = linear_programming_solver(
        obj_coeffs=[5, 4],
        constraint_matrix=[[2, 3]],
        constraint_bounds=[60],
        constraint_types=['<='],
        prob_type='MAX'
    )
except Exception as e:
    print(f"Error: {str(e)}")
```

---

## Examples

### Contoh 1: Produksi Mebel

```python
from modules.solvers import linear_programming_solver

# Maximize: 800*x1 + 600*x2
# Subject to:
# 2*x1 + 3*x2 <= 60
# 5*x1 + 3*x2 <= 100
# x1, x2 >= 0

result = linear_programming_solver(
    obj_coeffs=[800, 600],
    constraint_matrix=[[2, 3], [5, 3]],
    constraint_bounds=[60, 100],
    constraint_types=['<=', '<='],
    prob_type='MAX'
)

print(f"Optimal Value: {result['optimal_value']}")
print(f"Variables: {result['variables']}")
```

### Contoh 2: Distribusi Barang

```python
from modules.solvers import transportation_problem_solver

result = transportation_problem_solver(
    supply=[100, 150, 120],
    demand=[80, 90, 100],
    cost_matrix=[
        [4, 6, 8],
        [5, 4, 7],
        [6, 5, 4]
    ]
)

print(f"Total Cost: {result['total_cost']}")
print(f"Allocation:\n{result['allocation']}")
```

### Contoh 3: Alokasi Pekerjaan

```python
from modules.solvers import assignment_problem_solver

result = assignment_problem_solver(
    cost_matrix=[
        [10, 19, 8, 15],
        [10, 18, 7, 17],
        [13, 16, 9, 14],
        [12, 19, 8, 18]
    ]
)

print(f"Total Cost: {result['total_cost']}")
for (worker, task), cost in zip(result['assignment'], result['assignment_cost']):
    print(f"Worker {worker+1} -> Task {task+1}: Cost ${cost:.2f}")
```

---

## Limitations & Notes

- ✅ Semua solver menggunakan pendekatan optimal
- ⚠️ Untuk LP besar, waktu komputasi mungkin lebih lama
- ⚠️ Transportation: Supply harus sama dengan demand
- ⚠️ Assignment: Matriks harus square (n×n)
- ℹ️ Shortest path: Tidak support negative weight

---

## Performance Tips

1. **Linear Programming**: Kurangi jumlah variabel/constraint untuk performa lebih baik
2. **Transportation**: Gunakan data normalized untuk hasil yang lebih stabil
3. **Assignment**: Performa optimal untuk n ≤ 100
4. **Shortest Path**: Efficient untuk graf dengan ribuan node

---

## Version History

- **v1.0.0** (Current) - Initial release dengan 4 solver utama

---

## Support & Issues

Untuk laporan bug atau saran fitur, hubungi development team.
