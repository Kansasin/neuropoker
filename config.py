MIN_BET = 100  # минимальная ставка  # перенести в game_settings
BOTS_NAMES = ''  # имена ботов через пробел

BOTS_NUMBER = 5  # количество ботов в игре  # перенести в game_settings
PLAYERS_NUMBER = 6  # количество игроков в игре  # перенести в game_settings

SERIES_LENGTH = 5  # длина обучающей серии игр
SERIES_NUMBER = 1000000  # количество серий
BOTS_LEARNING_SERIES_LENGTH = 0  # время обучения ботов
AUTOSAVES_FREQUENCY = 15  # частота автосохранений

IMPORT_PATH = ''  # последний импортированный файл
EXPORT_PATH = ''  # последний путь экспорта
DB_PATH = ''  # текущий путь до базы данных

RULES = """

Цель - собрать лучшую игровую комбинацию из пяти карт за пять раундов игры

Комбинации составляются из двух карт на руке и пяти карт на столе.
Лучшая комбинация выбирается по ее уровню, а если уровни равны, то по уровню старшей карты в комбинации

Комбинации (в порядке возрастания уровня):
1. Старшая карта - любая самая старшая карта по достоинству
2. Пара - две карты однинакового достоинства
3. Две пары - две комбинации Пара
4. Сет - три карты одинакового достоинства
5. Стрит - пять карт, достоинства которых выстраиваются по порядку (например, 2♣ 3♣ 4♥ 5♥ 6♥)
6. Флеш - пять карт одной масти
7. Фул хаус - комбинация Пара и комбинация Сет
8. Каре - четыре карты одного достоинства
9. Стрит-флеш - комбинации Стрит и Флеш
10.Роял флеш - комбинация Стрит-флеш со старшей картой Туз

Раунды

Игра делится на пять раундов: префлоп, флоп, терн, ривер и шоудаун
Каждый раунд делится на два этапа: раздача карт и ставки

Префлоп - каждому игроку на руки раздается по две карты, игроки делают ставки
Флоп - на стол выкладываются три общие карты, игроки делают ставки
Терн и ривер - на стол выкладываются четвертая и пятая карты соответственно, игроки делают ставки на каждом раунде
Шоудаун - игроки показывают свои карты, выбираются победители и делится банк

Раунд завершается только тогда, когда все ставки игроков равны (сбросившие карты и поставившие все не учитываются)


Очередность ходов

Перед началом среди игроков выбирается дилер, следующий за ним игрок является малым блайндом, а следующий за м.блайндом - большой блайнд.

Каждый раунд первым делает ставки м.блайнд, б.блайнд и оставшиеся в очереди. Последним ставку делает дилер, если ставок не было, либо игрок перед последним поднявшим ставку.

В каждой новой партии дилером выбирается предыдущий м.блайнд и в соответствии с этим роли выдаются по новой


Ставки

На префлопе м.блайнд обязательно ставит минимальную указанную ставку, б.блайнд обязательно ставит двойную минимальную ставку. Далее, остальные игроки могут сделать следующие действия:
1. поднять ставку (выше уже максимальной поставленной в текущем раунде)
2. уравнять ставку (сделать свою ставку равной текущей максимальной поставленной в текущем раунде)
3. пропустить ставку (если текущая ставка уже равна максимальной поставленной в текущем раунде)
4. сбросить карты (если не устраивают карты и играть дальше не имеет смысла)
5. поставить все (если не хватает фишек для уравнивания текущей максимальной ставки)

В остальных раундах, все игроки имеют возможность сделать любое из вышеперечисленных действий, если они еще не сбросили карты или еще не поставили все свои фишки.


Формат вывода имени

Имя - роль - банк - карты: <действие>

Наименование достоинств и мастей:

Масти:
♠ - пики (peaks)
♣ - крести (clubs)
♥ - черви (hearts)
♦ - бубны (diamonds)

Достоинства:
2 - два
3 - три
4 - четыре
5 - пять
6 - шесть
7 - семь
8 - восемь
9 - девять
T - десять (ten)
J - валет (jack)
Q - дама (queen)
K - король (king)
A - туз (ace)"""
