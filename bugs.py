from typing import List
import json

def unique_tags(payload: dict)->List[str]:
    # исправьте ошибку    
    tags = payload.get('tags', [])    
    for i,t in enumerate(tags):
        if isinstance(t, (bool, float)):  
            tags[i] = str(t)    
  
    result = list(set(tags))
    return result


js_str = '''{
    "title": "Звездные войны 1: Империя приносит баги",
    "description": "Эпичная сага по поиску багов в старом легаси проекте Империи",
"tags": [2, "семейное кино", "космос", 1.0, "сага", "эпик", "добро против зла", true, "челмедведосвин", "debug", "ipdb", "PyCharm", "бо#евик", "боевик", "эникей", "дарт багус", 5, 6,4, "блокбастер", "кино 2020", 7, 3, 9, 12, "каникулы в космосе", "коварство"],
"version": 17
}'''

js_str = json.loads(js_str)
print(unique_tags(js_str))



