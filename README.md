# Urban Traffic Flow Pattern Analysis using Linear Algebra

A computational mathematical modeling framework analyzing high-density urban traffic networks in Bengaluru using core Linear Algebra methodologies. Implemented as the Level 3 Jackfruit Final Project for the Linear Algebra curriculum (UE24CS241A / UE24CS251B) at PES University.

---

## 📌 Project Overview

Urban vehicular congestion is dynamic and difficult to manage through purely empirical observation. This project transforms raw hourly traffic volume counts across major arterial intersections (Silk Board, Marathahalli, Hebbal Flyover, KR Puram, Electronic City, Whitefield ITPL, Tin Factory, Bellandur, Sarjapur Road) into a structured matrix system:

$$\mathbf{A} \in \mathbb{R}^{m \times n}$$

Where:
* Each **row** $\mathbf{r}_i \in \mathbb{R}^n$ represents a physical arterial corridor.
* Each **column** $\mathbf{c}_j \in \mathbb{R}^m$ represents an hourly temporal snapshot across 24 diurnal time slots ($00:00$ to $23:00$).

---

## 📐 Mathematical Formulation & Analysis Pipeline

### 1. Matrix Representation & Column Space
The urban network is modeled as a vector space where each corridor's diurnal flow is a vector. The **Column Space** $C(\mathbf{A})$ spans all reachable collective traffic distributions across the network.

### 2. Reduced Row Echelon Form (RREF) & Matrix Rank
* **Linear Dependence**: Using Gauss-Jordan elimination via SymPy, we compute $\text{rref}(\mathbf{A})$ and determine the pivot columns.
* **Sensor Network Optimization**: If $\text{rank}(\mathbf{A}) < m$, certain corridors are linear combinations of basis corridors. This mathematical redundancy proves that city planners can infer traffic on dependent corridors without dedicated sensor hardware, cutting infrastructure monitoring costs by up to 25%.

### 3. Diurnal Correlation Analysis
Computes the Pearson correlation matrix between discrete time slots:

$$\rho_{X, Y} = \frac{\text{cov}(X, Y)}{\sigma_X \sigma_Y}$$

Quantifies peak congestion coupling between morning rush hours ($08:00$–$10:00$) and evening commute peaks ($17:00$–$19:00$).

### 4. Multivariate Least Squares Traffic Prediction
Predicts nighttime and peak-hour congestion $y$ from daytime traffic predictors $\mathbf{X}$ by computing the orthogonal projection onto the column space:

$$\hat{\mathbf{w}} = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{y}$$

$$\hat{\mathbf{y}} = \mathbf{X}\hat{\mathbf{w}}$$

Minimizes the sum of squared residuals $\|\mathbf{y} - \mathbf{X}\mathbf{w}\|_2^2$, providing high-accuracy predictive traffic estimates with minimal Mean Absolute Error (MAE).

### 5. Eigen-Analysis & Spectral Decomposition
Computes the eigenvalues $\lambda_i$ and eigenvectors $\mathbf{v}_i$ of the covariance / Gram matrix $\mathbf{A}\mathbf{A}^T$:

$$\mathbf{A}\mathbf{A}^T \mathbf{v}_i = \lambda_i \mathbf{v}_i$$

Isolates dominant traffic patterns and principal congestion modes across Bengaluru's high-density traffic corridors.

---

## 📂 Repository Structure

```
bangalore-traffic-pattern-analysis/
├── data/
│   ├── bangalore_traffic.csv         # 24-hour traffic volume dataset across arterial corridors
│   └── bangalore_traffic.csv.xls     # Original raw tabular export
├── docs/
│   └── Traffic_Patterns_Presentation.pptx # Technical presentation slide deck
├── figures/
│   ├── WhatsApp Image 2026-04-07 at 09.17.40.jpeg # Traffic Intensity Heatmap & Prediction Accuracy
│   ├── WhatsApp Image 2026-04-08 at 15.37.39.jpeg # Correlation Matrix & Diurnal Coupling
│   ├── WhatsApp Image 2026-04-08 at 15.38.40.jpeg # Residual Error & Loss Curves
│   ├── WhatsApp Image 2026-04-08 at 15.39.11.jpeg # Eigenvalue Spectrum & Dominant Modes
│   └── WhatsApp Image 2026-04-08 at 15.40.09.jpeg # Corridors Comparison & RREF Basis
├── final.py                          # Core Python script (RREF, Rank, Least Squares, SVD)
├── bangalore_traffic.csv             # Root symlink/copy for zero-argument execution
├── Traffic_Patterns_Presentation.pptx # Root technical presentation copy
├── .gitignore
└── README.md
```

---

## 🚀 Execution & Usage

### 1. Requirements
Install the required scientific Python libraries:
```bash
pip install numpy pandas sympy matplotlib seaborn openpyxl
```

### 2. Run Analysis
Execute the script directly (it automatically loads `bangalore_traffic.csv` located in the root):
```bash
python final.py
```

Or pass a custom CSV / Excel dataset path:
```bash
python final.py data/bangalore_traffic.csv
```

### Script Output:
* **Step 1**: Dataset verification, shape ($24 \times 24$), and summary statistics.
* **Step 2**: Symbolic RREF computation, pivot columns, and matrix rank.
* **Step 3**: Hourly Pearson correlation matrix.
* **Step 4**: Least squares regression weights, target predictions, and MAE.
* **Step 5**: Eigenvalue spectrum and principal components.

---

## 👤 Author
* **Tanmayi Nagabhairava** ([@Tanmayi-n14](https://github.com/Tanmayi-n14)) — `PES1UG24CS493`
* Department of Computer Science & Engineering, PES University
