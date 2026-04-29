
# Modeling
Information theory is used to reduce noise and identify the most significant signals within the unstructured text data.

*   **Noise Reduction & Signal Processing**: 
    *   **Stopword Removal**: Eliminates high-frequency tokens (e.g., "the", "is") that carry low information content (high entropy), allowing the model to focus on high-signal sentiment words[cite: 1].
    *   **Lemmatization**: Reduces morphological variants to a single base form (e.g., "running" to "run"), decreasing the vocabulary's state space and consolidating information[cite: 1].
    *   **PII Masking**: Replaces high-variance, unique identifiers (emails, phone numbers) with constant tokens like `[EMAIL]` or `[PHONE]`. This removes information that is irrelevant to sentiment while preserving the structural signal of the review[cite: 1].
*   **TF-IDF (Term Frequency-Inverse Document Frequency)**:
    *   This is a core information-theoretic weighting scheme[cite: 2].
    *   **Term Frequency (TF)**: Measures the local importance of a word within a specific review[cite: 2].
    *   **Inverse Document Frequency (IDF)**: Penalizes words that appear too frequently across the entire dataset, effectively identifying words that are "informative" because they are unique to specific types of feedback[cite: 2].

---

## 📊 Statistical Modeling & Concepts
The pipeline employs classical statistical methods to ensure the model generalizes well to new, unseen data.

*   **Dimensionality Management**:
    *   The `TfidfVectorizer` is constrained to a `max_features` of 10,000[cite: 2]. This statistical pruning prevents the "curse of dimensionality" and helps the model avoid overfitting on rare, non-representative tokens[cite: 2].
*   **Linear Regression**:
    *   The pipeline uses **Ordinary Least Squares (OLS)** through `LinearRegression` to model the relationship between the numerical text vectors ($X$) and the target ratings ($y$)[cite: 2].
    *   It assumes a linear relationship where the predicted sentiment score is a weighted sum of the presence and importance of specific words[cite: 4].
*   **Data Partitioning (Train-Test Split)**:
    *   The dataset is split into training and testing subsets (default 80/20)[cite: 3].
    *   This statistical validation technique ensures that the model's performance metrics are calculated on data it has never seen, providing an unbiased estimate of real-world accuracy[cite: 3].
*   **Random Seeding**:
    *   A fixed `random_seed` (42) is used during the split to ensure **reproducibility**[cite: 3]. This allows engineers to verify that changes in model performance are due to pipeline adjustments rather than statistical variations in how the data was sampled[cite: 3].

---

## 🛠️ Summary of the Working Pipeline

| Component | Technical Implementation | Goal |
| :--- | :--- | :--- |
| **Preprocessing** | Regex, NLTK, PII Masking[cite: 1] | Clean noise and enforce data privacy[cite: 1]. |
| **Data Splitting** | `train_test_split`[cite: 3] | Enable statistical validation and prevent overfitting[cite: 3]. |
| **Vectorization** | `TfidfVectorizer`[cite: 2] | Convert text into an information-weighted numerical matrix[cite: 2]. |
| **Estimation** | `LinearRegression`[cite: 2] | Map features to a continuous sentiment score[cite: 2, 4]. |
| **Persistence** | `joblib`[cite: 2, 4] | Serialize the trained model for production scoring[cite: 2, 4]. |

---

**Next Step:** Would you like to see how to implement **N-gram** features (Bigrams/Trigrams) to capture multi-word context like "not working"?
