
from typing import Iterable, Literal, NamedTuple


class ValueResult(NamedTuple):
    value: any
    is_default: bool
    last_dict: dict|None = None  # Останньо знайдений словник
    processed_keys: list|None = None   # Перелік успішно опрацьованих key


def get_value(data: dict, key: str|list, default: any = None, last_dict: bool = False, processed_keys: bool = False, return_type: Literal["dict", "NamedTuple"] = "dict") -> ValueResult:
    
    """
    Шукає вкладений об'єкт в data по заданому шляху (key), 
    Якщо знайде поверне його
    Якщо не знайде поверне result.value == None

    :param data: Словник по якому буде йти пошук
    :param key: Шлях до потрібного об'єкта, який слід повернути. Якщо це один рівень вкладеності можно передати str, якщо один або більше - list
    :param default: Значення яке буде повернене в result.value якщо об'єкт по заданому key не був знайдений
    :param last_dict: (optional) Якщо True поверне останній опрацьований об'єкт. Самий останній в разі успіху, або той об'єкт на рівні якого пошук пошук зупинився, в разі неуспіху
    :param processed_keys: (optional) Якщо True поверне масив опрацьованих об'єктів. В разі успіху з key=["x1", "x2"] processed_keys буде такий ["x1", "x2"] адже він опрацював всі вкладені об'єкт. Якщо буде bad case то масив буде менший, там будуть зазначені лише ті ключі на які успішно перейшов пошук
    Приклад:  
    in: get_value(data={"x1": {"x2": None}}, key=["x1", "x2", "x3"], last_dict=True, processed_keys=True)
    out: {"value": None, "is_default": true, "last_dict": {"x2": None}, processed_keys: ["x1"]}
    """
    if processed_keys:
        processed_keys_data = []  # Перелік успішно опрацьованих key
    else:
        processed_keys_data = None

    last_dict_data = None

    def added_processed_key(key):
        if processed_keys:
            processed_keys_data.append(key)
            return True
        else:
            return False
    
    def added_last_dict(data):
        nonlocal last_dict_data
        if last_dict and isinstance(data, dict):
            last_dict_data = data
            return True
        else:
            return False
    

    # print("INITIAL: ", data, key)
    # Приймаємо тільки словник
    if isinstance(data, dict):
        added_last_dict(data)

        # Якщо key == str && key in data
        if type(key) is str and key in data:
            value = data[key]
            added_processed_key(key)    # Додаємо ключ як опрацьований

        # Якщо key == list && key[0] in data
        elif isinstance(key, list) and key[0] in data:
            value_result = ValueResult(data, is_default=False)

            for k in key:
                value_result = get_value(data=value_result.value, key=k, return_type="NamedTuple")

                if value_result.is_default: # Якщо рекурсія повернула default - виходимо з циклу (неуспішно)
                    break
                else:   # Успішно
                    added_processed_key(k)     # Додаємо ключ як опрацьований
                    added_last_dict(value_result.value) # Записаємо last_dict якщо результат це словник
            
            # Успішно. Знайшли правильне значення
            if not value_result.is_default:
                value = value_result.value


    if 'value' in locals():
        is_default=False
    else:
        value = default
        is_default=True
    
    result = ValueResult(value=value, is_default=is_default, last_dict=last_dict_data, processed_keys=processed_keys_data)
    if return_type == "dict":
        return result._asdict()
    else:
        return result

