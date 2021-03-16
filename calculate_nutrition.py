# TIE-02107 Introduction to Programming
# Student name: Duy Vu
# Nutrition calculator

#Normally, on the back label of food, the nutritional value(carbonhydrat, protein,
#fat, fiber and total calories) are provied in the total of 100 grams of food.

#However, the actual net weight of food is usually not 100g, but maybe like
#1200g beef, 800g broccoli,... and the amount you eat for 1 meal is also
#different(e.g 250g beef, 350g broccoli).

#Therefore, this program will help you calculate your nutrion intake for one
# meal easier and avoid miscalculation.

#The program takes the 8 inputs: food's name; the amount of 4 kinds of nutrient:
#protein(g), fat(g), carb(g), fiber(g); the amount of total calories (kcal) of
#that food; the actual net weight(g) and the amount of meals you want to eat
#for that package of food

#It will print out the amount your nutrition intake for 1 meal of that food.

#After having the result, you also have an option of exporting data to a csv
#file to keep track of nutrition value per meal

import utils
import pandas as pd
from tkinter import *

LABEL_NAME = ['Carb (g)', 'Protein (g)', 'Fat (g)', 'Fiber (g)', 'Calories (kcal)']

class AppGUI:
    def __init__(self):
        self.__mainwindow = Tk()
        self.__column_names = ['Name'] + LABEL_NAME
        self.__dataframe = utils.read_data(self.__column_names)
        self.__nutrition_value = []
        
        # Entry values
        self.__food_name = Entry(self.__mainwindow, width=15)
        for _ in range(len(LABEL_NAME)):
            value_label = Entry(self.__mainwindow, width=15)
            self.__nutrition_value.append(value_label)
        self.__amount = Entry(self.__mainwindow, width=10)
        self.__serving_num = Entry(self.__mainwindow, width=10)
        self.__calculate_button = Button(self.__mainwindow, 
                                            text = "Nutriontion in 1 serving of food", 
                                            bg="aqua", 
                                            command = self.calculate_nutrition)
        self.__result_ui = []
        self.__stop_button = Button(self.__mainwindow, text = "QUIT!", command=self.quit)
        self.create_ui()

    def create_ui(self):
        """
        Initialize UI for the app
        """

        # Title and headings
        self.__mainwindow.title("Nutrion calculator")
        Label(self.__mainwindow, text='Name of food').grid(row=0, column=0, sticky=W)
        self.__food_name.grid(row=0, column=1)
        Label(self.__mainwindow, text = "Nutrion in 100 grams of food") \
            .grid(row=1, columnspan = 5, sticky=W+E)

        # Nutrition values
        for i in range(len(LABEL_NAME)):
            Label(self.__mainwindow, text=LABEL_NAME[i]).grid(row=2, column=i)
            self.__nutrition_value[i].grid(row=3, column=i)

        # Label for the amount of food and numbers of servings/meals
        Label(self.__mainwindow, text="Amount of food in 1 package (g)") \
            .grid(row=4, column=0, columnspan=2, sticky=W)
        self.__amount.grid(row=4, column=2, sticky=E)
        Label(self.__mainwindow, text="Numbers of meals you want to eat") \
            .grid(row=5, column=0, columnspan=3, sticky=W)
        self.__serving_num.grid(row=5, column=2, sticky=E)

        # Calculation button
        self.__calculate_button.grid(row=6, columnspan=2, sticky=W)

        # Label of results
        for i in range(len(LABEL_NAME)):
            result_ui = Label(self.__mainwindow)
            result_ui.grid(row=7, column=i)
            self.__result_ui.append(result_ui)

        #Explaination text
        self.__explanation_text = Label(self.__mainwindow)
        self.__explanation_text.grid(row=7, columnspan=2)

        # Quit button
        self.__stop_button.grid(row=8, column=4)

    def calculate_nutrition(self):
        """
        Calculate nutriition per meal 
        and print them on the UI
        """

        amount = utils.check_valid_input(self.__amount, self.__explanation_text)
        serving = utils.check_valid_input(self.__serving_num, self.__explanation_text, zero_value=True)
        float_value = [utils.check_valid_input(value, self.__explanation_text) for value in self.__nutrition_value]
        
        if utils.INVALID_INPUT in (amount, serving) or utils.INVALID_INPUT in float_value:
            self.delete_results()
            return

        serving_amount = amount / serving  # mass for 1 serving
        serving_ratio = 100 / serving_amount

        # Print results and store them
        self.__explanation_text.configure(text="")   
        row_data = [str(self.__food_name.get())]
        for i in range(len(self.__nutrition_value)):
            result = round(float_value[i]/serving_ratio, 1)
            self.__result_ui[i].configure(text=str(result))
            row_data.append(result)

        row_df = pd.DataFrame([row_data], columns=self.__column_names)
        self.__dataframe = pd.concat([self.__dataframe, row_df], ignore_index=True)
        
        # Export data if needed
        export_button = Button(self.__mainwindow, text='Export data', command=self.export_data)
        export_button.grid(row=8, column=0, columnspan=2, sticky=W)

    def delete_results(self):
        """ 
        Clear all entries
        """
        for i in range(len(self.__result_ui)):
            self.__result_ui[i].configure(text="")

    def export_data(self):
        """
        Export data to file
        """
        self.__dataframe.to_csv("Nutrition.csv", sep=',')
        self.delete_results()
        self.__explanation_text.configure(text="Your data is exported successfully!")

    def start(self):
        """ 
        Starts the mainloop. 
        """
        self.__mainwindow.mainloop()

    def quit(self):
        """ 
        Store data in parquet file with file's name and compression type decided by user 
        and end the execution of the program.
        """
        self.__dataframe.to_csv("Nutrition.csv", index=False)
        self.__mainwindow.destroy()


def main():
    ui = AppGUI()
    ui.start() 

main()
