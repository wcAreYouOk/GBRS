import numpy as np

from Code.tolls.GranularBall import GranularBall
from Code.tolls.OverlapControl import OverlapControl


class GBList:
	"""
	Granular-Balls list object
	"""

	def __init__(self, data=None, attribu=[]):
		self.data = data[:, :]
		self.attribu = attribu
		self.granular_balls = [GranularBall(self.data, self.attribu)]  # gbs is initialized with all data

	def init_granular_balls(self, purity=0.996, min_sample=1):
		"""
		Split the balls, initialize the balls list.
		purty=1,min_sample=2d
		:param purity: If the purity of a ball is greater than this value, stop splitting.
		:param min_sample: If the number of samples of a ball is less than this value, stop splitting.
		"""
		ll = len(self.granular_balls)
		i = 0
		while True:
			if self.granular_balls[i].purity < purity and self.granular_balls[i].num > min_sample:
				split_balls = self.granular_balls[i].split_2balls()
				if len(split_balls) > 1:
					self.granular_balls[i] = split_balls[0]
					self.granular_balls.append(split_balls[1])
					ll += 1
				else:
					i += 1
			else:
				i += 1
			if i >= ll:
				break
		ball_lists = self.granular_balls
		Bal_List = OverlapControl(ball_lists, self.data, self.attribu, min_sample)  # do overlap
		self.granular_balls = Bal_List
		self.get_data()
		self.data = self.get_data()

	def get_data_size(self):
		return list(map(lambda x: len(x.data), self.granular_balls))

	def get_purity(self):
		return list(map(lambda x: x.purity, self.granular_balls))

	def get_center(self):
		"""
		:return: the center of each ball.
		"""
		return np.array(list(map(lambda x: x.center, self.granular_balls)))

	def get_r(self):
		"""
		:return: return radius r
		"""
		return np.array(list(map(lambda x: x.r, self.granular_balls)))

	def get_data(self):
		"""
		:return: Data from all existing granular balls in the GBlist.
		"""
		list_data = [ball.data for ball in self.granular_balls]
		return np.vstack(list_data)

	def del_ball(self, purty=0., num_data=0):
		# delete ball
		T_ball = []
		for ball in self.granular_balls:
			if ball.purity >= purty and ball.num >= num_data:
				T_ball.append(ball)
		self.granular_balls = T_ball.copy()
		self.data = self.get_data()

	def R_get_center(self, i):
		# get ball's center
		attribu = self.attribu
		attribu.append(i)
		centers = []
		for ball in range(self.granular_balls):
			center = []
			data_no_label = ball.data[:, attribu]
			center = data_no_label.mean(0)
			centers.append(center)
		return centers
