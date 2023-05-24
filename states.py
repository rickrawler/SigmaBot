from aiogram.dispatcher.filters.state import StatesGroup, State


class ClientState(StatesGroup):
    STARTED = State()
    REGISTERED = State()
    QUIZING = State()
    BANNED = State()
    REGISTERING = State()
    CHOOSING_ACTION = State()
    CHOOSED = State()
    CHOOSED_FIELD = State()
    EDITING = State()
    EDITED = State()
    CREATING = State()
    CREATED = State()
    FINDING = State()
    FOUND = State()
    WATCHING = State()
    WATCHED = State()


class RegistrationSteps(StatesGroup):
    NAME = State()
    PHONE_NUMBER = State()
    END_OF_REGISTRATION = State()


class DriversRegistrationSteps(StatesGroup):
    START_DRIVER_REGISTRATION = State()
    DRIVING_EXPERIENCE = State()
    EXPERIENCE_LESS_THAN_ONE_YEAR = State()
    PASSING_METRO_STATIONS = State()
    FREE_SLOTS_NUMBER = State()


class PassengerRegistrationSteps(StatesGroup):
    START_PASSENGER_REGISTRATION = State()
    PASSENGER_METRO_STATION = State()
    BENEFITS = State()


class EditProfileStates(StatesGroup):
    CHOOSED_FIELD = State()
    NAME = State()
    PHONE = State()
    EXPERIENCE = State()
    STATIONS = State()
    STATION = State()
    BENEFIT = State()
    CANCELLED = State()


class QuizSteps(StatesGroup):
    pass


class CreatingRideStates(StatesGroup):
    DIRECTION = State()
    DATE = State()
    COMMENT = State()
    CONFIRMING = State()
    CREATED = ClientState.CREATED
