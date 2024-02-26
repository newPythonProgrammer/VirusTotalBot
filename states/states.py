from aiogram.dispatcher.filters.state import State, StatesGroup

class FSM_ADMIN_SPAM(StatesGroup):
    text = State()
    btns = State()

class ADD_TOKEN(StatesGroup):
    token = State()

class DEL_TOKEN(StatesGroup):
    token = State()

class ADD_PROXY(StatesGroup):
    proxy = State()

class DEL_PROXY(StatesGroup):
    proxy_id = State()