from geopy.geocoders import Nominatim

def get_lat_long(city_name):
    geolocator = Nominatim(user_agent="meu_app_de_geolocalizacao")
    location = geolocator.geocode(city_name)
    
    if location:
        return (location.latitude, location.longitude)
    else:
        return "Cidade não encontrada!"

# Exemplo de uso:
city = "Vitória"
latitude, longitude = get_lat_long(city)
print(f"Latitude: {latitude}, Longitude: {longitude}")
