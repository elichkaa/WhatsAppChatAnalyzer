import re
from datetime import datetime
from base import Message

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