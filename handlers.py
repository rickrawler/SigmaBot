from datetime import date
from kb import *
from misc import bot, all_users
from misc import dp
from misc import registered_users
from states import ClientState, RegistrationSteps, DriversRegistrationSteps, \
    PassengerRegistrationSteps, EditProfileStates, CreatingRideStates
from text import *

from user import User, Driver, Passenger
from utils import DRIVER_EXPERIENCE_REGEXP

rides = {
}


@dp.message_handler(commands=["start"])
async def start(message, state):
    msg = "Выберите подходящий вариант"

    next_state = ClientState.CHOOSING_ACTION if check_if_registered(
        message.from_id) else ClientState.QUIZING

    await message.answer(msg, reply_markup=DRIVER_OR_PASSENGER_KEYBOARD)
    await state.set_state(next_state)


@dp.message_handler(
    lambda message: message.text == "Я водитель" or message.text == "Я "
                                                                    "пассажир",
    state=ClientState.QUIZING)
async def start_quiz(message, state):
    user_id = message.from_id
    role = message.text
    user = Driver(user_id) if role == "Я водитель" else Passenger(user_id)
    all_users[user_id] = user
    await message.answer(ARE_YOU_EMPLOYED_QUESTION,
                         reply_markup=YES_NO_KEYBOARD)
    await state.set_state(ClientState.REGISTERING)


@dp.message_handler(state=ClientState.CHOOSING_ACTION)
async def choose_action(message, state):
    user_id = message.from_id
    user = all_users[user_id]
    role = user.role

    msg = "Что вы хотите сделать?"
    markup = DRIVER_ACTIONS_KEYBOARD if role == "Я водитель" else PASSENGER_ACTIONS_KEYBOARD

    await message.answer(msg, reply_markup=markup)
    await state.set_state(ClientState.CHOOSED)


@dp.message_handler(state=ClientState.CHOOSED)
async def action_handler(message, state):
    action = message.text
    await FUNCTIONS_FOR_ACTIONS[action](message, state)


@dp.message_handler(state=ClientState.REGISTERING)
async def ask_name(message, state):
    if message.text == "Да" or message.text == "Имя":
        await message.answer(REGISTRATION_STARTED_MESSAGE,
                             reply_markup=HIDE_KEYBOARD)
        await message.answer(WHATS_YOUR_NAME_QUESTION)
        await state.set_state(RegistrationSteps.NAME)
    else:
        await message.answer(ARENT_EMPLOYED_MESSAGE,
                             reply_markup=HIDE_KEYBOARD)
        await state.set_state(ClientState.BANNED)


@dp.message_handler(lambda s: len(s.text) <= 20, state=RegistrationSteps.NAME)
async def ask_phone_number(message, state):
    user_id = message.from_id
    user = all_users[user_id]
    user.name = message.text
    role = user.role
    next_state = DriversRegistrationSteps.START_DRIVER_REGISTRATION if role \
                                                                       == "Я " \
                                                                          "водитель" else PassengerRegistrationSteps.START_PASSENGER_REGISTRATION

    await message.answer(WHATS_YOUR_PHONE_NUMBER_QUESTION)
    await state.set_state(next_state)


@dp.message_handler(lambda s: len(s.text) <= 12,
                    state=DriversRegistrationSteps.START_DRIVER_REGISTRATION)
async def start_driver_registration(message, state):
    user_id = message.from_id
    user = all_users[user_id]
    user.phone = message.text
    await message.answer(DRIVER_EXPERIENCE_QUESTION)
    await state.set_state(DriversRegistrationSteps.DRIVING_EXPERIENCE)


@dp.message_handler(regexp=DRIVER_EXPERIENCE_REGEXP,
                    state=DriversRegistrationSteps.DRIVING_EXPERIENCE)
async def check_driver_experience(message, state):
    experience = message.text
    if int(experience.split()[0]) < 1:
        msg = LESS_THAN_ONE_YEAR_EXPERIENCE_WARNING
        markup = LITTLE_EXPERIENCE_WARNING_KEYBOARD

        next_state = DriversRegistrationSteps.EXPERIENCE_LESS_THAN_ONE_YEAR
    else:
        msg = WHICH_STATIONS_WILL_BE_PASSED_QUESTION
        markup = None
        next_state = DriversRegistrationSteps.PASSING_METRO_STATIONS
    await message.answer(msg, reply_markup=markup)
    await state.set_state(next_state)


@dp.message_handler(state=DriversRegistrationSteps
                    .EXPERIENCE_LESS_THAN_ONE_YEAR)
async def process_young_driver(message, state):
    user_id = message.from_id
    user = all_users[user_id]
    if message.text == BECAME_A_PASSENGER:
        user.role = "Я пассажир"
        new_user = Passenger(user_id)
        all_users[user_id] = new_user
        new_user.name = user.name
        new_user.phone = user.phone

        msg = WHERE_ARE_PASSENGER_LIVING_QUESTION
        next_state = PassengerRegistrationSteps.PASSENGER_METRO_STATION
    else:
        msg = WHICH_STATIONS_WILL_BE_PASSED_QUESTION
        next_state = DriversRegistrationSteps.PASSING_METRO_STATIONS
    await message.answer(msg, reply_markup=HIDE_KEYBOARD)
    await state.set_state(next_state)


@dp.message_handler(state=DriversRegistrationSteps.PASSING_METRO_STATIONS)
async def ask_how_many_slots(message, state):
    user_id = message.from_id
    user = all_users[user_id]
    user.passing_stations = message.text
    await message.answer(HOW_MANY_FREE_SLOTS_QUESTION)
    await state.set_state(RegistrationSteps.END_OF_REGISTRATION)


@dp.message_handler(lambda s: len(s.text) <= 40,
                    state=RegistrationSteps.END_OF_REGISTRATION)
async def end_registration(message, state):
    user_id = message.from_id
    user = all_users[user_id]
    role = user.role
    if role == "Я водитель":
        user.capacity = message.text
    else:
        user.benefits = message.text

    registered_users[user_id] = user

    print(user.info)
    print(user.role)

    markup = PASSENGER_ACTIONS_KEYBOARD if role == 'Я пассажир' else DRIVER_ACTIONS_KEYBOARD

    await message.answer(REGISTRARION_ENDED_MESSAGE, reply_markup=markup)
    await state.set_state(ClientState.CHOOSED)


@dp.message_handler(
    state=PassengerRegistrationSteps.START_PASSENGER_REGISTRATION)
async def ask_metro_station(message, state):
    user_id = message.from_id
    user = all_users.get(user_id)
    user.phone = message.text
    await message.answer(WHERE_ARE_PASSENGER_LIVING_QUESTION)
    await state.set_state(PassengerRegistrationSteps.PASSENGER_METRO_STATION)


@dp.message_handler(state=PassengerRegistrationSteps.PASSENGER_METRO_STATION)
async def ask_benefits(message, state):
    user_id = message.from_id
    user = all_users.get(user_id)
    user.metro_station = message.text

    await message.answer(HOW_WILL_BENEFIT_QUESTION)
    await state.set_state(RegistrationSteps.END_OF_REGISTRATION)


def check_if_registered(client_id):
    return client_id in registered_users


async def my_rides_handler(message, state):
    chat_id = message.from_id

    await bot.send_message(chat_id=chat_id, text="Что вы хотите сделать?",
                           reply_markup=MY_RIDES_KEYBOARD)
    await state.set_state(ClientState.WATCHED)


@dp.message_handler(state=ClientState.WATCHED)
async def action_chosen(message, state):
    action = message.text
    user_id = message.from_id
    if action == "Отмена" or action == "Вернуться в меню":
        await choose_action(registered_users[user_id].role,
                            state)


@dp.message_handler(state=ClientState.FINDING)
async def find_a_ride_handler(message, state):
    rides = get_rides()
    user_id = message.from_id
    if not rides:
        role = registered_users[user_id].role

        markup = PASSENGER_ACTIONS_KEYBOARD if role == 'Я пассажир' else DRIVER_ACTIONS_KEYBOARD

        await message.answer(NO_AVIABLE_RIDES_MESSAGE, reply_markup=markup)
        await state.set_state(ClientState.CHOOSED)
    else:
        pass

"""
@dp.message_handler(commands=["start"])#state=ClientState.CREATING)
async def create_a_ride_handler(message, state):
    user_id = message.from_id
    if user_id not in rides:
        rides[user_id] = []

    if message.text == "Начать заново" or message.text == "Отменить":
        rides[user_id] = []
        markup = CREATING_RIDE_QUESTIONS_KEYBOARDS.first()
        next_state = await state.get_state().group.first()
        msg = CREATING_RIDE_QUESTIONS[next_state]
    else:
        rides[user_id].append(message.text)

        next_state = await state.get_state(message.from_id).next()
        markup = CREATING_RIDE_QUESTIONS_KEYBOARDS[next_state]
        msg = CREATING_RIDE_QUESTIONS[next_state]
    await message.answer(msg, reply_markup=markup)
    await state.set_state(next_state)
"""


#@dp.message_handler(state=ClientState.EDITING)
async def edit_profile(message, state):
    user_id = message.from_id
    role = registered_users[user_id].role
    markup = EDIT_DRIVER_PROFILE_KEYBOARD if role == "Я водитель" else EDIT_PASSENGER_PROFILE_KEYBOARD
    await message.answer(WHICH_FIELD_TO_CHANGE, reply_markup=markup)
    await state.set_state(ClientState.CHOOSED_FIELD)


@dp.message_handler(state=ClientState.CHOOSED_FIELD)
async def edit_field(message, state):
    await state.set_state(FIELDS_STATES[message.text])
    if message.text != "Отмена":
        await message.answer(ENTER_NEW_VALUE_MESSAGE,
                             reply_markup=HIDE_KEYBOARD)
    else:
        await choose_action(message, state)


@dp.message_handler(state=EditProfileStates)
async def set_new_field(message, state):
    user_id = message.from_id
    user = registered_users[user_id]
    current_state = await state.get_state()
    print(user.info)
    if message.text != "Отмена":
        user.__setattr__(FIELDS_ATTRIBUTES[current_state], message.text)
    print(f"new {STATES_FIELDS[await state.get_state()]} is {message.text}")
    print(user.info)

    await message.answer(SUCCESSFULLY_CHANGED_MESSAGE)
    await state.set_state(ClientState.EDITING)
    await edit_profile(message, state)


def get_rides():
    return None


@dp.message_handler(state="*")
async def unknown_message(message):
    await message.reply("Неизвестная команда")


STATES_FOR_ACTIONS = {
    "Мои поездки": ClientState.WATCHING,
    "Найти поездку": ClientState.FINDING,
    "Создать поездку": ClientState.CREATING,
    "Редактировать профиль": ClientState.EDITING,
    "Отмена": ClientState.CHOOSING_ACTION,
    "Вернуться в меню": ClientState.CHOOSING_ACTION,

}

FUNCTIONS_FOR_ACTIONS = {
    "Мои поездки": my_rides_handler,
    "Найти поездку": find_a_ride_handler,
    #"Создать поездку": create_a_ride_handler,
    "Редактировать профиль": edit_profile,

}

FIELDS_STATES = {
    "Имя": EditProfileStates.NAME,
    "Контактный номер": EditProfileStates.PHONE,
    "Проезжаемые станции": EditProfileStates.STATIONS,
    "Стаж вождения": EditProfileStates.EXPERIENCE,
    "Возможная польза": EditProfileStates.BENEFIT,
    "Станция метро": EditProfileStates.STATION,
    "Отмена": ClientState.CHOOSING_ACTION,

}

STATES_FIELDS = {value.state: key for key, value in
                 FIELDS_STATES.items()}

FIELDS_ATTRIBUTES = {
    "EditProfileStates:NAME": 'name',
    "EditProfileStates:PHONE": 'phone',
    "EditProfileStates:STATIONS": 'passing_stations',
    "EditProfileStates:EXPERIENCE": 'driver_experience',
    "EditProfileStates:BENEFIT": 'benefits',
    "EditProfileStates:STATION": 'metro_station',

}



CREATING_RIDE_QUESTIONS_KEYBOARDS = {
    CreatingRideStates.DIRECTION: CHOOSE_RIDE_DIRECTION_KEYBOARD,
    CreatingRideStates.DATE: CHOOSE_RIDE_DATE_KEYBOARD,
    CreatingRideStates.COMMENT: ADD_RIDE_COMMENT_KEYBOARD,
    CreatingRideStates.CONFIRMING: CONFIRM_RIDE_KEYBOARD,

}

CREATING_RIDE_QUESTIONS = {
    CreatingRideStates.DIRECTION: CHOOSE_DIRECTION_MESSAGE,
    CreatingRideStates.DATE: CHOOSE_DATE_MESSAGE,
    CreatingRideStates.COMMENT: ADD_COMMENT_MESSAGE,
    CreatingRideStates.CONFIRMING: CONFIRM_DETAILS_MESSAGE,

}