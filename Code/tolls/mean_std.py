import numpy as np


def mean_std(a):
	# calculate average and standard
	a = np.array(a)
	std = np.sqrt(((a - np.mean(a)) ** 2).sum() / (a.size - 1))
	return a.mean(), std
