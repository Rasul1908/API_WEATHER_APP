from flask import Flask, render_template
import pandas as pd
app=Flask(__name__)

stations=pd.read_csv("data_small/stations.txt",skiprows=17)
stations= stations[['STAID','STANAME                                 ']]
@app.route("/")
def home():
    return render_template('home.html',data=stations.to_html())


@app.route("/about/")
def about():
    return render_template('about.html')


@app.route('/api/v1/<station>/<date>/')
def api(station,date):
    filename="data_small/TG_STAID" + str(station).zfill(6) +".txt"
    df=pd.read_csv(filename,skiprows=20,parse_dates =["    DATE"])
    temperature= (df.loc[df["    DATE"] == date ]['   TG'].squeeze())/10

    print(temperature)
    result_dictionary={"station": station, "date":date,"temperature":temperature}
    return result_dictionary

@app.route('/api/v1/<station2>/')
def api2(station2):
    filename="data_small/TG_STAID" + str(station2).zfill(6) +".txt"
    df=pd.read_csv(filename,skiprows=20,parse_dates =["    DATE"])

    result_dictionary2=df.to_dict(orient='records')
    return result_dictionary2


@app.route('/api/v1/yearly/<station3>/<year>/')
def api3(station3,year):
    filename="data_small/TG_STAID" + str(station3).zfill(6) +".txt"
    df=pd.read_csv(filename,skiprows=20)
    df["    DATE"]=df["    DATE"].astype(str)
    df=df[df["    DATE"].str.startswith(str(year))]

    result_dictionary2=df.to_dict(orient='records')
    return result_dictionary2

app.run(debug=True,port=3001)


