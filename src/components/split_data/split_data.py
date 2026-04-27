import argparse
import os

import pandas as pd
from sklearn.model_selection import train_test_split


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--train_fraction', type=float, default=0.8)
    parser.add_argument('--random_seed', type=int, default=42)
    parser.add_argument('--results_dataset1', required=True)
    parser.add_argument('--results_dataset2', required=True)
    args = parser.parse_args()

    csv_files = [f for f in os.listdir(args.dataset) if f.endswith('.csv')]
    df = pd.read_csv(os.path.join(args.dataset, csv_files[0]))

    train, test = train_test_split(
        df,
        train_size=args.train_fraction,
        random_state=args.random_seed,
    )

    os.makedirs(args.results_dataset1, exist_ok=True)
    os.makedirs(args.results_dataset2, exist_ok=True)

    train.to_csv(os.path.join(args.results_dataset1, 'train.csv'), index=False)
    test.to_csv(os.path.join(args.results_dataset2, 'test.csv'), index=False)
    print(f"Split {len(df)} rows → train:{len(train)}, test:{len(test)}")


if __name__ == '__main__':
    main()
