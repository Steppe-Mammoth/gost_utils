def format(value, decimal_places=2, separator=" ", decimal_point="."):
    """
    Конвертує float у формат грошової суми.

    :param value: Число (float), яке потрібно відформатувати.
    :param decimal_places: Кількість знаків після коми.
    :param separator: Роздільник тисяч (наприклад, , або пробіл).
    :param decimal_point: Символ десяткової крапки (., ,).
    :return: Відформатований рядок.
    """
    try:
        formatted_value = f"{value:,.{decimal_places}f}"
        if separator != ",":
            formatted_value = formatted_value.replace(",", separator)
        if decimal_point != ".":
            formatted_value = formatted_value.replace(".", decimal_point)
        return formatted_value
    except Exception as e:
        return f"Помилка форматування: {e}"