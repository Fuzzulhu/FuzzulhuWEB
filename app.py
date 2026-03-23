from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception:
        return "<h1>FuzzulhuWEB - Servidor Flask Activo</h1><p>Configurando entorno para la integración con Supabase.</p>"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
