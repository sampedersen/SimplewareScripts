"""
set_colors_order.py

Script for assigning the colors and mask order according to pre-established standards. Must be implemented within
Synopsys Simpleware's scripting environment.

Author: Sam Pedersen
Date: 2023-08-02
"""



#! python3
import scanip_api3 as sip
import sys

# Add module to path for importing
module_path = "P:\\WoodsLab\\ACT-head_models\\FEM\\Sam\\Scripts\\Python\\Simpleware\\quality_checking\\"
sys.path.append(module_path)

# Import quality checking module
import quality_check_functions as qc

"""
########################################################################################################################
Notes for use: 
- Intended to be implemented on the final 11 tissue masks, WM, GM, eyes, CSF, air, blood, cancellous, cortical, skin, 
    fat, and muscle
- All tissue masks in the project file must have lower case names and match the spelling exactly
- If there is a masks missing, the script will stop; if there are additional masks beyond the 11 listed above, it will
    not be effected by the script 
- Sets the colors of the masks to pre-determined palette
- Sets order of the tissue masks based on pre-determined priority
- Makes all the listed masks visible  
########################################################################################################################
"""

qc.colors_order_visibility()
