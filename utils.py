from tkinter import *
import pandas as pd

INVALID_INPUT = None

def check_valid_input(entry, explanation_text, zero_value=False):
    """
    Check if input value is valid or not.
    In other words, all entries must only accept
    non-negative number, 
    """

    try: 
        entry_num = float(entry.get()) 

        if entry_num < 0:
            explanation_text.configure(text="Please type in positive numbers!")
            entry.delete(0, END)
            return INVALID_INPUT

        if zero_value and (entry_num == 0):
            explanation_text.configure(text="Number of meals must not be 0!")
            entry.delete(0, END)
            return INVALID_INPUT

        return entry_num

    except ValueError:
        explanation_text.configure(text="Please type in number only!")
        entry.delete(0, END)
        return INVALID_INPUT


def read_data(columns_name):
    """
    Read csv file containing user info
    """
    try: 
        df = pd.read_csv("Nutrition.csv", sep=',', index_col=False) 
    except OSError:
        df = pd.DataFrame(columns=columns_name)

    return df
