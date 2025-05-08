import requests
import datetime

def get_predictions():
    headers = {
        "X-RapidAPI-Key": "33a9b48d6fmsh163314ef6d9f9bcp1636f0jsnfd42903275f2",
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    today = datetime.datetime.now().strftime('%Y-%m-%d')
    fixtures_url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    params = {"date": today}
    fixtures_response = requests.get(fixtures_url, headers=headers, params=params)
    fixtures = fixtures_response.json().get("response", [])

    def confidence(odd):
        if odd < 1.3:
            return 90
        elif odd < 1.4:
            return 80
        elif odd < 1.5:
            return 70
        else:
            return 0

    predictions = {
        "very_high": [],
        "high": [],
        "medium": []
    }

    for match in fixtures:
        try:
            fixture_id = match["fixture"]["id"]
            home = match["teams"]["home"]["name"]
            away = match["teams"]["away"]["name"]

            odds_url = "https://api-football-v1.p.rapidapi.com/v3/odds"
            odds_params = {
                "fixture": fixture_id,
                "bookmaker": "6"
            }
            odds_response = requests.get(odds_url, headers=headers, params=odds_params)
            odds_data = odds_response.json().get("response", [])

            if not odds_data:
                continue

            odds_values = odds_data[0]["bookmakers"][0]["bets"][0]["values"]
            odds_dict = {item["value"]: float(item["odd"]) for item in odds_values}

            if "Home" in odds_dict:
                conf = confidence(odds_dict["Home"])
                if conf >= 70:
                    predictions[
                        "very_high" if conf == 90 else "high" if conf == 80 else "medium"
                    ].append({
                        "match": f"{home} vs {away}",
                        "prediction": f"{home} to WIN",
                        "confidence": f"{conf}%",
                        "odds": str(odds_dict["Home"])
                    })

            elif "Away" in odds_dict:
                conf = confidence(odds_dict["Away"])
                if conf >= 70:
                    predictions[
                        "very_high" if conf == 90 else "high" if conf == 80 else "medium"
                    ].append({
                        "match": f"{home} vs {away}",
                        "prediction": f"{away} to WIN",
                        "confidence": f"{conf}%",
                        "odds": str(odds_dict["Away"])
                    })
        except Exception:
            continue

    return {
        "status": "success",
        "date": today,
        "counts": {
            "very_high": len(predictions["very_high"]),
            "high": len(predictions["high"]),
            "medium": len(predictions["medium"])
        },
        "predictions": predictions
    }