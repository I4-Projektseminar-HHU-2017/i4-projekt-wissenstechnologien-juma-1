<h2> I4-Projekt-Wissenstechnologien-JuMa </h2> <br>
scraper version 1.0 12.08.2017 <br>

<h3>DESCRIPTION</h3>
The aim of this project is <br>
1)	to scrape user reviews from metacritic.com from all categories (i.e. “overwhelming dislike”, “generally unfavourable”, “mixed or average”, “generally favourable”, universal acclaim”) <br>
<br>
and <br>
<br>
2)	feed them to a sentiment algorithm. Half of the reviews will be used as a training set and the other half will provide the test set that the algorithm tries to classify correctly (using Naïve Bayes). Based on what the algorithm has learned from the training set, it will try to classify the reviews and assign them the correct label (= which of the five categories above they fall into). <br>

<h3>GENERAL USAGE NOTES</h3>
•	Before using the program, you need to install Python 3.4, the NLTK and the concurrent.futures module. <br>
<br>
•	The program can be used in two different ways: <br>
a)	You can use the reviews provided under scraper/output and feed them to the algorithm. <br>
<br>
b)	You can use the scraper to scrape other reviews which you wish to train / test the algorithm with. <br>
<br>
•	This is a command line program. To use the program, you have to download all required files [i.e. all files under scraper] and save them in one folder. <br>
<br>
•	Firstly, you need to type <i> install_scraper.bat</i>. This will install the scraper and create the needed output-files (= the .txt files that will contain the reviews) as well as a scraper.bat file. If you want to use the reviews that are provided here, you can skip this step. <br>
<br>
•	To see a list of all applicable commands, type in <i> scrape -h</i>. To scrape some reviews from Metacritic.com, type <i> scrape </i>. Note that the scraping cannot be aborted. <br> 
<br>
•	The scraper scrapes user reviews from “games” by default. To change the category or any other settings, type<i> scrape -h </i> and read the instructions. <br>
<br>
•	You can now execute the sentiment algorithm by typing in <i> sentiment make </i>. The algorithm will read in the reviews and edit them to make classifying them easier, i.e. tokenizing, removing of stop words and creating dictionaries for each category [see above]. Then it will classify the reviews. <br>
<br>
•	The output shows a list of the most informative features (those features the algorithm detected to be most helpful when classifying reviews) and the accuracy in percent. Next to the features you can see which two categories the words could belong to and how likely it is that they do: <br>
<br>
Word = True 	category1 : category2 	= 2.6 : 1.0 <br> 
Means that it is 2.6 times more likely for word to fall into category1 than category2. <br>
The accuracy states in how many cases the algorithm’s prediction was correct, i.e. how many words from reviews he classified into a class that the word actually belongs to (based on the training set). <br>

<h3>CONTACT</h3>
•	Marco.Kluin@hhu.de <br>
•	Julia.Fuerst@hhu.de <br>

<br>
License: WTFPL

<br>

<h6>Copyright 2017 Marco Kluin, Julia Fuerst</h6>


