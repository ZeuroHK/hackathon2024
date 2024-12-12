from flask import Flask, request, jsonify, render_template
import requests
import markdown  # Import the markdown package

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_with_ai():
    data = request.json
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    url = "http://localhost:1234/v1/chat/completions"
    payload = {
        "model": "jpacifico/Chocolatine-3B-Instruct-DPO-Revised-Q4_K_M-GGUF",
        "messages": [{"role": "user", "content": user_message}],
        "max_tokens": 10000
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            ai_reply = response.json().get("choices", [])[0].get("message", {}).get("content", "").strip()
            
            # Convert AI reply to Markdown
            ai_reply_markdown = markdown.markdown(ai_reply)
            
            return jsonify({"response": ai_reply_markdown})
        else:
            return jsonify({"error": response.text}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500 

if __name__ == '__main__':
    app.run(debug=True)
