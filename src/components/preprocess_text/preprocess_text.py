import argparse
import os
import re

import nltk
import pandas as pd

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


def preprocess(text: str, args) -> str:
    if args.normalize_case:
        text = text.lower()
    if args.remove_urls:
        text = re.sub(r'http\S+|www\.\S+', '', text)
    if args.remove_emails:
        text = re.sub(r'\S+@\S+', '', text)
    if args.remove_numbers:
        text = re.sub(r'\d+', '', text)
    if args.normalize_backslashes:
        text = text.replace('\\', '/')
    if args.split_on_special_chars:
        text = re.sub(r'[_\-/]', ' ', text)
    if args.remove_special_chars:
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    if args.remove_duplicate_chars:
        text = re.sub(r'(.)\1{2,}', r'\1', text)

    tokens = word_tokenize(text)

    if args.remove_stop_words:
        stop_words = set(stopwords.words('english'))
        tokens = [t for t in tokens if t.lower() not in stop_words]

    if args.use_lemmatization:
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(t) for t in tokens]

    return ' '.join(tokens)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--text_column', default='reviewText')
    parser.add_argument('--remove_stop_words', type=lambda x: x.lower() == 'true', default=True)
    parser.add_argument('--use_lemmatization', type=lambda x: x.lower() == 'true', default=True)
    parser.add_argument('--normalize_case', type=lambda x: x.lower() == 'true', default=True)
    parser.add_argument('--remove_numbers', type=lambda x: x.lower() == 'true', default=True)
    parser.add_argument('--remove_special_chars', type=lambda x: x.lower() == 'true', default=True)
    parser.add_argument('--remove_duplicate_chars', type=lambda x: x.lower() == 'true', default=True)
    parser.add_argument('--remove_emails', type=lambda x: x.lower() == 'true', default=True)
    parser.add_argument('--remove_urls', type=lambda x: x.lower() == 'true', default=True)
    parser.add_argument('--normalize_backslashes', type=lambda x: x.lower() == 'true', default=True)
    parser.add_argument('--split_on_special_chars', type=lambda x: x.lower() == 'true', default=True)
    parser.add_argument('--results_dataset', required=True)
    args = parser.parse_args()

    csv_files = [f for f in os.listdir(args.dataset) if f.endswith('.csv')]
    df = pd.read_csv(os.path.join(args.dataset, csv_files[0]))

    df[args.text_column] = (
        df[args.text_column]
        .fillna('')
        .astype(str)
        .apply(lambda t: preprocess(t, args))
    )

    os.makedirs(args.results_dataset, exist_ok=True)
    df.to_csv(os.path.join(args.results_dataset, 'output.csv'), index=False)
    print(f"Preprocessed {len(df)} rows → {args.results_dataset}")


if __name__ == '__main__':
    main()
