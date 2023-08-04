# Import operating system and Simpleware modules
import os
import scanip_api3 as sip

""" 
quality_check_functions.py 

This module contains the functions used during the segmentation quality checking process. 

Author: Sam Pedersen
Date: 2023-07-20
"""


"""
########################################################################################################################
                                                !!! README !!!
- This module is intended for use within Synopsys Simpleware ScanIP's scripting environment
- These functions *cannot* be executed outside Simpleware or within alternative IDEs
- Simpleware's scripting environment will not re-import modules within the same session; if any edits are made to this
        module, exit Simpleware entirely and begin a new session. Otherwise, Simpleware will continue executing the 
        originally imported version of the module
- Before using this module, it must be added to the path within Simpleware and imported. As a result, it is 
    recommended to run the other scripts hosted in the quality checking script folder, which are written with importing 
    settings and necessary functions called appropriately.
#######################################################################################################################    
"""





# Function to display message box
def message_box(msg):
    """

    Function to display a message within a pop-up dialogue box.

    :param msg: (str) Message to be displayed

    """
    # Display a dialogue box with the designated message
    sip.App.GetInstance().ShowMessage(msg)





# Verify that the module has been imported
def verify_import():
    """

    Verifies to the user that the module has been successfully imported to the Simpleware environment.

    """
    # Displays predetermined message within dialogue box
    message_box("Quality check module imported successfully.")





# Set masks to pre-established colors and order within Simpleware
def colors_order_visibility():
    """

        Assigns tissues their respective colors and order of appearance within Simpleware.

        """

    # List of mask names
    masks = ["wm", "gm", "eyes", "csf", "air", "blood", "cancellous", "cortical", "skin", "fat", "muscle"]

    # Establish a dictionary for tissues and color codes
    color_dict = {
        "air": (65, 65, 65),
        "blood": (200, 0, 0),
        "cancellous": (22, 167, 11),
        "cortical": (0, 255, 0),
        "csf": (107, 220, 220),
        "eyes": (194, 230, 230),
        "fat": (239, 217, 151),
        "gm": (176, 176, 176),
        "muscle": (255, 64, 64),
        "skin": (140, 120, 83),
        "wm": (207, 221, 220),
    }

    # Establish order of tissues
    order_dict = {
        "air": 7,
        "blood": 6,
        "cancellous": 5,
        "cortical": 4,
        "csf": 8,
        "eyes": 9,
        "fat": 2,
        "gm": 10,
        "muscle": 1,
        "skin": 3,
        "wm": 11
    }

    # For each mask...
    for mask in masks:
        # Establish variables
        name = mask
        color = color_dict[name]
        order = order_dict[name]

        # Select specific mask
        sip.App.GetDocument().GetGenericMaskByName(name).Activate()

        # Set color
        sip.App.GetDocument().GetActiveGenericMask().SetColour(sip.Colour(*color))

        # Set order
        sip.App.GetDocument().MoveMaskTo(sip.App.GetDocument().GetActiveGenericMask(), order)

        # Make visible
        sip.App.GetDocument().GetActiveGenericMask().SetVisible(True)





# Remove the overlap between masks
def remove_overlap():
    """

    Removes the overlap/intersection between masks based on priority of tissues.

    """

    # Greymatter minus whitematter
    sip.App.GetDocument().ReplaceMaskUsingBooleanExpression("(gm MINUS wm)", sip.App.GetDocument().GetMaskByName("gm"),
                                                            sip.App.GetDocument().GetSliceIndices(sip.Doc.OrientationXY),
                                                            sip.Doc.OrientationXY)

    # Whitematter minus (eyes, csf)
    sip.App.GetDocument().ReplaceMaskUsingBooleanExpression("(wm MINUS eyes MINUS csf)",
                                                            sip.App.GetDocument().GetMaskByName("wm"),
                                                            sip.App.GetDocument().GetSliceIndices(sip.Doc.OrientationXY),
                                                            sip.Doc.OrientationXY)

    # Air minus (wm, gm, csf, blood, skin)
    sip.App.GetDocument().ReplaceMaskUsingBooleanExpression("(air MINUS wm MINUS gm MINUS csf MINUS blood MINUS skin)",
                                                            sip.App.GetDocument().GetMaskByName("air"),
                                                            sip.App.GetDocument().GetSliceIndices(sip.Doc.OrientationXY),
                                                            sip.Doc.OrientationXY)

    # Blood minus (wm, gm, eyes, skin)
    sip.App.GetDocument().ReplaceMaskUsingBooleanExpression("(blood MINUS wm MINUS gm MINUS eyes MINUS skin)",
                                                            sip.App.GetDocument().GetMaskByName("blood"),
                                                            sip.App.GetDocument().GetSliceIndices(sip.Doc.OrientationXY),
                                                            sip.Doc.OrientationXY)

    # Cortical minus (wm, gm, air, eyes, blood)
    sip.App.GetDocument().ReplaceMaskUsingBooleanExpression("(cortical MINUS wm MINUS gm MINUS air MINUS eyes MINUS blood)",
                                                            sip.App.GetDocument().GetMaskByName("cortical"),
                                                            sip.App.GetDocument().GetSliceIndices(sip.Doc.OrientationXY),
                                                            sip.Doc.OrientationXY)

    # Cancellous minus (wm, gm, air, eyes, blood)
    sip.App.GetDocument().ReplaceMaskUsingBooleanExpression("(cancellous MINUS wm MINUS gm MINUS air MINUS eyes MINUS blood)",
                                                            sip.App.GetDocument().GetMaskByName("cancellous"),
                                                            sip.App.GetDocument().GetSliceIndices(sip.Doc.OrientationXY),
                                                            sip.Doc.OrientationXY)

    # Cortical minus (skin, cancellous, csf)
    sip.App.GetDocument().ReplaceMaskUsingBooleanExpression("(cortical MINUS skin MINUS cancellous MINUS csf)",
                                                            sip.App.GetDocument().GetMaskByName("cortical"),
                                                            sip.App.GetDocument().GetSliceIndices(sip.Doc.OrientationXY),
                                                            sip.Doc.OrientationXY)

    # Cancellous minus (skin, csf)
    sip.App.GetDocument().ReplaceMaskUsingBooleanExpression("(cancellous MINUS skin MINUS csf)",
                                                            sip.App.GetDocument().GetMaskByName("cancellous"),
                                                            sip.App.GetDocument().GetSliceIndices(sip.Doc.OrientationXY),
                                                            sip.Doc.OrientationXY)

    # Fat minus (skin, wm, gm, eyes, air, blood, cortical, cancellous, csf)
    sip.App.GetDocument().ReplaceMaskUsingBooleanExpression(
        "(fat MINUS skin MINUS wm MINUS gm MINUS eyes MINUS air MINUS blood MINUS cortical MINUS cancellous MINUS csf)",
        sip.App.GetDocument().GetMaskByName("fat"), sip.App.GetDocument().GetSliceIndices(sip.Doc.OrientationXY),
        sip.Doc.OrientationXY)

    # Muscle minus (skin, wm, gm, eyes, air, blood, cortical, cancellous, csf, fat)
    sip.App.GetDocument().ReplaceMaskUsingBooleanExpression(
        "(muscle MINUS skin MINUS wm MINUS gm MINUS eyes MINUS air MINUS blood MINUS cortical MINUS cancellous MINUS csf MINUS fat)",
        sip.App.GetDocument().GetMaskByName("muscle"), sip.App.GetDocument().GetSliceIndices(sip.Doc.OrientationXY),
        sip.Doc.OrientationXY)

    # Eyes minus skin
    sip.App.GetDocument().ReplaceMaskUsingBooleanExpression("(eyes MINUS skin)",
                                                            sip.App.GetDocument().GetMaskByName("eyes"),
                                                            sip.App.GetDocument().GetSliceIndices(sip.Doc.OrientationXY),
                                                            sip.Doc.OrientationXY)

    # CSF minus eyes
    sip.App.GetDocument().ReplaceMaskUsingBooleanExpression("(csf MINUS eyes)",
                                                            sip.App.GetDocument().GetMaskByName("csf"),
                                                            sip.App.GetDocument().GetSliceIndices(sip.Doc.OrientationXY),
                                                            sip.Doc.OrientationXY)





# Generate the initial quality check #1 .sip file
def generate_base_file(participant_id, folder_location):
    """

    Creates a new .sip file by loading in the participant's T1.RAW, imports tissue masks, sets the masks' colors and
    orders, and saves it as a base .sip file within the participant's quality checking folder.

    :param participant_id: (int) Participant's 6-digit identifying number (ie, 999999 or 103485)
    :param folder_location: (str) Directory location that the participant's individual folder is contained within

    """

    # Establish participant's folder and location
    participantFolder = folder_location + "FS6.0_sub-" + str(participant_id) + "_ses01\\"

    ### Check for T1.raw:
    # Participant's T1s usually exist within their base participant folder, but may exist in
    # potentially one of two formats:
    #   - FS6.0_sub-999999_ses01_T1_rs.RAW
    #   - T1.RAW
    # The following for loop will check if either of these versions exist in the participant's folder;
    # if one version exists, it will continue the following functions; if it is unable to find either version in the
    # participant's folder, it will skip to the else clause at the end to display the dialogue window

    ### Checking for T1.raw:
    # Preallocate T1 variable
    T1 = None
    # Naming structure, option 1
    t1Name1 = f"FS6.0sub-{str(participant_id)}_ses01_T1_rs.RAW"
    # Naming structure, option 2
    t1Name2 = "T1.RAW"
    # List of T1 naming options (1 and 2)
    t1Names = [t1Name1, t1Name2]

    ### Check the T1 naming structure
    # For each naming option...
    for name in t1Names:
        # Identify T1_path as the full pathway to the participant's folder combined with each naming version
        T1_path = participantFolder + name
        # If a version of the T1 exists in the participant's folder...
        if os.path.exists(T1_path):
            T1 = T1_path  # ... set T1 to be the T1 path location and...
            break  # ... stop looking for a T1.

    ### If able to locate a T1 file:
    if T1:
        # Load the T1 into a new sip file
        sip.App.GetInstance().ImportRawImage(T1,
                                             sip.ImportOptions.DoublePixel, 256, 256, 256, 1.0, 1.0, 1.0, 0,
                                             sip.ImportOptions.BinaryFile, sip.ImportOptions.LittleEndian,
                                             sip.CommonImportConstraints().SetWindowLevel(0.0, 0.0).SetCrop(0, 0, 0,
                                                                                                            256, 256,
                                                                                                            256).SetPixelType(
                                                 sip.Doc.Float32)
                                             )

        # Rename background image as <participant_id>_T1
        sip.App.GetDocument().GetBackgroundByName("Raw import [W:0.00 L:0.00]").SetName(str(participant_id) + "_T1")

        # Begin importing final tissue masks
        # Establish location for finalized masks from participant's folder
        maskLocation = participantFolder + "Binarized_masks\\idv_mask\\"
        # List of masks to be imported
        masks = ["wm", "gm", "eyes", "csf", "air", "blood", "cancellous", "cortical", "skin", "fat", "muscle"]

        ### For each mask in the list...
        for mask in masks:
            # ... Set the name as the particular mask...
            maskName = mask
            # ... Import info, combining the mask name and import source location...
            importInfo = maskLocation + maskName + ".raw"

            # ... Import tissue mask as background image...
            sip.App.GetInstance().GetActiveDocument().ImportBackgroundFromRawImage(
                importInfo,
                sip.ImportOptions.UnsignedCharPixel, 256, 256, 256, 1, 1, 1, 0,
                sip.ImportOptions.BinaryFile, sip.ImportOptions.LittleEndian,
                sip.CommonImportConstraints().SetWindowLevel(0, 0).SetCrop(0, 0, 0, 256, 256, 256)
            )
            # ... Rename background image to mask's name...
            sip.App.GetDocument().GetBackgroundByName("Raw import [W:0.00 L:0.00]").SetName(maskName)
            # ... Copy background image into mask...
            sip.App.GetDocument().CopyBackgroundToMask()
            # ... Delete imported background image
            sip.App.GetDocument().RemoveBackground(sip.App.GetDocument().GetBackgroundByName(maskName))

        ### Colors and order
        # Call the colorsOrderVisibility() function above
        colors_order_visibility()

        ### Save file as <999999>_base.sip to participant's quality checking folder
        qcSave = f"{participantFolder}qualityCheck\\sipFiles\\{str(participant_id)}_base.sip"
        sip.App.GetDocument().SaveAs(qcSave)

    ### If the T1 was not locatable, display a dialogue box indicating such
    else:
        message_box("No RAW T1 scan found.")



# Finalize the .sip file, save and export tissues
def finalize_sip_file(participant_id,folder_location,check_stage):
    """

    Standardizes the colors/order/visibility of the masks in the .sip file before removing intersecting overlap,
    binarizing and exporting the tissue masks to the quality check folder, and saving the .sip file.

    :param participant_id: (int) Participant's 6-digit identifying number (ie, 999999 or 103485)
    :param folder_location: (str) Directory location that the participant's individual folder is contained within
    :param check_stage: (int) Should be either 1 or 2 to indicate if this is the end of quality check #1 or #2

    """

    # Establish participant's folder and location
    participantFolder = f"{folder_location}FS6.0_sub-{participant_id}_ses01\\qualityCheck\\"

    # Masks to binarize/export
    masks = ["wm", "gm", "eyes", "csf", "air", "blood", "cancellous", "cortical", "skin", "fat", "muscle"]

    # Standardize colors and order
    colors_order_visibility()
    # Separate masks
    remove_overlap()

    # Binarize and export tissue masks
    for mask in masks:
        name = mask
        exportLocation = f"{participantFolder}tissueMasks\\"
        exportingMask = exportLocation + name + ".raw"


        # Binarize
        sip.App.GetDocument().GetGenericMaskByName(name).Activate()
        sip.App.GetDocument().ApplyBinarisationFilter()

        # Export the mask
        sip.App.GetDocument().GetMaskByName(name).RawExport(exportingMask)


    # Save project
    sip.App.GetDocument().SaveAs(f"{participantFolder}sipFiles\\{participant_id}_QC{check_stage}.sip")





def stop_start_visual_checks(currentParticipant, checkStage, nextParticipant, folderLocation):
    # Close out current file
    finalize_sip_file(currentParticipant, folderLocation, checkStage)
    sip.App.GetDocument().Close()
    # Open next participant
    importFiles(nextParticipant,folderLocation)

