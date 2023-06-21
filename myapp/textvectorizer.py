from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import numpy
import string
import copy

# Serialize into a class for pickling
class TextVectorizer():
  stopwords = stopwords
  vectorizer = None  
  dtype = numpy.uint8
  def __init__(self, stopwords):
      self.vectorizer = CountVectorizer(analyzer = self.message_cleaning, dtype = self.dtype)
      # save all the stopwords inside the object
      self.stopwords = copy.deepcopy(stopwords)

  def message_cleaning(self, message):
      Test_punc_removed = [char for char in message if char not in string.punctuation]
      Test_punc_removed_join = ''.join(Test_punc_removed)
      Test_punc_removed_join_clean = [word for word in Test_punc_removed_join.split() if word.lower() not in self.stopwords]
      return Test_punc_removed_join_clean
