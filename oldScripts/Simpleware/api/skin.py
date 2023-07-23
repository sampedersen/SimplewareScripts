# Generate the intial skin mask
# Created by Samantha Pedersen (09/13/2021)
# Last updated: 07/25/2022
#! python3
from scanip_api3 import *

########################################################################################################################
###########################################       !!! README !!!         ###############################################
########################################################################################################################

# Script function:
#   1. Generate the initial skin mask
#   2. Generate the bottom 2 slices of the skin 
#   3. Generate the eyelids 
#   4. Generate "guidelines" mask 
#   5. Reorganize project file 

# Masks being used (make sure these exist in the project file):
#   - "uniform"
#   - "eyes"
#   - "eyes interior"

# Mask names to be avoided (make sure these names are not currently contained in the project file)
# Having a duplicate name will cause the script to crash. Either delete the mask/rename it
#   - "Copy of uniform"
#   - "skin"
#   - "bottom"
#   - "Copy of bottom"
#   - "eyelids"
#   - "negative_space"
#   - "skin_eyelids"

# Notes:
#   - Script will generate an initial skin mask that is approx 2 voxels thick 
#   - Manual cleaning must be applied afterwards
#       - Particularly, check the bottom 2 slices and clean-up in the interior edge
#       - Union "bottom" with "skin_eyelids" following clean-up

# !! IMPORTANT !! 
# Some T1 images may have the bottom portion of the head prematurely cropped (ie, chin is excluded)
# View the T1 within the axial perspective and identify the lowest slice *not* cropped
# Replace "height" with this identified slice number
# Example: If the headscan shows poor cropping in slices 1-7, height = 8
height = 5

i = 0
listOfSlices = []
while i <= height:
    listOfSlices.append(i)
    i += 1

j = height+1
removeSlices = []
while j < 256:
    removeSlices.append(j)
    j += 1


########################################################################################################################


# Generate initial skin mask 
App.GetDocument().GetGenericMaskByName("uniform").Activate()
App.GetDocument().GetActiveGenericMask().Duplicate()
App.GetDocument().GetGenericMaskByName("Copy of uniform").Activate()
App.GetDocument().GetGenericMaskByName("Copy of uniform").SetName("skin")

App.GetDocument().ApplyErodeFilter(Doc.TargetMask, 2, 2, 2, 0)
App.GetDocument().GetGenericMaskByName("skin").Activate()
App.GetDocument().ReplaceMaskUsingBooleanExpression("(NOT skin)", App.GetDocument().GetMaskByName("skin"),
                                                    App.GetDocument().GetSliceIndices(Doc.OrientationYZ), Doc.OrientationYZ)

App.GetDocument().GetGenericMaskByName("skin").Activate()
App.GetDocument().ReplaceMaskUsingBooleanExpression("(skin AND uniform)", App.GetDocument().GetMaskByName("skin"),
                                                    App.GetDocument().GetSliceIndices(Doc.OrientationYZ), Doc.OrientationYZ)

App.GetDocument().GetActiveMask().Unpaint([Point3D(128, 128, 1)], Mask.Disk, 300, True, [0, 1, 2], Doc.OrientationXY, True)




# Generate bottom 2 slices of skin mask 
App.GetDocument().CreateMask("bottom", Colour(255, 0, 191))
App.GetDocument().GetGenericMaskByName("bottom").Activate()
App.GetDocument().GetActiveMask().Paint([Point3D(128, 128, 1)], Mask.Disk, 300, True, [0, 1, 2], Doc.OrientationXY, True)
App.GetDocument().ReplaceMaskUsingBooleanExpression("(bottom AND uniform)",
                                                    App.GetDocument().GetMaskByName("bottom"),
                                                    App.GetDocument().GetSliceIndices(Doc.OrientationXY), Doc.OrientationXY)
App.GetDocument().GetGenericMaskByName("bottom").Activate()
App.GetDocument().ApplyErodeFilter(Doc.TargetMask, 2, 2, 0, 0)
App.GetDocument().GetGenericMaskByName("bottom").Activate()
App.GetDocument().ReplaceMaskUsingBooleanExpression("(NOT bottom)", App.GetDocument().GetMaskByName("bottom"),
                                                    App.GetDocument().GetSliceIndices(Doc.OrientationXY), Doc.OrientationXY)
App.GetDocument().ReplaceMaskUsingBooleanExpression("(bottom AND uniform)", App.GetDocument().GetMaskByName("bottom"),
                                                    App.GetDocument().GetSliceIndices(Doc.OrientationXY), Doc.OrientationXY)
App.GetDocument().GetActiveMask().Unpaint([Point3D(115, 129, 3)], Mask.Disk, 300, True,
    [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
    23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41,
    42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
    61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79,
    80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98,
    99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113,
    114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128,
    129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143,
    144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158,
    159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173,
    174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188,
    189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203,
    204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218,
    219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233,
    234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248,
    249, 250, 251, 252, 253, 254, 255],
    Doc.OrientationXY, True)
App.GetDocument().ReplaceMaskUsingBooleanExpression("(skin OR bottom)",
                                                    App.GetDocument().GetMaskByName("skin"),
                                                    App.GetDocument().GetSliceIndices(Doc.OrientationXY), Doc.OrientationXY)



# Generate eyelids
App.GetDocument().GetGenericMaskByName("eyes").Activate()
App.GetDocument().GetActiveGenericMask().Duplicate()
App.GetDocument().GetGenericMaskByName("Copy of eyes").Activate()
App.GetDocument().GetGenericMaskByName("Copy of eyes").SetName("eyelids")
App.GetDocument().ApplyDilateFilter(Doc.TargetMask, 2, 2, 2, 0)
App.GetDocument().ReplaceMaskUsingBooleanExpression("(eyelids MINUS \"eyes interior\")",
                                                    App.GetDocument().GetMaskByName("eyelids"),
                                                    App.GetDocument().GetSliceIndices(Doc.OrientationXY), Doc.OrientationXY)
App.GetDocument().ReplaceMaskUsingBooleanExpression("(eyelids MINUS eyes)",
                                                    App.GetDocument().GetMaskByName("eyelids"),
                                                    App.GetDocument().GetSliceIndices(Doc.OrientationXY), Doc.OrientationXY)
App.GetDocument().GetGenericMaskByName("uniform").Activate()
App.GetDocument().GetActiveGenericMask().Duplicate()
App.GetDocument().GetGenericMaskByName("Copy of uniform").Activate()
App.GetDocument().ReplaceMaskUsingBooleanExpression("(NOT \"Copy of uniform\")",
                                                    App.GetDocument().GetMaskByName("Copy of uniform"),
                                                    App.GetDocument().GetSliceIndices(Doc.OrientationXY), Doc.OrientationXY)
App.GetDocument().GetGenericMaskByName("Copy of uniform").SetName("negative_space")
App.GetDocument().ReplaceMaskUsingBooleanExpression("((negative_space AND (eyelids MINUS skin)) OR (eyelids AND (skin MINUS negative_space)))",
                                                    App.GetDocument().GetMaskByName("eyelids"),
                                                    App.GetDocument().GetSliceIndices(Doc.OrientationXY), Doc.OrientationXY)
App.GetDocument().GetGenericMaskByName("skin").Activate()
App.GetDocument().GetActiveGenericMask().Duplicate()
App.GetDocument().GetGenericMaskByName("Copy of skin").Activate()
App.GetDocument().GetGenericMaskByName("Copy of skin").SetName("skin_eyelids")
App.GetDocument().ReplaceMaskUsingBooleanExpression("(skin_eyelids MINUS eyes)",
                                                    App.GetDocument().GetMaskByName("skin_eyelids"),
                                                    App.GetDocument().GetSliceIndices(Doc.OrientationXY), Doc.OrientationXY)
App.GetDocument().ReplaceMaskUsingBooleanExpression("(skin_eyelids MINUS \"eyes interior\")",
                                                    App.GetDocument().GetMaskByName("skin_eyelids"),
                                                    App.GetDocument().GetSliceIndices(Doc.OrientationXY), Doc.OrientationXY)
App.GetDocument().ReplaceMaskUsingBooleanExpression("(skin_eyelids OR eyelids)",
                                                    App.GetDocument().GetMaskByName("skin_eyelids"),
                                                    App.GetDocument().GetSliceIndices(Doc.OrientationXY), Doc.OrientationXY)


# Generate "bottom_corrections" mask
App.GetDocument().GetGenericMaskByName("uniform").Activate()
App.GetDocument().GetActiveGenericMask().Duplicate()
App.GetDocument().GetGenericMaskByName("Copy of uniform").Activate()
App.GetDocument().GetGenericMaskByName("Copy of uniform").SetName("bottom_corrections")
App.GetDocument().GetGenericMaskByName("bottom_corrections").Activate()
App.GetDocument().ApplyErodeFilter(Doc.TargetMask, 2, 2, 0, 0)
App.GetDocument().GetGenericMaskByName("bottom_corrections").Activate()
App.GetDocument().ReplaceMaskUsingBooleanExpression("(NOT bottom_corrections)", App.GetDocument().GetMaskByName("bottom_corrections"), App.GetDocument().GetSliceIndices(Doc.OrientationXY), Doc.OrientationXY)
App.GetDocument().ReplaceMaskUsingBooleanExpression("(bottom_corrections AND uniform)", App.GetDocument().GetMaskByName("bottom_corrections"),
    listOfSlices, Doc.OrientationXY)
App.GetDocument().GetGenericMaskByName("bottom_corrections").Activate()
removeFrom = height + 1
App.GetDocument().GetActiveMask().Unpaint([Point3D(128, 128, removeFrom)], Mask.Disk, 300, True,
    removeSlices, Doc.OrientationXY, True)
App.GetDocument().GetActiveMask().Unpaint([Point3D(225, 25, removeFrom)], Mask.Disk, 300, True,
    removeSlices, Doc.OrientationXY, True)
App.GetDocument().GetActiveMask().Unpaint([Point3D(25, 25, removeFrom)], Mask.Disk, 300, True,
    removeSlices, Doc.OrientationXY, True)
App.GetDocument().GetActiveMask().Unpaint([Point3D(25, 225, removeFrom)], Mask.Disk, 300, True,
    removeSlices, Doc.OrientationXY, True)
App.GetDocument().GetActiveMask().Unpaint([Point3D(225, 225, removeFrom)], Mask.Disk, 300, True,
    removeSlices, Doc.OrientationXY, True)


# Re-organize Project Files 
App.GetDocument().RemoveMasks(
    [App.GetDocument().GetGenericMaskByName("negative_space"),
    App.GetDocument().GetGenericMaskByName("skin"),
    App.GetDocument().GetGenericMaskByName("eyelids"),
    App.GetDocument().GetGenericMaskByName("bottom")])
App.GetDocument().GetGenericMaskByName("skin_eyelids").SetName("skin")
App.GetDocument().IsolateMasks([App.GetDocument().GetGenericMaskByName("skin"),
    App.GetDocument().GetGenericMaskByName("bottom_corrections")])


