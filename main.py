"""
Aplikasi Python Untuk Masalah Operation Research
================================================
Penyusun: Ir.M Nasri AW, M.Eng.Sc, M.Kom / Dosen STIE Indonesia Malang
======================================================================
Aplikasi web interaktif untuk menyelesaikan berbagai masalah Operation Research
menggunakan Python dan Streamlit.

Author: OR Team
Version: 1.0.0
"""

import streamlit as st
import pandas as pd
import numpy as np
import math
from modules.solvers import (
    linear_programming_solver,
    transportation_problem_solver,
    assignment_problem_solver,
    shortest_path_solver,
    integer_programming_solver,
    queue_theory_solver,
    monte_carlo_simulation,
    classification_solver,
    clustering_solver,
)
from modules.utils import (
    create_lp_model,
    display_results,
    export_results,
)

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Python OR Solver - Operation Research",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .main-header .sub-header {
        font-size: 1rem;
        font-weight: 500;
        margin-top: 0.5rem;
        color: #ffffff;
    }
    .solver-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        border-left: 5px solid #667eea;
        margin: 10px 0;
    }
    .result-box {
        background-color: #e8f5e9;
        border-radius: 8px;
        padding: 15px;
        border-left: 4px solid #4caf50;
        margin: 10px 0;
    }
    .error-box {
        background-color: #ffebee;
        border-radius: 8px;
        padding: 15px;
        border-left: 4px solid #f44336;
        margin: 10px 0;
    }
    .info-box {
        background-color: #e3f2fd;
        border-radius: 8px;
        padding: 15px;
        border-left: 4px solid #2196f3;
        margin: 10px 0;
    }
    .stButton>button {
        background-color: #667eea;
        color: white;
        border-radius: 20px;
        padding: 10px 24px;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #764ba2;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE INITIALIZATION ====================
if 'solver_results' not in st.session_state:
    st.session_state.solver_results = None

# ==================== MAIN APPLICATION ====================
def main():
    # Header
    st.markdown(
        '<div class="main-header">'
        '🔧 Aplikasi Python Untuk Masalah Operation Research'
        '<div class="sub-header">Penyusun: Ir.M Nasri AW, M.Eng.Sc, M.Kom / Dosen STIEI Malang</div>'
        '</div>',
        unsafe_allow_html=True
    )
    
    st.markdown("""
    Aplikasi ini menyediakan tools untuk menyelesaikan berbagai masalah Operation Research 
    menggunakan metode optimasi yang tepat. Pilih jenis masalah yang ingin Anda selesaikan di sidebar.
    """)
    
    # ==================== SIDEBAR NAVIGATION ====================
    st.sidebar.title("📋 Menu Solver")
    solver_type = st.sidebar.radio(
        "Pilih Jenis Solver:",
        [
            "Linear Programming",
            "Integer Programming",
            "Transportation Problem",
            "Assignment Problem",
            "Shortest Path Problem",
            "Teori Antrian",
            "Simulasi Monte Carlo",
            "Klasifikasi",
            "Klaster",
            "Prediksi",
            "Churn",
            "Tentang Aplikasi"
        ],
        index=0
    )
    
    # ==================== SOLVER SELECTION ====================
    if solver_type == "Linear Programming":
        st.subheader("🎯 Linear Programming Solver")
        lp_solver_page()
        
    elif solver_type == "Integer Programming":
        st.subheader("🔢 Integer Programming Solver")
        integer_programming_page()
        
    elif solver_type == "Transportation Problem":
        st.subheader("🚚 Transportation Problem Solver")
        transportation_solver_page()
        
    elif solver_type == "Assignment Problem":
        st.subheader("👥 Assignment Problem Solver")
        assignment_solver_page()
        
    elif solver_type == "Shortest Path Problem":
        st.subheader("🛣️ Shortest Path Problem Solver")
        shortest_path_page()
        
    elif solver_type == "Teori Antrian":
        st.subheader("📋 Teori Antrian Solver")
        queue_theory_page()
        
    elif solver_type == "Simulasi Monte Carlo":
        st.subheader("🎲 Simulasi Monte Carlo")
        monte_carlo_page()
        
    elif solver_type == "Klasifikasi":
        st.subheader("📊 Klasifikasi Solver")
        classification_page()
        
    elif solver_type == "Klaster":
        st.subheader("🔗 Klaster Solver")
        clustering_page()
        
    elif solver_type == "Prediksi":
        st.subheader("📈 Prediksi Churn Pelanggan")
        prediction_page()
        
    elif solver_type == "Churn":
        st.subheader("📉 Analisis Churn Pelanggan")
        churn_page()
        
    elif solver_type == "Tentang Aplikasi":
        about_page()

# ==================== DATASET HELPERS ====================
def load_churn_dataset():
    data = [
        {'CustomerID': 1, 'Age': 23, 'MonthlySpend': 500000, 'VisitFreq': 5, 'SubscriptionMonths': 5, 'Churn': 'Tidak'},
        {'CustomerID': 2, 'Age': 45, 'MonthlySpend': 1200000, 'VisitFreq': 8, 'SubscriptionMonths': 24, 'Churn': 'Tidak'},
        {'CustomerID': 3, 'Age': 34, 'MonthlySpend': 800000, 'VisitFreq': 6, 'SubscriptionMonths': 12, 'Churn': 'Tidak'},
        {'CustomerID': 4, 'Age': 29, 'MonthlySpend': 600000, 'VisitFreq': 7, 'SubscriptionMonths': 8, 'Churn': 'Tidak'},
        {'CustomerID': 5, 'Age': 51, 'MonthlySpend': 1500000, 'VisitFreq': 9, 'SubscriptionMonths': 30, 'Churn': 'Tidak'},
        {'CustomerID': 6, 'Age': 22, 'MonthlySpend': 450000, 'VisitFreq': 4, 'SubscriptionMonths': 3, 'Churn': 'Ya'},
        {'CustomerID': 7, 'Age': 38, 'MonthlySpend': 900000, 'VisitFreq': 7, 'SubscriptionMonths': 15, 'Churn': 'Tidak'},
        {'CustomerID': 8, 'Age': 41, 'MonthlySpend': 1100000, 'VisitFreq': 8, 'SubscriptionMonths': 20, 'Churn': 'Tidak'},
        {'CustomerID': 9, 'Age': 33, 'MonthlySpend': 750000, 'VisitFreq': 6, 'SubscriptionMonths': 11, 'Churn': 'Tidak'},
        {'CustomerID': 10, 'Age': 27, 'MonthlySpend': 550000, 'VisitFreq': 5, 'SubscriptionMonths': 7, 'Churn': 'Tidak'},
        {'CustomerID': 11, 'Age': 48, 'MonthlySpend': 1300000, 'VisitFreq': 6, 'SubscriptionMonths': 28, 'Churn': 'Tidak'},
        {'CustomerID': 12, 'Age': 25, 'MonthlySpend': 480000, 'VisitFreq': 4, 'SubscriptionMonths': 4, 'Churn': 'Ya'},
        {'CustomerID': 13, 'Age': 36, 'MonthlySpend': 850000, 'VisitFreq': 5, 'SubscriptionMonths': 14, 'Churn': 'Tidak'},
        {'CustomerID': 14, 'Age': 30, 'MonthlySpend': 700000, 'VisitFreq': 6, 'SubscriptionMonths': 9, 'Churn': 'Tidak'},
        {'CustomerID': 15, 'Age': 52, 'MonthlySpend': 1400000, 'VisitFreq': 8, 'SubscriptionMonths': 29, 'Churn': 'Tidak'},
        {'CustomerID': 16, 'Age': 24, 'MonthlySpend': 460000, 'VisitFreq': 5, 'SubscriptionMonths': 6, 'Churn': 'Ya'},
        {'CustomerID': 17, 'Age': 39, 'MonthlySpend': 950000, 'VisitFreq': 7, 'SubscriptionMonths': 16, 'Churn': 'Tidak'},
        {'CustomerID': 18, 'Age': 42, 'MonthlySpend': 1150000, 'VisitFreq': 8, 'SubscriptionMonths': 22, 'Churn': 'Tidak'},
        {'CustomerID': 19, 'Age': 31, 'MonthlySpend': 770000, 'VisitFreq': 6, 'SubscriptionMonths': 10, 'Churn': 'Tidak'},
        {'CustomerID': 20, 'Age': 28, 'MonthlySpend': 580000, 'VisitFreq': 6, 'SubscriptionMonths': 8, 'Churn': 'Tidak'},
        {'CustomerID': 21, 'Age': 49, 'MonthlySpend': 1350000, 'VisitFreq': 9, 'SubscriptionMonths': 27, 'Churn': 'Tidak'},
        {'CustomerID': 22, 'Age': 26, 'MonthlySpend': 490000, 'VisitFreq': 5, 'SubscriptionMonths': 6, 'Churn': 'Ya'},
        {'CustomerID': 23, 'Age': 35, 'MonthlySpend': 820000, 'VisitFreq': 6, 'SubscriptionMonths': 13, 'Churn': 'Tidak'},
        {'CustomerID': 24, 'Age': 32, 'MonthlySpend': 720000, 'VisitFreq': 7, 'SubscriptionMonths': 11, 'Churn': 'Tidak'},
        {'CustomerID': 25, 'Age': 50, 'MonthlySpend': 1450000, 'VisitFreq': 9, 'SubscriptionMonths': 31, 'Churn': 'Tidak'},
        {'CustomerID': 26, 'Age': 21, 'MonthlySpend': 440000, 'VisitFreq': 4, 'SubscriptionMonths': 2, 'Churn': 'Ya'},
        {'CustomerID': 27, 'Age': 40, 'MonthlySpend': 1000000, 'VisitFreq': 8, 'SubscriptionMonths': 18, 'Churn': 'Tidak'},
        {'CustomerID': 28, 'Age': 43, 'MonthlySpend': 1120000, 'VisitFreq': 7, 'SubscriptionMonths': 21, 'Churn': 'Tidak'},
        {'CustomerID': 29, 'Age': 37, 'MonthlySpend': 880000, 'VisitFreq': 8, 'SubscriptionMonths': 17, 'Churn': 'Tidak'},
        {'CustomerID': 30, 'Age': 29, 'MonthlySpend': 610000, 'VisitFreq': 6, 'SubscriptionMonths': 9, 'Churn': 'Tidak'}
    ]
    df = pd.DataFrame(data)
    df['ChurnFlag'] = df['Churn'].map({'Ya': 1, 'Tidak': 0})
    return df

# ==================== LINEAR PROGRAMMING PAGE ====================
def lp_solver_page():
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div class="info-box">
        <b>Linear Programming</b>
        <br>Metode untuk mengoptimalkan fungsi objektif linear dengan kendala linear
        </div>
        """, unsafe_allow_html=True)
        
        prob_type = st.radio("Tipe Masalah:", ["Maksimasi", "Minimasi"])
        input_method = st.radio("Metode Input:", ["Manual", "Upload File"])
    
    with col2:
        if input_method == "Manual":
            st.write("**Konfigurasi Model LP**")
            
            num_vars = st.number_input("Jumlah Variabel:", min_value=2, max_value=10, value=2)
            num_constraints = st.number_input("Jumlah Kendala:", min_value=1, max_value=10, value=2)
            
            # Objective function
            st.write("#### Fungsi Objektif (Coefficients)")
            obj_coeffs = []
            cols = st.columns(num_vars)
            for i, col in enumerate(cols):
                with col:
                    coeff = st.number_input(f"x{i+1}", value=1.0, key=f"obj_{i}")
                    obj_coeffs.append(coeff)
            
            # Constraints
            st.write("#### Kendala")
            constraint_matrix = []
            constraint_bounds = []
            constraint_types = []
            
            for c in range(num_constraints):
                st.write(f"**Kendala {c+1}**")
                row_cols = st.columns(num_vars + 2)
                row = []
                
                for v in range(num_vars):
                    with row_cols[v]:
                        coeff = st.number_input(f"x{v+1}", value=1.0, key=f"constraint_{c}_{v}")
                        row.append(coeff)
                
                with row_cols[num_vars]:
                    constraint_type = st.selectbox(
                        "Tipe:", 
                        ["<=", "=", ">="],
                        key=f"type_{c}",
                        label_visibility="collapsed"
                    )
                    constraint_types.append(constraint_type)
                
                with row_cols[num_vars + 1]:
                    bound = st.number_input(
                        f"RHS",
                        value=1.0,
                        key=f"rhs_{c}",
                        label_visibility="collapsed"
                    )
                    constraint_bounds.append(bound)
                
                constraint_matrix.append(row)
            
            # Solve button
            if st.button("🚀 Selesaikan", key="solve_lp"):
                try:
                    result = linear_programming_solver(
                        obj_coeffs,
                        constraint_matrix,
                        constraint_bounds,
                        constraint_types,
                        prob_type.upper()
                    )
                    st.session_state.solver_results = result
                    display_results(result, "Linear Programming")
                except Exception as e:
                    st.markdown(f"""
                    <div class="error-box">
                    <b>❌ Error:</b> {str(e)}
                    </div>
                    """, unsafe_allow_html=True)
        
        else:  # Upload File
            st.write("**Upload File CSV/Excel**")
            uploaded_file = st.file_uploader(
                "Pilih file",
                type=["csv", "xlsx", "xls"]
            )
            
            if uploaded_file:
                try:
                    if uploaded_file.name.endswith('csv'):
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                    
                    st.write("Preview Data:")
                    st.dataframe(df, use_container_width=True)
                    
                except Exception as e:
                    st.error(f"Error membaca file: {str(e)}")

# ==================== TRANSPORTATION PROBLEM PAGE ====================
def transportation_solver_page():
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div class="info-box">
        <b>Transportation Problem</b>
        <br>Mengoptimalkan distribusi dari sumber ke tujuan dengan biaya minimal
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        num_sources = st.number_input("Jumlah Sumber:", min_value=2, max_value=10, value=3)
        num_destinations = st.number_input("Jumlah Tujuan:", min_value=2, max_value=10, value=3)
        
        st.write("**Supply (Penawaran dari Sumber)**")
        supply = []
        cols = st.columns(num_sources)
        for i, col in enumerate(cols):
            with col:
                s = st.number_input(f"Sumber {i+1}", min_value=1, value=100, key=f"supply_{i}")
                supply.append(s)
        
        st.write("**Cost Matrix (Biaya Transportasi)**")
        cost_matrix = []
        for i in range(num_sources):
            st.write(f"*Dari Sumber {i+1}*")
            row = []
            cols = st.columns(num_destinations)
            for j, col in enumerate(cols):
                with col:
                    cost = st.number_input(
                        f"ke Tujuan {j+1}",
                        min_value=0,
                        value=10,
                        key=f"cost_{i}_{j}"
                    )
                    row.append(cost)
            cost_matrix.append(row)
        
        st.write("**Demand (Permintaan di Tujuan)**")
        demand = []
        cols = st.columns(num_destinations)
        for j, col in enumerate(cols):
            with col:
                d = st.number_input(f"Tujuan {j+1}", min_value=1, value=100, key=f"demand_{j}")
                demand.append(d)
        
        if st.button("🚀 Selesaikan", key="solve_transport"):
            try:
                result = transportation_problem_solver(supply, demand, cost_matrix)
                st.session_state.solver_results = result
                display_results(result, "Transportation Problem")
            except Exception as e:
                st.markdown(f"""
                <div class="error-box">
                <b>❌ Error:</b> {str(e)}
                </div>
                """, unsafe_allow_html=True)

# ==================== ASSIGNMENT PROBLEM PAGE ====================
def assignment_solver_page():
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div class="info-box">
        <b>Assignment Problem</b>
        <br>Mengalokasikan tugas ke sumber daya dengan biaya minimal
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        size = st.number_input("Ukuran Problem (n×n):", min_value=2, max_value=10, value=3)
        
        st.write("**Cost Matrix**")
        cost_matrix = []
        for i in range(size):
            row = []
            cols = st.columns(size)
            for j, col in enumerate(cols):
                with col:
                    cost = st.number_input(
                        f"[{i+1},{j+1}]",
                        value=1,
                        key=f"assign_cost_{i}_{j}"
                    )
                    row.append(cost)
            cost_matrix.append(row)
        
        if st.button("🚀 Selesaikan", key="solve_assign"):
            try:
                result = assignment_problem_solver(cost_matrix)
                st.session_state.solver_results = result
                display_results(result, "Assignment Problem")
            except Exception as e:
                st.markdown(f"""
                <div class="error-box">
                <b>❌ Error:</b> {str(e)}
                </div>
                """, unsafe_allow_html=True)

# ==================== SHORTEST PATH PAGE ====================
def shortest_path_page():
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("""
        <div class="info-box">
        <b>Shortest Path Problem</b>
        <br>Menemukan rute terpendek antara dua simpul dalam graf menggunakan Dijkstra Algorithm
        </div>
        """, unsafe_allow_html=True)

        # Contoh data
        st.markdown("### 📊 Contoh Data")
        st.markdown("""
        **Graf dengan 5 node (A, B, C, D, E):**
        - A → B: 4, A → C: 2
        - B → C: 1, B → D: 5
        - C → D: 8, C → E: 10
        - D → E: 2
        """)

        # Input manual
        st.markdown("### 🔧 Input Manual")
        num_nodes = st.number_input("Jumlah Node:", min_value=2, max_value=10, value=5, key="sp_nodes")
        start_node = st.text_input("Node Awal:", value="A", key="sp_start")
        end_node = st.text_input("Node Tujuan:", value="E", key="sp_end")

    with col2:
        # Contoh predefined
        if st.button("🚀 Gunakan Contoh Data", key="solve_sp_example"):
            # Contoh graph: A-B-C-D-E
            graph = {
                'A': [('B', 4), ('C', 2)],
                'B': [('C', 1), ('D', 5)],
                'C': [('D', 8), ('E', 10)],
                'D': [('E', 2)],
                'E': []
            }
            try:
                result = shortest_path_solver(graph, 'A', 'E')
                st.session_state.solver_results = result
                display_results(result, "Shortest Path Problem")
            except Exception as e:
                st.markdown(f"""
                <div class="error-box">
                <b>❌ Error:</b> {str(e)}
                </div>
                """, unsafe_allow_html=True)

        # Input manual graph
        st.markdown("### 📝 Input Graf Manual")
        st.info("Format: node1-node2:weight (contoh: A-B:4)")

        graph_input = st.text_area(
            "Masukkan edges graf:",
            value="A-B:4\nA-C:2\nB-C:1\nB-D:5\nC-D:8\nC-E:10\nD-E:2",
            height=150,
            key="sp_graph_input"
        )

        if st.button("🚀 Selesaikan Manual", key="solve_sp_manual"):
            try:
                # Parse graph input
                graph = {}
                lines = graph_input.strip().split('\n')
                nodes = set()

                for line in lines:
                    if ':' in line:
                        edge_part, weight_part = line.split(':')
                        node1, node2 = edge_part.strip().split('-')
                        weight = float(weight_part.strip())

                        nodes.add(node1)
                        nodes.add(node2)

                        if node1 not in graph:
                            graph[node1] = []
                        if node2 not in graph:
                            graph[node2] = []

                        graph[node1].append((node2, weight))

                # Add empty lists for nodes with no outgoing edges
                for node in nodes:
                    if node not in graph:
                        graph[node] = []

                result = shortest_path_solver(graph, start_node, end_node)
                st.session_state.solver_results = result
                display_results(result, "Shortest Path Problem")

            except Exception as e:
                st.markdown(f"""
                <div class="error-box">
                <b>❌ Error:</b> {str(e)}
                </div>
                """, unsafe_allow_html=True)

# ==================== INTEGER PROGRAMMING PAGE ====================
def integer_programming_page():
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("""
        <div class="info-box">
        <b>Integer Programming</b>
        <br>Optimasi dengan variabel bilangan bulat (0-1 atau integer)
        </div>
        """, unsafe_allow_html=True)

        # Contoh data
        st.markdown("### 📊 Contoh Data")
        st.markdown("""
        **Knapsack Problem (0-1):**
        - Maximize: 10x₁ + 15x₂ + 20x₃
        - Subject to: 2x₁ + 3x₂ + 4x₃ ≤ 7
        - x₁, x₂, x₃ ∈ {0, 1}
        """)

        # Input parameters
        st.markdown("### 🔧 Parameter Input")
        prob_type = st.selectbox("Tipe Problem:", ["MAX", "MIN"], index=0, key="ip_type")
        num_vars = st.number_input("Jumlah Variabel:", min_value=1, max_value=10, value=3, key="ip_vars")

        # Objective coefficients
        st.markdown("**Koefisien Fungsi Objektif:**")
        obj_coeffs = []
        cols = st.columns(num_vars)
        for i, col in enumerate(cols):
            with col:
                coeff = st.number_input(f"x{i+1}", value=[10, 15, 20][i] if i < 3 else 1, key=f"ip_obj_{i}")
                obj_coeffs.append(coeff)

        # Constraints
        num_constraints = st.number_input("Jumlah Kendala:", min_value=1, max_value=10, value=1, key="ip_constraints")

        st.markdown("**Matriks Kendala:**")
        constraint_matrix = []
        constraint_bounds = []
        constraint_types = []

        for i in range(num_constraints):
            st.markdown(f"**Kendala {i+1}:**")
            row = []
            cols = st.columns(num_vars + 2)  # vars + bound + type

            for j in range(num_vars):
                with cols[j]:
                    coeff = st.number_input(f"a{i+1}{j+1}", value=[2, 3, 4][j] if i == 0 and j < 3 else 1,
                                          key=f"ip_const_{i}_{j}")
                    row.append(coeff)

            with cols[-2]:
                bound = st.number_input(f"b{i+1}", value=7 if i == 0 else 10, key=f"ip_bound_{i}")
                constraint_bounds.append(bound)

            with cols[-1]:
                ctype = st.selectbox(f"Tipe {i+1}", ["<=", "=", ">="], index=0, key=f"ip_type_{i}")
                constraint_types.append(ctype)

            constraint_matrix.append(row)

        # Variable types
        st.markdown("**Tipe Variabel:**")
        var_types = []
        cols = st.columns(num_vars)
        for i, col in enumerate(cols):
            with col:
                vtype = st.selectbox(f"x{i+1}", ["Integer", "Binary", "Continuous"], index=1 if i < 3 else 0,
                                   key=f"ip_vtype_{i}")
                var_types.append(vtype)

    with col2:
        # Solve with example
        if st.button("🚀 Gunakan Contoh Data", key="solve_ip_example"):
            try:
                obj_coeffs = [10, 15, 20]
                constraint_matrix = [[2, 3, 4]]
                constraint_bounds = [7]
                constraint_types = ["<="]
                var_types = ["Binary", "Binary", "Binary"]

                result = integer_programming_solver(obj_coeffs, constraint_matrix, constraint_bounds,
                                                  constraint_types, "MAX", var_types)
                st.session_state.solver_results = result
                display_results(result, "Integer Programming (0-1 Knapsack)")
            except Exception as e:
                st.markdown(f"""
                <div class="error-box">
                <b>❌ Error:</b> {str(e)}
                </div>
                """, unsafe_allow_html=True)

        # Solve with custom parameters
        if st.button("🚀 Selesaikan Manual", key="solve_ip_manual"):
            try:
                result = integer_programming_solver(obj_coeffs, constraint_matrix, constraint_bounds,
                                                  constraint_types, prob_type, var_types)
                st.session_state.solver_results = result
                display_results(result, "Integer Programming")
            except Exception as e:
                st.markdown(f"""
                <div class="error-box">
                <b>❌ Error:</b> {str(e)}
                </div>
                """, unsafe_allow_html=True)

        # Display info
        st.markdown("### 📈 Tipe Variabel")
        st.markdown("""
        - **Binary**: 0 atau 1 (untuk 0-1 programming)
        - **Integer**: Bilangan bulat (..., -2, -1, 0, 1, 2, ...)
        - **Continuous**: Bilangan real
        """)

# ==================== QUEUE THEORY PAGE ====================
def queue_theory_page():
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("""
        <div class="info-box">
        <b>Teori Antrian</b>
        <br>Analisis sistem antrian untuk optimasi pelayanan (M/M/1 dan M/M/c)
        </div>
        """, unsafe_allow_html=True)

        # Contoh data
        st.markdown("### 📊 Contoh Data")
        st.markdown("""
        **Sistem Bank:**
        - Tingkat kedatangan (λ): 10 pelanggan/jam
        - Tingkat pelayanan (μ): 12 pelanggan/jam
        - Jumlah server: 1 (M/M/1)
        """)

        # Input parameters
        st.markdown("### 🔧 Parameter Input")
        arrival_rate = st.number_input("Tingkat Kedatangan (λ):", min_value=0.1, value=10.0, step=0.1, key="qt_arrival")
        service_rate = st.number_input("Tingkat Pelayanan (μ):", min_value=0.1, value=12.0, step=0.1, key="qt_service")
        num_servers = st.number_input("Jumlah Server:", min_value=1, max_value=10, value=1, key="qt_servers")
        queue_type = st.selectbox("Tipe Antrian:", ["M/M/1", "M/M/c"], index=0, key="qt_type")

    with col2:
        # Solve with example
        if st.button("🚀 Gunakan Contoh Data", key="solve_qt_example"):
            try:
                result = queue_theory_solver(10.0, 12.0, 1, "M/M/1")
                st.session_state.solver_results = result
                display_results(result, "Queue Theory (M/M/1)")
            except Exception as e:
                st.markdown(f"""
                <div class="error-box">
                <b>❌ Error:</b> {str(e)}
                </div>
                """, unsafe_allow_html=True)

        # Solve with custom parameters
        if st.button("🚀 Hitung Manual", key="solve_qt_manual"):
            try:
                qt_type = "M/M/1" if num_servers == 1 else "M/M/c"
                result = queue_theory_solver(arrival_rate, service_rate, num_servers, qt_type)
                st.session_state.solver_results = result
                display_results(result, f"Queue Theory ({qt_type})")
            except Exception as e:
                st.markdown(f"""
                <div class="error-box">
                <b>❌ Error:</b> {str(e)}
                </div>
                """, unsafe_allow_html=True)

        # Display formulas
        st.markdown("### 📈 Rumus Utama")
        st.markdown("""
        **Utilization Factor (ρ):** λ/(c×μ)
        **Avg Customers in System (L):** λ×W
        **Avg Waiting Time (W):** 1/(μ-λ) untuk M/M/1
        **Probability Empty (P₀):** 1-ρ untuk M/M/1
        """)

# ==================== MONTE CARLO PAGE ====================
def monte_carlo_page():
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("""
        <div class="info-box">
        <b>Simulasi Monte Carlo</b>
        <br>Simulasi permintaan historis menggunakan distribusi empiris
        </div>
        """, unsafe_allow_html=True)

        # Contoh data
        st.markdown("### 📊 Data Permintaan Historis")
        st.write("Masukkan permintaan historis dan frekuensi jumlah minggu.")
        demand_input = st.text_area(
            "Permintaan (ribuan unit): Data (pisahkan koma)",
            value="0,1,2,3,4,5",
            height=80,
            key="mc_demand_input"
        )
        freq_input = st.text_area(
            "Frekuensi (minggu): Frekuensi (pisahkan koma)",
            value="6,8,8,9,11,10",
            height=80,
            key="mc_freq_input"
        )

        num_simulations = st.number_input("Jumlah Simulasi:", min_value=100, max_value=100000, value=1000, step=100, key="mc_sims")
        prediction_weeks = st.number_input("Jumlah Minggu Prediksi:", min_value=1, max_value=52, value=15, step=1, key="mc_weeks")

        st.markdown("### 📌 Catatan")
        st.markdown("Gunakan data historis untuk membentuk distribusi empiris; simulasi ini akan memprediksi total permintaan selama minggu prediksi.")

    with col2:
        if st.button("🚀 Jalankan Simulasi", key="solve_mc_manual"):
            try:
                demand_values = [float(x.strip()) for x in demand_input.split(',') if x.strip() != '']
                freq_values = [float(x.strip()) for x in freq_input.split(',') if x.strip() != '']

                if len(demand_values) != len(freq_values):
                    raise ValueError("Jumlah permintaan dan frekuensi harus sama.")

                total_freq = sum(freq_values)
                if total_freq <= 0:
                    raise ValueError("Frekuensi harus positif.")

                probabilities = [f / total_freq for f in freq_values]
                sample_matrix = np.random.choice(demand_values, size=(num_simulations, prediction_weeks), p=probabilities)
                total_demand = sample_matrix.sum(axis=1)
                average_weekly = total_demand / prediction_weeks

                result = {
                    "status": "Success",
                    "num_simulations": num_simulations,
                    "distribution": "Empirical",
                    "parameters": {
                        "demand_values": demand_values,
                        "frequencies": freq_values,
                        "probabilities": probabilities,
                        "prediction_weeks": int(prediction_weeks)
                    },
                    "statistics": {
                        "mean_total_demand": float(np.mean(total_demand)),
                        "std_total_demand": float(np.std(total_demand)),
                        "mean_weekly_demand": float(np.mean(average_weekly)),
                        "std_weekly_demand": float(np.std(average_weekly)),
                        "min_total_demand": float(np.min(total_demand)),
                        "max_total_demand": float(np.max(total_demand)),
                        "confidence_interval": {
                            "level": 0.95,
                            "lower": float(np.mean(total_demand) - 1.96 * np.std(total_demand) / np.sqrt(num_simulations)),
                            "upper": float(np.mean(total_demand) + 1.96 * np.std(total_demand) / np.sqrt(num_simulations))
                        }
                    },
                    "samples": total_demand.tolist()[:1000],
                    "prediction_weeks": int(prediction_weeks)
                }

                st.session_state.solver_results = result
                display_results(result, "Monte Carlo Simulation")
            except Exception as e:
                st.markdown(f"""
                <div class="error-box">
                <b>❌ Error:</b> {str(e)}
                </div>
                """, unsafe_allow_html=True)

        st.markdown("### 📈 Output Statistik")
        st.markdown("""
        - **Mean Total Demand**: Rata-rata total permintaan selama minggu prediksi
        - **Std Dev Total Demand**: Variabilitas total permintaan
        - **Mean Weekly Demand**: Rata-rata permintaan per minggu
        - **95% CI**: Confidence interval total permintaan
        - **Min/Max**: Total permintaan terendah dan tertinggi
        """)

# ==================== CLASSIFICATION PAGE ====================
def classification_page():
    df = load_churn_dataset()
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("""
        <div class="info-box">
        <b>Klasifikasi</b>
        <br>Gunakan model klasifikasi untuk memprediksi churn pelanggan
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📊 Data Pelanggan")
        st.write("Dataset churn pelanggan berdasarkan usia, pengeluaran, frekuensi kunjungan, dan lama berlangganan.")
        st.dataframe(df[['CustomerID', 'Age', 'MonthlySpend', 'VisitFreq', 'SubscriptionMonths', 'Churn']], use_container_width=True)

        st.markdown("### 🔧 Parameter Input")
        algorithm = st.selectbox("Algoritma:", ["logistic_regression", "random_forest", "svm", "knn"], index=0, key="clf_algo")

        if algorithm == "knn":
            n_neighbors = st.slider("Jumlah Tetangga (K):", min_value=1, max_value=20, value=5, key="clf_k")
            params = {"n_neighbors": n_neighbors}
        elif algorithm == "svm":
            C = st.slider("Parameter C:", min_value=0.1, max_value=10.0, value=1.0, step=0.1, key="clf_c")
            params = {"C": C}
        elif algorithm == "random_forest":
            n_estimators = st.slider("Jumlah Trees:", min_value=10, max_value=200, value=100, step=10, key="clf_trees")
            params = {"n_estimators": n_estimators}
        else:
            params = {}

    with col2:
        if st.button("🚀 Latih Model dan Evaluasi", key="solve_clf_example"):
            try:
                from sklearn.model_selection import train_test_split

                features = ['Age', 'MonthlySpend', 'VisitFreq', 'SubscriptionMonths']
                X = df[features].values
                y = df['ChurnFlag'].values

                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
                result = classification_solver(X_train, y_train, X_test, algorithm, params)

                st.session_state.solver_results = result
                display_results(result, f"Classification ({algorithm})")
            except Exception as e:
                st.markdown(f"""
                <div class="error-box">
                <b>❌ Error:</b> {str(e)}
                </div>
                """, unsafe_allow_html=True)

        st.markdown("### 📈 Metrik Evaluasi")
        st.markdown("""
        - **Accuracy**: Persentase prediksi benar
        - **Precision**: Benar positif dibanding prediksi positif
        - **Recall**: Benar positif dibanding total aktual positif
        - **F1-Score**: Rata-rata harmonis precision dan recall
        - **Confusion Matrix**: Visualisasi prediksi terhadap actual
        """)

        st.markdown("### 📌 Insight")
        st.write("Gunakan model ini untuk membantu mengidentifikasi pelanggan yang berisiko churn sehingga bisa dilakukan retensi.")

# ==================== CLUSTERING PAGE ====================
def clustering_page():
    df = load_churn_dataset()
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("""
        <div class="info-box">
        <b>Klaster</b>
        <br>Kelompokkan pelanggan berdasarkan perilaku dan pengeluaran
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📊 Data Pelanggan")
        st.write("Dataset churn pelanggan dengan fitur yang sama seperti contoh data.")
        st.dataframe(df[['Age', 'MonthlySpend', 'VisitFreq', 'SubscriptionMonths', 'Churn']], use_container_width=True)

        st.markdown("### 🔧 Parameter Input")
        algorithm = st.selectbox("Algoritma:", ["kmeans", "hierarchical", "dbscan"], index=0, key="clu_algo")
        n_clusters = st.slider("Jumlah Cluster:", min_value=2, max_value=6, value=3, key="clu_n")

        if algorithm == "kmeans":
            params = {"init": "k-means++", "random_state": 42}
        elif algorithm == "hierarchical":
            linkage = st.selectbox("Linkage Method:", ["ward", "complete", "average", "single"], index=0, key="clu_linkage")
            params = {"linkage": linkage}
        else:
            eps = st.slider("Epsilon:", min_value=0.1, max_value=5.0, value=0.5, step=0.1, key="clu_eps")
            min_samples = st.slider("Min Samples:", min_value=1, max_value=20, value=5, key="clu_min_samples")
            params = {"eps": eps, "min_samples": min_samples}

    with col2:
        if st.button("🚀 Analisis Klaster", key="solve_clu_example"):
            try:
                features = ['Age', 'MonthlySpend', 'VisitFreq', 'SubscriptionMonths']
                X = df[features].values
                result = clustering_solver(X, n_clusters, algorithm, params)
                st.session_state.solver_results = result
                display_results(result, f"Clustering ({algorithm})")

                df['Cluster'] = result['labels']
                st.markdown("### 📌 Distribusi Cluster")
                st.dataframe(df[['CustomerID', 'Age', 'MonthlySpend', 'VisitFreq', 'SubscriptionMonths', 'Churn', 'Cluster']].sort_values('Cluster'), use_container_width=True)
            except Exception as e:
                st.markdown(f"""
                <div class="error-box">
                <b>❌ Error:</b> {str(e)}
                </div>
                """, unsafe_allow_html=True)

        st.markdown("### 📈 Metrik Evaluasi")
        st.markdown("""
        - **Silhouette Score**: Mengukur seberapa baik objek dikelompokkan
        - **Calinski-Harabasz Score**: Rasio antara dispersi antar cluster dan dalam cluster
        - **Davies-Bouldin Score**: Rata-rata similarity antar cluster
        - **Cluster Sizes**: Jumlah data point per cluster
        """)

        st.markdown("### 📌 Insight")
        st.write("Analisis klaster ini membantu memahami segmentasi pelanggan berdasarkan perilaku berlangganan dan churn.")

# ==================== PREDICTION PAGE ====================
def prediction_page():
    df = load_churn_dataset()
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("""
        <div class="info-box">
        <b>Prediksi Churn</b>
        <br>Masukkan profil pelanggan untuk memprediksi apakah pelanggan akan churn
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📊 Contoh Data")
        st.write("Gunakan dataset churn sebagai acuan untuk nilai input.")
        st.dataframe(df[['Age', 'MonthlySpend', 'VisitFreq', 'SubscriptionMonths', 'Churn']], use_container_width=True)

        age = st.number_input("Usia:", min_value=18, max_value=80, value=30, key="pred_age")
        monthly_spend = st.number_input("Pengeluaran Bulanan (Rp):", min_value=100000, max_value=3000000, value=750000, step=50000, key="pred_spend")
        visit_freq = st.number_input("Frekuensi Kunjungan per Bulan:", min_value=1, max_value=12, value=6, key="pred_visit")
        subscription_months = st.number_input("Lama Berlangganan (Bulan):", min_value=1, max_value=60, value=10, key="pred_months")

        st.markdown("### 🔧 Pilih Model")
        algorithm = st.selectbox("Algoritma Prediksi:", ["logistic_regression", "random_forest", "svm", "knn"], index=0, key="pred_algo")
        if algorithm == "knn":
            n_neighbors = st.slider("Jumlah Tetangga (K):", min_value=1, max_value=20, value=5, key="pred_k")
            params = {"n_neighbors": n_neighbors}
        elif algorithm == "svm":
            C = st.slider("Parameter C:", min_value=0.1, max_value=10.0, value=1.0, step=0.1, key="pred_c")
            params = {"C": C}
        elif algorithm == "random_forest":
            n_estimators = st.slider("Jumlah Trees:", min_value=10, max_value=200, value=100, step=10, key="pred_trees")
            params = {"n_estimators": n_estimators}
        else:
            params = {}

    with col2:
        if st.button("🚀 Prediksi Churn", key="solve_prediction"):
            try:
                from sklearn.model_selection import train_test_split
                from sklearn.linear_model import LogisticRegression
                from sklearn.svm import SVC
                from sklearn.ensemble import RandomForestClassifier
                from sklearn.neighbors import KNeighborsClassifier

                feature_cols = ['Age', 'MonthlySpend', 'VisitFreq', 'SubscriptionMonths']
                X = df[feature_cols].values
                y = df['ChurnFlag'].values
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

                if algorithm == 'logistic_regression':
                    model = LogisticRegression(max_iter=1000)
                elif algorithm == 'svm':
                    model = SVC(probability=True, **params)
                elif algorithm == 'random_forest':
                    model = RandomForestClassifier(**params, random_state=42)
                else:
                    model = KNeighborsClassifier(**params)

                model.fit(X_train, y_train)
                new_customer = np.array([[age, monthly_spend, visit_freq, subscription_months]])
                prediction = model.predict(new_customer)[0]
                probability = None
                if hasattr(model, 'predict_proba'):
                    probability = model.predict_proba(new_customer)[0][1]

                churn_label = 'Ya' if prediction == 1 else 'Tidak'
                st.success(f"Prediksi Churn: {churn_label}")
                if probability is not None:
                    st.metric("Probabilitas Churn", f"{probability:.2%}")

                st.markdown("### 📌 Hasil Model")
                st.write(f"Model: {algorithm.replace('_', ' ').title()}")
                st.write(f"Training Accuracy: {model.score(X_train, y_train):.2f}")
                st.write(f"Test Accuracy: {model.score(X_test, y_test):.2f}")
            except Exception as e:
                st.markdown(f"""
                <div class="error-box">
                <b>❌ Error:</b> {str(e)}
                </div>
                """, unsafe_allow_html=True)

# ==================== CHURN PAGE ====================
def churn_page():
    df = load_churn_dataset()
    st.markdown("""
    <div class="info-box">
    <b>Analisis Churn</b>
    <br>Analisis komprehensif churn pelanggan menggunakan data seperti yang ditunjukkan.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📊 Preview Dataset")
    st.dataframe(df[['CustomerID', 'Age', 'MonthlySpend', 'VisitFreq', 'SubscriptionMonths', 'Churn']], use_container_width=True)

    churn_rate = df['ChurnFlag'].mean()
    churn_counts = df['Churn'].value_counts()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Pelanggan", len(df))
    col2.metric("Churn Rate", f"{churn_rate:.2%}")
    col3.metric("Pelanggan Churn", int(churn_counts.get('Ya', 0)))

    st.markdown("### 📈 Ringkasan Churn")
    churn_summary = df.groupby('Churn')[['MonthlySpend', 'VisitFreq', 'SubscriptionMonths', 'Age']].mean().round(2)
    st.dataframe(churn_summary)

    st.markdown("### 📌 Distribusi Churn")
    st.bar_chart(churn_counts)

    st.markdown("### 🔧 Model Churn (Logistic Regression)")
    try:
        from sklearn.model_selection import train_test_split
        features = ['Age', 'MonthlySpend', 'VisitFreq', 'SubscriptionMonths']
        X = df[features].values
        y = df['ChurnFlag'].values
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        result = classification_solver(X_train, y_train, X_test, 'logistic_regression', {})
        st.session_state.solver_results = result
        display_results(result, "Classification (churn)")
    except Exception as e:
        st.markdown(f"""
        <div class="error-box">
        <b>❌ Error:</b> {str(e)}
        </div>
        """, unsafe_allow_html=True)

# ==================== ABOUT PAGE ====================
def about_page():
    st.markdown("""
    ## 📚 Tentang Aplikasi
    
    **Aplikasi Python Untuk Masalah Operation Research** adalah aplikasi web interaktif 
    yang dirancang untuk membantu menyelesaikan berbagai masalah optimasi dalam 
    Operation Research.
    
    ### 🎯 Fitur Utama:
    - **Linear Programming Solver** - Menyelesaikan masalah LP dengan metode simplex
    - **Integer Programming Solver** - Optimasi dengan variabel bilangan bulat
    - **Transportation Problem** - Optimasi distribusi dengan biaya minimal
    - **Assignment Problem** - Alokasi optimal sumber daya ke tugas
    - **Shortest Path Problem** - Menemukan rute terpendek dalam jaringan
    - **Teori Antrian** - Analisis sistem antrian untuk optimasi pelayanan
    - **Simulasi Monte Carlo** - Simulasi probabilistik untuk analisis risiko
    - **Klasifikasi** - Algoritma machine learning untuk klasifikasi churn
    - **Klaster** - Algoritma clustering untuk segmentasi pelanggan
    - **Prediksi** - Memprediksi churn pelanggan berdasarkan profil
    - **Churn** - Analisis churn pelanggan dengan data riil
    
    ### 🛠️ Teknologi yang Digunakan:
    - **Python** - Bahasa pemrograman utama
    - **Streamlit** - Framework untuk UI web
    - **PuLP** - Solver untuk linear programming
    - **SciPy** - Perhitungan ilmiah
    - **Pandas** - Manipulasi data
    - **Plotly** - Visualisasi data
    
    ### 📖 Dokumentasi
    Untuk informasi lebih detail, lihat file README.md di folder aplikasi.
    
    ### 👨‍💻 Developer
    Dikembangkan dengan tujuan pendidikan dan penelitian Operation Research.
    """)

# ==================== RUN APPLICATION ====================
if __name__ == "__main__":
    main()
