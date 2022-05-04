import random
import config

class Player:
	def __init__(self, name):
		self.name = name
		self.index = None # порядок в очереди
	def get_cards(self):
		return [cards[self.index * 2], cards[self.index * 2 + 1]]
class Bot(Player):
	def __init__(self, name):
		super().__init__(name)
class User(Player):
	def __init__(self, name):
		super().__init__(name)
players = [Bot('BOT_Oleg'), Bot('BOT_Anton'), User('Igor')]
shuffle_players = lambda: random.shuffle(players)	# перемешать игроков
def set_queue():									# настроить очередь
	for i in range(len(players)):
		players[i].index = i
# print([(player.name, player.index) for player in players])


class Flush:
	def __init__(self, name):
		self.color = 'black' if name in ['P', 'C'] else 'red'
		self.icon = '♦' if name == 'D' else '♣' if name == 'C' else '♠' if name == 'P' else '♥' if name == 'H' else ''
		self.name = name
flushes = [Flush('D'), Flush('C'), Flush('P'), Flush('H')]

class Rank:
	def __init__(self, level): # A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K
		self.level = level
		self.icon = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'][int(level) - 1]
		self.is_ace = level == 1
ranks = [Rank(1), Rank(2), Rank(3), Rank(4), Rank(5), Rank(6), Rank(7), Rank(8), Rank(9), Rank(10), Rank(11), Rank(12), Rank(13)]

class Card:
	def __init__(self, rank, flush):
		self.rank = rank
		self.flush = flush
		self.icon = rank.icon + flush.name
cards = [Card(rank, flush) for rank in ranks for flush in flushes]
shuffle_cards = lambda: random.shuffle(cards)	# перемешать карты
def get_table_cards(stage = None):
	if stage == 'flop': return cards[-4:-1]
	elif stage == 'turn': return cards[-5:-1]
	elif stage == 'river': return cards[-6:-1]
	else: return []
# print(cards[-1].icon)
# print([card.icon for card in get_table_cards('river')])
# print([card.icon for card in cards])