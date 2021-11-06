import datetime

import datetime as dt

from server.school.user_type import UserType


class User:
    @staticmethod
    def create(json):
        print(json)
        if json['type'] == UserType.PARENT:
            return Parent(json['name'], json['children'], json['times'])
        if json['type'] == UserType.TEACHER:
            return Teacher(json['name'], json['children'])
        if json['type'] == UserType.ADMINISTRATOR:
            return Administrator(json['name'], json['children'], json['times'])
        else:
            raise ValueError('Неизвестный тип пользователя')

    def is_parent(self):
        return isinstance(self, Parent)

    def is_teacher(self):
        return isinstance(self, Teacher)

    def is_administrator(self):
        return isinstance(self, Administrator)

    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name


class Parent(User):
    def __init__(self, name, children, times):
        super().__init__(name)
        self.children = children
        self.times = self.make_times(times)

    @staticmethod
    def str_to_datetime(str_time):
        return datetime.datetime.strptime(str_time, "%H:%M")

    def make_times(self, tm):
        date_begin = self.str_to_datetime(tm['from'])
        date_end = self.str_to_datetime(tm['to'])
        return [(date_begin + dt.timedelta(minutes=i)).strftime("%H:%M") for i in
                range(0, int((date_end - date_begin).total_seconds() / 60) + 1, tm["step"])]

    def get_children(self):
        return self.children

    def get_child_by_id(self, child_id):
        return list(filter(lambda child: child['id'] == child_id, self.children))[0]

    def get_future_times(self, minutes_offset=0):
        def filter_time(tim):
            h, m = tim.split(':')
            time_real = dt.time(int(h), int(m))
            return time_real > (dt.datetime.now() + dt.timedelta(minutes=minutes_offset)).time()

        return list(filter(filter_time, self.times))


class Teacher(User):
    def __init__(self, name, children):
        super().__init__(name)
        self.children = children

    def get_children(self):
        return self.children


class Administrator(Parent):
    def get_grades(self):
        return sorted(list(set([c['grade'] for c in self.children])))
