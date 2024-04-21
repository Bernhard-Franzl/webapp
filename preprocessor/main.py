from preprocessor import Preprocessor

room_to_id ={"HS18":0, "HS19":1}
door_to_id = {"door1":0, "door2":1}

data_path = "/home/franzl/github_repos/webapp/data"
worker = Preprocessor(data_path, room_to_id, door_to_id)

listy_dirs = worker.get_list_of_data_dirs()

data = worker.accumulate_raw_data(listy_dirs)

cleaned_data = worker.clean_raw_data(data)

worker.calc_people_in_out(cleaned_data)


# Look into clean data once again       