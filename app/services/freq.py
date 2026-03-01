from wordfreq import zipf_frequency

def get_frequency_score(text):
    if not text:
        return "0"
    
    # Use the text directly without splitting into words
    freq = zipf_frequency(text.lower(), "en")
    return str(round(freq, 2))