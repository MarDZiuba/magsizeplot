# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 13:49:22 2022

@author: Марина
"""
# Import the required packages
import argparse
import os
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt 
import statannot as stan

# Specify user arguments
parser = argparse.ArgumentParser(description='This programs automates the routine of concatenating magnetosome measurements from multiple cells and producing a ready-for-publication plot. Only works with input excel tables produced using imageJ (Fiji)')
parser.add_argument("-i", type = str, help = "Input directory")
parser.add_argument("-p", type = str, choices = ["violinplot", "boxplot"], help = "Defines the plot type: violin or boxplot.")
parser.add_argument("-c", type = str, help = "The color palette of the graph. Default: colorblind. Options: see matplotlib color palettes https://matplotlib.org/stable/tutorials/colors/colormaps.html ")
parser.add_argument("-stat", type = str, help = "Calculates statistical significance of the difference in magnetosome sizes between strain pairs. Pass a .txt file indicating the pairs you want to compare: type each strain pair in a new line, separate them by comma (without spaces!)")
args = parser.parse_args()

# Create a function that opens all .csv files with magnetosome measurements,
# opens them one by one and concatenates the measurements. It also passes the 
# folder names to the resulting data series   

def concat_measurements(directoryName):
    directory=os.fsencode(directoryName)
    folname = os.path.basename(directoryName)
    Length=pd.Series(dtype = "float64", name = folname)
    for file in os.listdir(directory): 
        filename=os.fsdecode(file)
        fullName = directoryName + '\\' + filename
        if filename.endswith(".csv"):
            df=pd.read_csv(fullName)
            df = df.rename(columns = {"Length":folname})
            Series = [Length, df[folname]]
            Length=pd.concat(Series, ignore_index=True)
            #print(Length)
            continue    
        else:
            continue
    return Length

# Loop through the folders in the input directory and concatenate all data into a table 
inputdir = args.i
names = [] # Capture the strain names from the folder names in a list
table = pd.DataFrame(dtype = "float64")
for dirpath, dirnames, filenames in os.walk(inputdir):
    for name in dirnames:
        path = dirpath + "\\" + name
        strain = concat_measurements(path)
        table=pd.concat([table, strain], axis=1)
        names.append(name)
basestat = table.describe()      

# Saving the concatenated measurements and statistics to an excel file
excel = pd.ExcelWriter("Result.xlsx", engine = "xlsxwriter")
table.to_excel(excel, sheet_name="All_measurements", index=False) # Saving the table into an excel sheet
basestat.to_excel(excel, sheet_name="Statistics Summary", index=True)
excel.close()

# Plotting the measurements

# Parsing the color arguments
if args.c:    
    try:    
        sns.set_palette(args.c)
    except:
        print("No such color palette found")
else:    
    sns.set_palette("colorblind")


if args.p == "violinplot":
    ax = sns.violinplot(data=table)
elif args.p == "boxplot":
    ax = sns.boxplot(data=table)

ax.set(ylabel="Magnetosome diameter [nm]")
plt.xticks(rotation=45, ha = "right")
plt.tight_layout()

#Add annotation of statistics if the argument -s is provided

if args.stat:
    with open (args.stat, "r") as f:
        lines = f.read().splitlines()
        pairs = list()
        for l in lines:
            pair = tuple(l.split(","))
            pairs.append(pair)
            
    stan.add_stat_annotation(ax, data=table, box_pairs=pairs, test='Kruskal', text_format='star',loc='inside',
                        verbose=2)

plt.savefig("Result.pdf")
plt.savefig("Result.ps")
plt.show()

    
