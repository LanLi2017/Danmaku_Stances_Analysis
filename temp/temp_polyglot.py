from polyglot.downloader import downloader
print(downloader.supported_languages_table("sentiment2", 3))
from polyglot.text import Text
# text = Text('The movie was really good.')
# print("Language Detected: Code={}, Name={}\n".format(text.language.code, text.language.name))

# text = Text('这个电影真好看')
# for w in text.words:
#     print(f'{w}: {w.polarity}')
#
# text1 = Text('我喜欢太阳')
# for w in text1.words:
#     print(f'{w}: {w.polarity}')

# print(text.words)

# text = Text(u"O primeiro uso de desobediência civil em massa ocorreu em setembro de 1906.")
#
# print("{:<16}{}".format("Word", "POS Tag")+"\n"+"-"*30)
# for word, tag in text.pos_tags:
#     print(u"{:<16}{:>2}".format(word, tag))

# print("{:<16}{}".format("Word", "Polarity")+"\n"+"-"*30)
# for w in text.words:
#     print("{:<16}{:>2}".format(w, w.polarity))