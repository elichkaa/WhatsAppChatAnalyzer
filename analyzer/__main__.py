from editFile import editFile

from extractData import getWords, getWordsWithCount, getMessageCountByPerson, getMessageCountByDate, getMessagesByHour, getMessagesByHourForeachPerson

from transferToFile import wordsWithCountToFile, specialWordsToFile

from generateChart import generatePieChartForMessagesPercent, generateBarChartForMessagesCount, generateLineChartForMessagesByDate, generateLineChartForChatActivityPerHour, generateLineChartForParticipantActivityPerHour, defineOutputDirectory

import fire
import os

def printObjects(objects):
    for obj in objects:
        obj.printMessage()

def main(chat_filepath, output_directory):
    assert os.path.exists(output_directory), "I did not find the file at, "+str(output_directory)
    output_directory = os.path.abspath(output_directory)
    objects = []
    words = []
    objects = editFile(objects, chat_filepath)
    words = getWords(objects)
    wordsWithCount = getWordsWithCount(words)
    
    messagesByPerson = getMessageCountByPerson(objects)
    defineOutputDirectory(output_directory)
    generatePieChartForMessagesPercent(messagesByPerson)
    generateBarChartForMessagesCount(messagesByPerson)
    
    messagesByDate = getMessageCountByDate(objects)
    generateLineChartForMessagesByDate(messagesByDate)
    
    wordsWithCountToFile(wordsWithCount, output_directory)
    specialWordsToFile(wordsWithCount, output_directory)
    
    messagesByHour = getMessagesByHour(objects)
    generateLineChartForChatActivityPerHour(messagesByHour)
    
    messagesByHourForEveryParticipant = getMessagesByHourForeachPerson(objects)
    generateLineChartForParticipantActivityPerHour(messagesByHourForEveryParticipant)

if __name__ == "__main__":
    fire.Fire(main)









