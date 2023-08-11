import openai
import pyttsx3
import speech_recognition as sr
import time

#open ai key
openai.api_key="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"

#init text-to-speech engine with a specific voice
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) # for example, use the second voice in the list


def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print("Skipping unknown error")

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        temperature=0.5,
        stop = None,
        n=1,
    )
    return response["choices"][0]["text"]

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        #wait for user to say "easy"
        print("Say EZ to start asking EZ question...")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "easy":
                    while True:
                        # record audio
                        filename = "input.wav"
                        print("say bye to finish recording and goodbye to exit EZ")
                        print("Recording...")
                        with sr.Microphone() as source:
                            recognizer = sr.Recognizer()
                            source.pause_threshold = 1
                            audio = recognizer.listen(source,phrase_time_limit=None,timeout=None)
                            with open(filename, 'wb') as f:
                                f.write(audio.get_wav_data())
                        # transcribe audio to text
                        text = transcribe_audio_to_text(filename)
                        if text:
                            print(f"you said: {text}")
                            # check if user wants to end the conversation
                            if "goodbye" in text.lower():
                                speak_text("Goodbye!")
                                return
                            elif "bye" in text.lower():
                                speak_text("Bye bye!")
                                break
                            # generate response
                            response = generate_response(text)
                            print(response)
                            # read response using speech to text
                            speak_text(response)
                else:
                    print(f"Sorry, I didn't get that. Please try again. you said: {transcription}")
            except Exception as e:
                print("An error occured: {}".format(e))

if __name__ == "__main__":
    main()
