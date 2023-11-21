"""
bone_patching.py

Automate pre-processing applications to bone mask for quality checking procedures.

Author: Sam Pedersen
Date: 2023-11-14

########################################################################################################################
"""
"""
Notes:
- WIP
- patched_bone is the final patched bone mask
- unpatched_bone_regions indicates the areas that did not get patched 
- patched_bone_regions_raw indicates areas that received patch processing, before corrections
- patched_bone_regions_corrected indicates areas that received patch processing, following corrections
- Edits will be derived from whichever mask is called "bone"; original mask and properties will be preserved and untouched
Cannot have:

- Copy of bone
- bone_old

"""

# Import bone, T/F (avoid re-importing if users is re-patching intermittently)
import_bone = False
participant_id = 999999
sublist = "v3"

######

# ! python3
import scanip_api3 as sip
import sys

# Add module to path for importing
module_path = "P:\\WoodsLab\\ACT-head_models\\FEM\\Sam\\Scripts\\Python\\Simpleware\\quality_checking\\"
sys.path.append(module_path)

# Import quality checking module
import quality_check_functions as qc

######



if import_bone == True:
    # Import bone if needed; importing from Binarized_masks\final
    # Determine base directory location based on sublist
    base_dir = "P:\\WoodsLab\\ACT-head_models\\FEM\\manual_segmentation\\allParticipants\\"
    if sublist == "v1":
        base_location = f"{base_dir}PL_v1\\"
    elif sublist == "v2":
        base_location = f"{base_dir}PL_v2\\"
    elif sublist == "v3":
        base_location = f"{base_dir}PL_v3\\"
    elif sublist == "ET_old":
        base_location = f"{base_dir}PL_ETold\\"
    elif sublist == "ET_new":
        base_location = f"{base_dir}PL_ETnew\\"
    else:
        qc.message_box("No directory found at the sublist specified. Please ensure that you entered either v1, v2, v3, "
                       "ET_old, or ET_new.")
        base_location = "None"
        exit()
    # Define path to participant's folder
    participant_folder = f"{base_location}FS6.0_sub-{participant_id}_ses01\\"
    # Define path to participant's tissue masks folder
    mask_folder = f"{participant_folder}\\Binarized_masks\\final\\"
    qc.import_mask("bone",mask_folder)
    App.GetDocument().GetGenericMaskByName("bone_old").SetName("bone")

# Duplicate base bone masks to isolate large regions of skull
App.GetDocument().GetGenericMaskByName("bone").Activate()
App.GetDocument().GetActiveGenericMask().Duplicate()
App.GetDocument().GetGenericMaskByName("Copy of bone").SetName("unpatched_bone_regions")

# Isolate regions thicker than 1 voxel and bigger than 15 voxels as an island
App.GetDocument().GetGenericMaskByName("unpatched_bone_regions").Activate()
App.GetDocument().ApplyErodeFilter(Doc.TargetMask, 1, 1, 1, 0)
App.GetDocument().ApplyIslandRemovalFilter(15)

# Redilate mask, intersect with original bone mask
App.GetDocument().ApplyDilateFilter(Doc.TargetMask, 1, 1, 1, 0)
App.GetDocument().ReplaceMaskUsingBooleanExpression("(unpatched_bone_regions AND bone)", App.GetDocument().GetMaskByName("unpatched_bone_regions"), App.GetDocument().GetSliceIndices(Doc.OrientationXY), Doc.OrientationXY)

# Duplicate to isolate small pieces, removing islands smaller than 15
App.GetDocument().GetGenericMaskByName("bone").Activate()
App.GetDocument().GetActiveGenericMask().Duplicate()
App.GetDocument().GetGenericMaskByName("Copy of bone").Activate()
App.GetDocument().GetGenericMaskByName("Copy of bone").SetName("patched_bone_regions_raw")
App.GetDocument().ReplaceMaskUsingBooleanExpression("(patched_bone_regions_raw MINUS unpatched_bone_regions)", App.GetDocument().GetMaskByName("patched_bone_regions_raw"), App.GetDocument().GetSliceIndices(Doc.OrientationXY), Doc.OrientationXY)
App.GetDocument().GetGenericMaskByName("patched_bone_regions_raw").Activate()
App.GetDocument().ApplyIslandRemovalFilter(15)

# Duplicate and create patched mask
App.GetDocument().GetActiveGenericMask().Duplicate()
App.GetDocument().GetGenericMaskByName("Copy of patched_bone_regions_raw").Activate()
App.GetDocument().GetGenericMaskByName("Copy of patched_bone_regions_raw").SetName("patched_bone_regions_corrected")
App.GetDocument().ApplyCloseFilter(Doc.TargetMask, 2, 2, 2, 0)
App.GetDocument().ApplyDilateFilter(Doc.TargetMask, 1, 1, 1, 0)

# Remove potential overlap in interior region
App.GetDocument().ReplaceMaskUsingBooleanExpression("(patched_bone_regions_corrected MINUS wm)", App.GetDocument().GetMaskByName("patched_bone_regions_corrected"), App.GetDocument().GetSliceIndices(Doc.OrientationXY), Doc.OrientationXY)
App.GetDocument().ReplaceMaskUsingBooleanExpression("(patched_bone_regions_corrected MINUS gm)", App.GetDocument().GetMaskByName("patched_bone_regions_corrected"), App.GetDocument().GetSliceIndices(Doc.OrientationXY), Doc.OrientationXY)
App.GetDocument().ReplaceMaskUsingBooleanExpression("(patched_bone_regions_corrected MINUS csf)", App.GetDocument().GetMaskByName("patched_bone_regions_corrected"), App.GetDocument().GetSliceIndices(Doc.OrientationXY), Doc.OrientationXY)

# Create patched bone mask
App.GetDocument().GetGenericMaskByName("patched_bone_regions_corrected").Activate()
App.GetDocument().GetActiveGenericMask().Duplicate()
App.GetDocument().GetGenericMaskByName("Copy of patched_bone_regions_corrected").Activate()
App.GetDocument().GetGenericMaskByName("Copy of patched_bone_regions_corrected").SetName("patched_bone")
App.GetDocument().ReplaceMaskUsingBooleanExpression("(patched_bone OR bone)", App.GetDocument().GetMaskByName("patched_bone"), App.GetDocument().GetSliceIndices(Doc.OrientationYZ), Doc.OrientationYZ)




