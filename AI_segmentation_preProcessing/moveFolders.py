import os
import shutil
import time


########################################################################################################################

def copyFiles(participantNumber, baseDir, newFolder):

    # Start logging processing time
    startTime = time.time()
    # Participant's folder name
    participantFolder = f"FS6.0_sub-{participantNumber}_ses01\\"
    # Participant's full folder location
    oldLocation = baseDir + participantFolder
    # Participant new location
    newParticipantFolder = newFolder + participantFolder
    # Print participant info:
    print(f"Attempting to copy participant {participantNumber}.")



    # If participant's folder does not exist in entered location...
    if not os.path.exists(oldLocation):
        # Output message
        print(f"{participantFolder} could not be found in {baseDir}.")
        # Stop logging processing time
        endTime = time.time()
        elapsedTime = endTime - startTime
        # Print processing time
        print(f"Function completed in {elapsedTime:.2f} seconds.")
        return


    # Check that this participant does not already exist in the new folder
    # If the participant already exists in the new folder...
    if os.path.exists(newParticipantFolder):
        print(f"{participantNumber} already exists within {newFolder}. Did not replace pre-existing version.")
        endTime = time.time()
        elapsedTime = endTime - startTime
        print(f"Function completed in {elapsedTime:.2f} seconds.")
        return

    # If the participant's original file can be found and it does not exist in the new location, copy it
    else:

        print(f"Copying from: {oldLocation}")
        print(f"Copying to: {newParticipantFolder}")

        # If the participant's folder exists within the entered location, copy the participant's folder from the old
        # location to the new location
        shutil.copytree(oldLocation,newParticipantFolder)
        # Output message
        print(f"Successfully copied participant {participantNumber} from {baseDir} to {newFolder}.")
        # Stop logging processing time
        endTime = time.time()
        elapsedTime = endTime - startTime
        print(f"Function completed in {elapsedTime:.2f} seconds.")


########################################################################################################################

def moveFiles(participantNumber, baseDir, newFolder):

    # Start logging processing time
    startTime = time.time()
    # Participant's folder name
    participantFolder = f"FS6.0_sub-{participantNumber}_ses01\\"
    # Participant's full folder location
    oldLocation = baseDir + participantFolder
    # Participant new location
    newParticipantFolder = newFolder + participantFolder
    # Print participant info:
    print(f"Attempting to move participant {participantNumber}.")


    # If participant's folder does not exist in entered location...
    if not os.path.exists(oldLocation):
        # Output message
        print(f"{participantFolder} could not be found in {baseDir}.")
        # Stop logging processing time
        endTime = time.time()
        elapsedTime = endTime - startTime
        # Print processing time
        print(f"Function completed in {elapsedTime:.2f} seconds.")
        return

    # Check that participant does not already exist in new folder
    # If the participant already exists in the new folder...
    if os.path.exists(newParticipantFolder):
        print(f"{participantNumber} already exists within {newFolder}. Did not replace pre-existing version.")
        endTime = time.time()
        elapsedTime = endTime - startTime
        print(f"Function completed in {elapsedTime:.2f} seconds.")
        return

    else:
        # Output messages
        print(f"Moving from: {oldLocation}")
        print(f"Moving to: {newParticipantFolder}")

        # If the participant can be found and doesn't already exist in the new folder, move it
        shutil.move(oldLocation,newParticipantFolder)

        # Output message
        print(f"Successfully moved participant {participantNumber} from {baseDir} to {newFolder}.")
        # Stop logging processing time
        endTime = time.time()
        elapsedTime = endTime - startTime
        print(f"Function completed in {elapsedTime:.2f} seconds.")


########################################################################################################################


baseDir = "P:\\WoodsLab\\ACT-head_models\\FEM\\manual_segmentation\\"
newFolder_move = "P:\\WoodsLab\\ACT-head_models\\FEM\\manual_segmentation\\allParticipants\\PLV1\\"


# List of participant numbers
participants = [
    100031,100283,100317,100332,100340,100536,100551,100595,100602,100893,100947,101151,101204,101211,101283,101426,
    101502,101520,101549,101712,101738,101841,101861,102007,102112,102405,102707,102747,102778,103101,103116,103349,
    103527,103599,103744,103901,104183,104217,104285,104503,104567,104872,104956,105256,105335,105345,105592,105601,
    105643,105687,105971,106078,106089,106153,106309,106453,106624,106807,106817,106911,106986,107187,107321,107355,
    107620,107693,107802,107876,107997,108173,108223,108306,108341,108564,109021,109050,109106,109311,109427,109822,
    109937,110081,110090,110519,110588,111026,111894,112069,113108,113345,113374,113713,113788,114398,114701,114883,
    115302,115435,115504,115563,115769,115787,115791,115965,116036,202251,202268,202439,202481,202663,202755,202808,
    202927,202950,202980,203011,203091,203141,203204,203212,203330,203395,203441,203455,203479,203573,203665,203749,
    203789,203821,203846,203879,203896,203987,203995,204021,204060,204078,204133,204178,204183,204201,204228,204230,
    204758,204834,205042,205150,205205,300142,300166,300171,300414,300516,300686,300699,300700,300802,300824,300837,
    301112,301238,301263,301428,301501,301513,301538,301559,301600,301686,301723,301733,301743,301799,301970,301986,
    301997,302092,302117,302130,302141,302280,302304,302339,302345,302558,302561,302571,302674,302682,302718,302750,
    302762,302778,302784,302819,302827,302835,302854,302873,302921,302939,303009,303048,303058,303168,303182,303237,
    303293,303346,303367,303406,303455,303486,303518,304155,304176
    ]


for people in participants:
    # copyFiles(people, baseDir, newFolder_copy)
    moveFiles(people,baseDir,newFolder_move)
