from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

HARTREE_TO_KJ = 2625.49962   # 1Eh → kJ·mol-1

csv_file = Path("totalscandata.csv")     
df = pd.read_csv(csv_file)


col_R       = [c for c in df.columns if c.strip().lower().startswith("r")][0]
col_ub3     = [c for c in df.columns if "b3lyp" in c.lower()][0]
col_uhf     = [c for c in df.columns if "uhf"   in c.lower()][0]
col_uccsd   = [c for c in df.columns if "uccsd" in c.lower()][0]


def to_relative_kj(series):

    if (series < 0).all() and series.min() < -10:
        rel = (series - series.min()) * HARTREE_TO_KJ
    else:  
        rel = series - series.min()
    return rel

rel_ub3   = to_relative_kj(df[col_ub3].astype(float))
rel_uhf   = to_relative_kj(df[col_uhf].astype(float))
rel_uccsd = to_relative_kj(df[col_uccsd].astype(float))

R = df[col_R].astype(float)


plt.figure(figsize=(8,4.5))
plt.plot(R, rel_ub3,   color="#F0A500", label="UB3LYP/cc-pVTZ")
plt.plot(R, rel_uhf,   color="#0095FF", label="UHF/cc-pVTZ")
plt.plot(R, rel_uccsd, color="#00B89A", label="UCCSD/cc-pVTZ")

plt.xlabel("R (Å)")
plt.ylabel("E − E_min (kJ/mol)")
plt.legend()
plt.tight_layout()

out_png = "UHF-UB3LYP-UCCSD.png"
plt.savefig(out_png, dpi=200)
plt.show()

print(f"图已保存：{out_png}")
