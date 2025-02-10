
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


def set_value(data: dict|list, key: str|list|None, value: any, method: Literal["set", "push", "pushOne", "...push"], createKeys=True) -> any:
    import copy
    import json

    """
    :param data - об'єкт який буде модифікуватись
    :param key - шлях до потрібного ключа в об'єкта, значеня якого буде змінено. якщо кінечний ключ вкладений в інші то передавати шлях до нього в масиві (наприклад key=["key1", "key2", "key3"])
    :param value - значення для переданого ключа, це значення буде вставлено до ключа 
    :param method - метод, який задає інстуркцію як вставляти значення до цього ключа
    :param createKeys - якщо true то будуть створенні нові об'єкти, якщо в <object> немає якогось поля заданого в <key> 
    """

    new_data = copy.deepcopy(data)

    # Робота з масивом
    if isinstance(new_data, list):
        match method:
            case "set":
                new_data = value

            case "push":
                new_data.append(value)

            case "pushOne":
                # Додаємо значення тільки якщо його немає в списку
                if value not in data:
                    new_data.append(value)

            case "...push":
                if isinstance(value, Iterable):
                    new_data.extend(value)
                else:
                    raise ValueError
    

    elif isinstance(new_data, dict):
        if isinstance(key, str):
            keys = [key]
        elif isinstance(key, Iterable):
            keys = key
        else:
            raise ValueError
        
        current = new_data

        for idx_k, k in enumerate(keys):
            ...
            # if k in current:
            #     # Останній key
            #     if idx_k == len(keys) -1:
            #         if isinstance(current[k], list):
            #             res = set_value(data=current[k], key=None,method=method, createKeys=createKeys)
            #             current[k] = res
            # else:
            #     current[k]

        