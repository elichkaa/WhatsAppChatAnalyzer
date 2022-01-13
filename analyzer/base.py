class Message:
    def __init__(message, name, text, date):
        message.name = name
        message.text = text
        message.date = date

    def printMessage(message):
        print(message.date + " " + message.name + ": " + message.text)