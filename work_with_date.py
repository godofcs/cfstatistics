from datetime import date
from datetime import datetime
from tasks import parse

unix_day = 86_400
unix_week = 604_800
unix_month = unix_day * 30
unix_year = unix_day * 365


def how_solve_between(nick, l, r):
    r = dot_date(datetime.fromtimestamp(datetime.timestamp(datetime.strptime(r, "%d.%m.%Y")) + unix_day))
    print(l, r)
    return parse(nick, [1, l, r])


def dot_date(cur_date):
    return cur_date.strftime("%d.%m.%Y")


def how_solve_today(nick):
    return how_solve_between(nick, dot_date(date.today()), dot_date(date.today()))


def how_solve_in_week(nick):
    left_date = datetime.fromtimestamp(
        datetime.timestamp(datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)) - unix_week)
    return how_solve_between(nick, dot_date(left_date), dot_date(date.today()))


def how_solve_in_this_week(nick):
    left_date = datetime.fromtimestamp(datetime.timestamp(
        datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)) - unix_day * datetime.weekday(
        datetime.today()))
    return how_solve_between(nick, dot_date(left_date), dot_date(date.today()))


def how_solve_in_last_week(nick):
    left_date = datetime.fromtimestamp(datetime.timestamp(datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)) - unix_day * (datetime.weekday(datetime.today()) + 7))
    right_date = datetime.fromtimestamp(datetime.timestamp(datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)) - unix_day * (datetime.weekday(datetime.today()) + 1))
    return how_solve_between(nick, dot_date(left_date), dot_date(right_date))


def how_solve_in_month(nick):
    left_date = datetime.fromtimestamp(datetime.timestamp(datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)) - unix_month)
    return how_solve_between(nick, dot_date(left_date), dot_date(date.today()))


def how_solve_in_this_month(nick):
    left_date = datetime.fromtimestamp(
        datetime.timestamp(datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)))
    return how_solve_between(nick, dot_date(left_date), dot_date(date.today()))


def how_solve_in_last_month(nick):
    right_date = datetime.fromtimestamp(
        datetime.timestamp(datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)) - unix_day)
    left_date = right_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return how_solve_between(nick, dot_date(left_date), dot_date(right_date))


def how_solve_in_year(nick):
    left_date = datetime.fromtimestamp(
        datetime.timestamp(datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)) - unix_year)
    return how_solve_between(nick, dot_date(left_date), dot_date(date.today()))


def how_solve_in_this_year(nick):
    left_date = datetime.fromtimestamp(
        datetime.timestamp(datetime.today().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)))
    return how_solve_between(nick, dot_date(left_date), dot_date(date.today()))


def how_solve_in_last_year(nick):
    right_date = datetime.fromtimestamp(
        datetime.timestamp(datetime.today().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)) - unix_day)
    left_date = datetime.fromtimestamp(
        datetime.timestamp(right_date.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)))
    return how_solve_between(nick, dot_date(left_date), dot_date(right_date))


if __name__ == "__main__":
    print("Введите ник:")
    nick = input()
    print("Показать задачи за определённый промежуток или за всё время? all/int")
    ans = input()
    while not (ans in ["all", "int"]):
        print("Показать задачи за определённый промежуток или за всё время? all/int")
        ans = input()
    if ans == "all":
        parse(nick, [0])
    else:
        print("Выберите формат:")
        print("0: сколько решено за сегодня")
        print("1: сколько решено за неделю")
        print("2: сколько решено с начала этой недели")
        print("3: сколько решено на прошлой неделе")
        print("4: сколько решено за месяц")
        print("5: сколько решено с начала месяца")
        print("6: сколько решено за прошлый месяц")
        print("7: сколько решено за год")
        print("8: сколько решено с начала года")
        print("9: сколько решено за прошлый год")
        print("10: сколько решено в период с дата1 по дата2")
        ans = input()
        if ans == "0":
            how_solve_today(nick)
        elif ans == "1":
            how_solve_in_week(nick)
        elif ans == "2":
            how_solve_in_this_week(nick)
        elif ans == "3":
            how_solve_in_last_week(nick)
        elif ans == "4":
            how_solve_in_month(nick)
        elif ans == "5":
            how_solve_in_this_month(nick)
        elif ans == "6":
            how_solve_in_last_month(nick)
        elif ans == "7":
            how_solve_in_year(nick)
        elif ans == "8":
            how_solve_in_this_year(nick)
        elif ans == "9":
            how_solve_in_last_year(nick)
        else:
            print("Введите даты через пробел в формате 'ДД.ММ.ГГГГ'")
            while True:
                dates = input().split()
                if len(dates) == 2 and len(dates[0].split(".")) == 3 and len(dates[1].split(".")) == 3:
                    break
            how_solve_between(nick, dates[0], dates[1])
