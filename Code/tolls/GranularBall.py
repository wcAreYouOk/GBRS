import sys
import warnings
from collections import Counter

import numpy as np
from sklearn.cluster import KMeans

warnings.filterwarnings("ignore")


class GranularBall:
	"""class of the granular ball"""

	def __init__(self, data, attribute):
		"""
		:param data:  Labeled data set, the "-2" column is the class label, the last column is the index of each line
		and each of the preceding columns corresponds to a feature
		:param attribute: condition attribution
		"""
		self.data = data[:, :]
		self.attribute = attribute
		self.data_no_label = data[:, attribute]
		self.num, self.dim = self.data_no_label.shape  # samples numbers and dimension
		self.center = self.data_no_label.mean(0)
		self.label, self.purity, self.r = self.__get_label_and_purity_and_r()

	def __get_label_and_purity_and_r(self):
		"""
		:return: the label, purity and radio of the granular ball.
		"""
		count = Counter(self.data[:, -2])
		label = max(count, key=count.get)
		purity = count[label] / self.num
		a = np.sqrt(np.sum(np.square(np.array(self.data_no_label) - self.center), 1))  # The distance lists from the
		# sample point to the center in the granular-ball.
		r = max(a)  # ball's radius is max distance
		return label, purity, r

	def split_2balls(self):
		"""
		split granular-ball into two granular-balls
		:return: granular-balls list
		"""
		labels = set(self.data[:, -2].tolist())  # labels of dataset
		sample1 = -1  # Maximum sample point with label not 0
		sample0 = -1  # Maximum sample point with label 0
		label0 = sys.maxsize  # the maximum value who‘s label is not 0
		label1 = sys.maxsize  # the maximum value who‘s label is 0
		GBList = []  # granular-balls list with initial value is empty
		dol = np.sum(self.data_no_label, axis=1)  # statistics the values of data_no_label
		if len(labels) > 1:  # Obtain the sample point with the highest value labeled as 1 and non 1
			for i in range(len(self.data)):
				if self.data[i, -2] == 1 and dol[i] < label1:
					label1 = dol[i]
					sample1 = i
				elif self.data[i, -2] != 1 and dol[i] < label0:
					label0 = dol[i]
					sample0 = i
			ini = self.data_no_label[[sample0, sample1], :]  # initial the granular-ball's center
			clu = KMeans(n_clusters=2, init=ini).fit(self.data_no_label)  # select primary sample center
			label_cluster = clu.labels_
			if len(set(label_cluster)) > 1:  # GBList append ball1 and ball2
				ball1 = GranularBall(self.data[label_cluster == 0, :], self.attribute)
				ball2 = GranularBall(self.data[label_cluster == 1, :], self.attribute)
				GBList.append(ball1)
				GBList.append(ball2)
			else:
				GBList.append(self)
		else:
			GBList.append(self)
		return GBList
