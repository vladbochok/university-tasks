"""Vladyslav Bochok"""
import sys
from typing import Tuple
from error import *


class Lesson:
    """
    Class that stores data on missed lessons.
    If the data when creating an instance does not meet the requirements - raise LoadError
    """

    def __init__(self, course: str, data: int, when: int, num: int, kind: str, aud: int):
        self.course = course
        self.data = data
        self.when = when
        self.num = num
        self.kind = kind
        self.aud = aud

    def __str__(self):
        """Representation in the form of a term used in the output."""
        return '\t' + '\t'.join([str(self.data), str(self.when), str(self.num)])

    @property
    def course(self) -> str:
        return self.__course

    @property
    def data(self) -> int:
        return self.__data

    @property
    def when(self) -> int:
        return self.__when

    @property
    def num(self) -> int:
        return self.__num

    @property
    def kind(self) -> str:
        return self.__kind

    @property
    def aud(self) -> int:
        return self.__aud

    @course.setter
    def course(self, course: str):
        if not isinstance(course, str) or len(course) < 1 or len(course) > 37:
            raise LoadError(f'{course} is incorrect value for the field course')
        self.__course = course

    @data.setter
    def data(self, data: int):
        try:
            if int(data) < 1 or int(data) > 15:
                raise ValueError
            self.__data = int(data)
        except BaseException:
            raise LoadError(f'{data} is incorrect value for the field data')

    @when.setter
    def when(self, when: int):
        try:
            if int(when) < 1 or int(when) > 5:
                raise ValueError
            self.__when = int(when)
        except BaseException:
            raise LoadError(f'{when} is incorrect value for the field when')

    @num.setter
    def num(self, num: int):
        try:
            if int(num) < 1 or int(num) > 4:
                raise ValueError
            self.__num = int(num)
        except BaseException:
            raise LoadError(f'{num} is incorrect value for the field num')

    @kind.setter
    def kind(self, kind: str):
        try:
            if kind not in ("Le", "P", "Sem", "lab"):
                raise ValueError
            self.__kind = kind
        except BaseException:
            raise LoadError(f'{kind} is incorrect value for the field kind')

    @aud.setter
    def aud(self, aud: int):
        try:
            if int(aud) < 1:
                raise ValueError
            self.__aud = int(aud)
        except BaseException:
            raise LoadError(f'{aud} is incorrect value for the field aud')


class Student:
    """
    A class that stores data about the student and all his passes lessons
    If the data when creating an instance does not meet the requirements - raise LoadError
    """

    def __init__(self, last_name: str, first_name: str, group: str, whom: int):
        self.last_name = last_name
        self.first_name = first_name
        self.group = group
        self.whom = whom

        self.lessons = list()
        self.number_missed_lessons = dict()

        self.index = 0

    def get_name(self) -> Tuple[str, str]:
        return self.last_name, self.first_name

    def add(self, lesson: Lesson):
        """Adds a specific lesson to the list of missed."""
        self.lessons.append(lesson)

    def __iter__(self):
        """Returns an iterator that passes through all missed lessons."""
        self.index = 0
        return self

    def __next__(self):
        try:
            item = self.lessons[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        return item

    def __len__(self) -> int:
        """Returns the number of missed lessons."""
        return len(self.lessons)

    def __str__(self):
        """Representation in the form of a term used in the output."""
        return "\t".join([self.last_name, self.first_name, str(len(self))])

    def sort(self):
        """Sorts missed lessons"""
        self.lessons.sort(key=lambda lesson: (lesson.data, lesson.when, lesson.num))

    @property
    def last_name(self) -> str:
        return self.__last_name

    @property
    def first_name(self) -> str:
        return self.__first_name

    @property
    def group(self) -> str:
        return self.__group

    @property
    def whom(self) -> int:
        return self.__whom

    @last_name.setter
    def last_name(self, last_name: str):
        if not isinstance(last_name, str) or len(last_name) < 1 or len(last_name) > 29:
            raise LoadError(f'{last_name} is incorrect value for the field last_name')
        self.__last_name = last_name

    @first_name.setter
    def first_name(self, first_name: str):
        if not isinstance(first_name, str) or len(first_name) < 1 or len(first_name) > 21:
            raise LoadError(f'{first_name} is incorrect value for the field first_name')
        self.__first_name = first_name

    @group.setter
    def group(self, group: str):
        if not isinstance(group, str) or len(group) < 1 or len(group) > 4:
            raise LoadError(f'{group} is incorrect value for the field group')
        self.__group = group

    @whom.setter
    def whom(self, whom: int):
        try:
            if int(whom) < 1 or int(whom) > 4:
                raise ValueError
            self.__whom = int(whom)
        except BaseException:
            raise LoadError(f'{whom} is incorrect value for the field whom')


class Information:
    """A class that stores information about all students and their missed lessons"""

    def __init__(self):
        self._students = dict()

        self._number_missed_4_lessons = 0
        self._number_missed_lectures = 0

        self._expected_number_missed_4_lessons = None
        self._expected_number_missed_lectures = None

        self._out_path = None
        self._encoding = None

    def set_stat(self, cnt_missed_4_lessons: int, cnt_missed_lectures: int):
        """Updates statistics for comparison with actual data."""
        self._expected_number_missed_4_lessons = cnt_missed_4_lessons
        self._expected_number_missed_lectures = cnt_missed_lectures

    def load(self, last_name: str, first_name: str, group: str, whom: int, course: str, data: int, when: int, num: int,
             kind: str, aud: int):
        """Downloads data about the student and his missed lesson."""
        if not self._contains(last_name, first_name):  # If this student is not yet in the container, add it
            student = Student(last_name, first_name, group, whom)
            self._students[last_name, first_name] = student

        lesson = Lesson(course, data, when, num, kind, aud)
        self._update_statistics(lesson)
        self._students[last_name, first_name].add(lesson)

    def fit(self):
        """Returns the correspondence between valid and expected statistics."""
        return self._number_missed_4_lessons == self._expected_number_missed_4_lessons \
               and self._number_missed_lectures == self._expected_number_missed_lectures

    def output(self, out_name, out_enc):
        """
        Inputs data into a file.
        In case of unsuccessful uploading - raise WriteError
        """
        if out_name == "stdout":
            try:
                self._output(sys.stdout)
            except BaseException:
                raise WriteError()
        else:
            try:
                stream = open(out_name, 'w', encoding=out_enc)
                self._output(stream)
                stream.close()
            except:
                stream.close()
                raise WriteError()

    def clear_data(self):
        """Deletes all user data."""
        self._students = dict()

    def clear_stat(self):
        """Clear all expected statistics data."""
        self._number_missed_4_lessons = 0
        self._number_missed_lectures = 0

    def _update_statistics(self, lesson):
        """updates current statistics data."""
        self._number_missed_4_lessons += lesson.num == 4
        self._number_missed_lectures += lesson.kind == "Le"

    def _output(self, stream):
        try:
            # get a sorted list of only those students who missed only 4th lesson students
            for student in self._get_sorted_list_of_students():
                print(student, file=stream)
                number_lesson_missed_in_one_day = 0
                # create a variable that stores the previously considered student
                previous_lesson = None
                for current_lesson in student:
                    if previous_lesson is None:  # check if took the first lesson from the list
                        previous_lesson = current_lesson
                    # If the date in the neighboring lessons coincides then increase temporary variable
                    if self._is_lessons_take_place_in_one_day(previous_lesson, current_lesson):
                        number_lesson_missed_in_one_day += 1
                    else:
                        print(previous_lesson, '\t', number_lesson_missed_in_one_day, file=stream)
                        number_lesson_missed_in_one_day = 1

                    previous_lesson = current_lesson  # remember lesson as the previous one
                print(previous_lesson, '\t', number_lesson_missed_in_one_day, file=stream)
        except BaseException:
            raise WriteError()

    @staticmethod
    def _is_lessons_take_place_in_one_day(lesson1: Lesson, lesson2: Lesson) -> bool:
        return lesson1.data == lesson2.data and lesson1.when == lesson2.when

    def _contains(self, last_name: str, first_name: str) -> bool:
        """Checks if information about the student with the given name is stored."""
        return (last_name, first_name) in self._students

    def _get_sorted_list_of_students(self):
        list_of_student = list()

        for student in self._students.values():
            if self._check_student_miss_only_4_lesson(student):  # checks if the student skipped lessons other than 4
                student.sort()  # sort lessons for this one by: week, day
                list_of_student.append(student)
        # sort students by keys:  number of passes, surname, name
        list_of_student.sort(key=lambda student: (len(student), student.last_name, student.first_name))

        return list_of_student

    @staticmethod
    def _check_student_miss_only_4_lesson(student):
        return all(lesson.num == 4 for lesson in student)
