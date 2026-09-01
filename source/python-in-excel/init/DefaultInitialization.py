# Excel Python in Excel default Initialization
#
# Formulas → Initialization → replace the editor contents with this file → Save.
# Use this when the default imports or xl conversion settings were deleted or edited.
# This is the Excel default only. It does not include the Paul Python library functions.
# It has no contents() catalog; paste PaulPythonLibrary.py or Sampling.py for that.
#
# Requires Microsoft 365 Python in Excel.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels as sm
import excel
import warnings

warnings.simplefilter('ignore')

excel.set_xl_scalar_conversion(excel.convert_to_scalar)
excel.set_xl_array_conversion(excel.convert_to_dataframe)
