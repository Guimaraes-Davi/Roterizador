from geopy.distance import great_circle
from geopy.geocoders import Nominatim
from flask import Flask, request, jsonify
from flask_cors import CORS
import time


app = Flask(__name__)
CORS(app)

def get_coordinates(city_name):
    geolocator = Nominatim(user_agent="MyGeocoderApp/v1.0 (http://127.0.0.1:5500/index.html)")
    try:
        # Adiciona o país para restringir a busca a cidades do Brasil
        location = geolocator.geocode(f"{city_name}, Brazil", timeout=10)
        time.sleep(1)  # Atraso de 1 segundo entre as requisições
        if location:
            return (location.latitude, location.longitude)
        else:
            return None
    except Exception as e:
        print(f"Error fetching coordinates for {city_name}: {e}")
        return None

def organize_route(origin, destinations):
    try:
        # Obter coordenadas da cidade de origem
        origin_coords = get_coordinates(origin)

        # Criar um dicionário para armazenar distâncias
        distances = {}

        # Calcular a distância entre a cidade de origem e cada cidade de destino
        for city in destinations:
            destination_coords = get_coordinates(city)
            if destination_coords:  # Verifica se as coordenadas foram encontradas
                distance = great_circle(origin_coords, destination_coords).kilometers
                distances[city] = distance

        # Organizar cidades por distância
        sorted_destinations = sorted(distances.items(), key=lambda x: x[1])

        return sorted_destinations

    except ValueError as e:
        return str(e)

@app.route('/get_route', methods=['GET'])
def get_route():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    intermediaries = request.args.get('intermediaries', '')

    # Montar a lista de cidades intermediárias
    destination_list = intermediaries.split(",") if intermediaries else []
    destination_list.append(destination)  # Adiciona a cidade de destino

    # Organiza a rota
    sorted_route = organize_route(origin, destination_list)
    
    return jsonify(sorted_route)

if __name__ == '__main__':
    app.run(debug=True)
