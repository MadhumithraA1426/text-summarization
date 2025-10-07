from flask import Flask, render_template, request
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Download punkt and stopwords each time app starts (fixes deploy errors)
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

def summarize_text(text):
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text)
    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        freqTable[word] = freqTable.get(word, 0) + 1

    sentences = sent_tokenize(text)
    sentenceValue = dict()
    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                sentenceValue[sentence] = sentenceValue.get(sentence, 0) + freq

    sumValues = sum(sentenceValue.values())
    if len(sentenceValue) == 0:
        return ""
    average = int(sumValues / len(sentenceValue))
    summary = ''
    for sentence in sentences:
        if sentence in sentenceValue and sentenceValue[sentence] > (1.2 * average):
            summary += " " + sentence
    return summary.strip()

@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    text = ""
    if request.method == "POST":
        text = request.form.get("text")
        if text:
            summary = summarize_text(text)
    return render_template("index.html", summary=summary, original=text)

if __name__ == "__main__":
    app.run(debug=True)
