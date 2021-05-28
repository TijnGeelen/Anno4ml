from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn import tree
import random

from sklearn.metrics import classification_report, confusion_matrix, cohen_kappa_score

def read_corpus(corpus_file, use_sentiment):
    documents = []
    labels = []
    with open(corpus_file, encoding='utf-8') as f:
        for line in f:
            tokens = line.strip().split()

            documents.append(tokens[3:])

            if use_sentiment:
                # 2-class problem: positive vs negative
                labels.append( tokens[1] )
            else:
                # 6-class problem: books, camera, dvd, health, music, software
                labels.append( tokens[0] )

    return documents, labels
    
# a dummy function that just returns its input
def identity(x):
    return x

X, Y = read_corpus('testfile.txt', use_sentiment=False)
split_point = int(0.75*len(X))
Xtrain = X[:split_point]
Ytrain = Y[:split_point]
Xtest = X[split_point:]
Ytest = Y[split_point:]

# let's use the TF-IDF vectorizer
tfidf = True

# we use a dummy function as tokenizer and preprocessor,
# since the texts are already preprocessed and tokenized.
if tfidf:
    vec = TfidfVectorizer(preprocessor = identity,
                          tokenizer = identity)
else:
    vec = CountVectorizer(preprocessor = identity,
                          tokenizer = identity)

# Naive Bayes
classifier = Pipeline( [('vec', vec),
                        ('cls', MultinomialNB())] )

classifier.fit(Xtrain, Ytrain)
Yguess = classifier.predict(Xtest)

print("------------------------------------------------------------------------------")
print('Naive Bayes model:')
print(classification_report(Ytest, Yguess, digits=3))

mtrx = confusion_matrix(Ytest,Yguess,labels = ["Anger", "Anticipation", "Caring", "Disgust", "Fear", "Joy", "Sadness", "Surprise", "Trust", "Other", "None"])
print("Confusion matrix:")
print(mtrx)
kappa = cohen_kappa_score(Ytest, Yguess, labels = ["Anger", "Anticipation", "Caring", "Disgust", "Fear", "Joy", "Sadness", "Surprise", "Trust", "Other", "None"])
print("Kappa score")
print(kappa)


# Tree model
classifier = Pipeline( [('vec', vec),
                        ('cls', tree.DecisionTreeClassifier())] )
classifier.fit(Xtrain, Ytrain)
Yguess = classifier.predict(Xtest)

print("-----------------------------------------------------------------------------")
print("Tree Model")
print(classification_report(Ytest, Yguess, digits=3))

mtrx = confusion_matrix(Ytest,Yguess,labels = ["Anger", "Anticipation", "Caring", "Disgust", "Fear", "Joy", "Sadness", "Surprise", "Trust", "Other", "None"])
print("Confusion matrix:")
print(mtrx)
kappa = cohen_kappa_score(Ytest, Yguess, labels = ["Anger", "Anticipation", "Caring", "Disgust", "Fear", "Joy", "Sadness", "Surprise", "Trust", "Other", "None"])
print("Kappa score")
print(kappa)



