import argparse
from datetime import datetime

import numpy as np
import pandas as pd
from pathlib import Path
from sympy import Matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Default dataset
_DEFAULT_DATA = Path(__file__).resolve().parent / "bangalore_traffic.csv"




def _parse_args():
    p = argparse.ArgumentParser(
        description="Traffic analysis: load counts from CSV or Excel, print stats, show plots."
    )
    p.add_argument(
        "data",
        nargs="?",
        default=None,
        help=f"path to .csv or .xlsx (default: {_DEFAULT_DATA.name} next to this script)",
    )
    return p.parse_args()


def load_traffic_file(path: Path) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(
            f"Missing file: {path}. Put traffic_data.csv next to this script, "
            f"or run: python traffic.py path\\to\\file.csv"
        )

    suffix = path.suffix.lower()

    if suffix == ".csv":
        raw = pd.read_csv(path, index_col=0)

    elif suffix in (".xlsx", ".xls"):
        try:
            raw = pd.read_excel(path, index_col=0, engine="openpyxl")
        except ImportError as e:
            raise ImportError(
                "Install openpyxl to read .xlsx files: pip install openpyxl"
            ) from e
    else:
        raise ValueError(f"Unsupported file type {suffix!r}; use .csv, .xlsx, or .xls.")

    # Clean labels
    raw.index = raw.index.map(lambda x: str(x).strip().lstrip("="))
    raw.columns = [str(c).strip().lstrip("=") for c in raw.columns]

    # Detect column type
    use_cols = list(raw.columns)

    # Convert to numeric
    df = raw[use_cols].apply(pd.to_numeric, errors="coerce")

    if df.isna().any().any():
        raise ValueError(
            f"{path.name} has non-numeric or empty cells in the data block."
        )

    if df.shape[1] < 2:
        raise ValueError(f"{path.name} needs at least 2 numeric time columns.")

    return df


# -----------------------------
# MAIN EXECUTION
# -----------------------------
_args = _parse_args()
data_path = Path(_args.data).resolve() if _args.data else _DEFAULT_DATA

# -----------------------------
# STEP 1: DATASET
# -----------------------------

print("\n===== STEP 1: DATASET =====")
print(f"Loading: {data_path}")

df = load_traffic_file(data_path)

roads = df.index.tolist()
time_slots = list(df.columns)

mtime = datetime.fromtimestamp(data_path.stat().st_mtime)

print(
    f"Rows x columns: {df.shape[0]} x {df.shape[1]}  |  "
    f"file last modified: {mtime:%Y-%m-%d %H:%M:%S}"
)

print(df)

A = df.values


# -----------------------------
# STEP 2: RREF & RANK
# -----------------------------
print("\n===== STEP 2: RREF & RANK =====")

M = Matrix(A)
rref_matrix, pivots = M.rref()

rank = np.linalg.matrix_rank(A)

print("Rank:", rank)
print("Pivot columns:", pivots)


# -----------------------------
# STEP 3: CORRELATION
# -----------------------------
print("\n===== STEP 3: CORRELATION =====")

corr = df.corr(numeric_only=True)
print(corr)


# -----------------------------
# STEP 4: LEAST SQUARES
# -----------------------------
print("\n===== STEP 4: LEAST SQUARES =====")

X = A[:, :-1]   # all except last column
y = A[:, -1]    # last column

target_name = time_slots[-1]

coeffs, _, _, _ = np.linalg.lstsq(X, y, rcond=None)

prediction = X @ coeffs

error = np.mean(np.abs(prediction - y))

print(f"Target: {target_name}")
print("Coefficients:", coeffs)
print("Mean absolute error:", error)


# -----------------------------
# STEP 5: EIGEN ANALYSIS
# -----------------------------
print("\n===== STEP 5: EIGEN ANALYSIS =====")

# Use correlation matrix (square matrix)
eigenvalues, eigenvectors = np.linalg.eigh(corr.values.astype(float))

print("Eigenvalues:", np.round(eigenvalues, 2))


# -----------------------------
# STEP 6: VISUALIZATION
# -----------------------------

# Heatmap
nr, nc = df.shape
plt.figure(figsize=(max(10, nc * 0.4), max(6, nr * 0.35)))

sns.heatmap(df, annot=False)

plt.title("Traffic Heatmap")
plt.tight_layout()
plt.show()


# Correlation Heatmap
plt.figure(figsize=(10, 8))

sns.heatmap(corr, annot=False)

plt.title("Correlation Between Time Slots")
plt.tight_layout()
plt.show()


# Prediction vs Actual
plt.figure(figsize=(max(10, len(roads) * 0.4), 6))

x = np.arange(len(roads))

plt.bar(x - 0.2, y, 0.4, label="Actual")
plt.bar(x + 0.2, prediction, 0.4, label="Predicted")

plt.xticks(x, roads, rotation=45, ha="right")

plt.title(f"Prediction vs Actual ({target_name})")
plt.legend()
plt.tight_layout()
plt.show()


# Line graph (limit legend if too many roads)
plt.figure(figsize=(10, 6))

for i in range(len(roads)):
    plt.plot(time_slots, A[i], marker="o", markersize=2)

if len(roads) <= 15:
    plt.legend(roads, fontsize=8)

plt.title("Traffic Trends")
plt.grid()
plt.tight_layout()
plt.show()


# -----------------------------
# FINAL RESULT
# -----------------------------
print("\n===== FINAL RESULT =====")

nrow, ncol = A.shape

if rank < min(nrow, ncol):
    print("Linear dependency exists in data.")
else:
    print("Full rank data (independent columns).")

print(f"Prediction error ≈ {error:.2f}")
print("Eigenvalues indicate dominant traffic patterns.")