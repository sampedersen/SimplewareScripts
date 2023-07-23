
# Regenerate the "10" mask and CSF mask *after* edits has been effected
# Created by Samantha Pedersen (09/08/2021)
# Last updated: 07/25/2022
#! python3
from scanip_api3 import *

########################################################################################################################
###########################################       !!! README !!!         ###############################################
########################################################################################################################

# Script function:
#   1. Delete the pre-existing "10" and "csf" masks
#   2. Generate "10" by combining "gm", "wm", "eyes", "air", "blood", "bone", "skin", "fat", & "muscle"
#   3. Generate "csf" by subtracting "uniform" minus "10"
#   4. Add csf fluid in the eyes to "csf" mask ("csf" union "eyes interior")
#   5. Set "csf" color to blue
#   6. Move masks and toggle visibilities

# Masks being used (make sure these exist in the project file):
#   - "10"
#   - "csf"
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
#   - "Copy of uniform"

# Notes:
#   - This script is meant to regenerate an the 10 and csf mask; script will end prematurely if 10 or csf DNE
#   - If 10 and csf have not already be generated, execute generate10AndCSF.py instead

########################################################################################################################

# Delete pre-existing masks, 10 and csf
App.GetDocument().GetGenericMaskByName("10").Activate()
App.GetDocument().RemoveMask(App.GetDocument().GetActiveGenericMask())
App.GetDocument().GetGenericMaskByName("csf").Activate()
App.GetDocument().RemoveMask(App.GetDocument().GetActiveGenericMask())

########################################################################################################################

# Regenerate the 10 mask
App.GetDocument().GetGenericMaskByName("wm").Activate()
App.GetDocument().GetActiveGenericMask().Duplicate()
App.GetDocument().GetGenericMaskByName("Copy of wm").Activate()
App.GetDocument().GetGenericMaskByName("Copy of wm").SetName("10")
App.GetDocument().ReplaceMaskUsingBooleanExpression("(10 OR wm OR gm OR eyes OR air OR blood OR bone OR skin OR fat OR muscle)",
                                                    App.GetDocument().GetMaskByName("10"), 
                                                    App.GetDocument().GetSliceIndices(Doc.OrientationXY), Doc.OrientationXY)

########################################################################################################################

# Regenerate CSF mask 
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


