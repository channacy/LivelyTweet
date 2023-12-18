from sklearn.preprocessing import scale
import pickle 

with open('models/locationClassifier.pkl', 'rb') as location_classifier:
    locationClassifier = pickle.load(location_classifier)

with open('models/vectorizer.pkl', 'rb') as vectorizer_file:
    counter = pickle.load(vectorizer_file)

with open('models/text_sentiment_vectorizer.pkl', 'rb') as sentiment_text_vectorizer:
    text_vectorizer = pickle.load(sentiment_text_vectorizer)

with open('models/sentiment_model.pkl', 'rb') as sentiment_model:
    NB_classifier = pickle.load(sentiment_model)

with open('models/virality_model.pkl', 'rb') as virality_model:
    virality_classifier = pickle.load(virality_model)

def predictLocation(tweet):
  tweet_counts = counter.transform([tweet])
  prediction = locationClassifier.predict(tweet_counts)
  if prediction == [0]:
    location  = "New York"
  elif prediction == [1]:
    location = "London"
  else:
    location = "Paris"
  return location

def predictSentiment(tweet):
   tweet = [tweet]
   result = text_vectorizer.vectorizer.transform(tweet)
   prediction = NB_classifier.predict(result)
   if prediction == 0:
    return "Positive"
   else:
    return "Negative"

def predictVirality(tweet):
    tweet_info = [[55, 100000, 1060, 5, 20, 30, 4]]
    scaled_tweet = scale(tweet_info, axis = 0)
    print(virality_classifier.predict(scaled_tweet))
    return "NA"