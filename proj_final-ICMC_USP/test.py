import pandas as pd 
import requests as rq
from io import StringIO

names = ['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm', 'Species']

# Construct the raw URL
raw_url = f"https://github.com/Fabriloko/proj_final-ICMC_USP/blob/1c9753ff4714beb3480248428d251d35fa710c51/proj_final-ICMC_USP/iris.data"

# Send a GET request to the raw file URL
response = rq.get(raw_url)

# Check if the request was successful
if response.status_code == 200:
    # Return the content of the file
    data = StringIO(response.text)  # Convert the raw text response into a file-like object
    df = pd.read_csv(data)
    df    
else:
    print(f"Error: Unable to fetch file (HTTP {response.status_code})")
    None

