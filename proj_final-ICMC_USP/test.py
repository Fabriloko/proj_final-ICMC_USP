import pandas as pd 
import requests as rq
from io import StringIO
import matplotlib.pyplot as plt
import numpy as np

names = ['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm', 'Species']

# Construct the raw URL
raw_url = f"https://raw.githubusercontent.com/Fabriloko/proj_final-ICMC_USP/refs/heads/main/proj_final-ICMC_USP/iris.data"

# Send a GET request to the raw file URL
response = rq.get(raw_url)

# Check if the request was successful
if response.status_code == 200:
    # Return the content of the file
    data = StringIO(response.text)  # Convert the raw text response into a file-like object
    df = pd.read_csv(data, names= names)
    df    
else:
    print(f"Error: Unable to fetch file (HTTP {response.status_code})")
    None



for specie in df['Species'].unique():
    heatmap = df[df['Species'] == specie].copy()
    heatmap = heatmap.drop(['Species'], axis= 1)
    heatmap = heatmap.corr()

    fig, axs = plt.subplots(figsize= (8, 6), layout= "tight")
    fig.suptitle(f'Heatmap {specie}')
    fig.subplots_adjust(left=0.2, wspace=0.6)

    im = axs.imshow(heatmap, cmap='bwr')

    axs.set_xticks(np.arange(len(heatmap.columns)), labels= heatmap.columns)
    axs.set_yticks(np.arange(len(heatmap.columns)), labels= heatmap.columns)

    plt.setp(axs.get_xticklabels(), rotation= 45, ha= "right", rotation_mode= "anchor")

    heatmap = heatmap.rename(columns={"SepalLengthCm": 0, "SepalWidthCm": 1, "PetalLengthCm": 2, "PetalWidthCm": 3})

    for i in heatmap:
        for j in heatmap:
            text = axs.text(j, i, round(heatmap[i][j], 2), ha= "center", va= "center", color= "black")

# df