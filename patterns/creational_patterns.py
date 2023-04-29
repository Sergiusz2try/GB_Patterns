from copy import deepcopy
from quopri import decodestring


class User:
    pass


class Teacher(User):
    pass


class Student(User):
    pass


class UserFactory:
    types = {
        "teacher": Teacher,
        "student": Student,
    }

    @classmethod
    def create(cls, type_):
        return cls.types[type_]()
    

class CoursesPrototype:

    def clone(self):
        return deepcopy(self)
    

class Course(CoursesPrototype):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)


class InteractiveCourse(Course):
    pass


class RecordCourse(Course):
    pass


class CoursesFactory:
    types = {
        "interactive": InteractiveCourse,
        "record": RecordCourse,
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)
    

class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result
    

class Engine:

    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.category = []

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)
    
    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)
    
    def find_category_by_id(self, id):
        for item in self.category:
            if item.id == id:
                return item
        raise Exception(f"No category by id: {id}")
    
    @staticmethod
    def create_course(type_, name, category):
        return CoursesFactory.create(type_, name, category)

    def get_course(self, name):
        for i in self.courses:
            if i.name == name:
                return i
        raise Exception(f"No course by name: {name}")
    
    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')
    

class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs["name"]

        if name in cls.__instance:
            return cls.__instance
        else:
            cls.__instance["name"] = super().__call__(*args, **kwargs)
            return cls.__instance["name"]
        

class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('log--->', text)
