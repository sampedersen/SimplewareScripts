"""
segmentation.py

Module for implementing segmentation-related functions

This module contains functions for displaying a message within a dialogue box, verifies module importing to user,
standardized tissue mask colors, remove tissue overlap, generate initial skin tissue mask, (re)generate CSF and 10
masks,

Author: Sam Pedersen
Date: 23 July 2023

---------------------

Notes for use:
- This module's functions are intended to be use within Synopsys Simpleware ScanIP's scripting environment
- As is, these functions *cannot* be executed outside Simpleware or within alternative IDEs
- Simpleware's scripting environment will not re-import modules during the same session; if any edits are made to this
    module, exit Simpleware entirely and begin a new session. Otherwise, Simpleware will continue executing the version
    of the module originally imported
- This module is not intended for direct execution, only for external importing

"""


# Import operating system and Simpleware modules
import os
import scanip_api3 as sip


# Function to display message box
def message_box(msg):

    """

    Function to display a message within a pop-up dialogue box.

    Args:
        msg (str): Message to be displayed

    Returns:
        None

    """

    # Display dialogue box and message
    sip.App.GetInstance().ShowMessage(msg)


# Function to verify module has been imported successfully
def verify_import():

    """

    Verifies to user that segmentation.py module was successfully imported to Simpleware environment

    Args:
        None

    Return:
        None

    """

    sip.App.GetInstance().ShowMessage("QCFunctions module imported successfully.")


# Function to standardize colors of tissue masks
def colors_visibility(mask):

    """

    Assigns colors to tissue masks based on name. If trying to change the color of multiple masks at a time, use a for
    loop.

    Args:
        mask (str): Name of the mask to switch colors; must match one of the keys below

    Return:
        None

    """

    # Establish a dictionary of tissue names and their associated RBG color codes
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

    # Select for tissue-specific color
    color = color_dict[mask]
    # Set color and make visible
    sip.App.GetDocument().GetActiveGenericMask().SetColour(sip.Colour(*color))
    sip.App.GetDocument().GetActiveGenericMask().SetVisible(True)


# Function to remove overlap between tissue masks
def separate_masks():

    """

    Separates/removes any overlapping/intersecting masks based on priority of tissues. Must have all 11 masks.

    Args:
        None

    Return:
        None

    """

    # Shorten naming structures
    app = sip.App.GetInstance()
    doc = app.GetDocument()
    sliceIndices = doc.GetSliceIndices(sip.Doc.OrientationXY)
    sliceOrientation = sip.Doc.OrientationXY

    # Perform removal of overlap
    # GM - WM
    doc.ReplaceMaskUsingBooleanExpression("(gm MINUS wm)", doc.GetMaskByName("gm"), sliceIndices, sliceOrientation)
    # WM - (eyes, csf)
    doc.ReplaceMaskUsingBooleanExpression("(wm MINUS eyes MINUS csf)", doc.GetMaskByName("wm"), sliceIndices,
                                          sliceOrientation)
    # air - (wm, gm, csf, blood, skin)
    doc.ReplaceMaskUsingBooleanExpression("(air MINUS wm MINUS gm MINUS csf MINUS blood MINUS skin)",
                                          doc.GetMaskByName("air"), sliceIndices, sliceOrientation)
    # blood - (wm, gm, eyes, skin)
    doc.ReplaceMaskUsingBooleanExpression("(blood MINUS wm MINUS gm MINUS eyes MINUS skin)", doc.GetMaskByName("blood"),
                                          sliceIndices, sliceOrientation)
    # cortical - (wm, gm, air, eyes, blood)
    doc.ReplaceMaskUsingBooleanExpression("(cortical MINUS wm MINUS gm MINUS air MINUS eyes MINUS blood)",
                                          doc.GetMaskByName("cortical"), sliceIndices, sliceOrientation)
    # cancellous - (wm, gm, air, eyes, blood)
    doc.ReplaceMaskUsingBooleanExpression("(cancellous MINUS wm MINUS gm MINUS air MINUS eyes MINUS blood)",
                                          doc.GetMaskByName("cancellous"), sliceIndices, sliceOrientation)
    # cortical - (skin, cancellous, csf)
    doc.ReplaceMaskUsingBooleanExpression("(cortical MINUS skin MINUS cancellous MINUS csf)", doc.GetMaskByName("gm"),
                                          sliceIndices, sliceOrientation)
    # cancellous - (skin, csf)
    doc.ReplaceMaskUsingBooleanExpression("(cancellous MINUS skin MINUS csf)", doc.GetMaskByName("cancellous"),
                                          sliceIndices, sliceOrientation)
    # fat - (skin, wm, gm, eyes, air, blood, cortical, cancellous, csf)
    doc.ReplaceMaskUsingBooleanExpression(
        "(fat MINUS skin MINUS wm MINUS gm MINUS eyes MINUS air MINUS blood MINUS cortical MINUS cancellous MINUS csf)",
        doc.GetMaskByName("fat"), sliceIndices, sliceOrientation)
    # muscle - (skin, wm, gm, eyes, air, blood, cortical, cancellous, csf, fat)
    doc.ReplaceMaskUsingBooleanExpression(
        "(muscle MINUS skin MINUS wm MINUS gm MINUS eyes MINUS air MINUS blood MINUS cortical MINUS cancellous MINUS csf MINUS fat)",
        doc.GetMaskByName("muscle"), sliceIndices, sliceOrientation)
    # eyes - skin
    doc.ReplaceMaskUsingBooleanExpression("(eyes MINUS skin)", doc.GetMaskByName("eyes"), sliceIndices,
                                          sliceOrientation)
    # csf - eyes
    doc.ReplaceMaskUsingBooleanExpression("(csf MINUS eyes)", doc.GetMaskByName("csf"), sliceIndices, sliceOrientation)


# Function to generate the initial skin tissue mask
def segment_skin(lowerBuffer):

    """

    Creates initial skin tissue mask.

    Args:
        lowerBuffer (int): Number of slices, from the bottom, that the T1 scan is interrupted/orthogonally cropped

    Return:
         None

    """

    # Establish buffers
    listOfBufferSlices = [i for i in range(1,lowerBuffer+1)]
    listOfRemovedSlices =  [i for i in range(lowerBuffer+1,257)]
    listOfExtraSlices = [i for i in range(3,257)]

    # Generate initial skin mask
    sip.App.GetDocument().GetGenericMaskByName("uniform").Activate()
    sip.App.GetDocument().GetActiveGenericMask().Duplicate()
    sip.App.GetDocument().GetGenericMaskByName("Copy of uniform").Activate()
    sip.App.GetDocument().GetGenericMaskByName("Copy of uniform").SetName("skin")
    sip.App.GetDocument().ApplyErodeFilter(sip.Doc.TargetMask, 2, 2, 2, 0)
    sip.App.GetDocument().GetGenericMaskByName("skin").Activate()
    sip.App.GetDocument().ReplaceMaskUsingBooleanExpression("(NOT skin)", sip.App.GetDocument().GetMaskByName("skin"),
                                                            sip.App.GetDocument().GetSliceIndices(sip.Doc.OrientationYZ),
                                                            sip.Doc.OrientationYZ)
    sip.App.GetDocument().GetGenericMaskByName("skin").Activate()
    sip.App.GetDocument().ReplaceMaskUsingBooleanExpression("(skin AND uniform)", sip.App.GetDocument().GetMaskByName("skin"),
                                                            sip.App.GetDocument().GetSliceIndices(sip.Doc.OrientationYZ),
                                                            sip.Doc.OrientationYZ)
    sip.App.GetDocument().GetActiveMask().Unpaint([sip.Point3D(128, 128, 1)], sip.Mask.Disk, 300, True, [0, 1, 2],
                                                  sip.Doc.OrientationXY, True)

    # Generate bottom 2 slices of skin mask
    sip.App.GetDocument().CreateMask("bottom", sip.Colour(255, 0, 191))
    sip.App.GetDocument().GetGenericMaskByName("bottom").Activate()
    sip.App.GetDocument().GetActiveMask().Paint([sip.Point3D(128, 128, 1)], sip.Mask.Disk, 300, True, [0, 1, 2],
                                                sip.Doc.OrientationXY, True)
    sip.App.GetDocument().ReplaceMaskUsingBooleanExpression("(bottom AND uniform)",
                                                            sip.App.GetDocument().GetMaskByName("bottom"),
                                                            sip.App.GetDocument().GetSliceIndices(sip.Doc.OrientationXY),
                                                            sip.Doc.OrientationXY)
    sip.App.GetDocument().GetGenericMaskByName("bottom").Activate()
    sip.App.GetDocument().ApplyErodeFilter(sip.Doc.TargetMask, 2, 2, 0, 0)
    sip.App.GetDocument().GetGenericMaskByName("bottom").Activate()
    sip.App.GetDocument().ReplaceMaskUsingBooleanExpression("(NOT bottom)", sip.App.GetDocument().GetMaskByName("bottom"),
                                                        sip.App.GetDocument().GetSliceIndices(sip.Doc.OrientationXY),
                                                        sip.Doc.OrientationXY)
    sip.App.GetDocument().ReplaceMaskUsingBooleanExpression("(bottom AND uniform)",
                                                        sip.App.GetDocument().GetMaskByName("bottom"),
                                                        sip.App.GetDocument().GetSliceIndices(sip.Doc.OrientationXY),
                                                        sip.Doc.OrientationXY)
    sip.App.GetDocument().GetActiveMask().Unpaint([sip.Point3D(115, 129, 3)], sip.Mask.Disk, 300, True, listOfExtraSlices,
                                                  sip.Doc.OrientationXY, True)
    sip.App.GetDocument().ReplaceMaskUsingBooleanExpression("(skin OR bottom)",
                                                        sip.App.GetDocument().GetMaskByName("skin"),
                                                        sip.App.GetDocument().GetSliceIndices(sip.Doc.OrientationXY),
                                                        sip.Doc.OrientationXY)

    # Generate eyelids
    sip.App.GetDocument().GetGenericMaskByName("eyes").Activate()
    sip.App.GetDocument().GetActiveGenericMask().Duplicate()
    sip.App.GetDocument().GetGenericMaskByName("Copy of eyes").Activate()
    sip.App.GetDocument().GetGenericMaskByName("Copy of eyes").SetName("eyelids")
    sip.App.GetDocument().ApplyDilateFilter(sip.Doc.TargetMask, 2, 2, 2, 0)
    sip.App.GetDocument().ReplaceMaskUsingBooleanExpression("(eyelids MINUS \"eyes interior\")",
                                                            sip.App.GetDocument().GetMaskByName("eyelids"),
                                                            sip.App.GetDocument().GetSliceIndices(sip.Doc.OrientationXY),
                                                            sip.Doc.OrientationXY)
    sip.App.GetDocument().ReplaceMaskUsingBooleanExpression("(eyelids MINUS eyes)",
                                                            sip.App.GetDocument().GetMaskByName("eyelids"),
                                                            sip.App.GetDocument().GetSliceIndices(sip.Doc.OrientationXY),
                                                            sip.Doc.OrientationXY)
    sip.App.GetDocument().GetGenericMaskByName("uniform").Activate()
    sip.App.GetDocument().GetActiveGenericMask().Duplicate()
    sip.App.GetDocument().GetGenericMaskByName("Copy of uniform").Activate()
    sip.App.GetDocument().ReplaceMaskUsingBooleanExpression("(NOT \"Copy of uniform\")",
                                                            sip.App.GetDocument().GetMaskByName("Copy of uniform"),
                                                            sip.App.GetDocument().GetSliceIndices(sip.Doc.OrientationXY), sip.Doc.OrientationXY)
    sip.App.GetDocument().GetGenericMaskByName("Copy of uniform").SetName("negative_space")
    sip.App.GetDocument().ReplaceMaskUsingBooleanExpression("((negative_space AND (eyelids MINUS skin)) OR (eyelids AND (skin MINUS negative_space)))",
                                                            sip.App.GetDocument().GetMaskByName("eyelids"),
                                                            sip.App.GetDocument().GetSliceIndices(sip.Doc.OrientationXY),
                                                            sip.Doc.OrientationXY)
    sip.App.GetDocument().GetGenericMaskByName("skin").Activate()
    sip.App.GetDocument().GetActiveGenericMask().Duplicate()
    sip.App.GetDocument().GetGenericMaskByName("Copy of skin").Activate()
    sip.App.GetDocument().GetGenericMaskByName("Copy of skin").SetName("skin_eyelids")
    sip.App.GetDocument().ReplaceMaskUsingBooleanExpression("(skin_eyelids MINUS eyes)",
                                                            sip.App.GetDocument().GetMaskByName("skin_eyelids"),
                                                            sip.App.GetDocument().GetSliceIndices(sip.Doc.OrientationXY),
                                                            sip.Doc.OrientationXY)
    sip.App.GetDocument().ReplaceMaskUsingBooleanExpression("(skin_eyelids MINUS \"eyes interior\")",
                                                            sip.App.GetDocument().GetMaskByName("skin_eyelids"),
                                                            sip.App.GetDocument().GetSliceIndices(sip.Doc.OrientationXY),
                                                            sip.Doc.OrientationXY)
    sip.App.GetDocument().ReplaceMaskUsingBooleanExpression("(skin_eyelids OR eyelids)",
                                                            sip.App.GetDocument().GetMaskByName("skin_eyelids"),
                                                            sip.App.GetDocument().GetSliceIndices(sip.Doc.OrientationXY),
                                                            sip.Doc.OrientationXY)

    # Generate "bottom_corrections" mask
    sip.App.GetDocument().GetGenericMaskByName("uniform").Activate()
    sip.App.GetDocument().GetActiveGenericMask().Duplicate()
    sip.App.GetDocument().GetGenericMaskByName("Copy of uniform").Activate()
    sip.App.GetDocument().GetGenericMaskByName("Copy of uniform").SetName("bottom_corrections")
    sip.App.GetDocument().GetGenericMaskByName("bottom_corrections").Activate()
    sip.App.GetDocument().ApplyErodeFilter(sip.Doc.TargetMask, 2, 2, 0, 0)
    sip.App.GetDocument().GetGenericMaskByName("bottom_corrections").Activate()
    sip.App.GetDocument().ReplaceMaskUsingBooleanExpression("(NOT bottom_corrections)",
                                                            sip.App.GetDocument().GetMaskByName("bottom_corrections"),
                                                            sip.App.GetDocument().GetSliceIndices(sip.Doc.OrientationXY),
                                                            sip.Doc.OrientationXY)
    sip.App.GetDocument().ReplaceMaskUsingBooleanExpression("(bottom_corrections AND uniform)",
                                                            sip.App.GetDocument().GetMaskByName("bottom_corrections"),
                                                            listOfBufferSlices, sip.Doc.OrientationXY)
    sip.App.GetDocument().GetGenericMaskByName("bottom_corrections").Activate()
    sip.App.GetDocument().GetActiveMask().Unpaint([sip.Point3D(128, 128, lowerBuffer + 1)], sip.Mask.Disk, 300, True,
                                                  listOfRemovedSlices, sip.Doc.OrientationXY, True)
    sip.App.GetDocument().GetActiveMask().Unpaint([sip.Point3D(225, 25, lowerBuffer + 1)], sip.Mask.Disk, 300, True,
                                                  listOfRemovedSlices, sip.Doc.OrientationXY, True)
    sip.App.GetDocument().GetActiveMask().Unpaint([sip.Point3D(25, 25, lowerBuffer + 1)], sip.Mask.Disk, 300, True,
                                                  listOfRemovedSlices, sip.Doc.OrientationXY, True)
    sip.App.GetDocument().GetActiveMask().Unpaint([sip.Point3D(25, 225, lowerBuffer + 1)], sip.Mask.Disk, 300, True,
                                                  listOfRemovedSlices, sip.Doc.OrientationXY, True)
    sip.App.GetDocument().GetActiveMask().Unpaint([sip.Point3D(225, 225, lowerBuffer + 1)], sip.Mask.Disk, 300, True,
                                                  listOfRemovedSlices, sip.Doc.OrientationXY, True)

    # Re-organize Project Files
    sip.App.GetDocument().RemoveMasks([
        sip.App.GetDocument().GetGenericMaskByName("negative_space"),
        sip.App.GetDocument().GetGenericMaskByName("skin"),
        sip.App.GetDocument().GetGenericMaskByName("eyelids"),
        sip.App.GetDocument().GetGenericMaskByName("bottom")
    ])
    sip.App.GetDocument().GetGenericMaskByName("skin_eyelids").SetName("skin")
    sip.App.GetDocument().IsolateMasks([sip.App.GetDocument().GetGenericMaskByName("skin"),
                                        sip.App.GetDocument().GetGenericMaskByName("bottom_corrections")])


# Function to (re)generate the CSF and 10 masks for final segmentation protocols
def generate_csf_10(firstGen):
    """

    Function will either generate or regenerate the CSF mask and the 10 mask used in the process.

    Args:
        firstGen (bool): Indicates if this is the first time CSF/10 masks are generated, or if the script need to
        accommodate for regenerating them instead

    Return:
        None

    """

    # If this is not the first round of generation, delete the pre-existing 10 and CSF files
    if not firstGen:
        # Delete pre-existing files
        sip.App.GetDocument().GetGenericMaskByName("10").Activate()
        sip.App.GetDocument().RemoveMask(sip.App.GetDocument().GetActiveGenericMask())
        sip.App.GetDocument().GetGenericMaskByName("csf").Activate()
        sip.App.GetDocument().RemoveMask(sip.App.GetDocument().GetActiveGenericMask())

    # Once in a clean slate, generate 10 and CSF
    # Generate "10" mask
    sip.App.GetDocument().GetGenericMaskByName("wm").Activate()
    sip.App.GetDocument().GetActiveGenericMask().Duplicate()
    sip.App.GetDocument().GetGenericMaskByName("Copy of wm").Activate()
    sip.App.GetDocument().GetGenericMaskByName("Copy of wm").SetName("10")
    sip.App.GetDocument().ReplaceMaskUsingBooleanExpression(
        "(10 OR wm OR gm OR eyes OR air OR blood OR bone OR skin OR fat OR muscle)",
        sip.App.GetDocument().GetMaskByName("10"), sip.App.GetDocument().GetSliceIndices(sip.Doc.OrientationXY),
        sip.Doc.OrientationXY)

    # Generate the CSF mask
    sip.App.GetDocument().GetGenericMaskByName("uniform").Activate()
    sip.App.GetDocument().GetActiveGenericMask().Duplicate()
    sip.App.GetDocument().GetGenericMaskByName("Copy of uniform").Activate()
    sip.App.GetDocument().GetGenericMaskByName("Copy of uniform").SetName("csf")
    sip.App.GetDocument().ReplaceMaskUsingBooleanExpression("(csf MINUS 10)",
                                                            sip.App.GetDocument().GetMaskByName("csf"),
                                                            sip.App.GetDocument().GetSliceIndices(sip.Doc.OrientationXY),
                                                            sip.Doc.OrientationXY)

    # Add the fluid from the inside of the eyes
    sip.App.GetDocument().ReplaceMaskUsingBooleanExpression("(csf OR \"eyes interior\")",
                                                            sip.App.GetDocument().GetMaskByName("csf"),
                                                            sip.App.GetDocument().GetSliceIndices(sip.Doc.OrientationXY),
                                                            sip.Doc.OrientationXY)

    # Adjust color, position, visibility
    sip.App.GetDocument().GetGenericMaskByName("csf").Activate()
    sip.App.GetDocument().GetActiveGenericMask().SetColour(sip.Colour(107, 220, 220))
    sip.App.GetDocument().GetGenericMaskByName("csf").Activate()
    sip.App.GetDocument().MoveMaskTo(sip.App.GetDocument().GetActiveGenericMask(), 1)
    sip.App.GetDocument().GetGenericMaskByName("csf").SetVisible(True)
    sip.App.GetDocument().GetGenericMaskByName("10").SetVisible(False)

