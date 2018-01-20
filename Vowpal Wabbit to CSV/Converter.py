import csv
import pymorphy2
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import defaultdict

#Source files
source_file_name = "contents.csv"
result_file_name = "contents_vw.txt"
source_file = open(source_file_name,"r",encoding="utf8")
result_file = open(result_file_name,"w",encoding="utf8")

#Reading header
reader = csv.reader(source_file,delimiter="\t")
header = next(reader)

# Returns dictionary with word as a key and with number of occurrences of this word as a value
def normalize_text(text):
    stop_words = set(stopwords.words("russian"))
    morph = pymorphy2.MorphAnalyzer()
    result = defaultdict(int)
    sentences = sent_tokenize(text)
    for sentence in sentences:
        words = word_tokenize(sentence)
        for word in words:
            if word.lower() not in stop_words:
                info = morph.parse(word)[0];
                if info.tag.POS is not None:
                    result[info.normal_form]+=1
    return result

# Gets as a parameters: csv.reader object, opened result file, header array,
# array with indexes where column is text, array with indexes where column is value, position of label in header
def converter(reader,result_file, header, text_columns, value_columns,label_pos):
    for row in reader:
        label = row[label_pos]
        result_file.write(" "+label)
        for i in text_columns:
            text = row[i]
            result_file.write(" |"+header[i])
            res = normalize_text(text)
            for word,count in res.items():
                if count == 1:
                    result_file.write(" "+word)
                else:
                    result_file.write(" "+word+":"+str(count))
        for i in value_columns:
            result_file.write(" |"+header[i])
            value = row[i]
            result_file.write(" "+value)

# Write in result file columns: 1 and 4 as text (title, content), 2 as value (category_id), 0 as label
converter(reader,result_file,header,[1,4],[2],0)

source_file.close()
result_file.close()