## Baseline Text Preprocessing – Documentation

### Overview

User-generated reviews often contain noise, inconsistencies, informal language and not only reviews are in english there are some transcriptions, preprocessing is 
required to make the model performance better and interpretable. The baseline system has a structured text preprocessing module implemented using the Azure Machine 
Learning Preprocess Text component. This module easily transforms raw, unstructured user review data into a clean and standardized format suitable to
make things easy for machine learning tasks.

### Language Standardization and Normalization

The preprocessing pipeline begins by specifying the language as English, ensuring that all transformations are appropriately applied. One of the first steps is 
expanding short form of the words, where words like “don’t” are converted into their full equivalents like “do not.” This step helps maintain consistency  and improves 
the model’s ability to recognize patterns across similar phrases. Next, the system applies case normalization, converting all text to lowercase. This ensures that words 
such as “Good” and “good” are treated identically, preventing redundancy. Following this, stopword removal is performed. Commonly used words such 
as “the,” “is,” and “and” are removed, These words could be noise in feature space also they do not have a semantic meaning to contribute.

### Lemmetization, Sentence detection and Character removal

The module also enables lemmatization, which reduces words to their base or root form. For example, “running,” “runs,” and “ran” are all transformed into “run.” This step 
is way useful because it reduces the dimensionality in feature space and it consolidates the similar words. For the sentence detection, By knowing where each sentence starts
and stops, the computer can understand and analyze the text much better. Also to furthur clean the data the pipeline removes numbers, special characters and dupicate 
characters which are irrelavent in analysis.

### Privacy Enforcement

For a privacy aspects, the preprocessing module removes email addresses , phone numbers, ensuring that personally identifiable information (PII) is not 
included in the training data which makes it responsoble for data handling practices. All preprocessing steps are applied specifically to the reviewText 
column, which contains the primary user-generated content.

Overall, this preprocessing module makes a balance between cleaning noisy data and preserving meaningful insights. While aggressive cleaning improves model stability,
it may also remove important context. Therefore, understanding these trade-offs is essential when evaluating model performance and designing future improvements.
