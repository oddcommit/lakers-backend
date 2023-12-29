class DCity:
    def __init__(
        self,
        id: int,  # pylint: disable=redefined-builtin
        name: str,
        city_code: str,
        pref_code: str,
    ):
        self._id = id
        self._name = name
        self._city_code = city_code
        self._pref_code = pref_code

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def city_code(self):
        return self._city_code

    @property
    def pref_code(self):
        return self._pref_code
