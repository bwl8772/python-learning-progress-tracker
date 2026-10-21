import re

COURSES = ('Python', 'DSA', 'Databases', 'Flask')


def valid_name(name):
    return len(name) >= 2 and re.fullmatch(r"[A-Za-z]+(?:[-'][A-Za-z]+)*", name) is not None


class Tracker:
    def __init__(self):
        self.students = {}
        self.emails = set()

    def add_students(self):
        print("Enter student credentials or 'back' to return:")
        count = 0
        while True:
            line = input().strip()
            if line.lower() == 'back':
                print(f'Total {count} students have been added.')
                return
            parts = line.split()
            if len(parts) < 3:
                print('Incorrect credentials.')
                continue
            first, last, email = parts[0], ' '.join(parts[1:-1]), parts[-1]
            if not valid_name(first):
                print('Incorrect first name.')
            elif len(last) < 2 or not all(re.fullmatch(r"[A-Za-z]+(?:[-'][A-Za-z]+)*", part) for part in last.split()):
                print('Incorrect last name.')
            elif re.fullmatch(r'[^@\s]+@[^@\s]+\.[^@\s]+', email) is None:
                print('Incorrect email.')
            elif email in self.emails:
                print('This email is already taken.')
            else:
                student_id = str(10000 + len(self.students))
                self.students[student_id] = {'name': first + ' ' + last, 'email': email, 'points': [0] * 4, 'tasks': [0] * 4, 'notified': set()}
                self.emails.add(email)
                count += 1
                print('The student has been added.')

    def list_students(self):
        if not self.students:
            print('No students found.')
        else:
            print('Students:')
            print('\n'.join(self.students))

    def add_points(self):
        print("Enter an id and points or 'back' to return:")
        while True:
            line = input().strip()
            if line.lower() == 'back':
                return
            parts = line.split()
            if len(parts) != 5 or any(re.fullmatch(r'[0-9]+', p) is None for p in parts[1:]):
                print('Incorrect points format.')
                continue
            student_id = parts[0]
            if student_id not in self.students:
                print(f'No student is found for id={student_id}.')
                continue
            student = self.students[student_id]
            for i, value in enumerate(map(int, parts[1:])):
                student['points'][i] += value
                if value:
                    student['tasks'][i] += 1
            print('Points updated.')

    def find(self):
        print("Enter an id or 'back' to return:")
        while True:
            student_id = input().strip()
            if student_id.lower() == 'back':
                return
            if student_id not in self.students:
                print(f'No student is found for id={student_id}.')
            else:
                values = self.students[student_id]['points']
                print(student_id + ' points: ' + '; '.join(f'{course}={points}' for course, points in zip(COURSES, values)))

    def statistics(self):
        print("Type the name of a course to see details or 'back' to quit:")
        enrolled = [sum(s['points'][i] > 0 for s in self.students.values()) for i in range(4)]
        tasks = [sum(s['tasks'][i] for s in self.students.values()) for i in range(4)]
        totals = [sum(s['points'][i] for s in self.students.values()) for i in range(4)]
        averages = [totals[i] / tasks[i] if tasks[i] else None for i in range(4)]
        for high_label, low_label, values in (
            ('Most popular', 'Least popular', enrolled),
            ('Highest activity', 'Lowest activity', tasks),
            ('Easiest course', 'Hardest course', averages),
        ):
            available = [v for v in values if v is not None]
            if not available or not any(available):
                high, low = [], []
            else:
                maximum, minimum = max(available), min(available)
                high = [i for i, v in enumerate(values) if v == maximum]
                low = [i for i, v in enumerate(values) if v == minimum and i not in high]
            print(high_label + ': ' + (', '.join(COURSES[i] for i in high) or 'n/a'))
            print(low_label + ': ' + (', '.join(COURSES[i] for i in low) or 'n/a'))
        while True:
            course = input().strip().lower()
            if course == 'back':
                return
            if course not in [c.lower() for c in COURSES]:
                print('Unknown course.')
                continue
            i = [c.lower() for c in COURSES].index(course)
            print(COURSES[i])
            print('id points completed')
            learners = [(student_id, s['points'][i]) for student_id, s in self.students.items() if s['points'][i] > 0]
            for student_id, points in sorted(learners, key=lambda item: (-item[1], int(item[0]))):
                percent = round(points / (600, 400, 480, 550)[i] * 100, 1)
                print(f'{student_id} {points} {percent:.1f}%')

    def notify(self):
        count = 0
        for student in self.students.values():
            sent = False
            for i, target in enumerate((600, 400, 480, 550)):
                if student['points'][i] >= target and i not in student['notified']:
                    print(f"To: {student['email']}")
                    print('Re: Your Learning Progress')
                    print(f"Hello, {student['name']}! You have accomplished our {COURSES[i]} course!")
                    student['notified'].add(i)
                    sent = True
            count += sent
        print(f'Total {count} students have been notified.')

    def run(self):
        print('Learning Progress Tracker')
        actions = {'add students': self.add_students, 'list': self.list_students, 'add points': self.add_points, 'find': self.find, 'statistics': self.statistics, 'notify': self.notify}
        while True:
            try:
                command = input().strip().lower()
            except EOFError:
                return
            if command == 'exit':
                print('Bye!')
                return
            elif command in actions:
                actions[command]()
            elif command == 'back':
                print("Enter 'exit' to exit the program.")
            elif not command:
                print('No input.')
            else:
                print('Unknown command!')


if __name__ == '__main__':
    Tracker().run()
