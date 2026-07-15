from flask import Flask, render_template, request, jsonify
from src.email_service import EmailService
from src.email_message import TextEmail

app = Flask(__name__)

emwork = EmailService()

@app.route('/')
def index() :
    return render_template('index.html')

@app.route('/send',methods=['POST']) 
def send() :
        to      = request.form.get('to')
        subject = request.form.get('subject')
        body    = request.form.get('body')
        cc_raw  = request.form.get('cc', '')

        cc = [addr.strip() for addr in cc_raw.split(',') if addr.strip()]

        message  = TextEmail(to, subject, body, cc=cc)
        resultat = emwork.send(message)

        if resultat:
            return jsonify({"success": True,  "message": "Email envoyé avec succès !"})
        else:
            return jsonify({"success": False, "message": "Échec de l'envoi."})

if	__name__	==	'__main__':
app.run(host='0.0.0.0',	port=5000,	debug=True)
