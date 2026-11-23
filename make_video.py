# ============ 1. KAHANI - AUTO MODEL ============
def get_new_story():
    import google.generativeai as genai
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise Exception("no key")
    genai.configure(api_key=api_key)

    # Pehle check kar kaunse model chalu hai
    available = []
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available.append(m.name)
        print("Chalu Models:", available)
    except Exception as e:
        print("List fail:", e)

    # Try kar ek-ek karke - jo pehla chalega wahi use hoga
    to_try = [
        'gemini-2.0-flash',
        'gemini-2.5-flash',
        'gemini-3-flash-preview',
        'gemini-1.5-flash',
        'gemini-pro',
    ]
    # Jo list me hai usko pehle rakho
    for a in available:
        if a.replace('models/', '') not in to_try:
            to_try.insert(0, a.replace('models/', ''))

    import random, datetime
    topics = ["Samosa", "Bhootiya School", "Cricket Match", "Jadui Cycle", "Chor Bazaar", "Mela", "Robot", "Jungle", "Barish", "Exam", "Golgappa", "Diwali", "Train", "Kite"]
    topic = random.choice(topics)
    prompt = f"""Guddu aur Bholu ki funny Hindi kahani likho. Topic: {topic}.
    Sirf is format me do:
    TITLE: Guddu Bholu Ka {topic} Wala Kamaal
    STORY: 150 word ki funny kahani. 6 chhote scene me. Guddu hoshiyar, Bholu bhola. End me - subscribe karo."""

    last_err = None
    for model_name in to_try:
        try:
            print(f"Trying model: {model_name}")
            model = genai.GenerativeModel(model_name)
            res = model.generate_content(prompt)
            print(f"CHAL GAYA: {model_name}")
            return res.text
        except Exception as e:
            print(f"Fail {model_name}: {e}")
            last_err = e
            continue
    raise Exception(f"Saare model fail: {last_err}")
