import nltk
nltk.download('punkt')
nltk.download('punkt_tab')   # new requirement in recent NLTK versions
nltk.download('stopwords')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from head.mouth import speak

# -------------------- Dataset --------------------
dataset_path = r"c:\Users\ACER\Desktop\pyhon\jarvis\data\brain_data\qna.txt"

def load_dataset(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        qna_pairs = [line.strip().split(':', 1) for line in lines if ':' in line]
        dataset = [{'question': q, 'answer': a} for q, a in qna_pairs]
        return dataset

# -------------------- Preprocessing --------------------
stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [ps.stem(token) for token in tokens if token.isalnum() and token not in stop_words]
    return ' '.join(tokens)

# -------------------- Vectorizer --------------------
def train_tfidf_vectorizer(dataset):
    corpus = [preprocess_text(qa['question']) for qa in dataset]
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)
    return vectorizer, X

# -------------------- Answering --------------------
def get_answer(question, vectorizer, X, dataset, threshold=0.2):
    question = preprocess_text(question)
    question_vec = vectorizer.transform([question])
    similarities = cosine_similarity(question_vec, X)
    best_match_index = similarities.argmax()
    best_score = similarities[0][best_match_index]

    if best_score < threshold:
        return "I'm sorry, I don't know the answer to that."

    return dataset[best_match_index]['answer']

# -------------------- Mind --------------------
def mind(text, vectorizer, X, dataset):
    answer = get_answer(text, vectorizer, X, dataset)
    print("Friday:", answer)
    speak(answer)  # Speak the answer
    return answer

if __name__ == "__main__":
    # Load dataset and train vectorizer only once
    dataset = load_dataset(dataset_path)
    vectorizer, X = train_tfidf_vectorizer(dataset)

    print("Friday: I am ready to assist you, sir. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Friday: Goodbye, sir.")
            speak("Goodbye, sir.")
            break
        mind(user_input, vectorizer, X, dataset)
