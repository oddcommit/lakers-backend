import urllib
from dataclasses import dataclass

import requests
from pandarallel import pandarallel
from pandas import DataFrame
from requests import JSONDecodeError
from requests.exceptions import ConnectionError as RequestsConnectionError

pandarallel.initialize(progress_bar=True)


@dataclass(frozen=True)
class KokudoChiriinAPIAccessor(object):
    retry_max: int = 3

    def fetch_lat_lon(
        self, location: str, retry_num: int = 0
    ) -> dict[str, float | str]:
        api_url = "https://msearch.gsi.go.jp/address-search/AddressSearch?q="
        s_quote = urllib.parse.quote(location)
        response = requests.get(api_url + s_quote, timeout=None)

        try:
            result = response.json()[0]
            params = result["geometry"]["coordinates"] + [result["properties"]["title"]]
            return {"代表点経度": params[0], "代表点緯度": params[1], "所在": location}
        except IndexError:
            print(f"error location: {location} {IndexError}")
            return {"所在": location}
        except JSONDecodeError:
            print(f"error location: {location} {JSONDecodeError}, retry_num{retry_num}")
            if retry_num < self.retry_max:
                print(f"location: {location} retry to get lan_lon")
                return self.fetch_lat_lon(location, retry_num + 1)
            print(f"error location: {location} has failed get lat_lon")
            return {"所在": location}

    def fetch_address(self, lon: str, lat: str, retry_num: int = 0) -> dict[str, str]:
        lon_quote = urllib.parse.quote(lon)
        lat_quote = urllib.parse.quote(lat)
        try:
            response = requests.get(
                f"https://mreversegeocoder.gsi.go.jp/reverse-geocoder/LonLatToAddress?lat={lat_quote}&lon={lon_quote}",
                timeout=None,
            )
            if response.json() != {}:
                return response.json()["results"]
        except RequestsConnectionError:
            if retry_num < self.retry_max:
                print(
                    f"{RequestsConnectionError} lon:{lon}, lat:{lat}, retry num:{retry_num}"
                )
                return self.fetch_address(lon, lat, retry_num + 1)
            print(f"{RequestsConnectionError} lon:{lon}, lat:{lat}, retry max")
            return {"muniCd": "99999", "lv01Nm": "不明"}
        print(f"not found lon:{lon}, lat:{lat}")
        return {"muniCd": "99999", "lv01Nm": "不明"}


def build_location_df(df: DataFrame) -> DataFrame:
    api_accessor = KokudoChiriinAPIAccessor()
    params = df.所在.parallel_apply(api_accessor.fetch_lat_lon)
    return DataFrame(params.to_list())
