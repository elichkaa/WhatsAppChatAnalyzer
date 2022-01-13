import re
from datetime import datetime

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