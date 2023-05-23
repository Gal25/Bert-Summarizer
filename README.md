# Bert-Summarizer

# Project goal:
our system deals with summarizing medical articles and studies, their summary will help for efficient and fast research as well as for quick diagnosis in emergency cases. The purpose of the system is to make people's work or research more accessible and efficient by saving time and money in reading concise summaries of long articles and studies and also to make accessible to people who lack knowledge - a summary on medical topics.

Our system provides a text summary of long texts or medical articles. Our product works on NLP technology and uses ML model. The purpose of the product is to optimize people's work or research by saving time and money in reading concise summaries of long articles and studies, and making knowledge accessible to people by summarizing.

# Requirements:
At the beginning of the project, we agreed on requirements that we would like to realize, and we used them to plan our project

• The model will be able to summarize long texts.

• Let the machine learn the relevant medical terms.

• The conclusion of the model will be fast and will not take much time for the user.

• The product will be designed in a way that users can understand it easily.

• The summary result will be accessible to the user in a convenient way.

• The article loading process will be efficient.

• The summary should be structured in a good syntactical way and not sentences that are not related to each other.

# How It Works?
The user uploads text (URL, as a file, or in a text line).
The user chooses how he wants to summarize his text (by number of sentences or by ratio).
The user enters more data to create an accurate summary.
With the help of ML model - BERT - which is used to summarize the text, in addition using ML model -  KeyBERT model - we find the subject of the text.
The relevant user receives the result - the topic + the summarized article. In addition, there are options to do with the summarized article such as downloading the file.

# Algorithms:
When it comes to summarizing an article and finding keywords, there are several alternatives available. BERT, GPT, and LSTM are powerful language models that excel in generating human-like text but can be fine-tuned for various natural language processing tasks. RAKE, TextRank, and YAKE are algorithms specifically designed for keyword extraction, considering word frequency, co-occurrence, and graph-based approaches. TF-IDF is a statistical method that determines keyword importance based on term frequency and rarity. Additionally, LDA is a topic modeling technique that can help identify keywords by extracting representative words within each topic. The choice of model or algorithm depends on the specific requirements and characteristics of the text data being analyzed.

**BERT's** powerful language understanding capabilities make it well-suited for generating high-quality summaries, while **KeyBERT's** reliance on BERT embeddings enables it to accurately extract key phrases that capture the core concepts of a text. Together, these models offer valuable solutions for summarization and keyword extraction tasks, providing efficient and accurate methods for understanding and extracting meaningful information from text data. 
For these reasons we chose to use BERT and KeyBERT

# Selected Approach:
There are 2 approaches in the solution that we implement in the task of summarizing the text in NLP, the approaches are: extractive summarization and abstract summarization.
 Extraction - extracts important phrases from the source text that are most relevant to the text. That is, to take the most important sentences in the text and put them in their original form, without change, to illustrate the main idea. Abstract - potential to invent new relevant phrases, which can be seen as a paraphrase. That is, to formulate in a free and different way the main idea of the text, without using original sentences but only conceptually. The goal of this approach is to create a better syntactic summary without using long sentences in the source text. We use both approaches in our project to create an efficient and concise summary, which will also contain the main sentences and be worded in the best way. So that the user can enjoy the best product.

# Modulation and Patterns:

**User space - app_frontend.py**
The front-end site is designed to fill a payload that will be sent to a server space for ML model inference. The main part of the payload is text that will be Moved to summary. In addition, the payload includes instructions on how to text To summarize: according to the ratio between the number of words in the source text vs. Summary, or by several sentences in the summary text.
Upon receiving a response payload from the server surface that includes the text summary, The front end will shape and normalize the ML model response for better representation and publish the result.

**Server space -  Python Flask - app.py** 
Python flask is a micro web framework used for object–relational mapping for converting data between front-end and ML model.

**ML Model**

1.**Bertsum.ipynb** - A trained ML (machine learning) model based on BERT extractive summarizer receives a payload and as a result of inferencing the model responds with a payload that includes the text summarization.
The summarization will be carried out according to the directive in the incoming payload.

2.**KeyBert.py** A trained ML (machine learning) model based on KeyBERT, The method returns a list of keywords/keyphrases extracted from the text and their probabilities. And we can classify texts by topic relevance.



