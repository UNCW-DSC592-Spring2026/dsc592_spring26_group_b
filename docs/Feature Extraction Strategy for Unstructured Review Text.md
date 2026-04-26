## Feature Extraction Strategy for Unstructured Review Text

###  Purpose and Context
Machine learning models operate on numerical inputs. App review text must therefore be transformed into numerical vectors before it can be consumed by any classifier or
regressor. This transformation is called feature extraction, the main thing is we should not feed the low quality data to the model, while preparing data 
(cleaning, formatting) at utmost care by not throwning away important aspects.

The current baseline pipeline passes preprocessed text directly into Linear Regression without an explicit feature extraction component. This means Azure ML applies 
a default tokenization-and-counting strategy under the hood, which is the simplest possible representation and explains much of the baseline's weak, biased behavior. 
This document proposes an explicit feature extraction stage and a suggested improvements ordered by engineering effort(choosing the best one).

###  Constraints Identified From Exploratory Analysis
The proposed strategy is shaped by findings from the EDA notebook (notebooks/data_exploration.ipynb):
- Severe class imbalance: 60.9% of reviews are rated 1.0; the 0.0 class has only 71 samples. Any feature representation must produce signal strong enough to differentiate
  minority classes.
- Hindi/Urdu words like "Bekar" (meaning "useless") appear in the 1.0 class. Bag-of-words models cannot distinguish these without semantic understanding.
- Reviews include English, Hindi, Urdu, and other languages. English-only stopword lists and tokenizers fail on non-English text.
- Phrases such as "does not work" and "won't" require multi-word context. Unigram representations treat "not" and "work" as independent features and lose the
  purpose entirely.
- Mean review length follows an inverted-U pattern across ratings,approx. 14 words at 0.0, ≈28 at 0.4–0.6, ≈18 at 1.0. Length itself carries signal independent of word
  content.
- Repeated letters "loooove", all-caps like "TRASH", and emojis carry strong sentiment but standard preprocessing can't be effective.

##  Proposed Feature Extraction Improvements

### N-Gram Features from Text component with the following configuration:

N-gram range: 1–2 (unigrams + bigrams), with 1–3 evaluated as a follow-up experiment.
Weighting: TF-IDF rather than raw counts.
min_df = 5 and max_df = 0.9 to drop both rare typos and extremely common terms.
sublinear_tf = True so highly repetitive words don't dominate vector magnitude.

Why for our data: Bigrams directly capture "not work", "easy use", "waste money", patterns identified in the EDA. TF-IDF down-weights generic words like "app" that 
appear in nearly every review.
Engineered numerical features alongside text vectors:

review_length (character count)
word_count
exclamation_count and question_count
caps_ratio (proportion of all-caps tokens)

Why for our data: The EDA confirmed length carries rating signal.

###  Domain Lexicon prior to vectorization. 
Replace observed slang ("gud" → "good", "worky" → "working", "bekar" → "useless") before n-gram extraction. This converts noisy informal language into the vocabulary the 
model already understands. Switch to a Word2Vec using the Azure ML Convert Word to Vector component, or pre-trained embeddings via Python script.
Embeddings capture semantic similarity — "amazing", "awesome", and "great" land in nearby vector space, which standard TF-IDF cannot do. Models trained on massive amount
of text, so for unseen text they understand partially. Add a language-detection step like langdetect and route non-English reviews through either a separate 
model branch or a translation step. This addresses the multilingual finding directly.

Finally based on the metrics, we will be choosing one of the feature extraction process for better model performance.
