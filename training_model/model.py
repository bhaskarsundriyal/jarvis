import nltk
from nltk.tokenize import word_tokenize
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from head.mouth import speak

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Dynamically get dataset path
dataset_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'brain_data', 'qna.txt')
dataset_path = os.path.abspath(dataset_path)

def load_dataset(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        qna_pairs = [line.strip().split(':') for line in lines if ':' in line]
        dataset = [{'question': q, 'answer': a} for q, a in qna_pairs]
        return dataset

def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()
    tokens = word_tokenize(text.lower())
    tokens = [ps.stem(token) for token in tokens if token.isalnum() and token not in stop_words]
    return ' '.join(tokens)

def train_tfidf_vectorizer(dataset):
    corpus = [preprocess_text(qa['question']) for qa in dataset]
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)
    return vectorizer, X

def get_answer(question, vectorizer, X, dataset, threshold=0.2):
    question = preprocess_text(question)
    question_vec = vectorizer.transform([question])
    similarities = cosine_similarity(question_vec, X)
    best_match_index = similarities.argmax()
    best_score = similarities[0][best_match_index]
    
    if best_score < threshold:
        return "I'm sorry, I don't know the answer to that."

    return dataset[best_match_index]['answer']

def mind(text):
    dataset = load_dataset(dataset_path)
    vectorizer, X = train_tfidf_vectorizer(dataset)
    answer = get_answer(text, vectorizer, X, dataset)
    print("Friday:", answer)  # Optional for testing
    speak(answer)

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Friday: Goodbye, sir.")
            break
        mind(user_input)
