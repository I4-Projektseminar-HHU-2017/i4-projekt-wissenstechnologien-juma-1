import io
import nltk.classify.util

from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem.snowball import SnowballStemmer
from src.const import *
from concurrent.futures import ThreadPoolExecutor, as_completed


class Sentiment:

    def __init__(self):
        
        # Der Prozentfaktor, um welche das Trainings- und das Testset gesplittet werden sollen
        self.split_rate = 0.5
        self.desired_amount = 5000

        # 1 = nur adjektiv-wörter aus den reviews extrahieren (dauert am längsten, 100 Wörter nur am besten)
        # 2 = adjektive und nomen aus den reviews extrahieren
        # 3 = alles was geht extrahieren
        self.pos_tagging_type = 3

        # {'1': [Liste der reviews für 1], '2': [Liste der reviews für 2], ...}
        self.raw_reviews = {}
        
        # Die Datenstruktur, von welcher nachher das fertige Train-Feature-Set für den NLTK Classifier erstellt werden soll
        # (Hier mit ein paar Daten ausgestattet, um das Aussehen zu visualisieren)
        self.processed_train_set = {'0': ({}, '0'),
                                    '1': ({}, '1'),
                                    '2': ({}, '2'),
                                    '3': ({}, '3'),
                                    '4': ({}, '4'),
                                    '5': ({}, '5'),
                                    '6': ({}, '6'),
                                    '7': ({}, '7'),
                                    '8': ({}, '8'),
                                    '9': ({}, '9'),
                                    '10': ({}, '10')}
        # Genauso wie self.processed_train_set, nur für das Test-Feature-Set
        self.processed_test_set = {}
        
        # Liste von Stoppwörtern
        self.stopwords = stopwords.words('english')
        
        # SnowballStemmer Objekt
        self.stemmer = SnowballStemmer("english")
        
        # NLTK Classifier
        self.classifier = None

    """
    Befehl im CMD: 'sentiment stats'
    
    -> Zeigt die Anzahl verfügbarer Reviews in den Textdateien an
    """
    def show_review_stats(self):
        self.execute_reader_pool()  # Textdateien lesen
        print("---------------------\n\n")
        print("Review amounts:\n")
        orderable_list = []
        for review_num, list in self.raw_reviews.items():
            orderable_list.append([review_num, list])
        for elem in sorted(orderable_list, key=lambda x: int(x[0])):
            print('{} points user reviews: {} total'.format(elem[0], len(elem[1])))  # Zeile für Zeile ausgeben
        print("---------------------\n\n")
    
    """
    Befehl im CMD: 'sentiment make'
    
    -> erstellt aus den Textdateien einen fertigen Naive-Bayes-Classifier mit NLTK
    """
    def create_classifier(self):
        self.execute_reader_pool()  # Textdateien lesen
        self.execute_train_set_processor_pool()  # Trainingsset erstellen
        self.execute_test_set_processor_pool()  # Testset erstellen

        train_set_final = self.convert_to_nltk_readable(self.processed_train_set)  # Trainingsset für NLTK verwendbar machen
        test_set_final = self.convert_to_nltk_readable(self.processed_test_set)  # Testset für NLTK verwendbar machen

        self.classifier = NaiveBayesClassifier.train(train_set_final)  # Classifier trainieren
        self.classifier.show_most_informative_features()

        accuracy = nltk.classify.util.accuracy(self.classifier, test_set_final)  # Testset einspeisen
        print("Accuracy: {}\n\n".format(round(accuracy * 100, 2)))
    
    """
    Befehl im CMD: 'sentiment analysis [Text]'
    
    Klassifiziert irgendeinen Text mit unserem Classifier und printet das am besten passende Label.
    
    ACHTUNG: der Text darf keine Line Breaks oder New Lines enthalten, sonst crasht das Programm!
    """
    def sentiment_analysis(self, text: str):
        if self.classifier is not None:
            print(self.classifier.classify(self.test_custom_text(text=text)), end='\n')
        else:
            print("Classifier has not been initialized yet. Please use the command \'sentiment make\' first before attempting to analyse some text!.\n\n")

    """
    ThreadPool um die Textdateien auszulesen
    """
    def execute_reader_pool(self):
        pool = ThreadPoolExecutor(THREADPOOL_SIZE)
        with pool as executor:
            # self.read_reviews wird ab hier mehrere Male parallel ausgeführt
            results_in_future = {executor.submit(self.read_reviews, int(count)): count for count in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
                                                   # Read-Methode                                         # Review-Punktezahlen
            print("Reading reviews...")
            for current_future in as_completed(results_in_future):
                current_review = results_in_future[current_future]  # Review-Zahl
                try:
                    review_list = current_future.result()
                    self.raw_reviews[str(current_review)] = review_list  # Ergebnis eines Threads in self.raw_reviews speichern
                    print('Textfile ' + str(current_review) + '_reviews.txt reading successful. {} reviews total.'.format(len(review_list)))
                except KeyboardInterrupt:
                    executor.shutdown(wait=True)
                except Exception as exc:
                    print('{} generated an exception: {}'.format(current_review, exc))
                    executor.shutdown(wait=True)

            executor.shutdown(wait=True)

        print("\nReading reviews Done")
        print("---------------------\n\n")

    """
    ThreadPool um die Trainingssets zu erstellen
    """
    def execute_train_set_processor_pool(self):
        pool = ThreadPoolExecutor(THREADPOOL_SIZE)
        with pool as executor:
            # self.process_reviews wird ab hier mehrere Male parallel ausgeführt, mit den Trainingsset, welche als Liste von Dictionaries 
            # aus self.get_train_set() kommen
            results_in_future = {executor.submit(self.process_reviews, process_set): process_set for process_set in self.get_train_set()}
                                                 # Process-Review Methode                                          # Liste von Trainingsdaten
            print("Creating training set...")
            for current_future in as_completed(results_in_future):
                try:
                    review_num = current_future.result()[0]
                    words = current_future.result()[1]
                    self.processed_train_set[str(review_num)] = (words, str(review_num))  # Ergebnisse der Threads speichern
                    print('Processing training set for reviews with {} points successful. {} tokenized words in total.'.format(review_num, len(words)))
                except KeyboardInterrupt:
                    executor.shutdown(wait=True)
                except Exception as exc:
                    print('Generated an exception: {}'.format(exc))
                    executor.shutdown(wait=True)

            executor.shutdown(wait=True)

        print("\nTokenizing training sets done.")
        print("---------------------\n\n")

    """
    ThreadPool um die Testsets zu erstellen
    """
    def execute_test_set_processor_pool(self):
        pool = ThreadPoolExecutor(THREADPOOL_SIZE)
        with pool as executor:
            # Hier passiert dasselbe wie in self.execute_train_set_processor_pool oben, nur mit dem Test-Set
            results_in_future = {executor.submit(self.process_reviews, process_set): process_set for process_set in self.get_test_set()}
                                                 # Process-Review Methode                                          # Liste von Testdaten
            print("Creating test set...")
            for current_future in as_completed(results_in_future):
                try:
                    review_num = current_future.result()[0]
                    words = current_future.result()[1]
                    self.processed_test_set[str(review_num)] = (words, str(review_num))  # Testdaten speichern
                    print('Processing test set for reviews with {} points successful. {} tokenized words in total.'.format(review_num, len(words)))
                except KeyboardInterrupt:
                    executor.shutdown(wait=True)
                except Exception as exc:
                    print('Generated an exception: {}'.format(exc))
                    executor.shutdown(wait=True)

            executor.shutdown(wait=True)

        print("\nTokenizing test sets done.")
        print("---------------------\n\n")

    """
    Diese Methode wird dazu verwendet, um jegliche Reviews zu tokenizen und für den Klassifizierer bereit zu machen.
    """
    def process_reviews(self, process_set: dict):
        return_list = []
        word_dict = {}

        for review_num, review_list in process_set.items():
            for review in review_list:
                review_tokenized = word_tokenize(review)  # Wörter tokenizen

                for word in review_tokenized:
                    if word.isalpha():  # nur wörter auslesen, zahlen erstmal ignorieren
                        if word.lower() not in self.stopwords:  # stoppwörter ignorieren
                            if self.pos_tagging_type != 3:
                                for x, pos in pos_tag(word_tokenize(word)):
                                    if self.pos_tagging_type == 1:
                                        if pos == 'JJ' or pos == 'JJR' or pos == 'JJS':
                                            if len(word_dict) != self.desired_amount:  # Hier wird sichergestellt, dass genau so viele Wörter extrahiert werden, wie in self.desired_amount angegeben (beispielsweise 5000 Wörter)
                                                word_dict[self.stemmer.stem(str(word.lower()))] = True  # {'Wort': True}
                                            else:
                                                return [str(review_num), word_dict]
                                    elif self.pos_tagging_type == 2:
                                        if pos == 'JJ' or pos == 'JJR' or pos == 'JJS' or pos == 'NN' or pos == 'NNS':
                                            if len(word_dict) != self.desired_amount:  # Hier wird sichergestellt, dass genau so viele Wörter extrahiert werden, wie in self.desired_amount angegeben (beispielsweise 5000 Wörter)
                                                word_dict[self.stemmer.stem(str(word.lower()))] = True  # {'Wort': True}
                                            else:
                                                return [str(review_num), word_dict]
                            else:
                                if len(word_dict) != self.desired_amount:  # Hier wird sichergestellt, dass genau so viele Wörter extrahiert werden, wie in self.desired_amount angegeben (beispielsweise 5000 Wörter)
                                    word_dict[self.stemmer.stem(str(word.lower()))] = True  # {'Wort': True}
                                else:
                                    return [str(review_num), word_dict]


            return_list = [str(review_num), word_dict]
                        
        return return_list

    """
    Diese Methode wird von self.execute_reader_pool verwendet, um die Textdateien zu lesen.
    """
    def read_reviews(self, count: int):
        reviews = []
        with io.open(OUTPUT_PATH + str(count) + REVIEW_TXT_SUFFIX, 'r', encoding='utf-8') as current_file:
            review_content = current_file.read().encode('utf-8').strip()  # unicode gedöns (muss sein sonst gibts leider error)
            review_content = str(review_content).split(DELIMITER)
            #max_reviews = self.desired_amount
            for review in review_content:
                #if max_reviews != 0:
                reviews.append(review)
                    #max_reviews -= 1
                #else:
                    #break
        return reviews
    
    """
    Aus den raw_reviews Trainingssets erstellen
    """
    def get_train_set(self):
        train_set = []
        for review_num, review_list in self.raw_reviews.items():
            slice_at = int(round((len(review_list) * (1 - self.split_rate)), 0)) - 1
            train_set.append({review_num: review_list[:slice_at]})
        return train_set

    """
    Aus den raw_reviews Testsets erstellen
    """
    def get_test_set(self):
        test_set = []
        for review_num, review_list in self.raw_reviews.items():
            slice_at = int(round((len(review_list) * (1 - self.split_rate)), 0)) - 1
            test_set.append({review_num: review_list[slice_at:]})
        return test_set

    """
    Trainings-/Testset in eine Form bringen, mit der NLTK was anfangen kann.
    
    [({'word1': True, 'word2':True}, 'pos'), ({'word1':True}, 'neg'), ...]
    
    Hier werden die Sets auch in Ihre Labels eingeteilt.
    """
    def convert_to_nltk_readable(self, processed_train_set):
        train_set_final = []
        for review_num, classification_set in processed_train_set.items():
            if len(classification_set[0]) > 0:
                sub_dict = {}
                for word, boolean in classification_set[0].items():
                    sub_dict[word] = boolean
                    
                # Hier werden die Reviews nach ihren Punkten in ihere zugehörigen Labels eingeteilt
                if str(review_num) in ['0', '1']:
                    train_set_final.append((sub_dict, 'overwhelming_dislike_(0|1)'))
                elif str(review_num) in ['2', '3']:
                    train_set_final.append((sub_dict, 'generally_unfavorable_(2|3)'))
                elif str(review_num) in ['4', '5']:
                    train_set_final.append((sub_dict, 'mixed_or_average_(4|5)'))
                elif str(review_num) in ['6', '7']:
                    train_set_final.append((sub_dict, 'generally_favorable_(6|7)'))
                elif str(review_num) in ['8', '9', '10']:
                    train_set_final.append((sub_dict, 'universal_acclaim_(8|9|10)'))
                """
                elif str(review_num) in ['10']:
                    train_set_final.append((sub_dict, 'perfect_(10)'))
                """
        return train_set_final

    """
    Diese Methode ist quasi eine Mini-Version von self.process_reviews(), nur das diese darauf
    ausgelegt ist, unsere zu klassifizierenden Texte zu tokenizen.
    """
    def test_custom_text(self, text: str):
        word_dict = {}
        tokenized = word_tokenize(text)
        for word in tokenized:
            if word.isalpha():  # nur wörter auslesen, zahlen erstmal ignorieren
                if word.lower() not in self.stopwords:  # stoppwörter ignorieren
                    word_dict[self.stemmer.stem(word.lower())] = True  # {'Wort': True}
        return word_dict