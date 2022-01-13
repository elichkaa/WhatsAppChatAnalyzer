from editFile import editFile

from extractData import getWords, getWordsWithCount, getMessageCountByPerson, getMessageCountByDate, getMessagesByHour, getMessagesByHourForeachPerson

from transferToFile import wordsWithCountToFile, specialWordsToFile

from generateChart import generatePieChartForMessagesPercent, generateBarChartForMessagesCount, generateLineChartForMessagesByDate, generateLineChartForChatActivityPerHour, generateLineChartForParticipantActivityPerHour

def printObjects(objects):
    for obj in objects:
        obj.printMessage()

def main(chat_filepath):
    objects = []
    words = []
    objects = editFile(objects, chat_filepath)
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

if __name__ == "__main__":
    main("./tests/chat.txt")









