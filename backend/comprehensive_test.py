import pandas as pd
from ai_engine import CryptoAI

print("--- Loading AI Engine ---")
# مدل‌ها لود می‌شوند (حدود ۳۰ ثانیه طول می‌کشد)
ai = CryptoAI()

# لیست جملات تستی (شامل انواع سناریوها برای به چالش کشیدن مدل‌ها)
test_cases = [
    # --- گروه 1: کلمات منفی ولی معنای مثبت (Efficiency / Profit) ---
    {"id": 1, "text": "The company fired 500 employees to reduce costs and improve profit margins."},
    {"id": 2, "text": "Cost cutting measures including layoffs will boost the quarterly earnings."},
    
    # --- گروه 2: شوک و نوسان (Supply Shock) ---
    {"id": 3, "text": "Whales are accumulating Bitcoin aggressively, leading to a massive supply shock."},
    {"id": 4, "text": "The sudden supply shock caused the price to stabilize at a higher level."},
    
    # --- گروه 3: اصلاح بازار (Correction) ---
    {"id": 5, "text": "After a paranoid rally, the market is finally experiencing a healthy correction."},
    {"id": 6, "text": "The market dip is healthy and necessary for the next bull run."},
    
    # --- گروه 4: خبر بد با ظاهر خوب (Bull Trap) ---
    {"id": 7, "text": "Despite the record high volume, the support level was shattered."},
    {"id": 8, "text": "Although the volume is high, the bearish trend is confirmed."},
    
    # --- گروه 5: جملات ترکیبی و سخت (Regulatory / Hack) ---
    {"id": 9, "text": "The strict regulations were finally lifted, opening doors for massive adoption."},
    {"id": 10, "text": "Fears of a ban have vanished as the government embraces digital assets."},
    {"id": 11, "text": "The hack resulted in zero loss of user funds due to insurance coverage."},
    {"id": 12, "text": "Panic selling has stopped and smart money is entering the market."}
]

print("\n" + "="*100)
print(f"{'ID':<3} | {'Text (Short)':<55} | {'VADER':<10} | {'FinBERT':<10} | {'Status'}")
print("="*100)

results = []

for case in test_cases:
    text = case['text']
    v_res = ai.analyze_vader(text)
    f_res = ai.analyze_finbert(text)
    
    # بررسی تضاد: اگر لیبل‌ها فرق داشتند، یعنی جذاب است
    status = "⚠️ CONFLICT" if v_res['label'] != f_res['label'] else "✅ SAME"
    
    # چاپ خوشگل در ترمینال
    print(f"{case['id']:<3} | {text[:52]+'...':<55} | {v_res['label']:<10} | {f_res['label']:<10} | {status}")
    
    if status == "⚠️ CONFLICT":
        # چاپ جزئیات بیشتر برای موارد تضاد
        print(f"    -> VADER Score: {v_res['score']} | FinBERT Score: {f_res['score']:.4f}")
        print("-" * 100)

print("\nDONE.")