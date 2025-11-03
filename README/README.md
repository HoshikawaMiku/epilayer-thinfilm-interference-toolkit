# Epilayer & Thin-Film Interference Toolkit  

A comprehensive Python suite for calculating epilayer thickness via double-beam interference and simulating thin-film multi-beam interference, featuring numerical analysis and intuitive visualization tools for optical research and education.  

[简体中文](README_zh.md) | [English](README.md)

## Overview  

This project integrates two specialized tools to explore interference phenomena in thin films and epilayers, designed for students, researchers, and engineers in optics and materials science:  

1. **Epilayer Thickness Calculator**: Leverages the double-beam interference principle to compute epilayer thickness, analyze sensitivity to key parameters (refractive index, wavenumber), and visualize how parameter variations impact results.  

2. **Thin-Film Multi-Beam Interference Simulator**: Uses numerical methods to model multi-beam interference in thin films, including intensity distributions and amplitude characteristics of transmitted beams, with visualizations to clarify underlying physical behaviors.  


## Core Features  

### 1. Epilayer Thickness Calculation  
- Precise thickness computation using the double-beam interference formula: `d = k / (2 * n1 * cosθ₁ * ṽ)`  
- Sensitivity analysis for critical parameters:  
  - Epilayer refractive index (`n1`)  
  - Infrared wavenumber (`ṽ`, reciprocal of wavelength)  
- Interactive visualizations of thickness variations with parameter changes  
- Customizable parameters for diverse material systems (e.g., SiC, GaN)  


### 2. Thin-Film Multi-Beam Interference Simulation  
- Light intensity distribution calculations, with comparisons between:  
  - S/p-wave separated analysis (accounting for polarization)  
  - Simplified calculations (without polarization distinction)  
- Amplitude characteristic analysis: Tracks amplitude directions of multi-order transmitted beams under a fixed incident angle  
- 3D surface plots of transmitted light intensity across a range of interference angles  
- Integration of Fresnel coefficients (reflection/transmission for s/p waves) for accurate wave behavior modeling  


## Requirements  

- Python 3.6+  
- NumPy (for numerical computations)  
- Matplotlib (for visualization)  

Install dependencies via:  
```bash
pip install numpy matplotlib
```  


## Usage Examples  

### 1. Epilayer Thickness Calculation  
```python
from doublebeam_epi_thickness import EpilayerThicknessCalculator

# Initialize with default parameters (SiC: n1=2.65, n2=2.68, etc.)
calculator = EpilayerThicknessCalculator()

# Perform calculations
calculator.calculate_thickness()
calculator.calculate_sensitivity()

# Print numerical results and model details
calculator.print_results()

# Generate sensitivity plots (shows thickness vs. n1 and wavenumber)
calculator.plot_sensitivity()

# Example: Custom parameters for GaN
gan_calculator = EpilayerThicknessCalculator(
    n1=2.5,    # GaN epilayer refractive index
    n2=2.55,   # GaN substrate refractive index
    nu_tilde=750,  # Wavenumber (cm⁻¹)
    m=2        # Interference order
)
gan_calculator.print_results()
```  


### 2. Thin-Film Multi-Beam Interference Simulation  
Run the script directly to generate a comprehensive visualization:  
```bash
python thin_film_multibeam_interference_sim.py
```  

The output is a PNG file (e.g., `Thin_film_multiple_beam_interference_simulation_(Fixed_incident_angle=15°).png`) containing:  
- A comparison of intensity distributions with/without s/p-wave separation  
- Amplitude directions of transmitted beams across different orders  
- A 3D surface plot of transmitted light intensity vs. interference angles  


## Code Structure  

| File | Description |  
|------|-------------|  
| `doublebeam_epi_thickness.py` | Core class (`EpilayerThicknessCalculator`) for double-beam interference-based thickness calculation, sensitivity analysis, and result visualization. |  
| `thin_film_multibeam_interference_sim.py` | Tools for multi-beam interference simulation, including Fresnel coefficient calculations, intensity computations, and 2D/3D visualizations. |  


## Parameter Explanations  

### For Epilayer Calculation  

| Parameter | Description | Unit |  
|-----------|-------------|------|  
| `n1` | Refractive index of the epilayer | Dimensionless |  
| `n2` | Refractive index of the substrate | Dimensionless |  
| `theta0_deg` | Incident angle in air | Degrees |  
| `nu_tilde` | Infrared wavenumber (1/λ) | cm⁻¹ |  
| `m` | Initial interference order | - |  


### For Thin-Film Simulation  

| Parameter | Description | Unit |  
|-----------|-------------|------|  
| `lambda_` | Wavelength of incident light | nm |  
| `n` | Refractive index of the thin film | Dimensionless |  
| `h` | Thickness of the thin film | nm |  
| `Ai` | Amplitude of the incident light | - |  
| `theta_max` | Range of image-side field angles | Radians |  
| `N` | Number of transmitted beams considered in the simulation | - |  


## License  

This project is licensed under the MIT License. See the `LICENSE` file for details.