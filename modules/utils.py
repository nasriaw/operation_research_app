"""
Utility Module untuk Operation Research Solver
==============================================

Berisi fungsi-fungsi utility untuk:
- Pembuatan model
- Visualisasi hasil
- Export data
- Validasi input
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from io import StringIO, BytesIO

# ==================== DISPLAY RESULTS ====================
def display_results(result, solver_type):
    """
    Menampilkan hasil solver dengan format yang rapi
    
    Parameters:
    -----------
    result : dict
        Hasil dari solver
    solver_type : str
        Tipe solver yang digunakan
    """
    
    # Determine status
    if "error" in result:
        status = "Error"
        st.error(f"❌ Error: {result['error']}")
    elif "status" in result:
        status = result['status']
        if status == "Success":
            st.success(f"✅ Operasi Berhasil! Status: {status}")
        else:
            st.warning(f"⚠️ Status: {status}")
    else:
        status = "Success"
        st.success(f"✅ Operasi Berhasil! Status: {status}")
    
    if "error" in result:
        return  # Don't display further results if there's an error
    
    if solver_type == "Linear Programming":
        display_lp_results(result)
    elif solver_type == "Integer Programming":
        display_integer_programming_results(result)
    elif solver_type == "Transportation Problem":
        display_transportation_results(result)
    elif solver_type == "Assignment Problem":
        display_assignment_results(result)
    elif solver_type == "Shortest Path Problem":
        display_shortest_path_results(result)
    elif "Queue Theory" in solver_type:
        display_queue_theory_results(result)
    elif solver_type == "Monte Carlo Simulation":
        display_monte_carlo_results(result)
    elif "Classification" in solver_type:
        display_classification_results(result)
    elif "Clustering" in solver_type:
        display_clustering_results(result)

# ==================== LINEAR PROGRAMMING RESULTS ====================
def display_lp_results(result):
    """Menampilkan hasil Linear Programming"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="result-box">
        <b>📊 Nilai Optimal</b>
        </div>
        """, unsafe_allow_html=True)
        st.metric("Optimal Value", f"{result['optimal_value']:.2f}")
    
    with col2:
        st.markdown("""
        <div class="result-box">
        <b>📈 Informasi Problem</b>
        </div>
        """, unsafe_allow_html=True)
        st.info(f"""
        - Tipe: {result['problem_type']}
        - Variabel: {result['num_variables']}
        - Kendala: {result['num_constraints']}
        """)
    
    # Nilai variabel
    st.write("**Nilai Variabel Optimal**")
    vars_df = pd.DataFrame(
        [(name, value) for name, value in result['variables'].items()],
        columns=['Variabel', 'Nilai']
    )
    st.dataframe(vars_df, use_container_width=True)
    
    # Visualisasi
    fig = px.bar(
        vars_df,
        x='Variabel',
        y='Nilai',
        title='Nilai Variabel Optimal',
        labels={'Nilai': 'Nilai Variabel'},
        color='Variabel'
    )
    st.plotly_chart(fig, use_container_width=True)

# ==================== TRANSPORTATION RESULTS ====================
def display_transportation_results(result):
    """Menampilkan hasil Transportation Problem"""
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Cost", f"${result['total_cost']:.2f}")
    with col2:
        st.metric("Sumber", result['num_sources'])
    with col3:
        st.metric("Tujuan", result['num_destinations'])
    
    # Allocation matrix
    st.write("**Matriks Alokasi (Unit)**")
    allocation_df = pd.DataFrame(
        result['allocation'],
        columns=[f'Tujuan {j+1}' for j in range(result['num_destinations'])],
        index=[f'Sumber {i+1}' for i in range(result['num_sources'])]
    )
    st.dataframe(allocation_df, use_container_width=True)
    
    # Heatmap visualization
    fig = go.Figure(data=go.Heatmap(
        z=result['allocation'],
        x=[f'Tujuan {j+1}' for j in range(result['num_destinations'])],
        y=[f'Sumber {i+1}' for i in range(result['num_sources'])],
        colorscale='Viridis',
        text=np.round(result['allocation'], 2),
        texttemplate='%{text}',
        textfont={"size": 12},
        colorbar=dict(title="Unit")
    ))
    fig.update_layout(title='Alokasi Optimal', height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Supply dan Demand info
    col1, col2 = st.columns(2)
    with col1:
        supply_df = pd.DataFrame(
            result['supply'],
            columns=['Supply'],
            index=[f'Sumber {i+1}' for i in range(result['num_sources'])]
        )
        st.write("**Supply**")
        st.dataframe(supply_df, use_container_width=True)
    
    with col2:
        demand_df = pd.DataFrame(
            result['demand'],
            columns=['Demand'],
            index=[f'Tujuan {j+1}' for j in range(result['num_destinations'])]
        )
        st.write("**Demand**")
        st.dataframe(demand_df, use_container_width=True)

# ==================== ASSIGNMENT RESULTS ====================
def display_assignment_results(result):
    """Menampilkan hasil Assignment Problem"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Cost", f"${result['total_cost']:.2f}")
    with col2:
        st.metric("Matrix Size", f"{result['matrix_size']}x{result['matrix_size']}")
    
    # Assignment details
    st.write("**Hasil Assignment**")
    assignment_data = []
    for (row, col), cost in zip(result['assignment'], result['assignment_cost']):
        assignment_data.append({
            'Pekerja': f'W{row+1}',
            'Tugas': f'T{col+1}',
            'Biaya': f"${cost:.2f}"
        })
    
    assignment_df = pd.DataFrame(assignment_data)
    st.dataframe(assignment_df, use_container_width=True)
    
    # Pie chart untuk cost distribution
    fig = px.pie(
        values=result['assignment_cost'],
        labels=[f"W{r+1}→T{c+1}" for r, c in result['assignment']],
        title='Distribusi Biaya Assignment'
    )
    st.plotly_chart(fig, use_container_width=True)

# ==================== SHORTEST PATH RESULTS ====================
def display_shortest_path_results(result):
    """Menampilkan hasil Shortest Path"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Distance", f"{result['distance']:.2f}")
    with col2:
        st.metric("Path Length", len(result['path']))
    
    st.write("**Rute Optimal**")
    path_str = " → ".join([str(node) for node in result['path']])
    st.info(f"```\n{path_str}\n```")
# ==================== INTEGER PROGRAMMING RESULTS ====================
def display_integer_programming_results(result):
    """Menampilkan hasil Integer Programming"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Optimal Value", f"{result['optimal_value']:.2f}")
    with col2:
        st.metric("Status", result['status'])
    
    # Nilai variabel
    st.write("**Nilai Variabel Optimal**")
    vars_df = pd.DataFrame(
        [(name, value) for name, value in result['variables'].items()],
        columns=['Variabel', 'Nilai']
    )
    st.dataframe(vars_df, use_container_width=True)
    
    # Visualisasi
    fig = px.bar(
        vars_df,
        x='Variabel',
        y='Nilai',
        title='Nilai Variabel Optimal (Integer)',
        labels={'Nilai': 'Nilai Variabel'},
        color='Variabel'
    )
    st.plotly_chart(fig, use_container_width=True)

# ==================== QUEUE THEORY RESULTS ====================
def display_queue_theory_results(result):
    """Menampilkan hasil Queue Theory"""
    
    if "error" in result:
        st.error(f"Error: {result['error']}")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Utilization (ρ)", f"{result['utilization_factor']:.3f}")
    with col2:
        st.metric("P₀ (Empty)", f"{result['probability_empty']:.3f}")
    with col3:
        st.metric("L (Avg in System)", f"{result['avg_customers_system']:.2f}")
    with col4:
        st.metric("W (Avg Wait Time)", f"{result['avg_waiting_time_system']:.2f}")
    
    # Detail metrics
    st.write("**Detail Metrik Sistem Antrian**")
    metrics_data = {
        'Metrik': ['Rata-rata Pelanggan dalam Sistem (L)', 'Rata-rata Pelanggan dalam Antrian (Lq)',
                  'Rata-rata Waktu Tunggu Sistem (W)', 'Rata-rata Waktu Tunggu Antrian (Wq)'],
        'Nilai': [result.get('avg_customers_system', 'N/A'), result.get('avg_customers_queue', 'N/A'),
                 result.get('avg_waiting_time_system', 'N/A'), result.get('avg_waiting_time_queue', 'N/A')]
    }
    
    if result['queue_type'] == 'M/M/c':
        metrics_data['Metrik'].extend(['Jumlah Server', 'Utilization per Server'])
        metrics_data['Nilai'].extend([result.get('num_servers', 'N/A'), result.get('utilization_factor', 'N/A')])
    
    if 'service_cost_per_hour' in result:
        metrics_data['Metrik'].extend(['Biaya Pelayanan per jam (Cs×c)', 'Biaya Tunggu per jam (Cw×Lq)', 'Total Biaya per jam'])
        metrics_data['Nilai'].extend([
            result.get('service_cost_per_hour', 'N/A'),
            result.get('waiting_cost_per_hour', 'N/A'),
            result.get('total_cost_per_hour', 'N/A')
        ])
    
    metrics_df = pd.DataFrame(metrics_data)
    st.dataframe(metrics_df, use_container_width=True)

# ==================== MONTE CARLO RESULTS ====================
def display_monte_carlo_results(result):
    """Menampilkan hasil Monte Carlo Simulation"""
    
    if "error" in result:
        st.error(f"Error: {result['error']}")
        return
    
    col1, col2, col3 = st.columns(3)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Jumlah Simulasi", result['num_simulations'])
    mean_value = result['statistics'].get('mean')
    std_value = result['statistics'].get('std_dev')
    min_value = result['statistics'].get('min')
    max_value = result['statistics'].get('max')

    # Fallback ke total demand jika struktur baru digunakan
    if mean_value is None:
        mean_value = result['statistics'].get('mean_total_demand')
    if std_value is None:
        std_value = result['statistics'].get('std_total_demand')
    if min_value is None:
        min_value = result['statistics'].get('min_total_demand')
    if max_value is None:
        max_value = result['statistics'].get('max_total_demand')

    with col2:
        st.metric("Mean", f"{mean_value:.4f}")
    with col3:
        st.metric("Std Dev", f"{std_value:.4f}")
    
    # Statistics summary
    st.write("**Ringkasan Statistik**")
    stats_data = {
        'Statistik': ['Mean', 'Standard Deviation', 'Minimum', 'Maximum', '95% CI Lower', '95% CI Upper'],
        'Nilai': [mean_value, std_value,
                 min_value, max_value,
                 result['statistics']['confidence_interval']['lower'],
                 result['statistics']['confidence_interval']['upper']]
    }
    stats_df = pd.DataFrame(stats_data)
    st.dataframe(stats_df, use_container_width=True)
    
    # Histogram
    if 'samples' in result and len(result['samples']) > 0:
        st.write("**Distribusi Hasil Simulasi**")
        fig = px.histogram(
            x=result['samples'][:1000],  # Limit for performance
            nbins=50,
            title=f'Histogram {result["distribution"]} Distribution',
            labels={'x': 'Nilai', 'y': 'Frekuensi'}
        )
        st.plotly_chart(fig, use_container_width=True)

# ==================== CLASSIFICATION RESULTS ====================
def display_classification_results(result):
    """Menampilkan hasil Classification"""
    
    if "error" in result:
        st.error(f"Error: {result['error']}")
        return
    
    col1, col2, col3 = st.columns(3)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Algoritma", result['algorithm'].replace('_', ' ').title())
    with col2:
        st.metric("Training Accuracy", f"{result['training_accuracy']:.3f}")
    with col3:
        st.metric("Jumlah Prediksi", len(result['predictions']))
    
    # Classification report
    if 'classification_report' in result and result['classification_report'] != "Could not generate classification report":
        st.write("**Classification Report**")
        try:
            # Convert classification report to DataFrame
            report_dict = result['classification_report']
            if isinstance(report_dict, dict):
                report_df = pd.DataFrame(report_dict).transpose()
                st.dataframe(report_df, use_container_width=True)
        except:
            st.write("Classification report tersedia dalam format teks.")
    
    # Confusion matrix
    if 'confusion_matrix' in result and result['confusion_matrix'] != "Could not generate confusion matrix":
        st.write("**Confusion Matrix**")
        try:
            cm_df = pd.DataFrame(result['confusion_matrix'])
            st.dataframe(cm_df, use_container_width=True)
        except:
            st.write("Confusion matrix tersedia dalam format array.")

# ==================== CLUSTERING RESULTS ====================
def display_clustering_results(result):
    """Menampilkan hasil Clustering"""
    
    if "error" in result:
        st.error(f"Error: {result['error']}")
        return
    
    col1, col2, col3 = st.columns(3)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Algoritma", result['algorithm'].title())
    with col2:
        st.metric("Jumlah Cluster", result['n_clusters'])
    with col3:
        st.metric("Silhouette Score", f"{result.get('evaluation_metrics', {}).get('silhouette_score', 'N/A'):.3f}"
                 if result.get('evaluation_metrics', {}).get('silhouette_score') is not None else "N/A")
    
    # Cluster sizes
    st.write("**Ukuran Cluster**")
    sizes_df = pd.DataFrame(
        list(result['cluster_sizes'].items()),
        columns=['Cluster', 'Jumlah Data']
    )
    st.dataframe(sizes_df, use_container_width=True)
    
    # Evaluation metrics
    if 'evaluation_metrics' in result:
        st.write("**Metrik Evaluasi**")
        eval_data = []
        for metric, value in result['evaluation_metrics'].items():
            if value is not None:
                eval_data.append({
                    'Metrik': metric.replace('_', ' ').title(),
                    'Nilai': f"{value:.4f}" if isinstance(value, (int, float)) else str(value)
                })
        
        if eval_data:
            eval_df = pd.DataFrame(eval_data)
            st.dataframe(eval_df, use_container_width=True)
    
    # Centroids (for K-means)
    if 'centroids' in result and result['centroids']:
        st.write("**Centroid Cluster**")
        centroids_df = pd.DataFrame(result['centroids'])
        centroids_df.index = [f'Cluster {i+1}' for i in range(len(centroids_df))]
        st.dataframe(centroids_df, use_container_width=True)
# ==================== EXPORT RESULTS ====================
def export_results(result, format='excel'):
    """
    Export hasil solver ke berbagai format
    
    Parameters:
    -----------
    result : dict
        Hasil solver
    format : str
        Format export ('excel', 'csv', 'json')
    
    Returns:
    --------
    bytes : File data
    """
    
    if format == 'excel':
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df = pd.DataFrame([result])
            df.to_excel(writer, sheet_name='Results')
        output.seek(0)
        return output.getvalue()
    
    elif format == 'csv':
        output = StringIO()
        df = pd.DataFrame([result])
        df.to_csv(output, index=False)
        return output.getvalue()
    
    else:  # json
        import json
        return json.dumps(result, indent=2)

# ==================== CREATE LP MODEL ====================
def create_lp_model(obj_coeffs, constraint_matrix, constraint_bounds, constraint_types):
    """
    Membuat model LP dari input
    
    Parameters:
    -----------
    obj_coeffs : list
        Koefisien fungsi objektif
    constraint_matrix : list of lists
        Matriks kendala
    constraint_bounds : list
        RHS dari kendala
    constraint_types : list
        Tipe kendala
    
    Returns:
    --------
    dict : Model representation
    """
    
    model = {
        'objective': obj_coeffs,
        'constraints': constraint_matrix,
        'bounds': constraint_bounds,
        'types': constraint_types,
        'num_variables': len(obj_coeffs),
        'num_constraints': len(constraint_matrix)
    }
    
    return model

# ==================== VALIDATE INPUT ====================
def validate_input(supply=None, demand=None, cost_matrix=None):
    """
    Validasi input untuk transportation problem
    
    Parameters:
    -----------
    supply : list
        Supply array
    demand : list
        Demand array
    cost_matrix : list of lists
        Cost matrix
    
    Returns:
    --------
    tuple : (is_valid, message)
    """
    
    if supply and demand:
        if sum(supply) != sum(demand):
            return False, "⚠️ Total Supply harus sama dengan Total Demand!"
    
    if cost_matrix:
        if len(cost_matrix) == 0 or len(cost_matrix[0]) == 0:
            return False, "⚠️ Cost matrix tidak boleh kosong!"
    
    return True, "✓ Input valid"

# ==================== GENERATE SAMPLE DATA ====================
def generate_sample_lp():
    """Generate sample data untuk Linear Programming"""
    
    return {
        'obj_coeffs': [5, 4],
        'constraints': [[2, 3], [5, 3]],
        'bounds': [60, 100],
        'types': ['<=', '<='],
        'description': 'Contoh: Produksi Mebel'
    }

def generate_sample_transportation():
    """Generate sample data untuk Transportation Problem"""
    
    return {
        'supply': [100, 150, 120],
        'demand': [80, 90, 100],
        'cost': [
            [4, 6, 8],
            [5, 4, 7],
            [6, 5, 4]
        ],
        'description': 'Contoh: Distribusi Barang'
    }

def generate_sample_assignment():
    """Generate sample data untuk Assignment Problem"""
    
    return {
        'cost': [
            [10, 19, 8, 15],
            [10, 18, 7, 17],
            [13, 16, 9, 14],
            [12, 19, 8, 18]
        ],
        'description': 'Contoh: Alokasi Pekerjaan'
    }

# ==================== UTILITY FUNCTIONS ====================
def format_number(num):
    """Format number untuk display"""
    if isinstance(num, float):
        return f"{num:.2f}"
    return str(num)

def get_status_icon(status):
    """Get icon untuk status"""
    status_icons = {
        'Optimal': '✅',
        'Feasible': '✓',
        'Infeasible': '❌',
        'Unbounded': '⚠️',
        'Not Found': '❌',
        'Found': '✅'
    }
    return status_icons.get(status, '❓')
