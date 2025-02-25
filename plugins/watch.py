import json
import urllib.request
import time

# Yahan apni API keys daalo
TELEGRAM_BOT_TOKEN = "7917351134:AAFz-wi0zC0PabOOPcWIydblZmkd51WYjWI"
TMDB_API_KEY = "2937f761448c84e103d3ea8699d5a33c"

# Telegram API URL
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/"

def get_trending_movies():
    """ TMDb API se trending movies fetch karta hai. """
    url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={TMDB_API_KEY}"
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            movies = data.get("results", [])[:10]  # Sirf top 10 movies lena
            return "\n".join([f"{i+1}. {movie['title']} ({movie.get('release_date', 'N/A')[:4]})" for i, movie in enumerate(movies)])
    except Exception as e:
        return f"Error fetching movies: {str(e)}"

def get_updates(offset=None):
    """ Telegram se naye messages fetch karta hai. """
    url = TELEGRAM_API_URL + "getUpdates?timeout=100"
    if offset:
        url += f"&offset={offset}"
    
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode())

def send_message(chat_id, text):
    """ Telegram pe message bhejta hai. """
    url = TELEGRAM_API_URL + f"sendMessage?chat_id={chat_id}&text={urllib.parse.quote(text)}"
    with urllib.request.urlopen(url) as response:
        return response.read()

def main():
    last_update_id = None
    
    while True:
        updates = get_updates(last_update_id)
        
        if "result" in updates and len(updates["result"]) > 0:
            for update in updates["result"]:
                last_update_id = update["update_id"] + 1  # Next update ke liye offset set karna
                message = update.get("message", {})
                chat_id = message.get("chat", {}).get("id")
                text = message.get("text", "").strip().lower()
                
                if text == "/watch":
                    movies = get_trending_movies()
                    send_message(chat_id, movies)
        
        time.sleep(2)  # Do second ka delay tak ki API spam na ho

if __name__ == "__main__":
    main()
