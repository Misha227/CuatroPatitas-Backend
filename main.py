from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Pet, PetType, FoodType
from groq import Groq
import os

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": "*", 
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Add OPTIONS method
        "allow_headers": ["Content-Type"],
        "supports_credentials": False
    }
})

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://cuatro_patitas_postgres_user:B4rN7PjzpSzTCyW3Tqpp8VQ3I3Zxzqhi@dpg-cssm7ijtq21c73a2loug-a.oregon-postgres.render.com/cuatro_patitas_postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

def validate_pet_data(data):
    required_fields = ['nombre', 'tipo', 'raza', 'peso', 'edad', 'tipoComida']

    for field in required_fields:
        if field not in data:
            return False, f"Campo requerido faltante: {field}"

    if data['tipo'] not in [t.value for t in PetType]:
        return False, "Tipo de mascota inválido"

    if data['tipoComida'] not in [t.value for t in FoodType]:
        return False, "Tipo de comida inválido"

    return True, None

@app.route('/api/mascotas', methods=['POST'])
def create_pet():
    try:
        data = request.get_json()

        is_valid, error_message = validate_pet_data(data)
        if not is_valid:
            return jsonify({'error': error_message}), 400

        new_pet = Pet(
            nombre=data['nombre'].strip(),
            tipo=data['tipo'],
            raza=data['raza'],
            peso=data['peso'],
            edad=data['edad'],
            tipo_comida=data['tipoComida']
        )

        db.session.add(new_pet)
        db.session.commit()

        return jsonify({
            'message': 'Mascota guardada exitosamente',
            'pet': new_pet.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/mascotas', methods=['GET'])
def get_pets():
    try:
        pets = Pet.query.all()
        return jsonify([pet.to_dict() for pet in pets]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mascotas/<int:pet_id>', methods=['GET'])
def get_pet(pet_id):
    try:
        pet = Pet.query.get_or_404(pet_id)
        return jsonify(pet.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/api/chat', methods=['POST'])
def get_chat_response():
    try:
        data = request.get_json()
        question = data['user_prompt']

        if not question:
            return jsonify({'error': 'Question is required'}), 400

        client = Groq(
            api_key="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",
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": question,
                }
            ],
            model="llama3-8b-8192",
            stream=False,
        )
        response = chat_completion.choices[0].message.content
        return jsonify({'response': response}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    port = int(os.environ.get('FLASK_RUN_PORT', 4000))
    app.run(host='0.0.0.0', port=port, debug=True)
