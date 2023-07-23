# Separate tissue masks to remove overlapping voxels
# Created by Samantha Pedersen (10/12/2021)
# Last updated: 07/25/2022
#! python3
from scanip_api3 import *

########################################################################################################################
###########################################       !!! README !!!         ###############################################
########################################################################################################################

# Script function:
#       1. Separate masks by deleting any overlap

# Masks being used (make sure these exist in the project file):
#   - "wm"
#   - "gm"
#   - "eyes"
#   - "csf"
#   - "air"
#   - "blood"
#   - "cancellous"
#   - "cortical"
#   - "skin"
#   - "fat"
#   - "muscle"


########################################################################################################################
###########################################       Tissue Separation      ###############################################
########################################################################################################################

# Greymatter minus whitematter
App.GetDocument().ReplaceMaskUsingBooleanExpression("(gm MINUS wm)",
                                                    App.GetDocument().GetMaskByName("gm"),
                                                    App.GetDocument().GetSliceIndices(Doc.OrientationXY),
                                                    Doc.OrientationXY)

# Whitematter mins (eyes, csf)
App.GetDocument().ReplaceMaskUsingBooleanExpression("(wm MINUS eyes MINUS csf)",
                                                    App.GetDocument().GetMaskByName("wm"),
                                                    App.GetDocument().GetSliceIndices(Doc.OrientationXY),
                                                    Doc.OrientationXY)

# Air minus (wm, gm, csf, blood, skin)
App.GetDocument().ReplaceMaskUsingBooleanExpression("(air MINUS wm MINUS gm MINUS csf MINUS blood MINUS skin)",
                                                    App.GetDocument().GetMaskByName("air"),
                                                    App.GetDocument().GetSliceIndices(Doc.OrientationXY),
                                                    Doc.OrientationXY)

# Blood minus (wm, gm, eyes, skin)
App.GetDocument().ReplaceMaskUsingBooleanExpression("(blood MINUS wm MINUS gm MINUS eyes MINUS skin)",
                                                    App.GetDocument().GetMaskByName("blood"),
                                                    App.GetDocument().GetSliceIndices(Doc.OrientationXY),
                                                    Doc.OrientationXY)

# Cortical minus (wm, gm, air, eyes, blood)
App.GetDocument().ReplaceMaskUsingBooleanExpression("(cortical MINUS wm MINUS gm MINUS air MINUS eyes MINUS blood)",
                                                    App.GetDocument().GetMaskByName("cortical"),
                                                    App.GetDocument().GetSliceIndices(Doc.OrientationXY),
                                                    Doc.OrientationXY)

# Cancellous minus (wm, gm, air, eyes, blood)
App.GetDocument().ReplaceMaskUsingBooleanExpression("(cancellous MINUS wm MINUS gm MINUS air MINUS eyes MINUS blood)",
                                                    App.GetDocument().GetMaskByName("cancellous"),
                                                    App.GetDocument().GetSliceIndices(Doc.OrientationXY),
                                                    Doc.OrientationXY)

# Cortical minus (skin, cancellous, csf)
App.GetDocument().ReplaceMaskUsingBooleanExpression("(cortical MINUS skin MINUS cancellous MINUS csf)",
                                                    App.GetDocument().GetMaskByName("cortical"),
                                                    App.GetDocument().GetSliceIndices(Doc.OrientationXY),
                                                    Doc.OrientationXY)

# Cancellous minus (skin, csf)
App.GetDocument().ReplaceMaskUsingBooleanExpression("(cancellous MINUS skin MINUS csf)",
                                                    App.GetDocument().GetMaskByName("cancellous"),
                                                    App.GetDocument().GetSliceIndices(Doc.OrientationXY),
                                                    Doc.OrientationXY)

# Fat minus (skin, wm, gm, eyes, air, blood, cortical, cancellous, csf)
App.GetDocument().ReplaceMaskUsingBooleanExpression("(fat MINUS skin MINUS wm MINUS gm MINUS eyes MINUS air MINUS blood MINUS cortical MINUS cancellous MINUS csf)",
                                                    App.GetDocument().GetMaskByName("fat"),
                                                    App.GetDocument().GetSliceIndices(Doc.OrientationXY), 
                                                    Doc.OrientationXY)

# Muscle minus (skin, wm, gm, eyes, air, blood, cortical, cancellous, csf, fat)
App.GetDocument().ReplaceMaskUsingBooleanExpression("(muscle MINUS skin MINUS wm MINUS gm MINUS eyes MINUS air MINUS blood MINUS cortical MINUS cancellous MINUS csf MINUS fat)",
                                                    App.GetDocument().GetMaskByName("muscle"),
                                                    App.GetDocument().GetSliceIndices(Doc.OrientationXY), 
                                                    Doc.OrientationXY)

# Eyes minus skin
App.GetDocument().ReplaceMaskUsingBooleanExpression("(eyes MINUS skin)",
                                                    App.GetDocument().GetMaskByName("eyes"),
                                                    App.GetDocument().GetSliceIndices(Doc.OrientationXY), 
                                                    Doc.OrientationXY)

# CSF minus eyes
App.GetDocument().ReplaceMaskUsingBooleanExpression("(csf MINUS eyes)",
                                                    App.GetDocument().GetMaskByName("csf"),
                                                    App.GetDocument().GetSliceIndices(Doc.OrientationXY), 
                                                    Doc.OrientationXY)
