import pytest
import re

valid_letters = []
regular_exp = r"^[А-я]{1}[0-9]{3}[А-я]{2}$"
for i in range(1040, 1104):
    valid_letters.append(chr(i))


def mas_to_str(mas):
    stroka = ""
    for i in range(len(mas)):
        stroka += str(mas[i])
    return stroka


def test_car_id_1():
    car_id = "к098нё"
    result = re.fullmatch(regular_exp, car_id)
    assert result is None


def test_car_id_2():
    car_id = "П156КИ"
    result = re.fullmatch(regular_exp, car_id)
    assert result is not None


def test_car_id_3():
    car_id = "123456"
    result = re.fullmatch(regular_exp, car_id)
    assert result is None


def test_car_id_complete():
    car_id = [0, 1, 2, 3, 4, 5]
    result = 1
    complete_result = 1
    for i in range(len(valid_letters)):
        car_id[0] = str(valid_letters[i])
        for j in range(10):
            car_id[1] = str(j)
            for k in range(10):
                car_id[2] = str(k)
                for l in range(10):
                    car_id[3] = str(l)
                    for p in range(len(valid_letters)):
                        car_id[4] = str(valid_letters[p])
                        for m in range(len(valid_letters)):
                            car_id[5] = str(valid_letters[m])
                            s = mas_to_str(car_id)
                            result = re.fullmatch(regular_exp, s)
                            if result is None: complete_result = None
    assert complete_result is not None
