import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap

# Set Chinese fonts (retained for proper display if needed)
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams["axes.unicode_minus"] = False  # Properly display negative signs

# Parameter settings
N = 15  # Number of transmitted light beams to study
lambda_ = 500  # Wavelength (nm)
n = 10  # Refractive index of the film
h = 25000  # Thickness of the film
Ai = 1  # Amplitude of incident light
a = 25 * np.pi / 180  # Azimuth angle of incident light amplitude (converted to radians)
theta_max = np.pi / 3  # Angular range of the image field (radians)
delta_theta = 0.001  # Calculation precision (radians)
fixed_incident_angle = 15 * np.pi / 180  # Fixed incident angle (15 degrees, converted to radians)

# Amplitudes of s-wave and p-wave in incident light
Asi = Ai * np.sin(a)
Api = Ai * np.cos(a)


# Define Fresnel formulas and related functions
def P(rs, rp):
    """Reflectance (combined contribution of s-wave and p-wave)"""
    return (rs * np.sin(a)) ** 2 + (rp * np.cos(a)) ** 2


def Rs(i, r):
    """s-wave reflection coefficient (Fresnel formula)"""
    return -np.sin(i - r) / np.sin(i + r)


def Rp(i, r):
    """p-wave reflection coefficient (Fresnel formula)"""
    return np.tan(i - r) / np.tan(i + r)


def Ts(i, r):
    """s-wave transmission coefficient (Fresnel formula)"""
    return 2 * np.sin(r) * np.cos(i) / np.sin(i + r)


def Tp(i, r):
    """p-wave transmission coefficient (Fresnel formula)"""
    return 2 * np.sin(r) * np.cos(i) / (np.sin(i + r) * np.cos(i - r))


def calculate_interference(N, lambda_, n, h, Ai, a, theta_max, delta_theta, fixed_angle):
    """Calculate interference results including intensity distributions and amplitudes"""
    # Angle range for interference calculation
    i1 = np.arange(-theta_max, theta_max + delta_theta, delta_theta)
    r1 = np.arcsin(np.sin(i1) / n)  # Refraction angle (Snell's law)

    # Phase difference between adjacent transmitted beams
    delta = 4 * np.pi / lambda_ * n * h * np.cos(r1)

    # Calculation distinguishing s/p waves
    As = Asi * Ts(i1, r1) * Ts(r1, i1)
    Ap = Api * Tp(i1, r1) * Tp(r1, i1)

    # Vectorized operations instead of loops for efficiency
    powers = np.arange(N)
    rs_pows = Rs(r1, i1)[:, np.newaxis] ** (2 * powers)
    rp_pows = Rp(r1, i1)[:, np.newaxis] ** (2 * powers)
    exp_terms = np.exp(1j * delta)[:, np.newaxis] ** powers

    Ast = As[:, np.newaxis] * rs_pows * exp_terms
    Apt = Ap[:, np.newaxis] * rp_pows * exp_terms

    It_1 = np.abs(Ast.sum(axis=1)) **2 + np.abs(Apt.sum(axis=1))** 2

    # Calculation using textbook formula (without distinguishing s/p waves)
    rs_vals = Rs(i1, r1)
    rp_vals = Rp(i1, r1)
    p = P(rs_vals, rp_vals)
    It_2 = (1 - p) ** 2 / ((1 - p) ** 2 + 4 * p * np.sin(delta / 2) ** 2) * Ai ** 2

    # Amplitude directions of transmitted beams of various orders (using fixed incident angle)
    ii = fixed_angle  # Fixed incident angle
    r = np.arcsin(np.sin(ii) / n)  # Corresponding refraction angle
    As_dir = Asi * Ts(ii, r) * Ts(r, ii)
    Ap_dir = Api * Tp(ii, r) * Tp(r, ii)

    # Amplitudes of each order
    orders = np.arange(1, N + 1)
    s_amplitudes = As_dir * (Rs(ii, r) ** 2) ** (orders - 1)
    p_amplitudes = Ap_dir * (Rp(ii, r) ** 2) ** (orders - 1)

    return i1, It_1, It_2, s_amplitudes, p_amplitudes, orders


# Calculate interference results
i1, It_1, It_2, s_amplitudes, p_amplitudes, orders = calculate_interference(
    N, lambda_, n, h, Ai, a, theta_max, delta_theta, fixed_incident_angle)

# Create custom colormap
colors = [(0, 0, 0), (0.8, 0.2, 0.2), (1, 1, 0), (1, 1, 1)]
custom_cmap = LinearSegmentedColormap.from_list("custom_hot", colors)

# Create color sequence for the second subplot (using viridis for good distinguishability)
colors_2nd = plt.cm.viridis(np.linspace(0, 1, len(orders)))

# Create figure
fig = plt.figure(figsize=(14, 10))
gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1], width_ratios=[1, 1])

# Subplot 1: Comparison of two calculation results
ax2 = fig.add_subplot(gs[0, 0])
ax2.plot(np.rad2deg(i1), It_1, 'b-', linewidth=1.5, label='Distinguishing s/p waves')
ax2.plot(np.rad2deg(i1), It_2, 'r--', linewidth=1.5, label='Not distinguishing s/p waves')
ax2.set_xlabel('Interference angle (°)', fontsize=12)
ax2.set_ylabel('Light intensity', fontsize=12)
ax2.set_title('Comparison of two calculation results', fontsize=14)
ax2.legend()
ax2.grid(True, linestyle='--', alpha=0.7)

# Subplot 2: Amplitude directions of transmitted light of various orders
ax3 = fig.add_subplot(gs[0, 1])
# Plot points for each order and add to legend
for i, (x, y, order, color) in enumerate(zip(s_amplitudes, p_amplitudes, orders, colors_2nd)):
    # Plot connecting lines
    if i > 0:
        ax3.plot([s_amplitudes[i - 1], x], [p_amplitudes[i - 1], y], '-', color=color, alpha=0.5)
    ax3.plot(x, y, 'o', color=color, markersize=6, label=f'Order {order}')

ax3.set_xlabel('s-wave amplitude', fontsize=12)
ax3.set_ylabel('p-wave amplitude', fontsize=12)
ax3.set_title(f'Amplitude directions of transmitted light at incident angle=15°', fontsize=14)
ax3.grid(True, linestyle='--', alpha=0.7)
ax3.axis('equal')

# Add legend, adjust position to avoid overlapping data
ax3.legend(title='Transmitted light order', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)

# Subplot 3: 3D surface plot of intensity distribution
ax4 = fig.add_subplot(gs[1, :], projection='3d')
X, Y = np.meshgrid(i1, np.linspace(0, max(It_1), 50))
Z = np.tile(It_1, (50, 1))
surf = ax4.plot_surface(np.rad2deg(X), Y, Z, cmap=custom_cmap, alpha=0.85)
ax4.set_xlabel('Interference angle (°)', fontsize=12)
ax4.set_ylabel('Intensity', fontsize=12)
ax4.set_zlabel('Relative intensity', fontsize=12)
ax4.set_title('Transmitted light intensity distribution', fontsize=14)
ax4.view_init(30, 45)

# Add color bar
cbar = fig.colorbar(surf, ax=ax4, shrink=0.7, aspect=10)
cbar.set_label('Light intensity')

# Adjust main title position (y ranges from 0 to 1, larger values mean higher position)
plt.suptitle(f'Thin-film multiple-beam interference simulation (Fixed incident angle=15°)', fontsize=16, y=0.98)
plt.tight_layout()

# Save image to current directory
plt.savefig('Thin_film_multiple_beam_interference_simulation_(Fixed_incident_angle=15°).png', dpi=300, bbox_inches='tight')
plt.close()

print("Image saved to current directory with filename: Thin_film_multiple_beam_interference_simulation_(Fixed_incident_angle=15°).png")