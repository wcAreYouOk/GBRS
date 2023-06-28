import copy
import csv
import sys
import warnings

import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler

from Code.tolls.GBList import GBList
from Code.tolls.mean_std import mean_std

warnings.filterwarnings("ignore")


def attribute_reduce(data, pur=1, d2=2):
	"""
	:param data: dataset
	:param pur: purity threshold
	:param d2: min_samples, the default value is 2
	:return: reduction attribute
	"""
	BallNum = -sys.maxsize  # the number of granular-balls
	attribute = []
	redAttribute = [i for i in range(len(data[0]) - 2)]  # redundant attribute
	while len(redAttribute):
		N_bal_num = -sys.maxsize  # Current number of granular-balls
		N_i = -1  # Preselection attribute
		for i in redAttribute:
			tempAttribu = copy.deepcopy(attribute)  # Temporary attribute
			tempAttribu.append(i)
			gb = GBList(data, tempAttribu)  # generate the list of granular balls
			gb.init_granular_balls(purity=pur, min_sample=2 * (len(data[0]) - d2))  # initialize the list
			ball_list1 = gb.granular_balls
			Pos_num = 0
			for ball in ball_list1:
				if ball.purity >= 1:
					Pos_num += ball.num  # find the current  domain samples
			if Pos_num > N_bal_num:
				N_bal_num = Pos_num
				N_i = i
		if N_bal_num >= BallNum:
			BallNum = N_bal_num
			attribute.append(N_i)
			redAttribute.remove(N_i)
		else:
			return attribute
	return attribute


if __name__ == "__main__":
	datan = ["wine"]
	for name in datan:
		with open(r"D:\py\GBRS\Result\\" + name + ".csv", "w", newline='', encoding="utf-8") as jg:
			writ = csv.writer(jg)
			df = pd.read_csv(r"D:\py\GBRS\DataSet\\" + name + ".csv")
			data = df.values
			numberSample, numberAttribute = data.shape
			minMax = MinMaxScaler()  # Dataset normalization
			U = np.hstack((minMax.fit_transform(data[:, 1:]), data[:, 0].reshape(numberSample, 1)))
			C = list(np.arange(0, numberAttribute - 1))
			D = list(set(U[:, -1]))
			index = np.array(range(0, numberSample)).reshape(numberSample, 1)
			sort_U = np.argsort(U[:, 0:-1], axis=0)
			U1 = np.hstack((U, index))
			index = np.array(range(numberSample)).reshape(numberSample, 1)  # column of index
			data_U = np.hstack((U, index))  # Add the index column to the last column of the data
			purity = 1  # purity threshold
			clf = KNeighborsClassifier(n_neighbors=3)
			orderAttributes = U[:, -1]
			mat_data = U[:, :-1]  # test dataset
			maxavg = -1  # Maximum accuracy
			maxStd = 0  # Standard deviation corresponding to maximum accuracy
			maxRow = []  # Standard deviation corresponding to attribute reduction
			for i in range((int)(numberAttribute)):
				nums = i
				Row = attribute_reduce(data_U, pur=purity, d2=nums)
				writ.writerow(["GBRS:", Row])
				print("Row:", Row)
				mat_data = U[:, Row]
				scores = cross_val_score(clf, mat_data, orderAttributes, cv=5)
				avg, std = mean_std(scores)
				if maxavg < avg:
					maxavg = avg
					maxStd = std
					maxRow = copy.deepcopy(Row)
			print("pre", maxavg)
			print("row", maxRow)
