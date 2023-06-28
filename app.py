from flask import Flask, request, jsonify
import joblib
from keybert import KeyBERT
import smtplib
import webbrowser


app = Flask(__name__)
model = joblib.load('models/finalized_model.sav')


@app.route('/')
def hello_world():
    return 'Summarization service'

@app.route('/keybert/', methods=['POST'])
def keyBert():
    kw_model = joblib.load('models/kw_model.sav')
    data = request.form
    text = data['text']
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', use_maxsum=True,
                                         nr_candidates=20, top_n=20)
    print("keywords --> \n", keywords)
    max= -float('inf')
    max_keyword = None
    for name, prob in keywords:
        if isinstance(prob, float) and prob > max:
            max = prob
            max_keyword = name

    response = {'result:': max_keyword}
    return jsonify(response)


@app.route('/sendemail', methods= ['POST'])
def send_email():
    data = request.form
    recipient = data['recipient_email']
    subject = data['subject']
    message = data['message']

    try:
        # Open default email client with pre-populated email
        mailto_link = f"mailto:{recipient}?subject={subject}&body={message}"
        webbrowser.open(mailto_link)
        response = {'result:': 'You can now send your email'}
        print("Email sent successfully!")
        return jsonify(response)

    except Exception as e:
        response = {'result:': 'An error occurred while sending the email'}

        print("An error occurred while sending the email:", str(e))
        return jsonify(response)



@app.route('/summarize/ratio', methods=['POST'])
def sum_ratio():
    print("ratio")
    data = request.form
    ratio = data['ratio']
    text = data['text']
    sum_result = model(text, ratio=float(ratio))
    response = {'result:': sum_result}
    return jsonify(response)


@app.route('/summarize/number', methods=['POST'])
def sum_number():
    print("number")
    data = request.form
    number = data['number']
    text = data['text']
    sum_result = model(text, num_sentences=int(number))
    response = {'result:': sum_result}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=1313, host='0.0.0.0', threaded=True)
