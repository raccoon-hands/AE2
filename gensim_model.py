import gensim
import string
import nltk
import contractions
import unicodedata
import html
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# -----FUNCTIONS--------
def openfile(filename):
    """Reads a text file as a string and does some preprocessing."""

    # read file as string
    file = open(filename,"r+")
    file_string = file.read() 
    file.close()
    
    # remove and decode html entities
    file_string = html.unescape(file_string)

    # remove duplicate and trailing whitespace
    file_string = ' '.join(file_string.split())

    # remove backslash characters
    file_string = file_string.replace('\\', '') 
    
    return file_string

def convert_utf(text):
    """converts utf to ascii"""
    text = text.replace('\u2018', "'").replace('\u2019', "'").replace('\u201C', "'").replace('\u201D', "'").replace('\u2013', '-').replace('\u2014', '-')
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore')
    return text.decode('ascii')

def tokenise_sentences(text):
    "tokenizes a text into sentences, then the sentences into cleaned words"
    #convert utf-8 characters to normal characters
    text = convert_utf(text)
   
    # make lowercase
    text = text.lower()

    # fix contractions
    text = contractions.fix(text)
    
    # tokenize text into sentences
    sentences = nltk.sent_tokenize(text)

    # initialise output variable
    data = []
    
    # punctuation and stop words to remove
    punct = list(string.punctuation)
    stop_words = ENGLISH_STOP_WORDS
    
    # tokenize sentences into cleaned words without stopwords
    for sentence in sentences:
        words = nltk.word_tokenize(sentence)

        # remove punctuation
        for i, word in enumerate(words):
            for char in word:
                if char in punct:
                    word = word.replace(char, "")
            words[i] = word
        
        # if an item consists entirely of punctuation and empty item is left in the list
        # so we need to remove them
        while "" in words:
            words.remove("")
            
        # remove stopwords
        # using sklearn's stopword list as it is bigger than nltk's
        for word in stop_words:
            while word in words:
                words.remove(word)
                
        # remove urllink as this is a html word which occurs frequently
        while "urllink" in words:
            words.remove("urllink")
            
        data.append(words)
        
    return data

#------MODEL----------

#Initialise model and train on the first file
data = openfile("blog1.txt")
data = tokenise_sentences(data)

# create empty model
model = gensim.models.Word2Vec(vector_size=200, min_count=1, sg=0)
model.save("./opposite_word_model")

# train the model on the tokenized data
model.build_vocab(data, update=False)
model.train(data, total_examples=model.corpus_count, epochs=model.epochs)
model.save('./opposite_word_model')

#Train the model on the rest of the data
file_names = ["blog2.txt", "blog3.txt", "blog4.txt", "blog5.txt",\
              "rousseau.txt", "woolf.txt", "kant.txt", "austen.txt", "sense_sensibility.txt"]

for file_name in file_names:
    with open(file_name, "r") as file:    
        content = file.read()

    data = tokenise_sentences(content)

    model.build_vocab(data, update=True)
    model.train(data, total_examples=model.corpus_count, epochs=model.epochs)
    model.save('./opposite_word_model')
    print("Finished training on " + file_name)
