import re
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

class Message:
    def __init__(message, name, text, date):
        message.name = name
        message.text = text
        message.date = date

    def printMessage(message):
        print(message.date + " " + message.name + ": " + message.text)

def removeMedia(line):
    if "‎" in line:
        return ""
    if "‪" in line:
        return re.sub(r'(\\[uU][0-9]{3}[a-zA-Z]{1}):', '', line)
    else: 
        return line

def getDateTime(dateString):
    obj = datetime.strptime(dateString, "[%d.%m.%y, %H:%M:%S]");
    return datetime.strftime(obj, "[%d.%m.%y, %H:%M:%S]");

def editFile(objects, chat_filepath):
    with open(chat_filepath, 'r', encoding="utf-8") as my_file:
        for line in my_file:
            line = removeMedia(line)
            if line == "": continue
            date = re.findall(r"^\[[0-9:.,\s]+\]", line)
            line = re.sub(r'^\[[0-9:.,\s]+\]', '', line).strip()
            if date and line != "":
                name = re.findall(r"[^:]+", line)
                line = re.sub(r'^[^:]+:', '', line).strip()
                date = getDateTime(date[0])
                message = Message(name[0], line, date)
                objects.append(message)
            else:
                objects[len(objects) - 1].text += "\n" + line
    return objects

def printObjects(objects):
    for obj in objects:
        obj.printMessage()

def getWords(objects):
    chat = [obj.text.lower().split() for obj in objects]
    words = []
    for sentence in chat:
        for word in sentence:
            words.append(re.sub(r'[\W]', '', word))
    return [i for i in words if i]

def getWordsWithCount(words):
    wordsDict = {i:words.count(i) for i in words}
    return sorted(wordsDict.items(), key=lambda x: x[1], reverse=True)

def wordsWithCountToFile(words):
    file = open('./files/100_most_common_words.txt', 'w', encoding="utf-8")
    count = 1
    for item in words:
        file.write(str(count) + ". " + item[0] + " " + str(item[1]) + "\n")
        if count == 100: break
        count += 1
    file.close()

def specialWordsToFile(words):
    file = open('./files/special_words.txt', 'w', encoding="utf-8")
    count = 1
    for item in words:
        if count == 200 or count == 300 or count == 400 or count == 500: 
            file.write(str(count) + ". " + item[0] + " " + str(item[1]) + "\n")
        count += 1
    file.close()

def getMessageCountByPerson(objects):
    stats = {}
    for text in objects:
        if text.name in stats.keys():
            stats[text.name] += 1 
        else:
            stats[text.name] = 1 
    return stats

def getMessageCountByDate(objects):
    stats = {}
    for text in objects:
        dateObj = datetime.strptime(text.date, "[%d.%m.%y, %H:%M:%S]");
        dateStr = datetime.strftime(dateObj, "%d.%m.%y");
        if dateStr in stats.keys():
            stats[dateStr] += 1 
        else:
            stats[dateStr] = 1 
    return stats

def getMessagesByHour(objects):
    stats = {}
    for text in objects:
        dateObj = datetime.strptime(text.date, "[%d.%m.%y, %H:%M:%S]");
        dateStr = datetime.strftime(dateObj, "%#H");
        if dateStr in stats.keys():
            stats[dateStr] += 1 
        else:
            stats[dateStr] = 1 
    stats = sorted(stats.items(), key=lambda x: x[0])
    return dict((x, y) for x, y in stats)

def getMessagesByHourForeachPerson(objects):
    personStats = {}
    for text in objects:
        if text.name in personStats.keys():
            dateObj = datetime.strptime(text.date, "[%d.%m.%y, %H:%M:%S]");
            dateStr = int(datetime.strftime(dateObj, "%#H"));
            if dateStr in personStats[text.name].keys():
                personStats[text.name][dateStr] += 1 
            else:
                personStats[text.name][dateStr] = 1
        else:
            keys = list(range(0, 24))
            values = [0] * 24
            personStats[text.name] = dict(zip(keys, values))
    for person in personStats:
        sortedValues = sorted(personStats[person].items(), key=lambda x: int(x[0]))
        personStats[person] = dict((x, y) for x, y in sortedValues)
    return personStats

def generatePieChartForMessagesPercent(messagesByPerson):
    labels = list(messagesByPerson.keys())
    values = list(messagesByPerson.values())
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent',
                        insidetextorientation='radial'
                        )])
    fig.write_image("./charts/task3.jpeg")
    #fig.show()

def generateBarChartForMessagesCount(messagesByPerson):
    labels = list(messagesByPerson.keys())
    values = list(messagesByPerson.values())
    fig = go.Figure(data=[go.Bar(x = labels, y = values)])
    fig.update_yaxes(title_text='Messages sent by participant')
    fig.update_traces(hovertemplate='Name of participant: %{x} <br>Message count: %{y}')
    fig.write_image("./charts/task4.jpeg")
    #fig.show()

def generateLineChartForMessagesByDate(messagesByDate):
    fig = px.line(messagesByDate.items(), x=0, y=1, title='Messages in chat by date')
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Messages sent')
    fig.update_traces(hovertemplate='Date: %{x} <br>Messages sent: %{y}')
    fig.write_image("./charts/task5.jpeg")
    #fig.show()

def generateLineChartForChatActivityPerHour(messagesByHour):
    fig = px.line(messagesByHour.items(), x=0, y=1, title='Hourly activity of chat')
    fig.update_xaxes(title_text='Hour')
    fig.update_yaxes(title_text='Messages sent')
    fig.update_traces(hovertemplate='Hour: %{x} <br>Message count: %{y}') 
    fig.write_image("./charts/task6.jpeg")
    #fig.show()

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
    fig.write_image("./charts/task7.jpeg")
    #fig.show()

def main(chat_filepath):
    objects = []
    words = []
    objects = editFile(objects, chat_filepath)
    printObjects(objects)
    words = getWords(objects)
    wordsWithCount = getWordsWithCount(words)
    
    messagesByPerson = getMessageCountByPerson(objects)
    generatePieChartForMessagesPercent(messagesByPerson)
    generateBarChartForMessagesCount(messagesByPerson)
    
    messagesByDate = getMessageCountByDate(objects)
    generateLineChartForMessagesByDate(messagesByDate)
    
    wordsWithCountToFile(wordsWithCount)
    specialWordsToFile(wordsWithCount)
    
    messagesByHour = getMessagesByHour(objects)
    generateLineChartForChatActivityPerHour(messagesByHour)
    
    messagesByHourForEveryParticipant = getMessagesByHourForeachPerson(objects)
    generateLineChartForParticipantActivityPerHour(messagesByHourForEveryParticipant)

main("phone.txt")









