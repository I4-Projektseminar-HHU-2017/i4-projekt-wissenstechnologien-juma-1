import nltk.classify.util
from nltk.classify import NaiveBayesClassifier

# Reviews einlesen
"""fobj = open("Datei.txt")
for line in fobj:
    print(line.rstrip())
fobj.close()"""
 
# feature extractor:
"""def word_feats(words):
    return dict([(word, True) for word in words])
 
oneids = Datei.fileids('one') vllt eher ('1') ?
twoids = Datei.fileids('two')
threeids = Datei.fileids('three')
fourids = Datei.fileids('four')
fiveids = Datei.fileids('five')
sixids = Datei.fileids('six')
sevenids = Datei.fileids('seven')
eightids = Datei.fileids('eight')
nineids = Datei.fileids('nine')
tenids = Datei.fileids('ten')
 
onefeats = [(word_feats(Datei.words(fileids=[f])), 'one') for f in oneids]
twofeats = [(word_feats(Datei.words(fileids=[f])), 'two') for f in twoids]
threefeats = [(word_feats(Datei.words(fileids=[f])), 'three') for f in threeids]
fourfeats = [(word_feats(Datei.words(fileids=[f])), 'four') for f in fourids]
fivefeats = [(word_feats(Datei.words(fileids=[f])), 'five') for f in fiveids]
sixfeats = [(word_feats(Datei.words(fileids=[f])), 'six') for f in sixids]
sevenfeats = [(word_feats(Datei.words(fileids=[f])), 'seven') for f in sevenids]
eightfeats = [(word_feats(Datei.words(fileids=[f])), 'eight') for f in eightids]
ninefeats = [(word_feats(Datei.words(fileids=[f])), 'nine') for f in nineids]
tenfeats = [(word_feats(Datei.words(fileids=[f])), 'ten') for f in tenids]

ODER (müsste natürlich noch angepasst werden):
mydir = '/home/juls/meine_movie_reviews'

mr = CategorizedPlaintextCorpusReader(mydir, r'(?!\.).*\.txt', cat_pattern=r'(neg|pos)/.*', encoding='ascii')
stop = stopwords.words('english')
documents = [([w for w in mr.words(i) if w.lower() not in stop and w.lower() not in string.punctuation], i.split('/')[0]) for i in mr.fileids()]

word_features = FreqDist(chain(*[i for i,j in documents]))
word_features = word_features.keys()[:100]


"""

# Teilen der Reviews in Training set(3/4) und Test set(1/4) 

negcutoff = (len(onefeats)+ len(twofeats) + len(threefeats)+len(fourfeats)+len(fivefeats))*3/4
neutctoff = len(sixfeats)*3/4
poscutoff = (len(sevenfeats)+len(eightfeats)+len(ninefeats)+len(tenfeats))*3/4


 
trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff] + neutfeats[:neutcutoff]
testfeats = negfeats[negcutoff:] + posfeats[poscutoff:] + neutfeats[neutcutoff:]
print 'trainiere an  %d Reviews, teste an %d Reviews' % (len(trainfeats), len(testfeats)) 

classifier = NaiveBayesClassifier.train(trainfeats)
# Genauigkeit ausgeben
print 'Genauigkeit:', nltk.classify.util.accuracy(classifier, testfeats)


# most informative Features ausgeben, alternativ nur gewisse Anzahl z.B. 5
classifier.show_most_informative_features()
