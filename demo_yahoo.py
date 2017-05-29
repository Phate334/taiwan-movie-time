# -*- coding: utf-8 -*-

import os
import json

from movie import yahoo

if not os.path.isdir("output"):
    os.mkdir("output")

with open(os.path.join("output", "theater_meta.json"), "w", encoding="utf-8") as f:
    theaters = [t for t in yahoo.get_theaters()]
    f.write(json.dumps(theaters, ensure_ascii=False))

with open(os.path.join("output", "theater_time.json"), "w", encoding="utf-8")  as f:
    theater_time = []
    for theater in theaters:
        theater_time += yahoo.get_theater_time(theater["id"])
    f.write(json.dumps(theater_time, ensure_ascii=False))

