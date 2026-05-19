"""
Solver Module untuk berbagai masalah Operation Research
========================================================

Module ini berisi implementasi solver untuk:
- Linear Programming
- Transportation Problem
- Assignment Problem
- Shortest Path Problem
"""

import math
import numpy as np
from scipy.optimize import linprog
from scipy.optimize import linear_sum_assignment
from pulp import *
import pandas as pd

# ==================== LINEAR PROGRAMMING SOLVER ====================
def linear_programming_solver(obj_coeffs, constraint_matrix, constraint_bounds, 
                               constraint_types, prob_type="MAX"):
    """
    Menyelesaikan masalah Linear Programming menggunakan PuLP
    
    Parameters:
    -----------
    obj_coeffs : list
        Koefisien fungsi objektif
    constraint_matrix : list of lists
        Matriks kendala
    constraint_bounds : list
        RHS dari setiap kendala
    constraint_types : list
        Tipe kendala (<=, =, >=)
    prob_type : str
        "MAX" untuk maksimasi, "MIN" untuk minimasi
    
    Returns:
    --------
    dict : Hasil optimasi dengan nilai optimal dan nilai variabel
    """
    
    num_vars = len(obj_coeffs)
    
    # Membuat problem
    if prob_type == "MAX":
        prob = LpProblem("OR_Problem", LpMaximize)
    else:
        prob = LpProblem("OR_Problem", LpMinimize)
    
    # Membuat variabel keputusan
    x = [LpVariable(f"x{i+1}", lowBound=0) for i in range(num_vars)]
    
    # Fungsi objektif
    prob += lpSum([obj_coeffs[i] * x[i] for i in range(num_vars)]), "Objective"
    
    # Kendala
    for c_idx, constraint in enumerate(constraint_matrix):
        expr = lpSum([constraint[i] * x[i] for i in range(num_vars)])
        
        if constraint_types[c_idx] == "<=":
            prob += expr <= constraint_bounds[c_idx], f"Constraint_{c_idx+1}"
        elif constraint_types[c_idx] == "=":
            prob += expr == constraint_bounds[c_idx], f"Constraint_{c_idx+1}"
        elif constraint_types[c_idx] == ">=":
            prob += expr >= constraint_bounds[c_idx], f"Constraint_{c_idx+1}"
    
    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))
    
    # Ekstrak hasil
    result = {
        "status": LpStatus[prob.status],
        "optimal_value": value(prob.objective),
        "variables": {x[i].name: x[i].varValue for i in range(num_vars)},
        "problem_type": prob_type,
        "num_variables": num_vars,
        "num_constraints": len(constraint_matrix)
    }
    
    return result

# ==================== TRANSPORTATION PROBLEM SOLVER ====================
def transportation_problem_solver(supply, demand, cost_matrix):
    """
    Menyelesaikan Transportation Problem
    
    Parameters:
    -----------
    supply : list
        Supply di setiap sumber
    demand : list
        Demand di setiap tujuan
    cost_matrix : list of lists
        Matriks biaya transportasi
    
    Returns:
    --------
    dict : Solusi optimal dengan allocation matrix dan total cost
    """
    
    num_sources = len(supply)
    num_destinations = len(demand)
    
    # Buat problem
    prob = LpProblem("Transportation_Problem", LpMinimize)
    
    # Variabel keputusan: x[i,j] = jumlah unit dari sumber i ke tujuan j
    x = {}
    for i in range(num_sources):
        for j in range(num_destinations):
            x[(i, j)] = LpVariable(f"x_{i}_{j}", lowBound=0, cat='Continuous')
    
    # Fungsi objektif: minimize total cost
    prob += lpSum([cost_matrix[i][j] * x[(i, j)] 
                   for i in range(num_sources) 
                   for j in range(num_destinations)]), "Total_Cost"
    
    # Constraint supply: total yang dikirim dari sumber i = supply[i]
    for i in range(num_sources):
        prob += lpSum([x[(i, j)] for j in range(num_destinations)]) == supply[i], f"Supply_{i}"
    
    # Constraint demand: total yang diterima di tujuan j = demand[j]
    for j in range(num_destinations):
        prob += lpSum([x[(i, j)] for i in range(num_sources)]) == demand[j], f"Demand_{j}"
    
    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))
    
    # Ekstrak hasil
    allocation = np.zeros((num_sources, num_destinations))
    for i in range(num_sources):
        for j in range(num_destinations):
            allocation[i][j] = x[(i, j)].varValue if x[(i, j)].varValue else 0
    
    result = {
        "status": LpStatus[prob.status],
        "total_cost": value(prob.objective),
        "allocation": allocation.tolist(),
        "num_sources": num_sources,
        "num_destinations": num_destinations,
        "supply": supply,
        "demand": demand
    }
    
    return result

# ==================== ASSIGNMENT PROBLEM SOLVER ====================
def assignment_problem_solver(cost_matrix):
    """
    Menyelesaikan Assignment Problem menggunakan Hungarian Algorithm
    
    Parameters:
    -----------
    cost_matrix : list of lists
        Matriks biaya assignment
    
    Returns:
    --------
    dict : Solusi optimal dengan assignment dan total cost
    """
    
    cost_array = np.array(cost_matrix)
    
    # Gunakan linear_sum_assignment (Hungarian algorithm)
    row_ind, col_ind = linear_sum_assignment(cost_array)
    
    total_cost = cost_array[row_ind, col_ind].sum()
    
    result = {
        "status": "Optimal",
        "total_cost": float(total_cost),
        "assignment": list(zip(row_ind.tolist(), col_ind.tolist())),
        "assignment_cost": cost_array[row_ind, col_ind].tolist(),
        "matrix_size": len(cost_matrix)
    }
    
    return result

# ==================== SHORTEST PATH SOLVER ====================
def shortest_path_solver(graph, start, end):
    """
    Menyelesaikan Shortest Path Problem menggunakan Dijkstra Algorithm
    
    Parameters:
    -----------
    graph : dict
        Graph representation sebagai adjacency list
    start : node
        Node awal
    end : node
        Node tujuan
    
    Returns:
    --------
    dict : Path terpendek dan total jarak
    """
    
    from heapq import heappush, heappop
    
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}
    pq = [(0, start)]
    
    while pq:
        current_distance, current_node = heappop(pq)
        
        if current_distance > distances[current_node]:
            continue
        
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heappush(pq, (distance, neighbor))
    
    # Reconstruct path
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    
    result = {
        "status": "Found" if distances[end] != float('inf') else "Not Found",
        "path": path,
        "distance": distances[end],
        "start": start,
        "end": end
    }
    
    return result

# ==================== SENSITIVITY ANALYSIS ====================
def sensitivity_analysis(lp_result):
    """
    Melakukan analisis sensitivitas terhadap hasil LP
    
    Parameters:
    -----------
    lp_result : dict
        Hasil dari linear_programming_solver
    
    Returns:
    --------
    dict : Informasi sensitivitas
    """
    
    # Implementasi sederhana
    sensitivity = {
        "objective_value": lp_result["optimal_value"],
        "variables": lp_result["variables"],
        "analysis": "Detailed sensitivity analysis can be extended here"
    }
    
    return sensitivity

# ==================== INTEGER PROGRAMMING SOLVER ====================
def integer_programming_solver(obj_coeffs, constraint_matrix, constraint_bounds, 
                                 constraint_types, prob_type="MAX", var_types=None):
    """
    Menyelesaikan masalah Integer Programming menggunakan PuLP
    
    Parameters:
    -----------
    obj_coeffs : list
        Koefisien fungsi objektif
    constraint_matrix : list of lists
        Matriks kendala
    constraint_bounds : list
        RHS dari setiap kendala
    constraint_types : list
        Tipe kendala (<=, =, >=)
    prob_type : str
        "MAX" untuk maksimasi, "MIN" untuk minimasi
    var_types : list, optional
        Tipe variabel ('Integer', 'Binary', atau 'Continuous')
    
    Returns:
    --------
    dict : Hasil optimasi dengan nilai optimal dan nilai variabel
    """
    
    num_vars = len(obj_coeffs)
    
    # Membuat problem
    if prob_type == "MAX":
        prob = LpProblem("Integer_Programming_Problem", LpMaximize)
    else:
        prob = LpProblem("Integer_Programming_Problem", LpMinimize)
    
    # Membuat variabel keputusan
    if var_types is None:
        var_types = ['Integer'] * num_vars
    
    variables = []
    for i in range(num_vars):
        if var_types[i] == 'Binary':
            var = LpVariable(f"x{i+1}", 0, 1, LpInteger)
        elif var_types[i] == 'Integer':
            var = LpVariable(f"x{i+1}", lowBound=0, cat=LpInteger)
        else:  # Continuous
            var = LpVariable(f"x{i+1}", lowBound=0)
        variables.append(var)
    
    # Menambahkan fungsi objektif
    prob += lpSum([obj_coeffs[i] * variables[i] for i in range(num_vars)])
    
    # Menambahkan kendala
    for i, constraint in enumerate(constraint_matrix):
        lhs = lpSum([constraint[j] * variables[j] for j in range(num_vars)])
        rhs = constraint_bounds[i]
        constraint_type = constraint_types[i]
        
        if constraint_type == "<=":
            prob += lhs <= rhs
        elif constraint_type == "=":
            prob += lhs == rhs
        elif constraint_type == ">=":
            prob += lhs >= rhs
    
    # Menyelesaikan problem
    status = prob.solve()
    
    # Mengumpulkan hasil
    result = {
        "status": LpStatus[status],
        "optimal_value": value(prob.objective),
        "variables": {f"x{i+1}": value(var) for i, var in enumerate(variables)},
        "solution_time": None,
        "iterations": None
    }
    
    return result

# ==================== QUEUE THEORY SOLVER ====================
def queue_theory_solver(arrival_rate, service_rate, num_servers=1, queue_type="M/M/1",
                         service_cost_per_server=0.0, waiting_cost_per_customer=0.0):
    """
    Menyelesaikan masalah Teori Antrian
    
    Parameters:
    -----------
    arrival_rate : float
        Tingkat kedatangan pelanggan (λ)
    service_rate : float
        Tingkat pelayanan (μ)
    num_servers : int
        Jumlah server
    queue_type : str
        Tipe antrian (M/M/1, M/M/c, dll.)
    service_cost_per_server : float
        Biaya pelayanan per server per jam
    waiting_cost_per_customer : float
        Biaya tunggu per pelanggan per jam
    
    Returns:
    --------
    dict : Hasil analisis antrian
    """
    
    if queue_type == "M/M/1":
        # M/M/1 Queue Model
        utilization = arrival_rate / service_rate
        if utilization >= 1:
            return {"error": "System unstable - utilization >= 1", "status": "Error"}
        
        # Probabilitas sistem kosong
        p0 = 1 - utilization
        
        # Rata-rata jumlah pelanggan dalam sistem
        l = utilization / (1 - utilization)
        
        # Rata-rata waktu tunggu dalam sistem
        w = 1 / (service_rate - arrival_rate)
        
        # Rata-rata waktu tunggu dalam antrian
        wq = utilization * w
        
        # Rata-rata panjang antrian
        lq = utilization * l
        
        service_cost = num_servers * service_cost_per_server
        waiting_cost = lq * waiting_cost_per_customer
        total_cost = service_cost + waiting_cost
        
        result = {
            "status": "Success",
            "queue_type": "M/M/1",
            "num_servers": num_servers,
            "utilization_factor": utilization,
            "probability_empty": p0,
            "avg_customers_system": l,
            "avg_customers_queue": lq,
            "avg_waiting_time_system": w,
            "avg_waiting_time_queue": wq,
            "service_cost_per_hour": service_cost,
            "waiting_cost_per_hour": waiting_cost,
            "total_cost_per_hour": total_cost
        }
        
    elif queue_type == "M/M/c":
        # M/M/c Queue Model (multiple servers)
        utilization = arrival_rate / (num_servers * service_rate)
        if utilization >= 1:
            return {"error": "System unstable - utilization >= 1", "status": "Error"}
        
        # Probabilitas sistem kosong
        a = arrival_rate / service_rate
        p0 = 1 / (sum([(a)**k / math.factorial(k) for k in range(num_servers)]) + 
                 (a**num_servers) / (math.factorial(num_servers) * (1 - utilization)))
        
        # Rata-rata panjang antrian
        lq = (p0 * a**num_servers * utilization) / (math.factorial(num_servers) * (1 - utilization)**2)
        
        # Rata-rata jumlah pelanggan dalam sistem
        l = lq + a
        
        # Rata-rata waktu tunggu dalam sistem
        w = l / arrival_rate
        
        # Rata-rata waktu tunggu dalam antrian
        wq = lq / arrival_rate
        
        service_cost = num_servers * service_cost_per_server
        waiting_cost = lq * waiting_cost_per_customer
        total_cost = service_cost + waiting_cost
        
        result = {
            "status": "Success",
            "queue_type": f"M/M/{num_servers}",
            "num_servers": num_servers,
            "utilization_factor": utilization,
            "probability_empty": p0,
            "avg_customers_system": l,
            "avg_customers_queue": lq,
            "avg_waiting_time_system": w,
            "avg_waiting_time_queue": wq,
            "service_cost_per_hour": service_cost,
            "waiting_cost_per_hour": waiting_cost,
            "total_cost_per_hour": total_cost
        }
    
    else:
        result = {"error": f"Queue type {queue_type} not implemented", "status": "Error"}
    
    return result

# ==================== MONTE CARLO SIMULATION ====================
def monte_carlo_simulation(num_simulations, distribution_type, params, 
                          target_function=None):
    """
    Melakukan simulasi Monte Carlo
    
    Parameters:
    -----------
    num_simulations : int
        Jumlah simulasi yang akan dilakukan
    distribution_type : str
        Tipe distribusi ('normal', 'uniform', 'exponential', dll.)
    params : dict
        Parameter distribusi
    target_function : callable, optional
        Fungsi yang akan dievaluasi pada setiap simulasi
    
    Returns:
    --------
    dict : Hasil simulasi Monte Carlo
    """
    
    np.random.seed(42)  # Untuk reproducibility
    
    # Generate random samples
    if distribution_type == 'normal':
        samples = np.random.normal(params['mean'], params['std'], num_simulations)
    elif distribution_type == 'uniform':
        samples = np.random.uniform(params['low'], params['high'], num_simulations)
    elif distribution_type == 'exponential':
        samples = np.random.exponential(params['scale'], num_simulations)
    elif distribution_type == 'poisson':
        samples = np.random.poisson(params['lam'], num_simulations)
    else:
        return {"error": f"Distribution {distribution_type} not supported", "status": "Error"}
    
    # Hitung statistik dasar
    mean = np.mean(samples)
    std = np.std(samples)
    min_val = np.min(samples)
    max_val = np.max(samples)
    
    # Hitung confidence interval (95%)
    confidence_level = 0.95
    z_score = 1.96  # untuk 95% confidence
    margin_error = z_score * (std / np.sqrt(num_simulations))
    ci_lower = mean - margin_error
    ci_upper = mean + margin_error
    
    # Jika ada target function, evaluasi
    if target_function:
        try:
            function_values = [target_function(x) for x in samples]
            function_mean = np.mean(function_values)
            function_std = np.std(function_values)
        except Exception as e:
            return {"error": f"Error evaluating target function: {str(e)}", "status": "Error"}
    else:
        function_values = None
        function_mean = None
        function_std = None
    
    result = {
        "status": "Success",
        "num_simulations": num_simulations,
        "distribution": distribution_type,
        "parameters": params,
        "statistics": {
            "mean": mean,
            "std_dev": std,
            "min": min_val,
            "max": max_val,
            "confidence_interval": {
                "level": confidence_level,
                "lower": ci_lower,
                "upper": ci_upper
            }
        },
        "samples": samples[:1000].tolist() if len(samples) > 1000 else samples.tolist(),  # Limit untuk display
        "function_results": {
            "values": function_values[:1000].tolist() if function_values and len(function_values) > 1000 else function_values,
            "mean": function_mean,
            "std_dev": function_std
        } if target_function else None
    }
    
    return result

# ==================== CLASSIFICATION SOLVER ====================
def classification_solver(X_train, y_train, X_test, algorithm='logistic_regression', 
                         params=None):
    """
    Melakukan klasifikasi menggunakan berbagai algoritma machine learning
    
    Parameters:
    -----------
    X_train : array-like
        Data training features
    y_train : array-like
        Data training labels
    X_test : array-like
        Data test features
    algorithm : str
        Algoritma klasifikasi ('logistic_regression', 'svm', 'random_forest', 'knn')
    params : dict, optional
        Parameter khusus algoritma
    
    Returns:
    --------
    dict : Hasil klasifikasi
    """
    
    try:
        from sklearn.linear_model import LogisticRegression
        from sklearn.svm import SVC
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.neighbors import KNeighborsClassifier
        from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
        from sklearn.model_selection import train_test_split
    except ImportError:
        return {"error": "scikit-learn not installed. Please install with: pip install scikit-learn", "status": "Error"}
    
    # Default parameters
    if params is None:
        params = {}
    
    # Pilih algoritma
    if algorithm == 'logistic_regression':
        model = LogisticRegression(**params)
    elif algorithm == 'svm':
        model = SVC(**params)
    elif algorithm == 'random_forest':
        model = RandomForestClassifier(**params)
    elif algorithm == 'knn':
        model = KNeighborsClassifier(**params)
    else:
        return {"error": f"Algorithm {algorithm} not supported"}
    
    # Training
    model.fit(X_train, y_train)
    
    # Prediction
    y_pred = model.predict(X_test)
    
    # Evaluasi
    accuracy = accuracy_score(y_train, model.predict(X_train))  # Training accuracy
    test_predictions = y_pred
    
    # Classification report
    try:
        report = classification_report(y_train, model.predict(X_train), output_dict=True)
    except:
        report = "Could not generate classification report"
    
    # Confusion matrix
    try:
        cm = confusion_matrix(y_train, model.predict(X_train)).tolist()
    except:
        cm = "Could not generate confusion matrix"
    
    result = {
        "status": "Success",
        "algorithm": algorithm,
        "parameters": params,
        "training_accuracy": accuracy,
        "predictions": test_predictions.tolist() if hasattr(test_predictions, 'tolist') else test_predictions,
        "classification_report": report,
        "confusion_matrix": cm,
        "model_info": str(model)
    }
    
    return result

# ==================== CLUSTERING SOLVER ====================
def clustering_solver(X, n_clusters, algorithm='kmeans', params=None):
    """
    Melakukan clustering menggunakan berbagai algoritma
    
    Parameters:
    -----------
    X : array-like
        Data untuk clustering
    n_clusters : int
        Jumlah cluster
    algorithm : str
        Algoritma clustering ('kmeans', 'hierarchical', 'dbscan')
    params : dict, optional
        Parameter khusus algoritma
    
    Returns:
    --------
    dict : Hasil clustering
    """
    
    try:
        from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
        from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
        import matplotlib.pyplot as plt
    except ImportError:
        return {"error": "scikit-learn not installed. Please install with: pip install scikit-learn matplotlib", "status": "Error"}
    
    # Default parameters
    if params is None:
        params = {}
    
    # Pilih algoritma
    if algorithm == 'kmeans':
        model = KMeans(n_clusters=n_clusters, **params)
    elif algorithm == 'hierarchical':
        model = AgglomerativeClustering(n_clusters=n_clusters, **params)
    elif algorithm == 'dbscan':
        model = DBSCAN(**params)
    else:
        return {"error": f"Algorithm {algorithm} not supported"}
    
    # Fitting
    labels = model.fit_predict(X)
    
    # Evaluasi (hanya untuk algoritma yang mendukung)
    silhouette = None
    ch_score = None
    db_score = None
    
    try:
        if len(np.unique(labels)) > 1 and len(np.unique(labels)) < len(X):
            silhouette = silhouette_score(X, labels)
            ch_score = calinski_harabasz_score(X, labels)
            db_score = davies_bouldin_score(X, labels)
    except:
        pass
    
    # Hitung ukuran cluster
    unique_labels, counts = np.unique(labels, return_counts=True)
    cluster_sizes = dict(zip(unique_labels.tolist(), counts.tolist()))
    
    # Hitung centroid (untuk K-means)
    centroids = None
    if algorithm == 'kmeans':
        centroids = model.cluster_centers_.tolist()
    
    result = {
        "status": "Success",
        "algorithm": algorithm,
        "n_clusters": n_clusters,
        "parameters": params,
        "labels": labels.tolist(),
        "cluster_sizes": cluster_sizes,
        "centroids": centroids,
        "evaluation_metrics": {
            "silhouette_score": silhouette,
            "calinski_harabasz_score": ch_score,
            "davies_bouldin_score": db_score
        },
        "model_info": str(model)
    }
    
    return result
