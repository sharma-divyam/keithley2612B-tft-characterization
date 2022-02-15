"""
Function to extract out user data from a text file.

This function will look for a .txt file in a specific location. The .txt file is meant to contain:

1) The path for the database which will contain everyone's data.
2) The list of operators


This .txt file will be stored in a central location (C:\Windows). This path can be freely changed.

In the text file, the first line is the path, and the rest of the lines are for operators. They should be separated by the newline character.

"""


import pandas as pd

