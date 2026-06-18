import cantera as ct
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# --- 1. USTAWIENIA POCZĄTKOWE ---
os.makedirs('figures', exist_ok=True)
os.makedirs('tables', exist_ok=True)

pressures_bar = [50, 100, 200]  # ciśnienia w komorze
p_ambient = 101325              # Ciśnienie atmosferyczne
g0 = 9.80665                    

of_ratios = np.arange(2.0, 10.0, 0.1)
gas = ct.Solution('h2o2.yaml')
all_results = []

# obliczeni
for p_bar in pressures_bar:
    p_chamber = p_bar * 1e5  
    
    for of in of_ratios:
        gas.TPY = 300, p_chamber, {'H2': 1.0, 'O2': of}
        gas.equilibrate('HP')
        T_c, h_c, s_c = gas.T, gas.enthalpy_mass, gas.entropy_mass
        chamber_composition = gas.X
        
        gas.SPX = s_c, p_ambient, chamber_composition
        T_e_frozen, h_e_frozen, M_e_frozen = gas.T, gas.enthalpy_mass, gas.mean_molecular_weight
        v_e_frozen = np.sqrt(2 * (h_c - h_e_frozen))
        isp_frozen = v_e_frozen / g0
        
        gas.SP = s_c, p_ambient
        gas.equilibrate('SP') 
        T_e_shift, h_e_shift, M_e_shift = gas.T, gas.enthalpy_mass, gas.mean_molecular_weight
        v_e_shift = np.sqrt(2 * (h_c - h_e_shift))
        isp_shift = v_e_shift / g0
        
        all_results.append({
            'Chamber_Pressure_bar': p_bar,
            'O/F': round(of, 2),
            'T_chamber_K': T_c,
            'T_exit_Frozen_K': T_e_frozen,
            'T_exit_Shift_K': T_e_shift,
            'M_exit_Frozen': M_e_frozen,
            'M_exit_Shift': M_e_shift,
            'Velocity_exit_Frozen_m_s': v_e_frozen, 
            'Velocity_exit_Shift_m_s': v_e_shift,   
            'Isp_Frozen_s': isp_frozen,
            'Isp_Equilibrium_s': isp_shift,
            'X_H2O': gas.X[gas.species_index('H2O')],
            'X_H2':  gas.X[gas.species_index('H2')],
            'X_OH':  gas.X[gas.species_index('OH')],
            'X_O2':  gas.X[gas.species_index('O2')],
            'X_H':   gas.X[gas.species_index('H')]
        })

df_all = pd.DataFrame(all_results)
df_all.to_csv('tables/hydrolox_results_all.csv', index=False)

#siatka do wykresów
isp_min = df_all[['Isp_Frozen_s', 'Isp_Equilibrium_s']].min().min() - 10
isp_max = df_all[['Isp_Frozen_s', 'Isp_Equilibrium_s']].max().max() + 25

vel_min = df_all[['Velocity_exit_Frozen_m_s', 'Velocity_exit_Shift_m_s']].min().min() - 100
vel_max = df_all[['Velocity_exit_Frozen_m_s', 'Velocity_exit_Shift_m_s']].max().max() + 250

t_min = df_all[['T_chamber_K', 'T_exit_Frozen_K', 'T_exit_Shift_K']].min().min() - 100
t_max = df_all[['T_chamber_K', 'T_exit_Frozen_K', 'T_exit_Shift_K']].max().max() + 300

m_min = df_all[['M_exit_Frozen', 'M_exit_Shift']].min().min() - 0.5
m_max = df_all[['M_exit_Frozen', 'M_exit_Shift']].max().max() + 0.5

#rysowanie do wykresów
for p_bar in pressures_bar:
    df_p = df_all[df_all['Chamber_Pressure_bar'] == p_bar]
    
    opt_frozen = df_p.loc[df_p['Isp_Frozen_s'].idxmax()]
    opt_eq = df_p.loc[df_p['Isp_Equilibrium_s'].idxmax()]

    # Wykres Isp
    plt.figure(figsize=(8, 5))
    plt.plot(df_p['O/F'], df_p['Isp_Frozen_s'], 'b-', linewidth=2, label='Frozen Flow')
    plt.plot(df_p['O/F'], df_p['Isp_Equilibrium_s'], 'r--', linewidth=2, label='Shifting Eq.')
    plt.plot(opt_frozen['O/F'], opt_frozen['Isp_Frozen_s'], 'bo')
    plt.plot(opt_eq['O/F'], opt_eq['Isp_Equilibrium_s'], 'ro')
    
    plt.text(opt_frozen['O/F'], opt_frozen['Isp_Frozen_s'] - 12, 
             f"Max: {opt_frozen['Isp_Frozen_s']:.1f} s", ha='center', color='blue', fontsize=10)
    plt.text(opt_eq['O/F'], opt_eq['Isp_Equilibrium_s'] + 6, 
             f"Max: {opt_eq['Isp_Equilibrium_s']:.1f} s", ha='center', color='red', fontsize=10)

    plt.ylim(isp_min, isp_max)
    plt.title(f'Specific Impulse vs O/F Ratio (Pc = {p_bar} bar)')
    plt.xlabel('O/F Ratio [-]')
    plt.ylabel('Isp [s]')
    plt.legend()
    plt.grid(True, alpha=0.5)
    plt.tight_layout()
    plt.savefig(f'figures/isp_comparison_{p_bar}bar.png')
    plt.close()

    # Wykres prędkość wylotowa
    plt.figure(figsize=(8, 5))
    plt.plot(df_p['O/F'], df_p['Velocity_exit_Frozen_m_s'], 'b-', linewidth=2, label='Frozen Flow')
    plt.plot(df_p['O/F'], df_p['Velocity_exit_Shift_m_s'], 'r--', linewidth=2, label='Shifting Eq.')
    plt.plot(opt_frozen['O/F'], opt_frozen['Velocity_exit_Frozen_m_s'], 'bo')
    plt.plot(opt_eq['O/F'], opt_eq['Velocity_exit_Shift_m_s'], 'ro')
    
    plt.text(opt_frozen['O/F'], opt_frozen['Velocity_exit_Frozen_m_s'] - 120, 
             f"Max: {opt_frozen['Velocity_exit_Frozen_m_s']:.0f} m/s", ha='center', color='blue', fontsize=10)
    plt.text(opt_eq['O/F'], opt_eq['Velocity_exit_Shift_m_s'] + 60, 
             f"Max: {opt_eq['Velocity_exit_Shift_m_s']:.0f} m/s", ha='center', color='red', fontsize=10)

    plt.ylim(vel_min, vel_max)
    plt.title(f'Exit Velocity vs O/F Ratio (Pc = {p_bar} bar)')
    plt.xlabel('O/F Ratio [-]')
    plt.ylabel('Exit Velocity [m/s]')
    plt.legend()
    plt.grid(True, alpha=0.5)
    plt.tight_layout()
    plt.savefig(f'figures/exit_velocity_{p_bar}bar.png')
    plt.close()

    # Wykres temperatury
    plt.figure(figsize=(8, 5))
    plt.plot(df_p['O/F'], df_p['T_chamber_K'], 'k-', linewidth=2, label='Chamber Temp.')
    plt.plot(df_p['O/F'], df_p['T_exit_Frozen_K'], 'b-', linewidth=2, label='Exit Temp. (Frozen)')
    plt.plot(df_p['O/F'], df_p['T_exit_Shift_K'], 'r--', linewidth=2, label='Exit Temp. (Shifting)')
    
    plt.ylim(t_min, t_max)
    plt.title(f'Temperatures vs O/F Ratio (Pc = {p_bar} bar)')
    plt.xlabel('O/F Ratio [-]')
    plt.ylabel('Temperature [K]')
    plt.legend()
    plt.grid(True, alpha=0.5)
    plt.tight_layout()
    plt.savefig(f'figures/temperatures_{p_bar}bar.png')
    plt.close()

    # Wykres Masy Molowe
    plt.figure(figsize=(8, 5))
    plt.plot(df_p['O/F'], df_p['M_exit_Frozen'], 'b-', linewidth=2, label='Exit Molar Mass (Frozen)')
    plt.plot(df_p['O/F'], df_p['M_exit_Shift'], 'r--', linewidth=2, label='Exit Molar Mass (Shifting)')
    
    plt.ylim(m_min, m_max)
    plt.title(f'Exit Mean Molecular Weight vs O/F (Pc = {p_bar} bar)')
    plt.xlabel('O/F Ratio [-]')
    plt.ylabel('Molecular Weight [kg/kmol]')
    plt.legend()
    plt.grid(True, alpha=0.5)
    plt.tight_layout()
    plt.savefig(f'figures/molar_mass_{p_bar}bar.png')
    plt.close()

    # Wykres Ułamki Molowe
    plt.figure(figsize=(8, 5))
    plt.plot(df_p['O/F'], df_p['X_H2O'], 'g-', linewidth=2, label='H2O')
    plt.plot(df_p['O/F'], df_p['X_H2'], 'c-', linewidth=2, label='H2')
    plt.plot(df_p['O/F'], df_p['X_OH'], 'm-', linewidth=2, label='OH')
    plt.plot(df_p['O/F'], df_p['X_O2'], 'y-', linewidth=2, label='O2')
    plt.plot(df_p['O/F'], df_p['X_H'], 'k:', linewidth=2, label='H (radicals)')
    
    plt.ylim(0, 1.05)
    plt.title(f'Exit Mole Fractions - Shifting Eq. (Pc = {p_bar} bar)')
    plt.xlabel('O/F Ratio [-]')
    plt.ylabel('Mole Fraction [-]')
    plt.legend()
    plt.grid(True, alpha=0.5)
    plt.tight_layout()
    plt.savefig(f'figures/mole_fractions_{p_bar}bar.png')
    plt.close()

# wykres zbiorczy isp
plt.figure(figsize=(10, 6))
colors = ['g', 'b', 'r']

for idx, p_bar in enumerate(pressures_bar):
    df_sub = df_all[df_all['Chamber_Pressure_bar'] == p_bar]
    opt_sub = df_sub.loc[df_sub['Isp_Equilibrium_s'].idxmax()]
    
    plt.plot(df_sub['O/F'], df_sub['Isp_Equilibrium_s'], 
             color=colors[idx], linewidth=2, label=f'Pc = {p_bar} bar')
    plt.plot(opt_sub['O/F'], opt_sub['Isp_Equilibrium_s'], marker='o', color=colors[idx])
    
    plt.text(opt_sub['O/F'], opt_sub['Isp_Equilibrium_s'] + 3, 
             f"{opt_sub['Isp_Equilibrium_s']:.1f} s", ha='center', color=colors[idx], fontsize=10, fontweight='bold')

plt.ylim(isp_min, isp_max)
plt.title('Influence of Chamber Pressure on Specific Impulse (Shifting Eq.)', fontsize=14)
plt.xlabel('O/F Ratio [-]', fontsize=12)
plt.ylabel('Isp [s]', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.5)
plt.tight_layout()
plt.savefig('figures/isp_pressure_sweep.png')
plt.close()

print("Calculations complete")