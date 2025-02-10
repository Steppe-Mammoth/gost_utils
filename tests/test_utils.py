import pytest

from gost_utils import utils


def test_get_value():
    data = [
        {
            "params": {
                "data": {
                    "x1": {
                        "x2": "Y"
                    }
                },
                "key": ["x1", "x2", "x3"],
                "last_dict": True,
                "processed_keys": True
            },
            "response": {
                "value": None,
                "is_default": True,
                "last_dict": {"x2": "Y"},
                "processed_keys": ['x1', 'x2']
            }
        },
        {
            "params": {
                "data": {
                    "x1": {
                        "x2": "Y"
                    }
                },
                "key": ["x1", "x2"],
                "last_dict": True,
                "processed_keys": True
            },
            "response": {
                "value": "Y",
                "is_default": False,
                "last_dict": {"x2": "Y"},
                "processed_keys": ['x1', 'x2']
            }
        },
        {
            "params": {
                "data": {
                    "x1": {
                        "x2": "O"
                    }
                },
                "key": ["x1", "x2"],
                "last_dict": False,
                "processed_keys": False
            },
            "response": {
                "value": "O",
                "is_default": False,
                "last_dict": None,
                "processed_keys": None
            }
        },

    ]

    for i in data:
        print("r")
        params = i["params"] 
        result = utils.get_value(**params)
        print(result)
        for res_k, res_v in i["response"].items():
            print(result[res_k], " == ", res_v )
            assert result[res_k] == res_v 
