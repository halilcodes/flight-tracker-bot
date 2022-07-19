import requests
import keys
import pprint
from datetime import datetime, timedelta


class FlightHandler:
    def __init__(self):
        self.base_endpoint = "http://tequila-api.kiwi.com/"
        self.search_url = "http://tequila-api.kiwi.com/v2/search"
        self.header = {"apikey": keys.tequila_api}

    def search_city(self, city):
        endpoint = f"{self.base_endpoint}/locations/query"
        params = dict()
        params['term'] = city
        params['location_types'] = "city"
        params['limit'] = 1

        response = requests.get(url=endpoint, params=params, headers=self.header)
        if response.status_code == 200:
            print("request is OK!")
        pprint.pprint(response.json())
        return response.json()

    def get_where_to_go(self, destination, sort="searches", limit=3):
        """
        :param destination: top areas to travel in where
        :param sort: searches (default) / bookings / clicks
        :param limit: number of results (default 5)
        :return:
        """
        endpoint = f"{self.base_endpoint}/locations/topdestinations"
        params = dict()
        params['limit'] = limit
        params['term'] = destination
        if sort in ["searches", "bookings", "clicks"]:
            params['source_popularity'] = sort

        response = requests.get(url=endpoint, params=params, headers=self.header)
        if response.status_code == 200:
            print("request is OK!")
        pprint.pprint(response.json())
        return response.json()

    def get_tophashtags(self, location, sort="searches", limit=3):
        endpoint = f"{self.base_endpoint}/locations/locations/tophashtags"
        params = dict()
        params['limit'] = limit
        params['term'] = location
        if sort in ["searches", "bookings", "clicks"]:
            params['source_popularity'] = sort

        response = requests.get(url=endpoint, params=params, headers=self.header)
        if response.status_code == 200:
            print("request is OK!")
        pprint.pprint(response.json())
        return response.json()

    def search_flight_eur(self, first_date=15, last_date=45, min_stay=2, max_stay=4, num=3, direct_flight=True):
        start_search = (datetime.today() + timedelta(days=first_date)).strftime("%d/%m/%Y")
        end_search = (datetime.today() + timedelta(days=last_date)).strftime("%d/%m/%Y")
        endpoint = f"{self.base_endpoint}/search"
        params = dict()
        params['fly_from'] = "ESB"
        params['fly_to'] = "europe"
        params['date_from'] = start_search
        params['date_to'] = end_search
        params['nights_in_dst_from'] = min_stay
        params['nights_in_dst_to'] = max_stay
        params['one_for_city'] = 1
        params['adults'] = 2
        params['curr'] = "TRY"
        params['conn_on_diff_airport'] = 0
        params['ret_from_diff_airport'] = 0
        params['ret_to_diff_airport'] = 0
        if direct_flight:
            params['max_stopovers'] = 0
        else:
            params['max_stopovers'] = 1
        params['limit'] = num

        response = requests.get(url=endpoint, params=params, headers=self.header)
        if response.status_code == 200:
            print("request is OK!")
        pprint.pprint(response.json())
        return response.json()


if __name__ == '__main__':
    flight = FlightHandler()
    # flight.search_city("amsterdam")
    # flight.get_where_to_go("ankara_tr")
    # flight.get_tophashtags("berlin")
    flight.search_flight_eur(direct_flight=False)


