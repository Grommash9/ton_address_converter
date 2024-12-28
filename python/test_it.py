from ton_address_converter import batch_convert_to_friendly, batch_convert_to_raw


def test_raw_address_converting():

    raw_address = "0:73f17af370bd9d1f754be87a8a2d46f178aa72a9fc26f8ed9305977313f5dd29"

    test_cases = [
        {"bounceable": True, "test_only": True, "url_safe": True, "result": "kQBz8XrzcL2dH3VL6HqKLUbxeKpyqfwm-O2TBZdzE_XdKY5W"},   # kQB...
        {"bounceable": True, "test_only": False, "url_safe": True, "result": "EQBz8XrzcL2dH3VL6HqKLUbxeKpyqfwm-O2TBZdzE_XdKTXc"},   # kQB...
        {"bounceable": False, "test_only": True, "url_safe": True, "result": "0QBz8XrzcL2dH3VL6HqKLUbxeKpyqfwm-O2TBZdzE_XdKdOT"},   # kQB...
        {"bounceable": False, "test_only": False, "url_safe": True, "result": "UQBz8XrzcL2dH3VL6HqKLUbxeKpyqfwm-O2TBZdzE_XdKWgZ"},   # kQB...
        {"bounceable": True, "test_only": True, "url_safe": False, "result": "kQBz8XrzcL2dH3VL6HqKLUbxeKpyqfwm+O2TBZdzE/XdKY5W"},   # kQB...
        {"bounceable": True, "test_only": False, "url_safe": False, "result": "EQBz8XrzcL2dH3VL6HqKLUbxeKpyqfwm+O2TBZdzE/XdKTXc"},   # kQB...
        {"bounceable": False, "test_only": True, "url_safe": False, "result": "0QBz8XrzcL2dH3VL6HqKLUbxeKpyqfwm+O2TBZdzE/XdKdOT"},   # kQB...
        {"bounceable": False, "test_only": False, "url_safe": False, "result": "UQBz8XrzcL2dH3VL6HqKLUbxeKpyqfwm+O2TBZdzE/XdKWgZ"},   # kQB...
    ]

    print("Testing all combinations:")
    for case in test_cases:
        result = batch_convert_to_friendly([raw_address], bounceable=case["bounceable"], 
                                        test_only=case["test_only"], url_safe=case["url_safe"])[0]
        print(f"\nResult: {result}")
        print(f"Parameters: bounceable={case['bounceable']}, test_only={case['test_only']}, url_safe={case['url_safe']}")
        assert result == case["result"]

def test_friendly_address_to_raw():

    test_cases = [
        {"raw": "0:73f17af370bd9d1f754be87a8a2d46f178aa72a9fc26f8ed9305977313f5dd29",
        "friendly": "kQBz8XrzcL2dH3VL6HqKLUbxeKpyqfwm-O2TBZdzE_XdKY5W"},
        {"raw": "0:73f17af370bd9d1f754be87a8a2d46f178aa72a9fc26f8ed9305977313f5dd29",
        "friendly": "EQBz8XrzcL2dH3VL6HqKLUbxeKpyqfwm-O2TBZdzE_XdKTXc"},
        {"raw": "0:73f17af370bd9d1f754be87a8a2d46f178aa72a9fc26f8ed9305977313f5dd29",
        "friendly": "0QBz8XrzcL2dH3VL6HqKLUbxeKpyqfwm-O2TBZdzE_XdKdOT"},
        {"raw": "0:73f17af370bd9d1f754be87a8a2d46f178aa72a9fc26f8ed9305977313f5dd29",
        "friendly": "UQBz8XrzcL2dH3VL6HqKLUbxeKpyqfwm-O2TBZdzE_XdKWgZ"},
        {"raw": "0:73f17af370bd9d1f754be87a8a2d46f178aa72a9fc26f8ed9305977313f5dd29",
        "friendly": "kQBz8XrzcL2dH3VL6HqKLUbxeKpyqfwm+O2TBZdzE/XdKY5W"},
        {"raw": "0:73f17af370bd9d1f754be87a8a2d46f178aa72a9fc26f8ed9305977313f5dd29",
        "friendly": "EQBz8XrzcL2dH3VL6HqKLUbxeKpyqfwm+O2TBZdzE/XdKTXc"},
        {"raw": "0:73f17af370bd9d1f754be87a8a2d46f178aa72a9fc26f8ed9305977313f5dd29",
        "friendly": "0QBz8XrzcL2dH3VL6HqKLUbxeKpyqfwm+O2TBZdzE/XdKdOT"},
        {"raw": "0:73f17af370bd9d1f754be87a8a2d46f178aa72a9fc26f8ed9305977313f5dd29",
        "friendly": "UQBz8XrzcL2dH3VL6HqKLUbxeKpyqfwm+O2TBZdzE/XdKWgZ"},
    ]

    print("Testing all combinations:")
    for case in test_cases:
        result = batch_convert_to_raw([case["friendly"]])[0]
        print(f"\nRaw: {result}")
        assert result == case["raw"]