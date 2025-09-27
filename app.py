import streamlit as st
import asyncio
import edge_tts
import os

st.title("🎙️ تبدیل متن فارسی به گفتار (Persian TTS)")
st.write("متن فارسی را وارد کنید، یک صدا و لحن انتخاب کنید، و خروجی صوتی بگیرید.")

# متن ورودی
text = st.text_area(
    "متن ورودی",
    "سلام! این یک نمونه تستی برای تبدیل متن به گفتار فارسی است."
)

# انتخاب صدا (voices)
async def get_persian_voices():
    voices = await edge_tts.VoicesManager.create()
    fa_voices = [v["Name"] for v in voices.voices if "fa" in v["Locale"]]
    return fa_voices

voices = asyncio.run(get_persian_voices())
voice_choice = st.selectbox("انتخاب صدا", voices)

# انتخاب لحن
style = st.selectbox("انتخاب لحن", ["عادی", "سریع", "آرام"])

# دکمه تبدیل
if st.button("تبدیل به گفتار"):
    if text.strip() == "":
        st.warning("لطفاً یک متن وارد کنید.")
    else:
        output_path = "output.mp3"

        async def generate_tts(text, filename, voice):
            try:
                communicate = edge_tts.Communicate(text, voice)
                await communicate.save(filename)
            except Exception as e:
                st.error(f"خطا در تولید فایل صوتی: {e}")

        # تولید فایل صوتی اصلی
        asyncio.run(generate_tts(text, output_path, voice_choice))
        st.success("✅ فایل صوتی ساخته شد!")
        st.audio(output_path)

        # تغییر سرعت با ffmpeg
        if style == "سریع":
            os.system(f"ffmpeg -y -i {output_path} -filter:a 'atempo=1.3' output_fast.mp3")
            st.audio("output_fast.mp3")
        elif style == "آرام":
            os.system(f"ffmpeg -y -i {output_path} -filter:a 'atempo=0.7' output_slow.mp3")
            st.audio("output_slow.mp3")
