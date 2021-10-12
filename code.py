import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

df=pd.read_csv('C:/countries/state.csv')
df.to_parquet('C:/countries/demo.parquet')
df=pd.read_parquet(r'C:/countries/demo.parquet')

df.replace(np.nan,0,inplace=True)

flagon=df[df['date']>'2021-05-03']

fig1=px.scatter(flagon,x='State',y='Total-Vaccinated',color='date',size='Vaccinated-today')
x=df.describe().drop(['count','std','25%','75%','50%'])
fig2=px.scatter(x)



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']      #This is used to add design to my webpage



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)    #Creating Dashboard

app.layout = html.Div([
    html.H1('Covid-19 Cases in India'),
    dcc.Tabs(id="covid-19-status", value='covid-19-1', children=[
        dcc.Tab(label='Tab One', value='covid-19-1'),
        dcc.Tab(label='Tab Two', value='covid-19-2'),
    ]),
    html.Div(id='covid-19-report')
])

@app.callback(Output('covid-19-report', 'children'),
              Input('covid-19-status', 'value'))
def render_content(tab):
    if tab == 'covid-19-1':            # This is Tab 1
        return html.Div(children=[
        html.H3(children='Covid-19 Vaccination doses delivered after May 3rd 2021'),
        html.Div(children='The data is represented in the form of a scatter plot'),
        dcc.Graph(id='scatter-plot1', figure=fig1)
        ])
    elif tab == 'covid-19-2':                   # This is Tab 2
        return html.Div(children=[
        html.H3(children='Covid-19 Vaccination mean calculations'),
        html.Div(children='The data is represented in the form of a scatter plot'),
        dcc.Graph(id='scatter-plot2', figure=fig2)
        ])



if __name__ == '__main__':
    app.run_server(debug=True)

email_user = 'rahulprabhu14@gmail.com'
email_password = 'xyz'
email_send = 'rahulprabhu14@gmail.com'

subject = 'Submission of Assignment'

msg = MIMEMultipart()           #Created object of MIME and saved in msg variable to give message
msg['From'] = email_user
msg['To'] = email_send
msg['Subject'] = subject

body = '''Hi Radha, sending this email from Python !
http://127.0.0.1:8050/
'''
msg.attach(MIMEText(body,'plain'))

filename='C:/Assignment/assignment.zip'


attachment  =open(filename,'rb')


part = MIMEBase('application','octet-stream')
part.set_payload((attachment).read())



encoders.encode_base64(part)
part.add_header('Content-Disposition',"attachment; filename= "+filename)




msg.attach(part)
text = msg.as_string()
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(email_user,email_password)


server.sendmail(email_user,email_send,text)
server.quit()
