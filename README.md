# Simpleware Scripts
This repository contains modules and scripts intended to be implemented within Synopsys Simpleware's scripting 
environment. Presently, these scripts are not intended to be executed outside the Simpleware scripting environment or 
directly within alternative IDEs. 


## Table of Contents

- [Installation](#installation) 
- [Quality Checks](#quality-checks)
  - [List of Scripts](#list-of-scripts)
- [Segmentation](#segmentation)




### Installation
Installation is intended to be relatively straight forward and easy. 
- Download the repository to your device and add it to your folder within the shared drive. 
- As long as you are mounted to the P-drive, you should be able to implement the scripts with minor/no modifications 
- Template scripts are pre-loaded to import modules from the P-drive; for example: 
```python
#! python3
import scanip_api3 as sip
import sys

module_path = "P:\\WoodsLab\\ACT-head_models\\FEM\\Sam\\Scripts\\Python\\Simpleware\\quality_checking\\"
sys.path.append(module_path)

import quality_check_functions as qc

```
- This is the default location to import modules and functions from; ensure this coincides with the target directory and
version of the module you wish to import and utilize 
- Note that Simpleware will not re-import modules within the same session; if edits are made to the module, exit the 
Simpleware window, re-open, and re-import the updated module. Otherwise, Simpleware will continue using the originally
imported version of the module
- When executing the scripts within Simpleware, simply load-in the Python script you would like to use; assuming 
directory paths do not need updates, scripts should be ready to implement 

### Quality Checks
This folder contains scripts, templated scripts, and the module for the segmentation quality checking process. 
`quality_check_functions.py` is the module hosting all functions; the file itself should not be executed 
withing Simpleware. Instead, users should implement one of the scripts/templated scripts included in the folder.

When using these scripts, please avoid making modifications/edits to the original module itself within the shared drive. 
Please implement edits to a localized version or direct concerns to the author. 

When implementing scripts, refer to the comments to ensure proper execution. Some do not require user input and will 
execute on command. Templated scripts may require the user to specify the participant's ID number, sublist categorization, 
target tissue masks, etc. Please see each script's comments for more information regarding user input. 

#### List of Scripts
- `finalize_sip_file.py`: Finalize the quality checking process at stage 1 or stage 2
- `generate_base_file.py`: Generate the initial visual check/base.sip file for later quality checks 
- `import_masks.py`: Import individual tissue mask into the current project file 
- `remove_overlap.py`: Remove the intersecting overlap between tissue masks based on priority levels
- `set_colors_order.py`: Assign colors and mask order according to pre-determined palette and priority
- `start_stop_visual_checks.py`: Save and finalize current participant's base visual checking file before generating and 
saving the next participant's base visual checking file


### Segmentation
This section is a work in progress. This folder will house scripts and functions utilized during the tissue segmentation 
T1 weighted MRI scans using Synopsys Simpleware. This folder will mirror the Quality Checking folder by establishing a 
module of functions that are then called through user-friendly scripts/templated scripts. 