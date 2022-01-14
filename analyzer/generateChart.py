import plotly.express as px
import plotly.graph_objects as go

def defineOutputDirectory(directory):
    global output_directory 
    output_directory = directory

def generatePieChartForMessagesPercent(messagesByPerson):
    labels = list(messagesByPerson.keys())
    values = list(messagesByPerson.values())
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent',
                        insidetextorientation='radial'
                        )])
    path = output_directory + "\\task3.jpeg"
    fig.write_image(output_directory + "\\task3.jpeg")

def generateBarChartForMessagesCount(messagesByPerson):
    labels = list(messagesByPerson.keys())
    values = list(messagesByPerson.values())
    fig = go.Figure(data=[go.Bar(x = labels, y = values)])
    fig.update_yaxes(title_text='Messages sent by participant')
    fig.update_traces(hovertemplate='Name of participant: %{x} <br>Message count: %{y}')
    fig.write_image(output_directory + "\\task4.jpeg")

def generateLineChartForMessagesByDate(messagesByDate):
    fig = px.line(messagesByDate.items(), x=0, y=1, title='Messages in chat by date')
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Messages sent')
    fig.update_traces(hovertemplate='Date: %{x} <br>Messages sent: %{y}')
    fig.write_image(output_directory + "\\task5.jpeg")

def generateLineChartForChatActivityPerHour(messagesByHour):
    fig = px.line(messagesByHour.items(), x=0, y=1, title='Hourly activity of chat')
    fig.update_xaxes(title_text='Hour')
    fig.update_yaxes(title_text='Messages sent')
    fig.update_traces(hovertemplate='Hour: %{x} <br>Message count: %{y}') 
    fig.write_image(output_directory + "\\task6.jpeg")

def generateLineChartForParticipantActivityPerHour(messagesByHour):
    fig = go.Figure()
    for person in messagesByHour:
        hours = list(messagesByHour[person].keys())
        texts = list(messagesByHour[person].values())
        fig.add_trace(go.Scatter(
            x=hours,
            y=texts,
            mode="lines",
            line=go.scatter.Line(), 
            showlegend=True,
            name=person))
    fig.update_xaxes(title_text='Hour')
    fig.update_yaxes(title_text='Messages sent by participant')
    fig.update_traces(hovertemplate='Hour: %{x} <br>Message count: %{y}') 
    fig.write_image(output_directory + "\\task7.jpeg")