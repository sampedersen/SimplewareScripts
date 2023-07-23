# Generate an *initial* "10" mask and CSF mask
# Created by Samantha Pedersen (09/08/2021)
# Last updated: 7/25/2022
#! python3
from scanip_api3 import *

########################################################################################################################
###########################################       !!! README !!!         ###############################################
########################################################################################################################

# Script function:
#   1. Generate "10" by combining "gm", "wm", "eyes", "air", "blood", "bone", "skin", "fat", & "muscle"
#   2. Generate "csf" by subtracting "uniform" minus "10"
#   4. Add csf fluid in the eyes to "csf" mask ("csf" union "eyes interior")
#   5. Set "csf" color to blue   
#   6. Move masks and toggle visibilities

# Masks being used (make sure these exist in the project file):
#   - "wm"
#   - "gm"
#   - "eyes"
#   - "air"
#   - "blood"
#   - "bone"
#   - "skin"
#   - "fat"
#   - "muscle"
#   - "uniform"
#   - "eyes interior"

# Mask names to be avoided (make sure these names are not currently contained in the project file)
# Having a duplicate name will cause the script to crash. Either delete the mask/rename it
#   - "Copy of wm"
#   - "10"
#   - "Copy of uniform"
#   - "csf"

# Notes:
#   - This script is meant to generate an *initial* 10 and csf mask; script will end prematurely if 10 or csf pre-exist
#   - To regenerate 10 and CSF after the initial masks have been created, execute regenerate10AndCSF.py

########################################################################################################################

# Generate "10" mask
App.GetDocument().GetGenericMaskByName("wm").Activate()
App.GetDocument().GetActiveGenericMask().Duplicate()
App.GetDocument().GetGenericMaskByName("Copy of wm").Activate()
App.GetDocument().GetGenericMaskByName("Copy of wm").SetName("10")
App.GetDocument().ReplaceMaskUsingBooleanExpression("(10 OR wm OR gm OR eyes OR air OR blood OR bone OR skin OR fat OR muscle)",
                                                    App.GetDocument().GetMaskByName("10"), 
                                                    App.GetDocument().GetSliceIndices(Doc.OrientationXY), Doc.OrientationXY)

########################################################################################################################
# Generate the CSF mask 
App.GetDocument().GetGenericMaskByName("uniform").Activate()
App.GetDocument().GetActiveGenericMask().Duplicate()
App.GetDocument().GetGenericMaskByName("Copy of uniform").Activate()
App.GetDocument().GetGenericMaskByName("Copy of uniform").SetName("csf")
App.GetDocument().ReplaceMaskUsingBooleanExpression("(csf MINUS 10)", 
                                                    App.GetDocument().GetMaskByName("csf"), 
                                                    App.GetDocument().GetSliceIndices(Doc.OrientationXY), Doc.OrientationXY)

# Add the fluid from the inside of the eyes 
App.GetDocument().ReplaceMaskUsingBooleanExpression("(csf OR \"eyes interior\")", 
                                                    App.GetDocument().GetMaskByName("csf"), 
                                                    App.GetDocument().GetSliceIndices(Doc.OrientationXY), Doc.OrientationXY)

########################################################################################################################
# Color, position, visibility
App.GetDocument().GetGenericMaskByName("csf").Activate()
App.GetDocument().GetActiveGenericMask().SetColour(Colour(107, 220, 220))
App.GetDocument().GetGenericMaskByName("csf").Activate()
App.GetDocument().MoveMaskTo(App.GetDocument().GetActiveGenericMask(), 1)
App.GetDocument().GetGenericMaskByName("csf").SetVisible(True)

# Make "10" non-visible
App.GetDocument().GetGenericMaskByName("10").SetVisible(False)



