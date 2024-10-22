from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Pet, PetType, FoodType

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type"]
    }
})


# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

def validate_pet_data(data):
    required_fields = ['nombre', 'tipo', 'raza', 'peso', 'edad', 'tipoComida']
    
    # Check if all required fields are present
    for field in required_fields:
        if field not in data:
            return False, f"Campo requerido faltante: {field}"
    
    # Validate tipo (pet type)
    if data['tipo'] not in [t.value for t in PetType]:
        return False, "Tipo de mascota inválido"
    
    # Validate tipo_comida (food type)
    if data['tipoComida'] not in [t.value for t in FoodType]:
        return False, "Tipo de comida inválido"
    
    return True, None

@app.route('/api/mascotas', methods=['POST'])
def create_pet():
    try:
        data = request.get_json()
        
        # Validate incoming dataclear

        is_valid, error_message = validate_pet_data(data)
        if not is_valid:
            return jsonify({'error': error_message}), 400

        # Create new pet instance
        new_pet = Pet(
            nombre=data['nombre'].strip(),
            tipo=data['tipo'],
            raza=data['raza'],
            peso=data['peso'],
            edad=data['edad'],
            tipo_comida=data['tipoComida']
        )
        
        # Save to database
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

if __name__ == '__main__':
    app.run(debug=True)