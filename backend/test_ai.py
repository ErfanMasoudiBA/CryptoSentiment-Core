from ai_engine import CryptoAI

print("--- Loading AI Models ---")
ai = CryptoAI()
print("MODELS LOADED SUCCESSFULLY!\n")

# سه تا جمله تست انتخاب کردم:
test_sentences = [
    # 1. جمله کاملاً مثبت و مالی (اینجا باید هر دو مثبت بگن)
    "Bitcoin price skyrocketed to the moon and investors are extremely happy with huge profits.",
    
    # 2. جمله منفی اما با کلمات گول‌زننده (VADER ممکنه گیج بشه ولی FinBERT باید بفهمه)
    "Despite the high volume, the market crashed and users lost all their assets.",
    
    # 3. همون جمله قبلی خودت (برای بررسی دوباره)
    "The strict regulations on crypto were finally lifted by the government."
]

print("="*60)
print(f"{'Text':<50} | {'VADER':<10} | {'FinBERT':<10}")
print("="*60)

for text in test_sentences:
    # تحلیل با هر دو مدل
    v_res = ai.analyze_vader(text)
    f_res = ai.analyze_finbert(text)
    
    # فقط ۳۰ کاراکتر اول متن رو نشون میدیم که تو جدول جا بشه
    short_text = text[:45] + "..."
    
    print(f"{short_text:<50} | {v_res['label']:<10} | {f_res['label']:<10}")
    print(f"Scores -> VADER: {v_res['score']} | FinBERT: {f_res['score']:.4f}")
    print("-" * 60)