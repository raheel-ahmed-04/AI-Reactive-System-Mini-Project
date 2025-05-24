from pyswip import Prolog

def build_kb(prolog):
    prolog.assertz("temperature(hot) :- temperature_value(T), T > 28")
    prolog.assertz("temperature(mild) :- temperature_value(T), T >= 15, T =< 28")
    prolog.assertz("temperature(cold) :- temperature_value(T), T < 15")

    # Default definitions to prevent existence error
    prolog.assertz("storm_expected :- fail")
    prolog.assertz("rain_expected :- fail")

    prolog.assertz("humidity(humid) :- rain_expected")
    prolog.assertz("humidity(dry) :- \\+ rain_expected")

    prolog.assertz("wind(strong) :- storm_expected")
    prolog.assertz("wind(moderate) :- cloudy(high)")
    prolog.assertz("wind(light) :- cloudy(low)")

    prolog.assertz('weather_prediction(sunny, "Hot temp + dry + low cloud + light wind") :- temperature(hot), humidity(dry), cloudy(low), wind(light)')
    prolog.assertz('weather_prediction(rainy, "Humid + high cloud + mild temp") :- humidity(humid), cloudy(high), temperature(mild)')
    prolog.assertz('weather_prediction(stormy, "Stormy wind + humid") :- wind(strong), humidity(humid)')
    prolog.assertz('weather_prediction(snowy, "Cold + humid + high clouds") :- temperature(cold), humidity(humid), cloudy(high)')
    prolog.assertz('weather_prediction(cloudy_day, "Medium cloud + dry + mild temp") :- cloudy(medium), humidity(dry), temperature(mild)')

def get_user_input():
    print("\n🌦️  Weather Prediction System")
    temp = float(input("Enter current temperature in Celsius: "))
    rain = input("Is rain expected? (yes/no): ").strip().lower() == 'yes'
    storm = input("Is a storm expected? (yes/no): ").strip().lower() == 'yes'
    cloud = input("Cloud level? (low, medium, high): ").strip().lower()
    return temp, rain, storm, cloud

def predict_weather(temp_value, rain_expected, storm_expected, cloud_level):
    prolog = Prolog()
    build_kb(prolog)

    prolog.assertz(f"temperature_value({temp_value})")
    prolog.assertz(f"cloudy({cloud_level})")
    if rain_expected:
        prolog.assertz("rain_expected")
    if storm_expected:
        prolog.assertz("storm_expected")

    results = list(prolog.query("weather_prediction(W, Reason)"))
    if results:
        return results[0]["W"], results[0]["Reason"]
    else:
        return "unknown", "No matching rule"

# Main Execution
if __name__ == "__main__":
    temp, rain, storm, cloud = get_user_input()
    result, explanation = predict_weather(temp, rain, storm, cloud)
    print(f"\n🌤️  Predicted Weather: {result.upper()}")
    print(f"🧠  Reason: {explanation}")
