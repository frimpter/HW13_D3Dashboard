# HW_13 B3 Dashboard

import pandas as pd
#import numpy as np
import csv
from flask import Flask, jsonify, request, redirect, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/names")
def sample_names():
    #Identify list of names
    csv_file = "templates/B3_ParticipantData.csv"
    names_df = pd.read_csv(csv_file, encoding="utf-8")
    #Return list of sample names as "BB_123"
    BB_names = names_df["ID"].radd("BB_").tolist()

    return BB_names


@app.route("/otu")
def otu_data():
    #Identify list of OTU descriptions
    csv_file = "templates/B3_OTUData.csv"
    otu_df = pd.read_csv(csv_file, encoding="utf-8")
    #Return list of OTU taxonomies
    otu = otu_df.iloc[:,1].tolist()

    return otu

@app.route("/metadata/<sample>")
def metadata(sample):
    #Identify (and clean) metadata for a selected sample
    csv_file = "templates/B3_ParticipantData.csv"
    meta_df = pd.read_csv(csv_file, encoding="utf-8")
    meta_df["ID"] = meta_df["ID"].radd("BB_") # Match ID to the input value in format "BB_123"
    meta_df = meta_df.rename(columns={"Ethnicity_Quest": "Ethnicity", "Innie_or_outie": "Type of BB", "Current City": "City", "Current State": "State"})
    meta_df = meta_df[["ID", "Gender", "Age", "Ethnicity", "Type of BB", "City", "State"]]
    meta_df = meta_df.set_index("ID")    
    sample_info = meta_df.loc[{sample}].to_dict() # Select the passed sample and convert values to dict

    #Return a dictionary of metadata
    return sample_info

@app.route("/wfreq/<sample>")
def washfreq(sample):
    #Identify weekly washing frequency for selected sample
    csv_file = "templates/B3_ParticipantData.csv"
    wash_df = pd.read_csv(csv_file, encoding="utf-8")
    wash_df["ID"] = wash_df["ID"].radd("BB_")
    wash_df = wash_df.rename(columns={"Wash_Freq of BB (# times per week)":"BB_Wash_Freq"})
    wash_df = wash_df[["ID", "BB_Wash_Freq"]]
    wash_df = wash_df.set_index("ID")
    sample_wash = int(wash_df.loc[{sample}, "BB_Wash_Freq"])

    #Return value for washing frequency
    return sample_wash

@app.route("/samples/<sample>")
def otu_samples(sample):
    #Identify OTU IDs and values for a selected sample
    csv_file = "templates/B3_OTUData.csv"
    otu_df = pd.read_csv(csv_file, encoding="utf-8")
    otu_df[otu_df.columns] = otu_df[otu_df.columns].apply(pd.to_numeric, errors="ignore")
    sample_df = otu_df[["OTU ID #", {sample}]]

    sample_df.columns = ["OTU ID", "Sample Values"]

    #Sort in descending order by sample value
    sample_df = sample_df.sort_values("Sample Values", ascending=False)

    #Return list of 2 dictionaries, 1 of OTU IDs and 1 of sample values, sorted by descending Sample Values
    otu = [sample_df.to_dict(orient="list")]

    return otu



if __name__ == "__main__":
    app.run(debug=True)
