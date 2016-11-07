import utils


def prompt(message='', selection_range=range(0, 10), instance=int):
    message += ' >>> '
    while True:
        selection = raw_input('\n' + message)
        try:
            selection = instance(selection)
        except ValueError:
            print 'select', instance
            continue
        if selection not in selection_range:
            print 'wrong range'
            continue
        return selection


def show_menu():
    print 'Menu'
    print '9.', 'create sample diary (progress will be lost)'
    print
    print '1.', 'show diary'
    print
    print '2.', 'add course'
    print '3.', 'add student'
    print
    print '4.', 'add student grade'
    print '5.', 'add student attendance'
    print
    print '6.', 'check student total average'
    print '7.', 'check student course total average'
    print '8.', 'check student attendances'
    print
    print '0.', 'Exit'
    return prompt()


def pretty_list_print(l):
    for index in range(len(l)):
        print str(index) + '.', l[index]


def select_student(diary):
    length = len(diary.students)
    student_index = prompt('student index (1, ' + str(length) + ') >>>', range(1, length + 1))
    return diary.students[student_index - 1]


def select_course(diary):
    length = len(diary.courses)
    index = prompt('course index (1, ' + str(length) + ') >>>', range(1, length + 1))
    return diary.courses[index - 1]


def main():
    file_name = 'serialization.json'
    # diary = utils.sample_diary_factory()
    diary = utils.Diary()
    diary.load(file_name)
    while True:
        selection = show_menu()
        if selection == 0:
            break
        elif selection == 1:
            utils.pretty_print(diary)
        elif selection == 2:
            pass
        elif selection == 3:
            pass
        elif selection == 4:
            student = select_student(diary)
            course = select_course(diary)
            score = prompt('select grade (2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0)', (2., 2.5, 3., 3.5, 4., 4.5, 5.), float)
            diary.add_score(student, course, score)
        elif selection == 5:
            student = select_student(diary)
            course = select_course(diary)
            attendance = prompt('(0 - absence, 1 - presence)', range(0, 2))
            attendance = True if attendance == 1 else False
            diary.add_attendance(student, course, attendance)
        elif selection == 6:
            student = select_student(diary)
            utils.pretty_print(student)
            print diary.get_total_average(student)
        elif selection == 7:
            student = select_student(diary)
            course = select_course(diary)
            utils.pretty_print(student)
            print course + ': ', diary.get_course_average(student, course)
        elif selection == 8:
            student = select_student(diary)
            attendance = diary.get_total_attendance(student)
            utils.pretty_print(student)
            print 'attendance (total, absences, presences): ' + str(attendance)
        elif selection == 9:
            diary = utils.sample_diary_factory()
        else:
            continue
        raw_input("press enter")
    diary.save(file_name)


if __name__ == '__main__':
    main()

