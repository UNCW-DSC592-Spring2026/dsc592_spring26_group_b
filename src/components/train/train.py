import argparse
import os

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--text_column', default='reviewText')
    parser.add_argument('--label_column', default='reviewerRating')
    parser.add_argument('--trained_model', required=True)
    args = parser.parse_args()

    csv_files = [f for f in os.listdir(args.dataset) if f.endswith('.csv')]
    df = pd.read_csv(os.path.join(args.dataset, csv_files[0]))

    X = df[args.text_column].fillna('')
    y = df[args.label_column]

    model = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=10000)),
        ('lr', LinearRegression()),
    ])
    model.fit(X, y)

    os.makedirs(args.trained_model, exist_ok=True)
    joblib.dump(model, os.path.join(args.trained_model, 'model.pkl'))
    print(f"Trained on {len(df)} rows → {args.trained_model}")


if __name__ == '__main__':
    main()
