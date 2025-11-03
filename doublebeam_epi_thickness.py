# Import required libraries: numpy for numerical calculations, matplotlib for visualization
import numpy as np
import matplotlib.pyplot as plt

# Set font parameters to ensure proper display of Chinese characters (if needed)
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False  # Fix negative sign display issue


class EpilayerThicknessCalculator:
    """
    Double-beam interference epilayer thickness calculation class
    Function: Calculate epilayer thickness based on double-beam interference principle,
              analyze parameter sensitivity, and support result visualization
    Core formula: d = k / (2 * n1 * cos1 * V)
    """

    def __init__(self, n1=2.65, n2=2.68, theta0_deg=15, nu_tilde=1000, m=1):
        """
        Class initialization: Store input parameters and pre-calculate basic parameters (cos1, k)
        :param n1: Refractive index of epilayer (dimensionless, default 2.65 typical for SiC in infrared region)
        :param n2: Refractive index of substrate (dimensionless, default 2.68 typical for SiC, n2>n1)
        :param theta0_deg: Incident angle in air (unit: degrees, default 15°)
        :param nu_tilde: Infrared wavenumber (unit: cm^-1, default 1000 cm^-1)
        :param m: Initial interference order (positive integer, default 1, adjustable based on extremum position)
        """
        # 1. Store input parameters (material, experiment, spectrum, and interference order parameters)
        self.n1 = n1  # Epilayer refractive index
        self.n2 = n2  # Substrate refractive index
        self.theta0_deg = theta0_deg  # Incident angle (degrees)
        self.nu_tilde = nu_tilde  # Wavenumber (cm^-1)
        self.m = m  # Initial interference order

        # 2. Pre-calculate basic parameters (avoid repeated calculations)
        self.cos_theta1 = self._calc_cos_theta1()  # Cosine of refraction angle in epilayer
        self.k = self._calc_k()  # Interference order correction term

        # 3. Initialize result variables (to be assigned after subsequent calculations)
        self.d = None  # Epilayer thickness (cm)
        self.d_dn1 = None  # Sensitivity of thickness to n1 (cm/unit refractive index)
        self.d_dnu = None  # Sensitivity of thickness to wavenumber (cm/(cm^-1))

    def _calc_cos_theta1(self):
        """
        Method: Calculate cosine of refraction angle (cos1) in epilayer using Snell's law
        :return: cos_theta1 (dimensionless)
        """
        theta0_rad = np.deg2rad(self.theta0_deg)  # Convert incident angle from degrees to radians (numpy trigonometric functions require radians)
        sin_theta1 = np.sin(theta0_rad) / self.n1  # Snell's law: sin1 = sin0 / n1 (air refractive index n0=1)
        cos_theta1 = np.sqrt(1 - sin_theta1 **2)  # Trigonometric identity: sin²θ + cos²θ = 1 (ensure n1>sin0 for real result)
        return cos_theta1

    def _calc_k(self):
        """
        Method: Determine interference order correction term k based on the relationship between n1 and n2
        :return: k (dimensionless)
        """
        if self.n2 > self.n1:
            # Case 1: n2>n1 (optically thinner → optically denser), both reflections have π phase shift, total phase difference cancels, k=m
            return self.m
        else:
            # Case 2: n2<n1, only air→epilayer reflection has π shift, total phase difference has extra π, k=m-0.5
            return self.m - 0.5

    def calculate_thickness(self):
        """
        Calculate epilayer thickness d (core method)
        :return: d (unit: cm)
        """
        # Substitute into double-beam interference thickness formula: d = k / (2 * n1 * cos1 * V)
        self.d = self.k / (2 * self.n1 * self.cos_theta1 * self.nu_tilde)
        return self.d

    def calculate_sensitivity(self):
        """
        Calculate sensitivity of thickness to key parameters (n1 and wavenumber)
        :return: d_dn1 (sensitivity of thickness to n1), d_dnu (sensitivity of thickness to wavenumber)
        """
        # 1. Sensitivity of thickness to n1: partial derivative formula (derived using chain rule)
        self.d_dn1 = -self.k / (2 * self.nu_tilde * self.n1** 2 * self.cos_theta1 **3)
        # 2. Sensitivity of thickness to wavenumber: partial derivative formula (direct derivative of thickness formula)
        self.d_dnu = -self.k / (2 * self.n1 * self.cos_theta1 * self.nu_tilde** 2)
        return self.d_dn1, self.d_dnu

    def print_results(self):
        """
        Output calculation results
        """
        # First check if calculations are completed (avoid outputting null values)
        if self.d is None or self.d_dn1 is None or self.d_dnu is None:
            self.calculate_thickness()
            self.calculate_sensitivity()

        # Print result title and separator
        print("Question 1 Output Results:")
        print(f"1. Epilayer thickness (cm): d = {self.d:.10f}")  # Keep 10 decimal places for precision
        print(f"2. Sensitivity of thickness to n1 (cm/unit refractive index): d/dn1 = {self.d_dn1:.12f}")
        print(f"3. Sensitivity of thickness to wavenumber (cm/(cm^-1)): d/dV = {self.d_dnu:.12f}")
        print(" ")

        # Print mathematical model
        print("Mathematical Model:")
        print("Epilayer thickness calculation formula: d = k / (2 * n1 * cos1 * V)")
        print("Parameter Explanations:")
        print(f"   - k: Interference order correction term (current n2={self.n2}, n1={self.n1}, so k={self.k})")
        print(f"   - cos1: Cosine of refraction angle in epilayer (current calculated value: {self.cos_theta1:.8f})")
        print(f"   - V: Infrared light wavenumber (current value: {self.nu_tilde} cm^-1, reciprocal of wavelength λ)")
        print(" ")

        # Print model explanation
        print("Model Explanation:")
        print("1. Core principle: 'Superposition' of two reflected light beams (similar to water wave superposition, with bright and dark regions)")
        print("   - First beam: Reflected directly from epilayer surface (does not pass through epilayer)")
        print("   - Second beam: Passes through epilayer, reflects off substrate, and returns (travels twice the epilayer thickness)")
        print("2. Why correct k? Because light undergoes a 'half-step' phase shift during reflection, requiring correction of 'step difference' between the two beams")
        print("3. What needs to be known in advance? 'Velocity indices' of n1 (epilayer) and n2 (substrate) (from literature or experimental measurement)")
        print("4. What can be calculated? Epilayer thickness inferred from light incidence angle and wavenumber")

    def plot_sensitivity(self):
        """
        Visual sensitivity analysis: Plot "parameter change-thickness change" curves to intuitively show sensitivity
        Contains two plots: 1. Effect of epilayer refractive index n1 on thickness; 2. Effect of wavenumber on thickness
        """
        # First check if basic calculations are completed
        if self.d is None:
            self.calculate_thickness()

        # Plot 1: Effect of n1 variation on thickness
        # Generate n1 variation range (±0.1 around default value 2.65, 50 points, simulating experimental error)
        n1_range = np.linspace(self.n1 - 0.1, self.n1 + 0.1, 50)
        # Calculate thickness for each n1 (need to recalculate cos1 and k as n1 affects cos1)
        d_n1_range = []
        for n1 in n1_range:
            # Temporarily calculate cos1 for current n1 (Snell's law)
            theta0_rad = np.deg2rad(self.theta0_deg)
            sin_theta1 = np.sin(theta0_rad) / n1
            cos_theta1 = np.sqrt(1 - sin_theta1 **2)
            # Temporarily calculate k (relationship between n2 and current n1)
            k = self.m if self.n2 > n1 else (self.m - 0.5)
            # Calculate thickness
            d = k / (2 * n1 * cos_theta1 * self.nu_tilde)
            d_n1_range.append(d)

        # Plot 2: Effect of wavenumber variation on thickness
        # Generate wavenumber variation range (±50 around default value 800 cm^-1, 50 points)
        nu_range = np.linspace(self.nu_tilde - 50, self.nu_tilde + 50, 50)
        # Calculate thickness for each wavenumber (cos1 and k are independent of wavenumber, reuse initial values)
        d_nu_range = [self.k / (2 * self.n1 * self.cos_theta1 * nu) for nu in nu_range]

        # Create plots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))  # 1 row, 2 columns of subplots, total size 14x5

        # Plot 1: n1-thickness relationship
        ax1.plot(n1_range, d_n1_range, color='#2E86AB', linewidth=2.5, marker='o', markersize=4)
        ax1.axvline(x=self.n1, color='red', linestyle='--', alpha=0.8, label=f'Default n1={self.n1}')
        ax1.axhline(y=self.d, color='gray', linestyle='--', alpha=0.8, label=f'Default thickness={self.d:.8f} cm')
        ax1.set_xlabel('Epilayer refractive index n1 (dimensionless)', fontsize=12)
        ax1.set_ylabel('Epilayer thickness d (cm)', fontsize=12)
        ax1.set_title('Effect of epilayer refractive index on thickness (Sensitivity: {:.10f} cm/unit n1)'.format(self.d_dn1), fontsize=13)
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3)

        # Plot 2: Wavenumber-thickness relationship
        ax2.plot(nu_range, d_nu_range, color='#A23B72', linewidth=2.5, marker='s', markersize=4)
        ax2.axvline(x=self.nu_tilde, color='red', linestyle='--', alpha=0.8, label=f'Default wavenumber={self.nu_tilde} cm^-1')
        ax2.axhline(y=self.d, color='gray', linestyle='--', alpha=0.8, label=f'Default thickness={self.d:.8f} cm')
        ax2.set_xlabel('Infrared wavenumber V (cm^-1)', fontsize=12)
        ax2.set_ylabel('Epilayer thickness d (cm)', fontsize=12)
        ax2.set_title('Effect of wavenumber on thickness (Sensitivity: {:.12f} cm/(cm^-1))'.format(self.d_dnu), fontsize=13)
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3)

        # Adjust subplot spacing to avoid overlap
        plt.tight_layout()
        # Display plots
        plt.show()


# Model usage example
if __name__ == "__main__":
    # 1. Initialize calculator (default parameters: SiC material, n1=2.65, n2=2.68, incident angle 15°, wavenumber 1000 cm^-1)
    calculator = EpilayerThicknessCalculator()

    # 2. Calculate thickness and sensitivity (can also directly call print_results or plot_sensitivity, which will automatically trigger calculations)
    calculator.calculate_thickness()
    calculator.calculate_sensitivity()

    # 3. Print text results
    calculator.print_results()

    # 4. Visual sensitivity analysis (intuitively show parameter effects)
    calculator.plot_sensitivity()

    # ---------------------- Extension: Custom parameter example (e.g., changing material) ----------------------
    # To calculate for other materials (e.g., GaN, n1=2.5, n2=2.55), simply pass parameters during initialization:
    # gaN_calculator = EpilayerThicknessCalculator(n1=2.5, n2=2.55, theta0_deg=15, nu_tilde=750, m=2)
    # gaN_calculator.print_results()
    # gaN_calculator.plot_sensitivity()