# -*- coding: utf-8 -*-

# Подземелье было выкопано ящеро-подобными монстрами рядом с аномальной рекой, постоянно выходящей из берегов.
# Из-за этого подземелье регулярно затапливается, монстры выживают, но не герои, рискнувшие спуститься к ним в поисках
# приключений.
# Почуяв безнаказанность, ящеры начали совершать набеги на ближайшие деревни. На защиту всех деревень не хватило
# солдат и вас, как известного в этих краях героя, наняли для их спасения.
#
# Карта подземелья представляет собой json-файл под названием rpg.json. Каждая локация в лабиринте описывается объектом,
# в котором находится единственный ключ с названием, соответствующем формату "Location_<N>_tm<T>",
# где N - это номер локации (целое число), а T (вещественное число) - это время,
# которое необходимо для перехода в эту локацию. Например, если игрок заходит в локацию "Location_8_tm30000",
# то он тратит на это 30000 секунд.
# По данному ключу находится список, который содержит в себе строки с описанием монстров а также другие локации.
# Описание монстра представляет собой строку в формате "Mob_exp<K>_tm<M>", где K (целое число) - это количество опыта,
# которое получает игрок, уничтожив данного монстра, а M (вещественное число) - это время,
# которое потратит игрок для уничтожения данного монстра.
# Например, уничтожив монстра "Boss_exp10_tm20", игрок потратит 20 секунд и получит 10 единиц опыта.
# Гарантируется, что в начале пути будет две локации и один монстр
# (то есть в коренном json-объекте содержится список, содержащий два json-объекта, одного монстра и ничего больше).
#
# На прохождение игры игроку дается 123456.0987654321 секунд.
# Цель игры: за отведенное время найти выход ("Hatch")
#
# По мере прохождения вглубь подземелья, оно начинает затапливаться, поэтому
# в каждую локацию можно попасть только один раз,
# и выйти из нее нельзя (то есть двигаться можно только вперед).
#
# Чтобы открыть люк ("Hatch") и выбраться через него на поверхность, нужно иметь не менее 280 очков опыта.
# Если до открытия люка время заканчивается - герой задыхается и умирает, воскрешаясь перед входом в подземелье,
# готовый к следующей попытке (игра начинается заново).
#
# Гарантируется, что искомый путь только один, и будьте аккуратны в рассчетах!
# При неправильном использовании библиотеки decimal человек, играющий с вашим скриптом рискует никогда не найти путь.
#
# Также, при каждом ходе игрока ваш скрипт должен запоминать следущую информацию:
# - текущую локацию
# - текущее количество опыта
# - текущие дату и время (для этого используйте библиотеку datetime)
# После успешного или неуспешного завершения игры вам необходимо записать
# всю собранную информацию в csv файл dungeon.csv.
# Названия столбцов для csv файла: current_location, current_experience, current_date
#
#
# Пример взаимодействия с игроком:
#
# Вы находитесь в Location_0_tm0
# У вас 0 опыта и осталось 123456.0987654321 секунд до наводнения
# Прошло времени: 00:00
#
# Внутри вы видите:
# — Вход в локацию: Location_1_tm1040
# — Вход в локацию: Location_2_tm123456
# Выберите действие:
# 1.Атаковать монстра
# 2.Перейти в другую локацию
# 3.Сдаться и выйти из игры
#
# Вы выбрали переход в локацию Location_2_tm1234567890
#
# Вы находитесь в Location_2_tm1234567890
# У вас 0 опыта и осталось 0.0987654321 секунд до наводнения
# Прошло времени: 20:00
#
# Внутри вы видите:
# — Монстра Mob_exp10_tm10
# — Вход в локацию: Location_3_tm55500
# — Вход в локацию: Location_4_tm66600
# Выберите действие:
# 1.Атаковать монстра
# 2.Перейти в другую локацию
# 3.Сдаться и выйти из игры
#
# Вы выбрали сражаться с монстром
#
# Вы находитесь в Location_2_tm0
# У вас 10 опыта и осталось -9.9012345679 секунд до наводнения
#
# Вы не успели открыть люк!!! НАВОДНЕНИЕ!!! Алярм!
#
# У вас темнеет в глазах... прощай, принцесса...
# Но что это?! Вы воскресли у входа в пещеру... Не зря матушка дала вам оберег :)
# Ну, на этот-то раз у вас все получится! Трепещите, монстры!
# Вы осторожно входите в пещеру... (текст умирания/воскрешения можно придумать свой ;)
#
# Вы находитесь в Location_0_tm0
# У вас 0 опыта и осталось 123456.0987654321 секунд до наводнения
# Прошло уже 0:00:00
# Внутри вы видите:
#  ...
#  ...
#
# и так далее...

import json
import common_operation as co
from decimal import Decimal
import datetime
import csv


remaining_time = '123456.0987654321'
field_names = ['current_location', 'current_experience', 'current_date']


class Model:

    def __init__(self):
        self.struct = {}

    @staticmethod
    def get_index(actions_list, item_name):
        index = 0
        for idx, list_item in enumerate(actions_list):
            if list_item[0] == item_name:
                index = idx
                break

        return index

    def move_to_location(self, new_location):
        current_location_data = self.get_current_location()
        location_index = self.get_index(current_location_data['actions_list'], new_location)
        self.struct = self.struct[current_location_data['location']][location_index]
        return new_location

    def get_current_location(self):
        location = list(self.struct.keys())
        if len(location):
            return {
                'location': location[0],
                'location_name': f'at {location[0]}',
                'actions_list': co.get_action_list(self.struct[location[0]]),
            }
        else:
            return {
                'location': '',
                'location_name': 'outside of maze',
                'actions_list': [['', '- Entrance to maze']]
            }

    def remove_mob(self, mob):
        current_location_data = self.get_current_location()
        self.struct[current_location_data['location']].remove(mob)


class View:

    @staticmethod
    def show_next_step():
        print('>' * 20)

    @staticmethod
    def show_statistic(time_left, gained_experience):
        print('\u001b[92;2mYou have {} exp and remaining time {} sec till flood\u001b[0m'
              .format(gained_experience, time_left))

    @staticmethod
    def show_position(location_info):
        print(f'\u001b[94;2mYou are now locate {location_info["location_name"]}')
        print('You are looking around and see:')
        if location_info['actions_list']:
            for index, things in enumerate(location_info['actions_list'], 1):
                print(f'\t\u001b[94;2m{index} \u001b[1m{things[1]}\u001b[0m')

    @staticmethod
    def fight_show(mob):
        print(f'\u001b[91;2mYou fight with \u001b[1m{mob}\u001b[0m')


class Controller:
    game_step_logger = []

    def __init__(self, dungeon_file, time):
        self.model = Model()
        self.view = View()
        self.file_data = dungeon_file
        self.actions_list = []
        self.remaining_time = time
        self.experience = 0

    def log_statistic(self):
        Controller.game_step_logger.append({
            'current_location': self.model.get_current_location()['location'],
            'current_experience': self.experience,
            'current_date': datetime.datetime.now().strftime('%d %B %Y %I:%M %p')
        })

    def show_location(self):
        current_location = self.model.get_current_location()
        current_location.update(remaining_time=self.remaining_time, gained_experience=self.experience)
        self.actions_list = current_location['actions_list']
        self.actions_list.append(['quit', '- Giving up, and end the game'])
        self.view.show_position(current_location)

    def move(self, location):
        if location:
            self.model.move_to_location(location)
            new_location_time = co.parse(location)[-1]
            self.remaining_time = str(Decimal(self.remaining_time) - Decimal(new_location_time))

        else:
            self.set_maze_structure()

    def fight(self, mob):
        enemy_data = co.parse(mob)
        self.experience += int(enemy_data[-2])
        self.remaining_time = str(Decimal(self.remaining_time) - Decimal(enemy_data[-1]))
        self.model.remove_mob(mob)
        self.view.fight_show(mob)

    def exit(self, exit_key):
        exit_data = co.parse(exit_key)
        self.remaining_time = str(Decimal(self.remaining_time) - Decimal(exit_data[-1]))

    def set_maze_structure(self):
        try:
            with open(self.file_data, 'r') as rpg_file:
                self.model.struct = json.load(rpg_file)
        except OSError as err:
            print(f'Error open read file: {err}')

    def reset_data(self, time):
        self.model = Model()
        self.actions_list = []
        self.remaining_time = time
        self.experience = 0

    def run_game(self):
        global remaining_time
        while True:

            if self.remaining_time[0] == '-':
                print('You wasted all your time, and could not found exit. Now you are sunk')
                self.reset_data(remaining_time)

                print('Now you resurrected in front of maze entrance!')
                print('Father give you another chance')

            self.view.show_next_step()
            self.view.show_statistic(time_left=self.remaining_time, gained_experience=self.experience)
            self.show_location()
            player_choice = input('\u001b[37;2mEnter you choice\u001b[0m (\u001b[1mnumber\u001b[0m):\t')
            if player_choice.isdigit() and 0 < int(player_choice) <= len(self.actions_list):
                player_choice = int(player_choice)
                if player_choice == len(self.actions_list):
                    print(f"\u001b[31;2mYou're gave up\u001b[0m")
                    break
                player_choice -= 1
                action_type = co.parse(self.actions_list[player_choice][0])

                if action_type is None:
                    self.move('')
                else:
                    action_type = action_type[0]
                    if action_type.upper() == 'LOCATION':
                        self.move(self.actions_list[player_choice][0])
                    elif 'MOB' in action_type.upper() or 'BOSS' in action_type.upper():
                        self.fight(self.actions_list[player_choice][0])
                    elif 'HATCH' in action_type.upper():
                        if self.experience < 200:
                            print('\u001b[31;2mYou have not enough experience. Try to fight with some mobs/boss\u001b[0m')
                        else:
                            self.exit(self.actions_list[player_choice][0])
                            self.view.show_next_step()
                            print('\u001b[32;1mCongrats! You are win!\u001b[0m')
                            self.log_statistic()
                            break
            self.log_statistic()
        with open('dungeon.csv', 'w', encoding='utf-8', newline='') as csv_statistic_file:
            writer = csv.DictWriter(csv_statistic_file, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(Controller.game_step_logger)


if __name__ == '__main__':
    dungeon = Controller('./rpg.json', remaining_time)
    dungeon.run_game()
