from gtts import gTTS

sample_texts = [
    "Hello, my name is John and I will go to the market tomorrow.",
    "This is a reminder to finish your assignment by Friday.",
    "Please call me when you arrive at the airport.",
    "Don't forget to schedule the meeting for next week.",
    "I have sent the documents to your email.",
    "Today is a great day to start something new.",
    "The weather is sunny, let's go for a walk.",
    "Can you help me with my project please?",
    "Remember to water the plants in the backyard.",
    "The train will leave at six in the evening."
]

for idx, text in enumerate(sample_texts, 1):
    tts = gTTS(text=text, lang='en')
    filename = f"sample_note_{idx}.mp3"
    tts.save(filename)
    print(f"Saved {filename}")
