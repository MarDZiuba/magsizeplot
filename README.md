# magsizeplot
## Automate Concatenation and Visualization of Magnetosome Measurements
This script is designed to automate the routine of concatenating magnetosome measurements from multiple cells and produce a ready-for-publication plot. The script takes as input a directory where Excel files with magnetosome measurements produced using imageJ (Fiji) are stored and generates a figure in either a violin or boxplot format. It also calculates statistical significance of the difference in magnetosome sizes between strain pairs if requested.

# Usage
This script accepts five arguments:

-h: print help statement on the program usage and exit.
-i: input directory, where the program will search for .csv files. Required.
-p: defines the plot type: violin or boxplot. Required.
-c: the color palette of the graph. Default: colorblind. Optional.
-stat: calculates statistical significance of the difference in magnetosome sizes between strain pairs. Pass a .txt file indicating the pairs you want to compare: type each strain pair in a new line, separate them by comma (without spaces!) Optional.

Here is an example command:

magsizeplot.exe -i /path/to/input_directory -p violinplot -stat /path/to/statistical_pairs.txt

The output files include Result.xlsx, which contains the concatenated measurements and statistics, and Result.pdf and Result.ps, which contain the generated figure in pdf and eps formats.

# Notes
This program only works with input Excel tables produced using imageJ (Fiji). The script is designed to open all .csv files with magnetosome measurements and concatenates them, also passing the folder names to the resulting data series.

If the -stat argument is provided, the program will calculate the Kruskal-Wallis H-test for each pair of strains in the .txt file and add significance annotations to the plot.

By default, the program uses the colorblind color palette. To use a different palette, pass the name of the palette to the -c argument. See seaborn tutorial for a list of available palettes: https://seaborn.pydata.org/tutorial/color_palettes.html
