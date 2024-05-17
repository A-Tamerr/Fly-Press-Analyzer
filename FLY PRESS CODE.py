import numpy as np
import matplotlib.pyplot as plt

# USER DEFINED - punch_diameter & sheet_thickness (all in mm)
punch_diameter = int(input("Enter Punch Diameter (in mm): "))
sheet_thickness = int(input("Enter Sheet Thickness (in mm): "))

## CONSTANTS
# Screw 
D_O = 50             # assumed -  Outer Diameter in mm      [CONSTANT]
D_I = 42             # assumed -  Inner Diameter in mm      [CONSTANT]
D_M = 46             # calculated -  Mean Diameter in mm    [CONSTANT]
P = 8                # assumed -  Pitch in mm               [CONSTANT]
M = 3                # assumed -  Modulus                   [CONSTANT]
L_screw = P*M        # calculated in mm                     [CONSTANT]

# Screw Material - AISI 1050
S_ult = 690                   # measured in MPa  [CONSTANT]
S_y = 580                     # measured in MPa  [CONSTANT]
S_sy_PS = 290                 # measured in MPa  [CONSTANT]
S_sy_SHEET = 375              # measured in MPa  [CONSTANT]
Safety_Factor = 4             # unit-less        [CONSTANT]

# Nut
Meu = 0.15                    # unit-less        [CONSTANT]
H_nut = 425                   # measured in mm   [CONSTANT]
A_c = 1385                    # measured in mm^2 [CONSTANT]

# Rotation
Omega_AVG = (np.pi)/2         # assumed - Average omega in rad/s^2

# Time
T_rise = 1                    # assumed - Time to rise in sec
T_lower = 1                   # assumed - Time to lower in sec

# Worker & Machine
F_worker = 294.3              # in Newtons, assumed
F_punch  = S_sy_SHEET * sheet_thickness * punch_diameter * np.pi # in Newtons, calculated
PartsPerShift = 15000   # given
PartsPerMinute = 30   # given
PartsPerShift = 15000   # given

# Ball/Flywheel Dimensions
Rho = 7280      # Ball/Flywheel material density measured in kg/m3


# Ball/Flywheel Dimensions
Inertia = (F_punch * sheet_thickness) / (1000*np.power(Omega_AVG,2)) 
R_ball = np.power(((15*Inertia)/(8*np.pi*Rho)),1/5)* 870.7491744 


# DYNAMIC Dimensions (all in mm)
T_L_A1 = (np.pi * D_M * Meu) - (L_screw)
T_L_A2 = (np.pi * D_M * Meu) + (L_screw)
T_L_B = (np.pi * D_M) - (Meu*L_screw)

T_L = 0.5 * F_punch * D_M * (T_L_A1/T_L_B)
T_r = 0.5 * F_punch * D_M * (T_L_A2/T_L_B)

Sigma = (4*F_punch) / (np.pi * (np.power(D_I,2)))          # Sigma
Tao = (16*T_r) / (np.pi * (np.power(D_I,3)))               # Tao

Sigma_Max = (Sigma/2) + (np.power(((np.power(Sigma/2,2)+ np.power(Tao,2))),0.5))       # Sigma_Max
Sigma_Min = (Sigma/2) - (np.power(((np.power(Sigma/2,2)+ np.power(Tao,2))),0.5))       # Sigma_Min

Tao_Max = (np.power(((np.power(Sigma/2,2)+ np.power(Tao,2))),0.5))                     # Tao Max
Sigma_VM_1 = np.power((Sigma_Max-Sigma_Min),2)
Sigma_VM_2 = np.power((Sigma_Max),2)
Sigma_VM_3 = np.power((0-Sigma_Min),2)
Sigma_VM = np.power(((Sigma_VM_1 + Sigma_VM_2 + Sigma_VM_3)/2),0.5) #von mises


L_handle = T_L / F_worker
IMA = F_punch / F_worker 
Rm = (P*IMA) / (2*np.pi)
L_rod = 2*Rm

print("The Radius of the a single flywheel ball is = ", round(R_ball,0),"mm")
print("The Rod length (Rm) is = ", round(Rm,0),"mm")
print("The Handle's Length is = ", round(np.absolute(L_handle),0),"mm")
print("T(L) = ", round(T_L/1000,0),"N.m")
print("T(r) = ", round(T_r/1000,0),"N.m")
print("Tao = ", round(Tao,2),"MPa")
print("Tao Max = ", round(Tao_Max,2),"MPa")
print("Sigma Max = ", round(Sigma_Max,2),"MPa")
print("Sigma Min = ", round(Sigma_Min,2),"MPa")
print("Sigma VM = ", round(Sigma_VM,2),"MPa")


if (Sigma_VM <= S_sy_PS):
     print("Safe to Use ✔")
else:
     print("Unsafe ❌")


## Plotting punching force versus punch diameter 

# Define function to calculate punching force
def calculate_punching_force(punch_diameter, sheet_thickness):
    S_sy_SHEET = 375  # Measured in MPa, assuming constant
    
    # Calculate punching force
    F_punch = S_sy_SHEET * sheet_thickness * punch_diameter * np.pi / 10000
    return F_punch

# Define punch diameters from 20 to 100 mm
punch_diameters = np.arange(20, 101, 1)

# Define sheet thicknesses from 0.5 to 10 mm
sheet_thicknesses = np.arange(0.5, 10.5, 0.5)

# Plot punching force vs. punch diameter for each sheet thickness
plt.figure(figsize=(10, 6))
for thickness in sheet_thicknesses:
    punching_forces = [calculate_punching_force(diameter, thickness) for diameter in punch_diameters]
    plt.plot(punch_diameters, punching_forces, label=f'Sheet Thickness: {thickness} mm')

plt.title('Punching Force vs. Punch Diameter for Different Sheet Thicknesses')
plt.xlabel('Punch Diameter (mm)')
plt.ylabel('Punching Force (kN)')
plt.grid(True)
plt.legend()    


YorN = input("Would you like to see the plot ?(Y/N): ")
if (YorN == 'Y' or YorN == 'YES' or YorN == 'yes' or YorN == 'y'): plt.show()
else: print ("\nThank you and Goodbye!\nMDPS352 - Machine Design\nSpring 2024\n\n")

     
     
