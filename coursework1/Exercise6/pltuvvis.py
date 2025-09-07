import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = {
    "State":       [1,      2,      3,      4,      5],
    "E_TD_eV":     [7.2259, 8.6013, 9.5526, 9.6056, 9.6819],
    "Lambda_TD":   [171.58, 144.15, 129.79, 129.08, 128.06], # nm
    "f_TD":        [0.0005, 0.0649, 0.0149, 0.0425, 0.0324],
    "E_CIS_eV":    [8.9807, 10.7887, 11.5467, 11.8369, 12.3579],
    "Lambda_CIS":  [138.06, 114.92, 107.38, 104.74, 100.33], # nm
    "f_CIS":       [0.0,    0.1599, 0.0169, 0.0344, 0.1985],
}
df = pd.DataFrame(data)


FWHM_nm = 10.0          # 半高全宽，nm；可调成 15–30 看着更宽
sigma_nm = FWHM_nm / (2*np.sqrt(2*np.log(2)))   # 高斯 σ
λ_grid = np.linspace(80, 180, 8000)             # 绘图波长范围（nm）

def make_spectrum(lambdas, osc_strengths, grid, sigma):
    """返回给定网格上的连续光谱（单位：相对强度）。"""
    inten = np.zeros_like(grid)
    for lam, f in zip(lambdas, osc_strengths):
        inten += f * np.exp(-(grid - lam)**2 / (2*sigma**2))
    return inten / inten.max()   # 归一化到 1


spec_td  = make_spectrum(df["Lambda_TD"],  df["f_TD"],  λ_grid, sigma_nm)
spec_cis = make_spectrum(df["Lambda_CIS"], df["f_CIS"], λ_grid, sigma_nm)


plt.figure(figsize=(8, 4))


plt.plot(λ_grid, spec_td,  label="TD-TDA",  linewidth=1.6)
plt.plot(λ_grid, spec_cis, label="CIS",     linewidth=1.6)

for idx, row in df.iterrows():
    plt.vlines(row["Lambda_TD"], 0, row["f_TD"]/max(df["f_TD"]), color="#1f77b4", alpha=0.4)
    plt.vlines(row["Lambda_CIS"], 0, row["f_CIS"]/max(df["f_CIS"]), color="#ff7f0e", alpha=0.4)

#plt.gca().invert_xaxis()                # 光谱惯例：短波在左
plt.xlabel("Wavelength / nm")
plt.ylabel("Relative Intensity (a.u.)")
plt.title("Simulated UV/Vis Spectra (Gaussian TD-TDA vs CIS)")
plt.legend()
plt.tight_layout()
plt.show()
