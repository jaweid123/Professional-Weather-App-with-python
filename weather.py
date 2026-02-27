import customtkinter as ctk
import requests

# تنظیم ظاهر
ctk.set_appearance_mode("dark")  # dark / light
ctk.set_default_color_theme("blue")

# -------------------------
# توابع دریافت اطلاعات
# -------------------------

def get_coordinates(city_name):
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1"
    response = requests.get(geo_url)
    data = response.json()
    if "results" not in data:
        return None
    result = data["results"][0]
    return result["latitude"], result["longitude"], result["name"], result["country"]

def get_weather(lat, lon):
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&current_weather=true"
    )
    response = requests.get(weather_url)
    data = response.json()
    return data["current_weather"]

def describe_temperature(temp):
    if temp < 0:
        return "❄ Very Cold"
    elif temp < 10:
        return "Cold"
    elif temp < 20:
        return "Cool"
    elif temp < 30:
        return "Warm"
    else:
        return "🔥 Hot"

# -------------------------
# جستجو
# -------------------------

def search_weather():
    city = city_entry.get()
    if not city:
        result_label.configure(text="Please enter a city name")
        return
    
    location = get_coordinates(city)
    if location is None:
        result_label.configure(text="City not found")
        return
    
    lat, lon, city_name, country = location
    weather = get_weather(lat, lon)

    temp = weather["temperature"]
    wind = weather["windspeed"]
    direction = weather["winddirection"]
    description = describe_temperature(temp)

    result_label.configure(
        text=f"{city_name}, {country}\n\n"
             f"🌡 {temp} °C\n"
             f"💨 Wind: {wind} km/h\n"
             f"🧭 Direction: {direction}°\n\n"
             f"{description}"
    )

# -------------------------
# طراحی UI حرفه‌ای
# -------------------------

app = ctk.CTk()
app.geometry("500x500")
app.title("Professional Weather App")

# کارت اصلی
main_frame = ctk.CTkFrame(app, corner_radius=20)
main_frame.pack(pady=40, padx=40, fill="both", expand=True)

title = ctk.CTkLabel(
    main_frame,
    text="🌍 Global Weather",
    font=ctk.CTkFont(size=28, weight="bold")
)
title.pack(pady=20)

city_entry = ctk.CTkEntry(
    main_frame,
    placeholder_text="Enter city name...",
    width=300,
    height=40,
    corner_radius=15
)
city_entry.pack(pady=15)

search_button = ctk.CTkButton(
    main_frame,
    text="Search",
    width=200,
    height=40,
    corner_radius=15,
    command=search_weather
)
search_button.pack(pady=10)

result_label = ctk.CTkLabel(
    main_frame,
    text="",
    font=ctk.CTkFont(size=18),
    justify="center"
)
result_label.pack(pady=30)

app.mainloop()