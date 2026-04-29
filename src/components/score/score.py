import argparse
import os

import joblib
import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--trained_model', required=True)
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--text_column', default='reviewText')
    parser.add_argument('--scored_dataset', required=True)
    args = parser.parse_args()

    csv_files = [f for f in os.listdir(args.dataset) if f.endswith('.csv')]
    df = pd.read_csv(os.path.join(args.dataset, csv_files[0]))

    model = joblib.load(os.path.join(args.trained_model, 'model.pkl'))
    df['score'] = model.predict(df[args.text_column].fillna(''))

    os.makedirs(args.scored_dataset, exist_ok=True)
    df.to_csv(os.path.join(args.scored_dataset, 'scored.csv'), index=False)
    print(f"Scored {len(df)} rows → {args.scored_dataset}")


if __name__ == '__main__':
    main()
