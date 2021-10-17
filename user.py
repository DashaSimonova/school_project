class User:
    @staticmethod
    def create(json):
        if json['type'] == 'parent':
            return Parent(json['name'], json['children'])
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
    def __init__(self, name, children):
        super().__init__(name)
        self.children = children

    def get_children(self):
        return self.children


class Teacher(User):
    pass
