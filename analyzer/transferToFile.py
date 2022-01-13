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