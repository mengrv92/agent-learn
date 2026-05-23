import httpx

def get_weather(latitude, longitude):
    response = httpx.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true")
    data = response.json()
    return f"{data['current_weather']['temperature']}°C, 风速 {data['current_weather']['windspeed']} km/h"
  
  
def get_game_info(game_name):
    """Return information for a given sport.

    Supported games: 篮球, 排球, 足球, 橄榄球
    """
    games = [
        {
            "key": "篮球",
            "name": "篮球 (Basketball)",
            "description": "两队各五名球员在矩形场地上进行投篮得分的运动。",
            "team_size": 12,
            "players_on_field": 5,
        },
        {
            "key": "排球",
            "name": "排球 (Volleyball)",
            "description": "两队在网两侧通过击球使球落在对方场地以得分的运动。",
            "team_size": 12,
            "players_on_field": 6,
        },
        {
            "key": "足球",
            "name": "足球 (Soccer)",
            "description": "两队各十一名球员在草地上以脚踢球进球得分的运动。",
            "team_size": 23,
            "players_on_field": 11,
        },
        {
            "key": "橄榄球",
            "name": "橄榄球 (Rugby)",
            "description": "两队在椭圆形球场上通过持球冲刺、传球或踢球得分的运动。",
            "team_size": 23,
            "players_on_field": 15,
        },
    ]
    game_name_lower = game_name.lower()
    return next((game for game in games if game_name_lower in game["name"].lower()), None)




tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定经纬度的当前天气",
            "parameters": { 
                "type": "object",
                "properties": {
                    "latitude": { "type": "number"}, 
                    "longitude": { "type": "number" }
                },
                "required": ["latitude", "longitude"],
                "additional_properties": False, # 不允许额外的参数
            },
            "strict": True # 严格模式，参数必须完全匹配
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_game_info",
            "description": "获取指定运动的相关信息和人数规模",
            "parameters": { 
                "type": "object",
                "properties": {
                    "game_name": { "type": "string"}, 
                },
                "required": ["game_name"],
                "additional_properties": False, # 不允许额外的参数
            },
            "strict": True # 严格模式，参数必须完全匹配
        }
    }   
]