M564 S0 H0 # allow movement of axes without homing
G90 F1000 # move abs at 1000 mm/s
G1 E-120 # to lower
G1 E120 # to raise
T1 G1 E5 # -> max power
    G1 E-5 #low power
    
