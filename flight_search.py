from datetime import datetime, timedelta
import requests
TEQUILA_API_KEY = "HMEaFEe42X82z5L_-M-4Hi91EptMk4Pm"


class FlightSearch:
    def get_location_iata_code(self, city_name):
        self.headers = {
            "apikey": TEQUILA_API_KEY
        }
        self.query = {
            "term" : city_name,
            "location_types": "city",
        }
        self.response = requests.get(url="https://tequila-api.kiwi.com/locations/query", params=self.query,
                                     headers=self.headers)
        self.response.raise_for_status()
        return self.response.json()["locations"][0]["code"]

    def get_trip_deals(self, flyFrom, flyTo, flight_type, adults, children):
        today = datetime.now()
        after_6_months = today + timedelta(days=365//2)
        self.headers = {
            "apikey": TEQUILA_API_KEY
        }
        self.details = {
            "fly_from": flyFrom,
            "fly_to": flyTo,
            "dateFrom": today.date().strftime("%d/%m/%Y"),
            "dateTo": after_6_months.date().strftime("%d/%m/%Y"),
            "flight_type": flight_type,
            "curr": "INR",
            "adults": adults,
            "children": children,
            "limit": "10",


        }
        results = [self.details]
        self.response = requests.get(url="https://tequila-api.kiwi.com/v2/search", params=self.details, headers=self.headers)


        for data in self.response.json()["data"]:
            result = {}
            result["price"] = data["price"]
            result["airlines"] = f"{data['airlines'][0]}-{data['route'][0]['flight_no']}"
            date = data["route"][0]["local_departure"].split("T")[0]
            time = ":".join(data["route"][0]["local_departure"].split("T")[1].split(".")[0].split(":")[:2])
            result["departure"] =  f"{date} {time}"
            date = data["local_arrival"].split("T")[0]
            time = ":".join(data["local_arrival"].split("T")[1].split(".")[0].split(":")[:2])
            result["arrival"] = f"{date} {time}"
            result["link"] = data["deep_link"]
            results.append(result)

        return results