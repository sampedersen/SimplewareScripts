# Standardize the colors of the 11 masks and put them in their final order
# Created by Samantha Pedersen (09/08/2021)
# Last updated: 07/25/2022
#! python3
from scanip_api3 import *

########################################################################################################################
###########################################       !!! README !!!         ###############################################
########################################################################################################################

# Script function:
#   1. Set colors for all the masks
#   2. Put the masks in order for CSF editing
#   3. Isolate mask visibility
#   4. Organize the masks

# Masks being used (make sure these exist in the project file):
#   - "muscle"
#   - "skin"
#   - "cortical"
#   - "cancellous"
#   - "bone"
#   - "fat"
#   - "blood"
#   - "air"
#   - "csf"
#   - "eyes"
#   - "gm"
#   - "wm"

########################################################################################################################

# Set colors 
App.GetDocument().GetGenericMaskByName("muscle").Activate()
App.GetDocument().GetActiveGenericMask().SetColour(Colour(255, 64, 64))
App.GetDocument().GetGenericMaskByName("skin").Activate()
App.GetDocument().GetActiveGenericMask().SetColour(Colour(140, 120, 83))
App.GetDocument().GetGenericMaskByName("cortical").Activate()
App.GetDocument().GetActiveGenericMask().SetColour(Colour(22, 167, 11))
App.GetDocument().GetGenericMaskByName("cancellous").Activate()
App.GetDocument().GetActiveGenericMask().SetColour(Colour(22, 167, 11))
App.GetDocument().GetGenericMaskByName("bone").Activate()
App.GetDocument().GetActiveGenericMask().SetColour(Colour(22, 167, 11))
App.GetDocument().GetGenericMaskByName("fat").Activate()
App.GetDocument().GetActiveGenericMask().SetColour(Colour(239, 217, 151))
App.GetDocument().GetGenericMaskByName("blood").Activate()
App.GetDocument().GetActiveGenericMask().SetColour(Colour(200, 0, 0))
App.GetDocument().GetGenericMaskByName("air").Activate()
App.GetDocument().GetActiveGenericMask().SetColour(Colour(65, 65, 65))
App.GetDocument().GetGenericMaskByName("csf").Activate()
App.GetDocument().GetActiveGenericMask().SetColour(Colour(107, 220, 220))
App.GetDocument().GetGenericMaskByName("eyes").Activate()
App.GetDocument().GetActiveGenericMask().SetColour(Colour(194, 230, 230))
App.GetDocument().GetGenericMaskByName("gm").Activate()
App.GetDocument().GetActiveGenericMask().SetColour(Colour(176, 176, 176))
App.GetDocument().GetGenericMaskByName("wm").Activate()
App.GetDocument().GetActiveGenericMask().SetColour(Colour(207, 221, 220))

# Mask order
App.GetDocument().GetGenericMaskByName("uniform").Activate()
App.GetDocument().MoveMaskTo(App.GetDocument().GetActiveGenericMask(), 1)
App.GetDocument().GetGenericMaskByName("muscle").Activate()
App.GetDocument().MoveMaskTo(App.GetDocument().GetActiveGenericMask(), 2)
App.GetDocument().GetGenericMaskByName("fat").Activate()
App.GetDocument().MoveMaskTo(App.GetDocument().GetActiveGenericMask(), 3)
App.GetDocument().GetGenericMaskByName("skin").Activate()
App.GetDocument().MoveMaskTo(App.GetDocument().GetActiveGenericMask(), 4)
App.GetDocument().GetGenericMaskByName("cortical").Activate()
App.GetDocument().MoveMaskTo(App.GetDocument().GetActiveGenericMask(), 5)
App.GetDocument().GetGenericMaskByName("cancellous").Activate()
App.GetDocument().MoveMaskTo(App.GetDocument().GetActiveGenericMask(), 6)
App.GetDocument().GetGenericMaskByName("bone").Activate()
App.GetDocument().MoveMaskTo(App.GetDocument().GetActiveGenericMask(), 7)
App.GetDocument().GetGenericMaskByName("blood").Activate()
App.GetDocument().MoveMaskTo(App.GetDocument().GetActiveGenericMask(), 8)
App.GetDocument().GetGenericMaskByName("air").Activate()
App.GetDocument().MoveMaskTo(App.GetDocument().GetActiveGenericMask(), 9)
App.GetDocument().GetGenericMaskByName("csf").Activate()
App.GetDocument().MoveMaskTo(App.GetDocument().GetActiveGenericMask(), 10)
App.GetDocument().GetGenericMaskByName("eyes").Activate()
App.GetDocument().MoveMaskTo(App.GetDocument().GetActiveGenericMask(), 11)
App.GetDocument().GetGenericMaskByName("gm").Activate()
App.GetDocument().MoveMaskTo(App.GetDocument().GetActiveGenericMask(), 12)
App.GetDocument().GetGenericMaskByName("wm").Activate()
App.GetDocument().MoveMaskTo(App.GetDocument().GetActiveGenericMask(), 13)

# Visibility
App.GetDocument().IsolateMasks(
    [App.GetDocument().GetGenericMaskByName("wm"),
    App.GetDocument().GetGenericMaskByName("gm"),
    App.GetDocument().GetGenericMaskByName("eyes"),
    App.GetDocument().GetGenericMaskByName("air"),
    App.GetDocument().GetGenericMaskByName("blood"),
    App.GetDocument().GetGenericMaskByName("bone"),
    App.GetDocument().GetGenericMaskByName("skin"),
    App.GetDocument().GetGenericMaskByName("fat"),
    App.GetDocument().GetGenericMaskByName("muscle"),
    App.GetDocument().GetGenericMaskByName("csf")])
