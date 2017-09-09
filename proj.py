#!/usr/bin/python -i
"""Prosjekt 1"""

import numpy as np
import math as m
import matplotlib.pyplot as plt

#kjapp måte å konvertere fra streng til numpy-array
to_vector = lambda string: np.array([float(x) for x in string.strip().split()])

#kjapp måte å konvertere fra multi-streng til numpy-matrise
to_matrix = lambda string: np.matrix([[float(y) for y in x.split()] for x in string.strip().splitlines()])

#antall inndelte høydepartier
altitudes = 50

#Sannsynlighetsfordelingen for lav risiko/høy risiko ved bunn
P_bottom = to_vector("0.99 0.01")

#Overgangssannsynlighet til neste høydeparti
P_transition = to_matrix("""
0.95 0.05
0.00 1.00
""")

#Mengde med overgangspotenser; fra 0 til 49.
P_transitions = [P_transition ** altitude for altitude in range(altitudes)]

#A
"""
Denne sier seg litt selv, viss ikke: les oppgaveteksten på nytt.
"""
altitude_risks = [(P_bottom @ P_transition).A1 for P_transition in P_transitions]

#plt.imshow(altitude_risks.T, cmap='pink', interpolation='nearest')
#y_values = ["Low risk", "High risk"]
#plt.yticks([0, 1], y_values)
#plt.title("Risk given altitude")
#plt.show()

#B
"""
Her simulerer vi jernbanen 25 ganger og samler gjennomsnittet.
numpy.choice velger mellom 0 og 1 utifra fordelingen i p.
Kan effektiviseres fordi man ikke lenger har noe valg etter høyrisiko-soner.
"""
realizations = 25
#Vi gjør klar lista så vi kan legge til direkte istedenfor å bruke append().
average_risks = np.empty([altitudes, 2])
for realization in range(realizations):
	current_state = np.random.choice([0, 1], p = P_bottom) #first state
	average_risks[0][current_state] += 1/realizations
	for altitude in range(1, altitudes):
		state_transition = np.ravel(P_transition[current_state])
		current_state = np.random.choice([0, 1], p = state_transition)
		average_risks[altitude][current_state] += 1/realizations

#plt.imshow(average_risks.T, cmap='pink', interpolation='nearest')
#plt.show()

#C
"""
Legg till kommentar hær
"""
#Vi antar at vi kjenner til om området k er høyrisiko/lavrisiko
k = 20

#Vi velger hvilket senario vi vil simulere.
P_Xk = to_vector("1.00 0.00") #state 1 // low risk
#P_Xk = to_vector("0.00 1.00") #state 2 // high risk

#Vi gjør klar lista så vi kan legge til direkte istedenfor å bruke append().
cond_altitude_risks = np.empty([altitudes, 2])
cond_altitude_risks[k] = P_Xk
for altitude in range(k+1, altitudes):
	distance_from_k = altitude-k #always positive
	P_Xlk = P_Xk @ P_transitions[distance_from_k]
	cond_altitude_risks[altitude] = P_Xlk

for altitude in reversed(range(k)):
	distance_from_k = k-altitude #always positive

	P_Xl = np.ravel(P_bottom @ P_transitions[altitude])
	#Given P_Xk, l = (1,0) or l = (0,1), calculates P(X_k = P_Xk | X_k = l)
	P_Xkl = [np.ravel(state @ P_transitions[distance_from_k]) for state in ([1,0],[0,1])]

	P_Xlk = [
		np.dot(P_Xk, P_Xkl[i])*P_Xl[i]/
		(np.dot(P_Xk, P_Xkl[0])*P_Xl[0] + np.dot(P_Xk, P_Xkl[1])*P_Xl[1])
	for i in range(2)]

	cond_altitude_risks[altitude] = P_Xlk

#plt.imshow(cond_altitude_risks.T, cmap='pink', interpolation='nearest')
#plt.show()

#D
"""
Denne sier seg også litt selv; viss ikke: les oppgaveteksten.
"""
total_cost = sum(5000 * high_risk for low_risk, high_risk in altitude_risks)
#print(min(1E5, total_cost)) # 100000 < 158617.552552

#E
"""
Legg till kommentar hær
"""
V = [0 for k in range(altitudes)]
for k in range(altitudes):
	for state in ([1,0],[0,1]):
		P_Xk = state #This is not P_Xk | P_X0
		cond_altitude_risks = np.empty([altitudes, 2])
		cond_altitude_risks[k] = P_Xk
		for altitude in range(k+1, altitudes):
			distance_from_k = altitude-k #always positive
			P_Xlk = P_Xk @ P_transitions[distance_from_k]
			cond_altitude_risks[altitude] = P_Xlk

		for altitude in reversed(range(k)):
			"""P(Xk = 2 | Xl = 2) = 100%"""
			distance_from_k = k-altitude #always positive

			P_Xl = np.ravel(P_bottom @ P_transitions[altitude])
			#Given P_Xk, l = (1,0) or l = (0,1), calculates P(X_k = P_Xk | X_k = l)
			P_Xkl = [np.ravel(state @ P_transitions[distance_from_k]) for state in ([1,0],[0,1])]

			P_Xlk = [
				np.dot(P_Xk, P_Xkl[i])*P_Xl[i]/
				(np.dot(P_Xk, P_Xkl[0])*P_Xl[0]+np.dot(P_Xk, P_Xkl[1])*P_Xl[1])
			for i in range(2)]

			cond_altitude_risks[altitude] = P_Xlk

		k_sum = sum(5000 * high_risk for low_risk, high_risk in cond_altitude_risks)
		V[k] += min(1E5, k_sum) * np.dot(np.ravel(P_bottom @ P_transitions[k]), state)

#plt.plot(V)
#print(f"Minimum value is {min(V)} at {V.index(min(V))}.")
#plt.show()
