import os
import pandas as pd
import ast
from tqdm import tqdm  # برای نمایش نوار پیشرفت
from ai_engine import CryptoAI

# Paths relative to this script's directory (backend/), so it works from any cwd
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, 'data', 'cryptonews.csv')
OUTPUT_FILE = os.path.join(SCRIPT_DIR, 'data', 'benchmark_results.csv')

# LIMIT = 1000
LIMIT = None

def run_benchmark():
    print("--- 🚀 Starting Full Benchmark ---")
    
    # 1. لود کردن هوش مصنوعی
    print("⏳ Loading AI Models...")
    ai = CryptoAI()
    
    # 2. خواندن فایل CSV
    print(f"📂 Reading {INPUT_FILE}...")
    if not os.path.isfile(INPUT_FILE):
        print(f"❌ Error: CSV file not found at {INPUT_FILE}")
        print("   Make sure backend/data/cryptonews.csv exists.")
        return
    try:
        df = pd.read_csv(INPUT_FILE)
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return

    # اعمال لیمیت (اگر نیاز باشد)
    if LIMIT:
        df = df.head(LIMIT)
    
    print(f"📊 Analyzing {len(df)} news items...")

    results = []
    
    # شمارنده‌های دقت
    vader_correct = 0
    finbert_correct = 0
    total = 0

    # 3. حلقه اصلی با نوار پیشرفت
    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Processing"):
        try:
            # ترکیب تیتر و متن برای تحلیل دقیق‌تر
            text = str(row['title']) + " " + str(row['text'])
            
            # --- الف) استخراج لیبل اصلی (Target) ---
            # فرمت فایل کاگل: "{'class': 'negative', ...}"
            try:
                sentiment_dict = ast.literal_eval(row['sentiment'])
                original_label = sentiment_dict.get('class', 'neutral')
            except:
                original_label = 'neutral'
            
            # --- ب) تحلیل با مدل‌های ما ---
            vader_res = ai.analyze_vader(text)
            finbert_res = ai.analyze_finbert(text)
            
            # --- ج) مقایسه ---
            # مدل‌ها معمولاً خروجی lowercase دارند، پس safe عمل می‌کنیم
            orig = original_label.lower()
            vad = vader_res['label'].lower()
            fin = finbert_res['label'].lower()
            
            is_vader_right = (orig == vad)
            is_finbert_right = (orig == fin)
            
            if is_vader_right:
                vader_correct += 1
            if is_finbert_right:
                finbert_correct += 1
            
            total += 1
            
            # ذخیره نتیجه این سطر
            results.append({
                "id": index,
                "original": orig,
                "vader_pred": vad,
                "finbert_pred": fin,
                "vader_correct": is_vader_right,
                "finbert_correct": is_finbert_right
            })
            
        except Exception as e:
            print(f"Error on row {index}: {e}")
            continue

    # 4. محاسبه و چاپ نتایج نهایی
    if total > 0:
        vader_accuracy = (vader_correct / total) * 100
        finbert_accuracy = (finbert_correct / total) * 100
        
        print("\n" + "="*40)
        print("🏁 BENCHMARK RESULTS 🏁")
        print("="*40)
        print(f"Total Rows Analyzed: {total}")
        print("-" * 40)
        print(f"🔹 VADER Accuracy:   {vader_accuracy:.2f}%")
        print(f"🔸 FinBERT Accuracy: {finbert_accuracy:.2f}%")
        print("="*40)
        
        
        results_df = pd.DataFrame(results)
        results_df.to_csv(OUTPUT_FILE, index=False)
        print(f"✅ Detailed results saved to: {OUTPUT_FILE}")
        
    else:
        print("No data processed.")

if __name__ == "__main__":
    
    run_benchmark()