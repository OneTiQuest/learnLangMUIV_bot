# Локальное состояние пользователей бота
state = {}

def set_state(key, value):
    if key not in state:
        state[key] = {}

    state[key] = value

def get_state(key):
    return state.get(key)
