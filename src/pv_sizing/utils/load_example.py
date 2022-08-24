import pandas as pd
import os

this_dir, this_filename = os.path.split(__file__)
DATA_PATH = os.path.join(this_dir, "example_data", "example_irr.csv")
example_irr = pd.read_csv(DATA_PATH, index_col='time')

this_dir, this_filename = os.path.split(__file__)
DATA_PATH = os.path.join(this_dir, "example_data", "example_load.csv")
example_load = pd.read_csv(DATA_PATH, index_col='time')


