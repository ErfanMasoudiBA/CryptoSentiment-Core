# """
# Advanced AI logic for cryptocurrency sentiment analysis.
# Supports VADER (fast, rule-based) and FinBERT (transformer-based, financial domain).
# """

# import torch
# from scipy.special import softmax
# from transformers import AutoTokenizer, AutoModelForSequenceClassification
# from nltk.sentiment.vader import SentimentIntensityAnalyzer

# # Ensure VADER lexicon is available
# import nltk
# nltk.download("vader_lexicon", quiet=True)


# class CryptoAI:
#     """Dual-model sentiment analyzer: VADER and FinBERT."""

#     def __init__(self):
#         self._vader = SentimentIntensityAnalyzer()
#         self._tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
#         self._finbert_model = AutoModelForSequenceClassification.from_pretrained(
#             "ProsusAI/finbert",
#             use_safetensors=True,
#         )
#         self._finbert_model.eval()
#         print("FinBERT Model Loaded")

#     def analyze_vader(self, text: str) -> dict:
#         """
#         Analyze sentiment using VADER.
#         Returns: {"label": "positive"|"negative"|"neutral", "score": float}
#         """
#         if not text or not str(text).strip():
#             return {"label": "neutral", "score": 0.0}

#         try:
#             text = str(text).strip()
#             scores = self._vader.polarity_scores(text)
#             compound = scores["compound"]

#             if compound >= 0.05:
#                 label = "positive"
#             elif compound <= -0.05:
#                 label = "negative"
#             else:
#                 label = "neutral"

#             return {"label": label, "score": float(compound)}
#         except Exception as e:
#             return {"label": "neutral", "score": 0.0, "error": str(e)}

#     def analyze_finbert(self, text: str) -> dict:
#         """
#         Analyze sentiment using FinBERT.
#         Returns: {"label": "positive"|"negative"|"neutral", "score": float}
#         """
#         if not text or not str(text).strip():
#             return {"label": "neutral", "score": 0.0}

#         try:
#             text = str(text).strip()
#             inputs = self._tokenizer(
#                 text,
#                 padding=True,
#                 truncation=True,
#                 return_tensors="pt",
#                 max_length=512,
#             )

#             with torch.no_grad():
#                 outputs = self._finbert_model(**inputs)

#             logits = outputs.logits
#             if logits.dim() == 2:
#                 logits = logits[0]
#             probs = softmax(logits.numpy())

#             pred_idx = int(probs.argmax())
#             score = float(probs[pred_idx])

#             id2label = self._finbert_model.config.id2label
#             label = id2label.get(str(pred_idx), "neutral").lower()

#             return {"label": label, "score": score}
#         except Exception as e:
#             return {"label": "neutral", "score": 0.0, "error": str(e)}

#     def compare_models(self, text: str) -> dict:
#         """
#         Run both VADER and FinBERT on the same text and return a comparison.
#         """
#         if not text or not str(text).strip():
#             return {
#                 "text": "",
#                 "vader": {"label": "neutral", "score": 0.0},
#                 "finbert": {"label": "neutral", "score": 0.0},
#                 "agreement": True,
#             }

#         vader_result = self.analyze_vader(text)
#         finbert_result = self.analyze_finbert(text)

#         vader_label = vader_result.get("label", "neutral")
#         finbert_label = finbert_result.get("label", "neutral")
#         agreement = vader_label == finbert_label

#         return {
#             "text": text[:200] + ("..." if len(text) > 200 else ""),
#             "vader": {"label": vader_label, "score": vader_result.get("score", 0.0)},
#             "finbert": {"label": finbert_label, "score": finbert_result.get("score", 0.0)},
#             "agreement": agreement,
#         }



import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class CryptoAI:
    def __init__(self):
        print("--- Initializing AI Engines ---")
        
        # 1. راه اندازی VADER
        try:
            self.vader = SentimentIntensityAnalyzer()
            print("✅ VADER Loaded")
        except:
            import nltk
            nltk.download('vader_lexicon')
            self.vader = SentimentIntensityAnalyzer()

        # 2. راه اندازی FinBERT
        print("⏳ Loading FinBERT (ProsusAI)...")
        model_name = "ProsusAI/finbert"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.finbert_model = AutoModelForSequenceClassification.from_pretrained(model_name)
        print("✅ FinBERT Loaded")

    def analyze_vader(self, text):
        score = self.vader.polarity_scores(text)['compound']
        if score >= 0.05:
            label = "positive"
        elif score <= -0.05:
            label = "negative"
        else:
            label = "neutral"
        return {"label": label, "score": score}

    def analyze_finbert(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        
        with torch.no_grad():
            outputs = self.finbert_model(**inputs)
            logits = outputs.logits
            
            # تبدیل خروجی خام به درصد احتمالات
            probabilities = F.softmax(logits, dim=1)
            
            # پیدا کردن بالاترین احتمال
            highest_prob_score = torch.max(probabilities).item()
            predicted_class_index = torch.argmax(probabilities).item()
            
            # --- بخش اصلاح شده: دریافت برچسب واقعی از کانفیگ مدل ---
            # مدل ProsusAI معمولاً اینطوری است: {0: 'positive', 1: 'negative', 2: 'neutral'}
            labels_map = self.finbert_model.config.id2label
            predicted_label = labels_map[predicted_class_index]
            
            # نرمال سازی نام لیبل ها (چون گاهی با حروف بزرگ هستند)
            predicted_label = predicted_label.lower()

        return {"label": predicted_label, "score": highest_prob_score}