import dash_core_components as dcc
import dash
from dash.exceptions import PreventUpdate
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from datetime import datetime
import time

df = pd.read_csv("recsys_data.csv")
app = dash.Dash(__name__)
server = app.server
df.date = pd.to_datetime(df.date)              # making the date column from string to datetime type
df1 = df[df.status==1]                # filtered dataframe where it only includes the completed rows, where status == 1
df1 = df1.sort_values(by='date').reset_index()  # sort the df1 by increasing order of date, and resetting the index.
df1 = df1.iloc[170000:,:]                      # cutting the dataframe to show the surveys of the last 14 hours

app.layout = html.Div(
    [
        html.H1("Input the userId to get the top 3 surveys that the user will complete",
            style = {
                'margin-left': '24%',
                'color':'#0A3E7C',
                'font-family':'cursive'
            }),
        dcc.Dropdown(
            id = 'userid_input',
            options=[
                {'label': t, 'value': t} for t in df['user'].unique()  # all the unique values of user column.
            ],


        ),
        html.Br(),
        html.H3('Here are the top 3 surveys recommended for the given user (it includes only the surveys completed in last 14 hours):',
            style = {
                'margin-left':'26%',
                'margin-top':'1%',
                'color':'#008B8B',
                'font-family':"Times New Roman",

            }),
        html.Br(),


        html.H3(
            id="out",
            style = {
                'margin-left':'42%',
                'margin-top':'1%',
                'color':'#663300',
                'font-family':'Helvetica',

            }),


        html.H3(
            id="out1",
            style = {
                'margin-left':'42%',
                'margin-top':'1%',
                'color':'#663300',
                'font-family':'Helvetica'
            }),

        html.H3(
            id="out2",
            style = {
                'margin-left':'42%',
                'margin-top':'1%',
                'color':'#663300',
                'font-family':'Helvetica'
            }),
        html.Br(),

],
    style = {
                "background-color": "coral"
            },
)


@app.callback(
    [Output("out", "children"),Output("out1", "children"),Output("out2", "children")],
   [ Input("userid_input", "value")],
)

def recommender(userId): # takes input one of the userId's
    a =list(df1['survey'].value_counts().index) # the survey id's sorted by the highest completion to lowest which is once.
    s = df[df['user'] == userId].survey # All the surveys for the given user.
    r = set()
    if userId is None:
        raise PreventUpdate
    else:
        for i in a:
            for j in s:
                if j != i:
                    r.add(i)
                elif len(r) == 0:
                    break
                else:
                    r.remove(i)
                    break

            if len(r) == 3:
                break
    if len(r) == 3:
        return f'{list(r)[0]}  ' ,f'{list(r)[1]}  ' , f'{list(r)[2]}'   # returns a set where it has the id's of the best 3 surveys for that specific user

if __name__ == "__main__":
    app.run_server(debug=True)
