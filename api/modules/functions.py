import random
import string
import datetime
def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def check_image_type(image):
    try:
        if not image.name.endswith(".png") and not image.name.endswith(".jpg"):
            return False
    except:
        return False
    return True

def check_timelines(schedules):
    for schedule in schedules:
        for another_timeline in schedule["timelines"]:
            for timeline in schedule["timelines"]:
                if timeline["id"] != another_timeline["id"]:
                    another_start_time = datetime.datetime.strptime(another_timeline["start_time"], "%H:%M")
                    another_end_time = datetime.datetime.strptime(another_timeline["end_time"], "%H:%M")
                    start_time = datetime.datetime.strptime(timeline["start_time"], "%H:%M")
                    end_time = datetime.datetime.strptime(timeline["end_time"], "%H:%M")
                    if another_start_time < start_time and another_end_time > start_time or another_start_time < end_time and another_end_time > end_time or another_end_time == end_time or another_start_time == start_time or another_end_time <= another_start_time or end_time <= start_time or another_start_time > start_time and another_end_time < end_time:
                        return False
    return True