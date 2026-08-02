import requests

def main():
    try:
        geo_response = requests.get('http://ip-api.com/json/', timeout=5)
        geo_data = geo_response.json()
        
        if geo_data.get('status') != 'success':
            return
            
        city = geo_data.get('city')
        country = geo_data.get('country')
        
    except requests.RequestException as e:
        return

    try:
        url = f"https://wttr.in/{city}?m&lang=en&format=%C,+temperature:%20%t%20(feels%20like%20%f),%20wind:%20%w"
        
        weather_response = requests.get(url, timeout=5)
        
        if weather_response.status_code == 200:
            return weather_response.text.strip()
        else:
            return
            
    except requests.RequestException as e:
        return

if __name__ == "__main__":
    print(main())