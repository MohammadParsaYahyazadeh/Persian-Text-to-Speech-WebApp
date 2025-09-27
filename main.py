from gtts import gTTS

def main():
    text = """سلام! این یک تست تبدیل متن به گفتار فارسی است.
    امیدوارم پروژه شما موفق باشه."""
    
    # تولید صدا
    tts = gTTS(text=text, lang="fa", tld="com")
    tts.save("output.mp3")
    print("✅ فایل صوتی ساخته شد: output.mp3")

if __name__ == "__main__":
    main()
