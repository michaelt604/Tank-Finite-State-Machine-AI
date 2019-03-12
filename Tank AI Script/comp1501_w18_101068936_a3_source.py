#<HighGround>
#This bot is designed fully integrate patrol feature instead of dead run towards target
# 'A' is distanceToTarget
# 'B' is last angle
# 'C' is horizontal movement
# 'D' is vertical movement
# 'E' is rotation
# 'F' is lockedon
# 'G' is rotate speed
# 'H' is the last direction of movement (n=0),(e=1),(s=2),(w=3)

from library_for_glad_ai_tors import *
import math

#Starting function
def start(arg):
	position = get_position(arg)

	# Starts program moving South
	if position[0] - get_w_border(arg) > get_e_border(arg) - position[0]:
		return "scanning_S", {'CHARGE': True, 'SHIELD': False, 'F': 0, 'G': 1, 'H': "S", 'C': 0, 'D': 0}

	# Starts program moving north
	else:
		return "scanning_N", {'CHARGE': True, 'SHIELD': False, 'F': 0, 'G': 1, 'H': "N", 'C': 0, 'D': 0}

#Scans 360 degrees around the tank to find opponents
def scanning_N(arg):
	for i in range(0, 360):
		scan = get_radar_data(arg, i)
		if scan[0] == "opponent":
			return "move_and_aim", {('ROT_C' + str(get_saved_data(arg, 'E'))): get_saved_data(arg, 'G'), 'A': scan[1],
								  'B': i, 'ACLT_X': 0, 'ACLT_Y': 0,
								  'LAUNCH': False, 'SHIELD': False}

	charge = False
	if get_weapon_power(arg) < 100:
		charge = True

	(x, y) = get_position(arg)
	border = get_n_border(arg)
	if y < border + 100:
		return "scanning_E", {'A': scan[1], 'B': i, "ACLT_X": +1, "ACLT_Y": +0, 'LAUNCH': False, 'CHARGE': charge,
							  'SHIELD': False, 'H': "E"}
	else:
		return "scanning_N", {'A': scan[1], 'B': i, "ACLT_X": +0, "ACLT_Y": -1, 'LAUNCH': False, 'CHARGE': charge,
							  'SHIELD': False, 'H': "N"}


#Scans 360 degrees around the tank to find opponents
def scanning_E(arg):
	for i in range(0, 360):
		scan = get_radar_data(arg, i)
		if scan[0] == "opponent":
			return "move_and_aim", {('ROT_C' + str(get_saved_data(arg, 'E'))): get_saved_data(arg, 'G'), 'A': scan[1],
								  'B': i, 'ACLT_X': 0, 'ACLT_Y': 0,
								  'LAUNCH': False, 'SHIELD': False}

	charge = False
	if get_weapon_power(arg) < 100:
		charge = True

	(x, y) = get_position(arg)
	border = get_e_border(arg)
	if x >= border - 100:
		return "scanning_S", {'A': scan[1], 'B': i, 'C': 0, 'D': +1, "ACLT_X": +0, "ACLT_Y": +1, 'LAUNCH': False, 'CHARGE': charge,
							  'SHIELD': False, 'H': "S"}
	else:
		return "scanning_E", {'A': scan[1], 'B': i, 'C': 1, 'D': 0, "ACLT_X": +1, "ACLT_Y": +0, 'LAUNCH': False, 'CHARGE': charge,
							  'SHIELD': False, 'H': "E"}


#Scans 360 degrees around the tank to find opponents
def scanning_S(arg):
	for i in range(0, 360):
		scan = get_radar_data(arg, i)
		if scan[0] == "opponent":
			return "move_and_aim", {('ROT_C' + str(get_saved_data(arg, 'E'))): get_saved_data(arg, 'G'), 'A': scan[1],
								  'B': i, 'ACLT_X': 0, 'ACLT_Y': 0,
								  'LAUNCH': False, 'SHIELD': False}

	charge = False
	if get_weapon_power(arg) < 100:
		charge = True

	(x, y) = get_position(arg)
	border = get_s_border(arg)
	if y >= border - 100:
		return "scanning_W", {'A': scan[1], 'B': i, 'C': -1, 'D': 0, "ACLT_X": -1, "ACLT_Y": +0, 'LAUNCH': False, 'CHARGE': charge,
							  'SHIELD': False, 'H': "W"}
	else:
		return "scanning_S", {'A': scan[1], 'B': i, 'C': 0, 'D': 1, "ACLT_X": +0, "ACLT_Y": +1, 'LAUNCH': False, 'CHARGE': charge,
							  'SHIELD': False, 'H': "S"}


#Scans 360 degrees around the tank to find opponents
def scanning_W(arg):
	for i in range(0, 360):
		scan = get_radar_data(arg, i)
		if scan[0] == "opponent":
			return "move_and_aim", {('ROT_C' + str(get_saved_data(arg, 'E'))): get_saved_data(arg, 'G'), 'A': scan[1],
								  'B': i, 'ACLT_X': 0, 'ACLT_Y': 0,
								  'LAUNCH': False, 'SHIELD': False}

	charge = False
	if get_weapon_power(arg) < 100:
		charge = True

	(x, y) = get_position(arg)
	border = get_w_border(arg)
	if x < border + 100:
		return "scanning_N", {'A': scan[1], 'B': i, 'C': 0, 'D': -1, "ACLT_X": +0, "ACLT_Y": -1, 'LAUNCH': False, 'CHARGE': charge,
							  'SHIELD': False, 'H': "N"}
	else:
		return "scanning_W", {'A': scan[1], 'B': i, 'C': -1, 'D': 0, "ACLT_X": -1, "ACLT_Y": +0, 'LAUNCH': False, 'CHARGE': charge,
							  'SHIELD': False, 'H': "W"}


#Scans +- 15 degrees from the tank barrel to find enemies
def quick_scan(arg):
	angle = int(get_saved_data(arg, 'B'))
	total = 0
	count = 0

	(x, y) = get_position(arg)

	current_weapon_angle = get_weapon_angle(arg)

	#Physical scanning
	for i in range (angle - 15, angle + 15):
		scan = get_radar_data(arg, i)
		if scan[0] == "opponent":
			total += i
			count += 1

	#If an opponent is found it will average all locations enemy was seen at
	if total > 0:
		avgAng = total / count
		curAng = get_weapon_angle(arg)

		scan = get_radar_data(arg, avgAng)
		if scan[0] == "opponent":
			bound = (avgAng - curAng + 540)
			boundFix = bound % 360 - 180

			if scan[1] < 100:
				dist = 4
				rotSpd = 1
			elif scan[1] < 200:
				dist = 3
				rotSpd = 0.4
			elif scan[1] < 400:
				dist = 2.5
				rotSpd = 0.3
			elif scan[1] < 600:
				dist = 2
				rotSpd = 0.2
			else:
				dist = 1.5
				rotSpd = 0.1


			if dist >= boundFix >= -dist:
				if get_radar_data(arg, curAng)[0] == "opponent":
					if scan[1] > 800 or scan[1] < 500 or get_saved_data(arg, 'F') >= 0:
						return"firingandforgetting", {'CHARGE': True, 'LAUNCH': True, 'SHIELD': True}
					else:
						return "quick_scan", {'A': scan[1], 'B': avgAng, 'ACLT_X': 0, 'ACLT_Y': 0, 'SHIELD': True, 'F': 1}

			else:
				distance = scan[1]
				enemyAngle = avgAng
				current_weapon_angle = curAng
				(x, y) = get_position(arg)

				x_Distance = math.cos(math.radians(enemyAngle))
				y_Distance = ((y - math.sin(math.radians(enemyAngle)) * distance) - y) / distance

				current_direction_vector_x = int( math.cos(math.radians(current_weapon_angle)) * 500)
				current_direction_vector_y = int(-math.sin(math.radians(current_weapon_angle)) * 500)

				desired_direction_vector_x = x_Distance * 500
				desired_direction_vector_y = y_Distance * 500

				cross_product = current_direction_vector_x * desired_direction_vector_y - current_direction_vector_y * desired_direction_vector_x

				if 0 <= avgAng < 180:
					moveY = -1
				else:
					moveY = 1

				if cross_product > 0:
					return "quick_scan", {'A': scan[1], 'B': curAng, 'ROT_CW': rotSpd, 'E': "W", 'ACLT_X': 0, 'ACLT_Y': moveY, 'SHIELD': False, 'F': 0}
				else:
					return "quick_scan", {'A': scan[1], 'B': curAng, 'ROT_CC': rotSpd, 'E': "C", 'ACLT_X': 0, 'ACLT_Y': moveY, 'SHIELD': False, 'F': 0}


	#If no enemy redetected
	return ("scanning_" + get_saved_data(arg, 'H')), {'ACLT_X': 0, 'ACLT_Y': 0, 'SHIELD': False}


def move_and_aim(arg):
	current_weapon_angle = get_weapon_angle(arg)
	enemyAngle = get_saved_data(arg, "B")

	#Checks to see if the function is bound properly
	bound = (current_weapon_angle - enemyAngle + 540)
	boundFix = bound % 360 - 180
	rotVal = 1

	if 10 >= boundFix >= -10:
		return "quick_scan", {'ACLT_X': 0, 'ACLT_Y': 0, 'G': 1}

	else:
		distance = get_saved_data(arg, 'A')
		(x, y) = get_position(arg)
		x_Distance = math.cos(math.radians(enemyAngle))
		y_Distance = ((y - math.sin(math.radians(enemyAngle)) * distance) - y) / distance

		current_direction_vector_x = int( math.cos(math.radians(current_weapon_angle)) * 500)
		current_direction_vector_y = int(-math.sin(math.radians(current_weapon_angle)) * 500)

		desired_direction_vector_x = x_Distance * 500
		desired_direction_vector_y = y_Distance * 500

		cross_product = current_direction_vector_x * desired_direction_vector_y - current_direction_vector_y * desired_direction_vector_x

		if 35 >= boundFix >= -35:
			rotVal = 0.5
		if distance < 300:
			return ("scanning_" + get_saved_data(arg, 'H')), {'ROT_CW': 1, 'G': rotVal, 'ACLT_X': get_saved_data(arg, 'C'), 'ACLT_Y': get_saved_data(arg, 'D'), 'C': x_Distance, 'D': y_Distance, 'E': "W"}

		if cross_product > 0:
			return ("scanning_" + get_saved_data(arg, 'H')), {'ROT_CW': rotVal, 'G': rotVal, 'ACLT_X': 0, 'ACLT_Y': 0, 'C': x_Distance, 'D': y_Distance, 'E': "W"}
		else:
			return ("scanning_" + get_saved_data(arg, 'H')), {'ROT_CC': rotVal, 'G': rotVal, 'ACLT_X': 0, 'ACLT_Y': 0, 'C': x_Distance, 'D': y_Distance, 'E': "C"}



def firingandforgetting(arg):
	if get_radar_data(arg, get_weapon_angle(arg))[0] == "opponent":
		return 'firingandforgetting', {'LAUNCH': True, 'CHARGE': True, 'SHIELD': True}
	else:
		return ("scanning_" + get_saved_data(arg, 'H')), {'LAUNCH': True, 'CHARGE': True, 'SHIELD': True}
