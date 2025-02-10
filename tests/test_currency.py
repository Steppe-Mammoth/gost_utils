import gost_utils



def test_currency_format():
    data = [
        {
            "params": {
                "value": 1500.5,
                "decimal_places": 2,
                "separator": " ",
                "decimal_point": ".", 
            },
            "response": "1 500.50"
        },
        {
            "params": {
                "value": 15000000.5,
                "decimal_places": 2,
                "separator": " ",
                "decimal_point": ".", 
            },
            "response": "15 000 000.50"
        },
        {
            "params": {
                "value": 10.5,
                "decimal_places": 5,
                "separator": " ",
                "decimal_point": ".", 
            },
            "response": "10.50000"
        },

    ]

    for i in data:
        params = i["params"] 
        result = gost_utils.currency.format(**params)
        print("result: ", result)
        assert result == i["response"] 


