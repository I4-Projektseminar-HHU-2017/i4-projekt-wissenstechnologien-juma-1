import io

counter = list(range(0, 11))

words = {}		# {'0_words':[wörter aus 0 punkte reviews], '1_words':[wörter aus 1 punkte reviews], '2_words':[wörter aus 2 punkte reviews], ...}
for count in counter:
	with io.open("./output/" + str(count) + "_reviews.txt", 'r', encoding = 'utf-8') as current_file:
		content = current_file.read().encode('utf-8').strip()
		current_number = str(count) + "_words"
		words[current_number] = str(content).split()

print(words['0_words'])
print(words['10_words'])

# diese werden alle benoetigt
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# In dieser Form erwartet der Classifier den Input, dict mit word und True
def create_word_features(words):
# Zunaechst werden die Stoppwoerter entfernt, weil sie keinen Gehalt haben
    useful_words = [word for word in words if word not in stopwords.words("english")]
    my_dict = dict([(word, True) for word in useful_words])
    return my_dict

#leere Liste, Schleife laeuft über alle 0-Punkte Reviews im Ordner und erstellt Merkmale fuer Kategorie, "zero" ist Label für Kategorie
zero_reviews = []
for fileid in output.fileids('0_words'):
	words = output.words(fileid)
	neg_reviews.append((create_word_features(words), "zero"))

#print(0_reviews[0])    
#print(len(0_reviews))

one_reviews = []
for fileid in output.fileids('1_words'):
    words = output.words(fileid)
    one_reviews.append((create_word_features(words), "one"))
    
two_reviews = []
for fileid in output.fileids('2_words'):
    words = output.words(fileid)
    two_reviews.append((create_word_features(words), "two"))

three_reviews = []
for fileid in output.fileids('3_words'):
    words = output.words(fileid)
    three_reviews.append((create_word_features(words), "three"))

four_reviews = []
for fileid in output.fileids('4_words'):
    words = output.words(fileid)
    four_reviews.append((create_word_features(words), "four"))

five_reviews = []
for fileid in output.fileids('5_words'):
    words = output.words(fileid)
    five_reviews.append((create_word_features(words), "five"))

six_reviews = []
for fileid in output.fileids('6_words'):
    words = output.words(fileid)
    six_reviews.append((create_word_features(words), "six"))

seven_reviews = []
for fileid in output.fileids('7_words'):
    words = output.words(fileid)
    seven_reviews.append((create_word_features(words), "seven"))
    
eight_reviews = []
for fileid in output.fileids('8_words'):
    words = output.words(fileid)
    eight_reviews.append((create_word_features(words), "eight"))

nine_reviews = []
for fileid in output.fileids('9_words'):
    words = output.words(fileid)
    nine_reviews.append((create_word_features(words), "nine"))

ten_reviews = []
for fileid in output.fileids('10_words'):
    words = output.words(fileid)
    ten_reviews.append((create_word_features(words), "ten"))

#Aufteilen der Reviews in trainings- und testset
train_set = zero_reviews[:750] + one_reviews[:750] + two_reviews[:750] + three_reviews[:750]+ four_reviews[:750] + five_reviews[:750]+ six_reviews[:750] + seven_reviews[:750] + eight_reviews[:750] + nine_reviews[:750] + ten_reviews[:750]
test_set =  zero_reviews[750:] + one_reviews[750:] + two_reviews[750:] + three_reviews[750:]+ four_reviews[750:] + five_reviews[750:]+ six_reviews[750:] + seven_reviews[750:] + eight_reviews[750:] + nine_reviews[750:] + ten_reviews[750:]
print(len(train_set),  len(test_set))

#Erstellen des Classifier und trainieren mit trainingsset
classifier = NaiveBayesClassifier.train(train_set)

#Genauigkeit des Classifiers in Bezug auf Testset
accuracy = nltk.classify.util.accuracy(classifier, test_set)
print(accuracy * 100)

# Moeglichkeit, einzelne Reviews zu klassifizieren, könnten wir vllt live vorfuehren? :)
words = word_tokenize(review_film)
words = create_word_features(words)
classifier.classify(words) 


