import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from pyswip import Prolog


def build_kb(prolog):
    prolog.assertz("temperature(hot) :- temperature_value(T), T > 28")
    prolog.assertz("temperature(mild) :- temperature_value(T), T >= 15, T =< 28")
    prolog.assertz("temperature(cold) :- temperature_value(T), T < 15")

    prolog.assertz("storm_expected :- fail")
    prolog.assertz("rain_expected :- fail")

    prolog.assertz("humidity(humid) :- rain_expected")
    prolog.assertz("humidity(dry) :- \\+ rain_expected")

    prolog.assertz("wind(strong) :- storm_expected")
    prolog.assertz("wind(moderate) :- cloudy(high); cloudy(medium)")
    prolog.assertz("wind(light) :- cloudy(low)")

    # Existing patterns
    prolog.assertz('weather_prediction(sunny, "Hot temp + dry + low cloud + light wind") :- temperature(hot), humidity(dry), cloudy(low), wind(light)')
    prolog.assertz('weather_prediction(rainy, "Humid + high cloud + mild temp") :- humidity(humid), cloudy(high), temperature(mild)')
    prolog.assertz('weather_prediction(stormy, "Stormy wind + humid") :- wind(strong), humidity(humid)')
    prolog.assertz('weather_prediction(snowy, "Cold + humid + high clouds") :- temperature(cold), humidity(humid), cloudy(high)')
    prolog.assertz('weather_prediction(cloudy_day, "Medium cloud + dry + mild temp") :- cloudy(medium), humidity(dry), temperature(mild)')

    # 🌥️ New medium cloud level-based rules
    prolog.assertz('weather_prediction(partly_cloudy_hot, "Hot and humid with medium clouds") :- temperature(hot), humidity(humid), cloudy(medium)')
    prolog.assertz('weather_prediction(partly_cloudy_mild, "Mild and dry with medium cloud cover") :- temperature(mild), humidity(dry), cloudy(medium)')
    prolog.assertz('weather_prediction(partly_cloudy_cold, "Cold with medium clouds and moderate wind") :- temperature(cold), cloudy(medium), wind(moderate)')
    prolog.assertz('weather_prediction(breezy_humid_medium, "Humid with moderate wind and medium clouds") :- humidity(humid), cloudy(medium), wind(moderate)')

    # Existing broad/fallback rules
    prolog.assertz('weather_prediction(partly_sunny, "Hot temperature + humid + low clouds = possible muggy but sunny conditions") :- temperature(hot), humidity(humid), cloudy(low)')
    prolog.assertz('weather_prediction(very_hot_dry, "Very hot and dry with low clouds suggests hot dry day") :- temperature(hot), humidity(dry), cloudy(low)')
    prolog.assertz('weather_prediction(chilly_clear_day, "Cold temperature + dry + low clouds + light wind") :- temperature(cold), humidity(dry), cloudy(low), wind(light)')

    # Fallback
    prolog.assertz('weather_prediction(unknown, "Conditions do not match any known pattern")')


def predict_weather(temp_value, rain_expected, storm_expected, cloud_level, wind_override):
    prolog = Prolog()
    build_kb(prolog)

    prolog.assertz(f"temperature_value({temp_value})")
    prolog.assertz(f"cloudy({cloud_level})")

    if rain_expected:
        prolog.assertz("rain_expected")
    if storm_expected:
        prolog.assertz("storm_expected")
    if wind_override != "auto":
        prolog.assertz(f"wind({wind_override})")

    results = list(prolog.query("weather_prediction(W, Reason)"))
    if results:
        return results[0]["W"], results[0]["Reason"]
    else:
        return "unknown", "No matching rule"


def load_icon(path, size=(24, 24)):
    return ImageTk.PhotoImage(Image.open(path).resize(size))


def show_prediction():
    try:
        temp = float(temp_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for temperature.")
        return

    rain = rain_var.get()
    storm = storm_var.get()
    cloud = cloud_var.get()
    wind = wind_var.get()

    if cloud == "":
        messagebox.showerror("Missing Selection", "Please choose a cloud level.")
        return

    weather, reason = predict_weather(temp, rain, storm, cloud, wind)
    result_var.set(f"Predicted Weather: {weather.upper()}")
    reason_var.set(f"Reason: {reason}")


# GUI Setup
root = tk.Tk()
root.title("🌤️ Weather Prediction System")
root.geometry("740x430")
root.resizable(False, False)

# Background
bg_img = Image.open("./bg.jpg")
bg_photo = ImageTk.PhotoImage(bg_img)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Title
title_label = tk.Label(root, text="Weather Prediction System", font=("Segoe UI", 16, "bold"), bg="#e6f1fb", fg="#003366")
title_label.place(x=45, y=55)

# Variables
rain_var = tk.BooleanVar()
storm_var = tk.BooleanVar()
cloud_var = tk.StringVar()
wind_var = tk.StringVar(value="auto")
result_var = tk.StringVar()
reason_var = tk.StringVar()

# Icons
icon_temp = load_icon("icons/temp.png")
icon_rain = load_icon("icons/rain.png")
icon_storm = load_icon("icons/storm.png")
icon_cloud = load_icon("icons/cloud.png")
icon_wind = load_icon("icons/wind.png")

# Frame
frame = tk.Frame(root, bg="#FFFFFF")
frame.place(x=350, y=70)

ttk.Label(frame, text="Enter Temperature (°C):", image=icon_temp, compound="left").grid(row=0, column=0, sticky="w")
temp_entry = ttk.Entry(frame, width=22)
temp_entry.grid(row=0, column=1, pady=5)

ttk.Label(frame, text="Rain Expected?", image=icon_rain, compound="left").grid(row=1, column=0, sticky="w")
ttk.Checkbutton(frame, variable=rain_var).grid(row=1, column=1, sticky="w")

ttk.Label(frame, text="Storm Expected?", image=icon_storm, compound="left").grid(row=2, column=0, sticky="w")
ttk.Checkbutton(frame, variable=storm_var).grid(row=2, column=1, sticky="w")

ttk.Label(frame, text="Cloud Level:", image=icon_cloud, compound="left").grid(row=3, column=0, sticky="w")
cloud_combo = ttk.Combobox(frame, textvariable=cloud_var, values=["low", "medium", "high"], state="readonly")
cloud_combo.grid(row=3, column=1, pady=5)

ttk.Label(frame, text="Wind:", image=icon_wind, compound="left").grid(row=4, column=0, sticky="w")
wind_combo = ttk.Combobox(frame, textvariable=wind_var, values=["auto", "light", "moderate", "strong"], state="readonly")
wind_combo.grid(row=4, column=1, pady=5)

ttk.Button(frame, text="Predict Weather", command=show_prediction).grid(row=5, columnspan=2, pady=10)

result_label = ttk.Label(frame, textvariable=result_var, font=("Segoe UI", 12, "bold"), wraplength=300, justify="center")
result_label.grid(row=6, columnspan=2, pady=(15, 5))

reason_label = ttk.Label(frame, textvariable=reason_var, font=("Segoe UI", 10), wraplength=300, justify="center")
reason_label.grid(row=7, columnspan=2)

root.mainloop()
