from flask import Flask, render_template, flash, url_for, request, redirect

tests = [
   {'id': 0, 'data': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
    'answer': 3117,
    },
   {'id': 1, 'data': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565,
    },
    {'id': 2, 'data': {'lesson': [1594702800, 1594706400],
              'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513,
                        1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009,
                        1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773,
                        1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503,
                        1594706524, 1594706524, 1594706579, 1594706641],
              'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
     'answer': 3577,
     },
]

DEBUG = True
SECRET_KEY = 'very secret key'

app = Flask(__name__)
app.config.from_object(__name__)


def datavalid(ind, time):
    if ind == len(time) - 1:
        return True
    if time[ind] > time[ind + 1]:
        return False
    return True


def calculate(time1, time2):
    presence = []
    for index in range(0, len(time1), 2):
        for ind in range(0, len(time2), 2):
            if not datavalid(index + 1, time1) or not datavalid(ind + 1, time2):
                raise ValueError('Incorrect data in the test')
            else:
                if time1[index] <= time2[ind] and time2[ind + 1] <= time1[index + 1]:
                    presence.extend([time2[ind], time2[ind + 1]])
                elif time1[index] <= time2[ind] <= time1[index + 1]:
                    presence.extend([time2[ind], time1[index + 1]])
                elif time1[index] <= time2[ind + 1] <= time1[index + 1]:
                    presence.extend([time1[index], time2[ind + 1]])
                elif time2[ind] <= time1[index] and time1[index + 1] <= time2[ind + 1]:
                    presence.extend([time1[index], time1[index + 1]])
    return presence


def appearance(intervals):
    generous_presence = calculate(intervals['tutor'], intervals['pupil'])
    lesson_presence = calculate(generous_presence, intervals['lesson'])
    answer = 0
    for index in range(0, len(lesson_presence), 2):
        answer += lesson_presence[index + 1] - lesson_presence[index]
    return answer


@app.route('/', methods=['POST', 'GET'])
def main():
    return render_template('index.html', tests=tests, title='Список уроков')


@app.route('/lesson/<int:id>')
def lesson(id):
    try:
        test_answer = appearance(tests[id]['data'])
        print(f"Время общего присутствия ученика и учителя на уроке: {test_answer}")
        assert test_answer == tests[id]['answer'], f'Error on test case {id}, got {test_answer}, expected {tests[id]["answer"]}'
    except ValueError as e:
        test_answer = 'Некорректные данные'
        print(f"{e} number {id}")
    return render_template('lesson.html', id=id, time=test_answer, title=f'Урок#{id}')


if __name__ == '__main__':
    app.run()
