# -*- coding: utf-8 -*-

import os
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

from movie import yahoo

if not os.path.isdir("output"):
    os.mkdir("output")

with open(os.path.join("output", "theater_meta.json"), "w", encoding="utf-8") as f:
    theaters = [t for t in yahoo.get_theaters()]
    f.write(json.dumps(theaters, ensure_ascii=False))

with open(os.path.join("output", "theater_time.json"), "w", encoding="utf-8")  as f:
    theater_time = []
    with ThreadPoolExecutor() as executor:
        theater_crawler = {executor.submit(yahoo.get_theater_time, t['id']): t for t in theaters}
        for future in as_completed(theater_crawler):
            try:
                theater_time += future.result()
            except Exception as e:
                print(e)
    f.write(json.dumps(theater_time, ensure_ascii=False))

