import datetime

import datetime as dt


class User:
    @staticmethod
    def create(json):
        if json['type'] == 'parent':
            return Parent(json['name'], json['children'], json['times'])
        if json['type'] == 'teacher':
            return Teacher(json['name'])
        else:
            raise ValueError('Неизвестный тип пользователя')

    def is_parent(self):
        return isinstance(self, Parent)

    def is_teacher(self):
        return isinstance(self, Teacher)

    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name


class Parent(User):
    def __init__(self, name, children, times):
        super().__init__(name)
        self.children = children
        self.times = self.make_times(times)

    def make_times(self, tm):
        date_begin = datetime.datetime.strptime(tm["from"], "%H:%M")
        date_end = datetime.datetime.strptime(tm["to"], "%H:%M")
        return [(date_begin + dt.timedelta(minutes=i)).strftime("%H:%M") for i in
             range(0, int((date_end - date_begin).total_seconds() / 60) + 1, tm["step"])]


    def get_children(self):
        return self.children

    def get_times(self):
        return self.times


class Teacher(User):
    pass
