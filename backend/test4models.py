from textblob import TextBlob
from transformers import pipeline
from ai_engine import CryptoAI

print("--- 🚀 Loading All 4 Models for Comparison ---")

# 1. لود کردن مدل‌های خودمان (VADER + FinBERT)
print("1️⃣ Loading Our Engine (VADER & FinBERT)...")
my_ai = CryptoAI()

# 2. لود کردن مدل عمومی (General BERT)
print("2️⃣ Loading Generic BERT (DistilBERT)...")
# این مدل روی نقدهای فیلم (IMDB) آموزش دیده و اصلاً مالی نیست
generic_bert = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def analyze_all(text):
    print(f"\n📝 Text: '{text}'")
    print("-" * 60)
    
    # --- A. TextBlob (The Weakest) ---
    blob_score = TextBlob(text).sentiment.polarity
    blob_label = "Positive" if blob_score > 0 else "Negative" if blob_score < 0 else "Neutral"
    print(f"❌ TextBlob:     {blob_label:<10} (Score: {blob_score:.2f}) -> [Too Generic]")
    
    # --- B. VADER (Our Fast Model) ---
    vader = my_ai.analyze_vader(text)
    print(f"✅ VADER:        {vader['label'].title():<10} (Score: {vader['score']:.2f}) -> [Good for Social Media]")

    # --- C. Generic BERT (The Confused One) ---
    bert_res = generic_bert(text)[0]
    print(f"❌ Generic BERT: {bert_res['label'].title():<10} (Score: {bert_res['score']:.2f}) -> [Does not understand Finance]")

    # --- D. FinBERT (The Expert) ---
    finbert = my_ai.analyze_finbert(text)
    print(f"🏆 FinBERT:      {finbert['label'].title():<10} (Score: {finbert['score']:.2f}) -> [Correct Financial Context]")
    print("-" * 60)

# --- سناریوهای تستی برای ضایع کردن مدل‌های دیگر ---

# سناریوی ۱: اصلاح تکنیکال (TextBlob فکر میکنه بده چون کلمه correction داره)
analyze_all("The market is experiencing a healthy correction after the rally.")

# سناریوی ۲: لیکوئید شدن شورت‌ها (Generic BERT نمیفهمه Short یعنی چی)
# معنی: کسانی که شرط بستن قیمت میاد پایین، باختن (پس قیمت میره بالا -> مثبت)
analyze_all("Short sellers got liquidated as Bitcoin surged.")

# سناریوی ۳: نوسان (Generic BERT فکر میکنه نوسان یه چیز عادیه)
analyze_all("Extreme volatility detected in the altcoin market.")