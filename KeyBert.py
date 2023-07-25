from keybert import KeyBERT
import joblib

kw_model = KeyBERT()

joblib.dump(kw_model, 'models/kw_model.sav')




