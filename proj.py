#!/usr/bin/python -i
"""Project 1 / Problem 2"""

import numpy as np
import math as m
import matplotlib.pyplot as plt
from collections import namedtuple
from numpy.random import choice

#Quick way to convert from string to array
to_vector = lambda string: np.array([float(x) for x in string.strip().split()])

#Quick way to convert form multiline string to matrix
to_matrix = lambda string: np.matrix([[float(y) for y in x.split()] for x in string.strip().splitlines()])

#Number of altitude sections
altitudes = 50

#A (modified, see next comment) namedtuple for the distributions
Risks = namedtuple("Risks", "low high")

#The functionality of __getitem__ is changed from nt.key to nt["key"]
getitem = lambda self, key: self._asdict()[key]
Risks.__getitem__ = getitem

#The probability distribution for low risk/high risk at the bottom
bottom_state = Risks(*(to_vector("0.99 0.01")))

#Transition probability matrix for the next section
P_transition = to_matrix("""
0.95 0.05
0.00 1.00
""")

#A list of powers of the transition matrix; from 0 to (49), for speed.
P_transitions = [P_transition ** altitude for altitude in range(altitudes)]

#probability distribution at altitude
def P(X, **sensor):
	"""Markov probability
	This function uses bottom_state and P_transition to calculate
	P(X = altitude), or P(X = altitude, high = sensor_altitude), if
	the **sensor input is given.

	The return value i the probability distribution at altitude X,
	this is given as a (modified) namedtuple: (low: low_val, high: high_val).

	Example output:
	(low: 0.95, high: 0.05)
	"""
	altitude = X #alias
	if not sensor:
		#A1 turns [[matrix]] to [list], which is more easily accessible
		return Risks(*(bottom_state @ P_transitions[altitude]).A1)

	#sensor exists = conditional probability
	sensor_kw, sensor_altitude = sensor.popitem()
	sensor_state = {"low":[1,0],"high":[0,1]}[sensor_kw]
	distance_from_sensor = abs(sensor_altitude - altitude)

	#If X is above sensor altitude, we can discard of bottom_state
	if sensor_altitude <= altitude:
		return Risks(*(sensor_state @ P_transitions[distance_from_sensor]).A1)

	#Otherwise we need take care of both sensor_state and bottom_state
	elif sensor_altitude > altitude:
		return Risks(
		#P(altitude = low | sensor = state)
		P(X = altitude)["low"]
		* P(X = sensor_altitude, low = altitude)[sensor_kw]
		/(
		P(X = altitude)["low"]
		* P(X = sensor_altitude, low = altitude)[sensor_kw]
		+ P(X = altitude)["high"]
		* P(X = sensor_altitude, high = altitude)[sensor_kw]
		)
		,
		#P(altitude = high | sensor = state)
		P(X = altitude)["high"] *
		P(X = sensor_altitude, high = altitude)[sensor_kw]
		/(
		P(X = altitude)["low"]
		* P(X = sensor_altitude, low = altitude)[sensor_kw]
		+ P(X = altitude)["high"]
		* P(X = sensor_altitude, high = altitude)[sensor_kw])
		)

#A
"""
Calculates the probability distribution for each altitude
Then fetches the low risks.
This can be done in a single line, but we need the high risks for question d).
"""
#A1 turns [[matrix]] to [list], which is more easily accessible
altitude_risks = [P(X = altitude) for altitude in range(altitudes)]
low_risks = [risk["low"] for risk in altitude_risks]

#plot
plt.title("Probability of low risk given altitude")
plt.xlabel("altitude"); plt.ylabel("probability")
plt.bar(range(altitudes), low_risks)
plt.show()

#B
"""
We simulate 25 different railroad scenarios.
We use this to make an average risk prospect.
"""

#simulation of a railroad
def realization():
	"""Runs a simulation of a hypothetical railroad, and
	returns a list of the altitudes assigned a binary value
	depending on their risk state: 1 = low, 0 = high.

	Example output:
	[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0]
	"""

	#initialize empty list
	risk_at_altitudes = [None for altitude in range(altitudes)]

	#This chooses 0 or 1 depending on the distribution of bottom_state
	#0 and 1 refers to state 1 and 2, respectively
	current_state = choice([0, 1], p = bottom_state)
	risk_at_altitudes[0] = 1 - current_state


	for altitude in range(1, altitudes):
		#Selects a row distribution in the transition matrix given current state
		current_transition = (P_transition[current_state]).A1

		#This chooses 0 or 1 depending on the distribution of P_transition
		current_state = choice([0, 1], p = current_transition)
		risk_at_altitudes[altitude] = 1 - current_state

	return risk_at_altitudes

# 25 is the number of simulations
realizations = [realization() for _ in range(25)]
average_risks = [sum(altitude_risk)/25 for altitude_risk in zip(*realizations)]

#Plot
plt.title("Realization risks given altitude")
plt.xlabel("altitude"); plt.ylabel("realization")
plt.imshow(realizations, cmap='pink', interpolation='nearest')
plt.show()

#Plot
plt.title("Average realization risk given altitude")
plt.xlabel("altitude"); plt.ylabel("Average")
plt.bar(range(altitudes), average_risks)
plt.show()

#C
"""
We place a sensor at altitude k and assume its status ("low" or "high").
We then calculate the conditional probability.
"""
#Vi antar at vi kjenner til om området k er høyrisiko/lavrisiko
k = 20-1 #20. høydeparti er indeks 19 ved nullindeksering

altitude_risks_lowk=[P(X = altitude, low = k) for altitude in range(altitudes)]
high_risks_lowk = [risk["high"] for risk in altitude_risks_lowk]

#Plot
plt.title(f"High risk probability given low risk at {k}")
plt.xlabel("altitude"); plt.ylabel("Probability")
plt.bar(range(altitudes), high_risks_lowk)
plt.show()

altitude_risks_highk=[P(X = altitude, high = k)for altitude in range(altitudes)]
high_risks_highk = [risk["high"] for risk in altitude_risks_highk]

#Plot
plt.title(f"High risk probability given high risk at {k}")
plt.xlabel("altitude"); plt.ylabel("Probability")
plt.bar(range(altitudes), high_risks_highk)
plt.show()

#D
"""
We calculate the minimal cost given that each high risk zone costs NOK5000.
"""
total_cost = 5000 * sum(risk["high"] for risk in altitude_risks)
print(f"The minimum cost is {min(1E5, total_cost)}") # 100000 < 158617.552552

#E
"""
We calculate the expected cost, given that a sensor is telling us the
state of altitude k.
"""

#initialize empty list
V = [0 for k in range(altitudes)]

for state in ("low", "high"):
	for k in range(altitudes):
		cost = 5000 * sum(P(X = alt, **{state: k})["high"] for alt in range(altitudes))
		V[k] += min(1E5, cost) * P(X = k)[state]

print(f"Minimum value is {min(V)} at {V.index(min(V))}.")

#Plot
plt.title("Estimated cost given sensor at altitude k")
plt.xlabel("sensor altitude"); plt.ylabel("estimated cost")
plt.plot(V)
plt.show()
