from keybert import KeyBERT
import joblib

kw_model = KeyBERT()

joblib.dump(kw_model, 'kw_model.sav')

# data=open('data/hypertension.txt', 'r', encoding='utf-8').read()
#
# keywords = kw_model.extract_keywords(data, keyphrase_ngram_range=(1, 2), stop_words='english', use_maxsum=True, nr_candidates=20, top_n=20)
# print("keywords --> \n", keywords)
#
#
# word_list = [keyword for keyword, prob in keywords]
# max= -float('inf')
# max_keyword = None
# for name, prob in keywords:
#     if isinstance(prob, float) and prob > max:
#         max = prob
#         max_keyword = name
#
# print("Main Subject:", max_keyword)

