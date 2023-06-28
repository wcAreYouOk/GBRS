import numpy as np
from sklearn.cluster import KMeans

from Code.tolls.GBOverlap import GBOverlap
from Code.tolls.GranularBall import GranularBall


def OverlapControl(ball_list, data, attributes_reduction, LBS):
	"""
	Control the process of de overlapping
	:param ball_list: granular-ball list
	:param data:
	:param attributes_reduction:
	:param LBS:
	:return:
	"""
	Ball_list = GBOverlap(ball_list, LBS)  # continue to split ball which are overlapped
	# do last overlap for granular ball aimed raise ball's quality
	while True:
		init_center = []  # ball's center
		Ball_num1 = len(Ball_list)
		for i in range(len(Ball_list)):
			init_center.append(Ball_list[i].center)
		ClusterLists = KMeans(init=np.array(init_center), n_clusters=len(Ball_list)).fit(data[:, attributes_reduction])
		data_label = ClusterLists.labels_
		ball_list = []
		for i in set(data_label):
			ball_list.append(GranularBall(data[data_label == i, :], attributes_reduction))
		Ball_list = GBOverlap(ball_list, LBS)
		Ball_num2 = len(Ball_list)  # get ball numbers
		if Ball_num1 == Ball_num2:  # stop until ball's numbers don't change
			break
	return Ball_list
