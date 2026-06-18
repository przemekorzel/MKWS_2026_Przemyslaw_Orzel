# MKWS 2026 – Comparative Analysis of Expansion Models in LOX/LH2 Rocket Engines

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Cantera](https://img.shields.io/badge/Cantera-3.0+-orange.svg)

Thermochemical equilibrium analysis and performance optimization of a high-performance rocket engine burning **Liquid Oxygen (LOX)** and **Liquid Hydrogen (LH2)** using the **Cantera** library.

Project completed as part of the course *"Computer Methods in Combustion"* (MKWS 2026).

---

## Table of Contents
* [Project Description](#project-description)
* [Requirements](#requirements)
* [Usage](#usage)
* [File Structure](#file-structure)
* [Report & Results](#report--results)

---

## Project Description

The goal of the project is to evaluate the ideal specific impulse ($I_{sp}$) and exit velocity of a hydrolox rocket engine. The study compares the **Frozen Flow** and **Shifting Equilibrium** nozzle expansion models across a wide range of oxidizer-to-fuel (O/F) ratios and multiple chamber pressures.

**Assumptions:**
| Parameter | Value |
| :--- | :--- |
| Chamber pressures ($p_c$) | 50, 100, 200 bar |
| Ambient pressure ($p_a$) | 1 atm (Sea Level) |
| Inlet temperature | 300 K |
| Kinetic mechanism | `h2o2.yaml` (Built-in) |

---

## Requirements

The project uses Python 3.10+. Required libraries are listed in `requirements.txt`:
* `cantera`
* `numpy`
* `pandas`
* `matplotlib`

Install dependencies locally:
```bash
pip install -r requirements.txt
