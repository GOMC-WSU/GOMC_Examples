import math
import itertools

def lorentz_berthelot(atom1, atom2):
    """
    Applies Lorentz-Berthelot combining rules to find mixed sigma and epsilon.
    """
    # Arithmetic mean for Sigma
    sigma_mix = (atom1['sigma'] + atom2['sigma']) / 2.0
    
    # Geometric mean for Epsilon
    epsilon_mix = math.sqrt(atom1['epsilon'] * atom2['epsilon'])
    
    return sigma_mix, epsilon_mix

def compute_lennard_jones(epsilon, sigma, r):
    """
    Computes Energy (E) and Force (F) for a given distance r.
    """
    if r == 0:
        return float('inf'), float('inf')
    
    sr6 = (sigma / r) ** 6
    sr12 = sr6 ** 2
    
    E = 4 * epsilon * (sr12 - sr6)
    
    # F = -dV/dr = (24 * epsilon / r) * (2 * (sigma/r)^12 - (sigma/r)^6)
    F = (24 * epsilon / r) * (2 * sr12 - sr6)
    
    return E, F

def generate_interaction_tables(atoms_list, start_r, end_r, delta_r, filename="OPC_table_01.inp"):
    """
    Generates tables for all unique pairs of atoms in the provided list.
    """
    steps = int((end_r - start_r) / delta_r)
    
    # Create all unique combinations (with replacement allows Ar-Ar, Ne-Ne, etc.)
    pairs = list(itertools.combinations_with_replacement(atoms_list, 2))
    
    with open(filename, 'w') as f:
        for a1, a2 in pairs:
            # Calculate mixed parameters
            sigma_ij, epsilon_ij = lorentz_berthelot(a1, a2)
            pair_name = f"{a1['name']}{a2['name']}"
            
            # Header format
            f.write(f"TYPE {pair_name}\n")
#            f.write(f"Params: sigma={sigma_ij:.4f}, epsilon={epsilon_ij:.4f}\n")
#            f.write(f"{'r':<10} {'E':<15} {'F':<15}\n")
#            f.write("-" * 45 + "\n")
            
            # Data Loop
            current_r = start_r
            for _ in range(steps + 1):
                if current_r <= 1e-10: 
                    current_r += delta_r
                    continue
                
                E, F = compute_lennard_jones(epsilon_ij, sigma_ij, current_r)
                
                f.write(f"{current_r:<10.4f} {E:<15.6f} {F:<15.6f}\n")
                current_r += delta_r
                
#            f.write("\n\n")

    print(f"Computed {len(pairs)} interaction pairs.")
    print(f"Data written to {filename}")

# --- CONFIGURATION SECTION ---

# 1. Define individual atoms (Sigma in Angstroms, Epsilon in K)
atoms = [
    {"name": "OW0", "epsilon": 107.0857, "sigma": 3.1665},
    {"name": "HW0", "epsilon": 0.0, "sigma": 0},
    {"name": "LP0", "epsilon": 0.0, "sigma": 0},
]

# 2. Distance parameters
start_dist = 0.01
end_dist   = 10.0
delta_r    = 0.01

# --- EXECUTION ---
if __name__ == "__main__":
    generate_interaction_tables(atoms, start_dist, end_dist, delta_r)
