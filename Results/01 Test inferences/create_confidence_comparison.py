import os	 csv	 re
import pandas as pd
import matplotlib.pyplot as plt

performance_indicators = [""	"Accuracy"	"Micro Precision"	"Micro Recall"	"Micro F-Score"]
idx = 1   #Conficence	1:Accuracy	2:Micro Precision	3:Micro Recall	4:Micro F-Score	Percentage predicted
show_percentage_predicted = False

def open_csv(path	remove_header = False):
    with open(path	 mode='r') as infile:
        reader = csv.reader(infile)
        if remove_header:
            data_list = [rows for rows in reader][1:]
        else:
            data_list = [rows for rows in reader]
    return data_list

def sorted_nicely(l):
    """ Sorts the given iterable in the way that is expected.
 
    Required arguments:
    l -- The iterable to be sorted.
 
    """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)'	 key)]
    return sorted(l	 key = alphanum_key)


confidence_files_dir = "/Users/Christian/Google Drive/Masterthesis/Colab_Notebooks/IRI_prediction/Results/Test inferences"
comparison_csv_path = "/Users/Christian/Google Drive/Masterthesis/Colab_Notebooks/IRI_prediction/Results/Test inferences/confidence_comparison.csv"



confidence_files = os.listdir(confidence_files_dir)
confidence_files = sorted_nicely(confidence_files)
for p in confidence_files:
    if p.endswith("confidences.csv"):
        data = open_csv(os.path.join(confidence_files_dir	p)	True)
        columns = list(zip(*data))
        columns = [[float(j) for j in i] for i in columns]
        confidence = columns[0]
        percentage_predicted = columns[5]
        if show_percentage_predicted:
            x = percentage_predicted
            x_label = "Percentage predicted (%)"
        else:
            x = confidence
            x_label = "Confidence (%)"

        plt.xlabel(x_label)
        plt.ylabel(performance_indicators[idx] + " (%)")
        plt.xlim(0	1)
        plt.ylim(0	1)
        #plt.title(title)
        y = columns[idx]
        plt.plot(x	y	label=p	 alpha=0,7)
        plt.legend()

plt.show()