# MKWS 2026 – Comparative Analysis of Expansion Models in LOX/LH2 Rocket Engines

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Cantera](https://img.shields.io/badge/Cantera-3.0+-orange.svg)
![LaTeX](https://img.shields.io/badge/LaTeX-Report-red.svg)

This repository contains the computational research conducted for the **"Computer Methods in Combustion" (MKWS 2026)** course. The project investigates the performance of a liquid oxygen/liquid hydrogen (LOX/LH2) rocket engine by comparing two fundamental thermodynamic nozzle expansion models: **Frozen Flow** and **Shifting Equilibrium**.

---

## 📑 Table of Contents
* [Scientific Scope](#-scientific-scope)
* [System Assumptions](#-system-assumptions)
* [Requirements](#-requirements)
* [Usage](#-usage)
* [File Structure](#-file-structure)
* [Short summary of Results](#-summary-of-results)
* [Technical Report](#-technical-report)

---

## 🔬 Scientific Scope
The study quantifies how chemical recombination effects in a de Laval nozzle influence performance metrics such as **Specific Impulse ($I_{sp}$)** and **Exit Velocity ($v_e$)**. To better highlight the divergence between the two thermodynamic models, the analysis is performed as a parametric sweep across three distinct chamber pressures: **50, 100, and 200 bar**.

**Key Methodology:**
* **Combustion Modeling:** Constant-pressure adiabatic equilibrium (HP state).
* **Expansion Modeling:** Isentropic nozzle expansion (SP state).
* **Solvers:** Utilizing Cantera's Gibbs free energy minimization algorithms.

---

## ⚙️ System Assumptions
| Parameter | Value |
| :--- | :--- |
| **Chamber pressures ($p_c$)** | 50, 100, 200 bar |
| **Ambient pressure ($p_a$)** | 1 atm (101.325 kPa) |
| **Inlet temperature ($T_{in}$)** | 300 K |
| **Kinetic mechanism** | `h2o2.yaml` |

---

## 🛠 Requirements
The project is built on Python 3.10+. Dependencies can be installed using the `requirements.txt` file:
```bash
pip install -r requirements.txt
