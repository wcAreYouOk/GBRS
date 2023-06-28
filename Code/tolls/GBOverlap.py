import numpy as np


def GBOverlap(ball_list, LBS):
	"""
	:param ball_list: the process of granular-balls List do overlap
	:param LBS: the lower bound of the size
	:return: the universe is granulated into many stable granular-balls
	"""
	Ball_list = ball_list
	Ball_list = sorted(Ball_list, key=lambda x: -x.r, reverse=True)
	ballsNum = len(Ball_list)
	j = 0
	ball = []
	while True:
		if len(ball) == 0:
			ball.append([Ball_list[j].center, Ball_list[j].r, Ball_list[j].label, Ball_list[j].num])
			j += 1
		else:
			flag = False
			for index, values in enumerate(ball):
				if values[2] != Ball_list[j].label and (
						np.sum((values[0] - Ball_list[j].center) ** 2) ** 0.5) < (
						values[1] + Ball_list[j].r) and Ball_list[j].r > 0 and Ball_list[j].num >= LBS / 2 and \
						values[3] >= LBS / 2:
					balls = Ball_list[j].split_2balls()
					if len(balls) > 1:
						Ball_list[j] = balls[0]
						Ball_list.append(balls[1])
						ballsNum += 1
					else:
						Ball_list[j] = balls[0]
			if flag == False:
				ball.append([Ball_list[j].center, Ball_list[j].r, Ball_list[j].label, Ball_list[j].num])
				j += 1
		if j >= ballsNum:
			break
		"""
		if two ball's label is different and overlapped，in this step,we can continue split positive domain can keep boundary region don't change, but this measure is unnecessary.
		while 1:
			if len(ball) == 0:
				ball.append([Ball_list[j].center, Ball_list[j].r, Ball_list[j].label, Ball_list[j].num,Ball_list[j]])
				j += 1
			else:
				flag = False
				for index, values in enumerate(ball):
					if values[2] != Ball_list[j].label and (
							np.sum((values[0] - Ball_list[j].center) ** 2) ** 0.5) < (
							values[1] + Ball_list[j].r) and Ball_list[j].r > 0 and (Ball_list[j].purity==1 or values[-1].purity==1):# do overlap
						if(values[-1].purity==1):
							balls = Ball_list[j].split_2balls()
							if len(balls) > 1:
								Ball_list[j] = balls[0]
								Ball_list.append(balls[1])
								ballsNum += 1
							else:
								Ball_list[j] = balls[0]
						elif Ball_list[j].purity<0.99:
							balls = values[-1].split_2balls()
							if len(balls) > 1:
								values[-1] = balls[0]
								Ball_list.append(balls[1])
								ballsNum += 1
							else:
								Ball_list[j] = balls[0]
				if flag == False:
					ball.append([Ball_list[j].center, Ball_list[j].r, Ball_list[j].label, Ball_list[j].num,Ball_list[j]])
					j += 1
			if j >= ballsNum:
				break
		"""
		return Ball_list
