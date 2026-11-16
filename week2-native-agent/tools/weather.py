"""天气查询工具。

职责：根据城市查询天气，返回结构化的天气信息。
"""

def get_weather(city: str):
    """模拟天气查询工具"""

    weather_data = {
        "东京": {
            "weather": "rainy",
            "temperature": 18
        },
        "北京": {
            "weather": "sunny",
            "temperature": 25
        }
    }

    if city not in weather_data:
        return {"error": f"暂不支持查询城市：{city}"}

    return {
        "city": city,
        "notice": "模拟天气数据，不代表实时天气",
        **weather_data[city]
    }