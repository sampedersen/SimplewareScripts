"""
generate_regenerate_csf_10.py

Script to utilize segmentation module functions and (re) generate the CSF/10 masks

Author: Sam Pedersen
Date: 23 July 2023

"""
###########

# Indicate below if the CSF and 10 mask are being generated for the 1st time (firstGen = True) or if the CSF and 10
# mask are being regenerated (firstGen = False)
# Defaulted to False for regenerating purposes, change to True on first round of generating

firstGen = False


###########


# Import scanip_api3 and sys modules
# ! python3
import sys

# Add the script module to the path
### !!!! VERIFY THIS WITH P-DRIVE FINAL LOCATIONS !!!! ###
module_path = "C:\\Users\\samanthapedersen\\PycharmProjects\\quality_checking\\"
sys.path.append(module_path)

# Import the custom module for segmentation
from lib.functions.segmentation import segmentation as seg

# Perform (re)generation:
seg.generate_csf_10(firstGen)