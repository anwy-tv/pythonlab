def word_analyzer(words):
    print("Все слова:", words)
    if len(words) == 0:
        print("слов нет")
    else: print("всего", len(words),"слов(-а)")
    count = {}
    for word in words:
        if word in count:
            count[word] += 1 
        else: count[word] = 1
    print("частота слов:")
    for word in words:
        print(word, "-", count[word])
    top_word = words[0]
    for word in words:
        if count[word] > count[top_word]:
            top_word = word
    print("Самое частое слово", top_word)

    shorty = words[0]
    long = words[0]
    for word in words:
        if len(word) < len(shorty):
            shorty = word
        if len(word) > len(long):
            long = word
    print("Самое короткое слово", shorty)
    print("Самое длинное слово", long)

text = input("Введите текст: ")

words = text.lower().split()

word_analyzer(words)

long_words = []
for word in words:
    if len(word) >= 3:
        long_words.append(word)
print("Слова больше 3 букв:", long_words)
print("Анализ слов больше 3 букв")
word_analyzer(long_words)