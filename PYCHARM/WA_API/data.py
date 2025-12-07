# Глобальные хранилища данных
users = {}
user_counter = 1

submissions = {}
counter_submissions = 1

sessions = {}  # token -> user_id

rounds = {}  # id -> {"id":1, "name":"Kolo 1", "rules":"", "start_date":"", "end_date":""}
round_counter = 1

tasks = {}  # id -> {"id":1, "round_id":1, "name":"Task 1", "description":""}

participants = {}  # round_id -> list of {"user_id":1, "status":"active"}

ratings = {}  # submission_id -> [{"points":x, "comment":"", "judge_id":1}]

results = {}  # round_id -> [{"user_id":1, "score":x, "rank":1}, ...]

reports = {}  # round_id -> file path / data

roles = ['soutezici', 'rozhodci', 'admin', 'poradatel']