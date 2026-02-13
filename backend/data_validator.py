import pandas as pd
import ast
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# دانلود دیکشنری لغات برای تحلیل احساسات (فقط بار اول اجرا می‌شود)
nltk.download('vader_lexicon', quiet=True)

def validate_dataset():
    print("--- Loading Dataset ---")
    try:
        # خواندن فایل CSV
        df = pd.read_csv('data/cryptonews.csv')
        print(f"Total rows loaded: {len(df)}")
    except FileNotFoundError:
        print("Error: File 'cryptonews.csv' not found in 'backend/data/' folder.")
        return

    # راه‌اندازی هوش مصنوعی (VADER)
    analyzer = SentimentIntensityAnalyzer()
    
    match_count = 0
    total_checked = 0
    
    print("\n--- Starting Validation (Checking first 100 rows) ---")
    
    # برای تست سرعت، فعلا فقط 100 تای اول را چک می‌کنیم
    for index, row in df.head(100).iterrows():
        text = str(row['title']) + " " + str(row['text'])
        
        # 1. استخراج برچسب اصلی از فایل (ستون sentiment)
        # فرمت دیتا در فایل: "{'class': 'negative', ...}"
        try:
            original_sentiment_dict = ast.literal_eval(row['sentiment'])
            original_label = original_sentiment_dict.get('class', 'neutral')
        except:
            original_label = 'neutral'
            
        # 2. تحلیل با هوش مصنوعی خودمان
        score = analyzer.polarity_scores(text)['compound']
        
        # تبدیل امتیاز عددی به برچسب متنی
        if score >= 0.05:
            my_label = 'positive'
        elif score <= -0.05:
            my_label = 'negative'
        else:
            my_label = 'neutral'
            
        # 3. مقایسه
        total_checked += 1
        if original_label == my_label:
            match_count += 1
            
        # چاپ نمونه برای ۵ تای اول
        if index < 5:
            print(f"News #{index}: Origin={original_label} | AI_Prediction={my_label} | Score={score}")

    # محاسبه دقت
    accuracy = (match_count / total_checked) * 100
    print("-" * 30)
    print(f"Validation Finished.")
    print(f"Accuracy match between Dataset and VADER AI: {accuracy:.2f}%")
    print("-" * 30)

if __name__ == "__main__":
    validate_dataset()