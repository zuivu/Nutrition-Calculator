import tkinter as tk
import numpy as np
import pandas as pd
import pyarrow.parquet as pq

INVALID_INPUT = None

def check_valid_input(entry, explanation_text, zero_value=False):
    """
    """

    try: 
        entry_num = float(entry.get()) 

        if entry_num < 0:
            explanation_text.configure(text="Please type in positive numbers!")
            entry.delete(0, tk.END)
            return INVALID_INPUT

        if zero_value and (entry_num == 0):
            explanation_text.configure(text="The numbers of serving must be larger than zero")
            entry.delete(0, tk.END)
            return INVALID_INPUT

        return entry_num

    except ValueError:
        explanation_text.configure(text="Please type in number only!")
        entry.delete(0, tk.END)
        return INVALID_INPUT


def read_data(file_in, columns_name):
    """
    """
    
    try: 
        df = pq.read_table(file_in) 
    except OSError:
        df = pd.DataFrame(columns=columns_name, dtype=np.float32)
    return df


def store_data(file_out, **kwargs):
    """
    """

    table = pq.read_table(file_out, **kwargs)
    table.to_pandas()


def export_data(data_frame, file_name):
    """
    """
    
    data_frame.to_csv(file_name)