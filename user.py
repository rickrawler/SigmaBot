class User:
    def __init__(self, user_id):
        self.name = None
        self.phone = None
        self._id = user_id
        self._nickname = None
        self.role = None

    @property
    def id(self):
        return self._id

    @property
    def nickname(self):
        return self._nickname

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        self._phone = value

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        self._role = value


class Driver(User):
    def __init__(self, user_id):
        super().__init__(user_id)
        self.driver_experience = None
        self.role = "Я водитель"
        self.capacity = None
        self.passing_stations = None

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        self._role = value

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        self._capacity = value

    @property
    def passing_stations(self):
        return self._passing_stations

    @passing_stations.setter
    def passing_stations(self, value):
        self._passing_stations = value

    @property
    def info(self):
        return [self.id, self.name, self.phone, self.nickname,
                self.capacity]


class Passenger(User):
    def __init__(self, user_id):
        super().__init__(user_id)
        self.role = "Я пассажир"
        self.metro_station = None
        self.benefits = None

    @property
    def metro_station(self):
        return self._metro_station

    @metro_station.setter
    def metro_station(self, value):
        self._metro_station = value

    @property
    def benefits(self):
        return self._benefits

    @benefits.setter
    def benefits(self, value):
        self._benefits = value

    @property
    def info(self):
        return [self.id, self.name, self.phone, self.nickname,
                self.benefits]

