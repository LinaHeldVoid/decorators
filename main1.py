import json
import os
from datetime import datetime


def logger(path):
    path = path
    log_count = 1

    def __logger(old_function):
        final = []
        a = []

        def new_function(*args, **kwargs):
            if args is not None:
                a.append(args)
            if kwargs is not None:
                a.append(kwargs)

            result = old_function(*args, **kwargs)

            date = f'Время вызова функции: {datetime.now()}'
            name = f'Название функции: {old_function.__name__}'
            params = f'Аргументы функции: {a}'
            value = f'Значение функции: {result}'
            final.append(date)
            final.append(name)
            final.append(params)
            final.append(value)

            nonlocal path
            with open(path, 'a', encoding='utf-8') as f:
                json.dump(final, f, ensure_ascii=False)

            return result
        return new_function
    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(paths[0])
        def hello_world():
            return 'Hello World'

        @logger(paths[1])
        def summator(a, b=0):
            return a + b

        @logger(paths[2])
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()
