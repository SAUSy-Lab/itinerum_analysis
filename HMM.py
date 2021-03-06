# Hidden Markov Models and related functions

from math import exp, log
from gaussian import gaussian_log_prob


def viterbi(states, emission_probs, start_probs, transition_probs):
	"""
	Returns the optimal path determined by the viterbi function.
	All probability values are logged.
	'states' is a list of integer ID's for the possible states with length 'S'
	'emission_probs' is a list of length O (number of observations) by S.
	'start_probs' length S list summing to one defining prob of initial state
	'transition_probs' is an SxS matrix of state transition probabilities
	i.e. transition_probs[from_state][to_state]
	See https://en.wikipedia.org/wiki/Viterbi_algorithm for background
	"""
	V = [{}]
	path = {}
	for state in states:
		# Initialize base cases (t == 0)
		V[0][state] = start_probs[state] + emission_probs[0][state]
		path[state] = [state]
	for t in range(1, len(emission_probs)):  # Run Viterbi for t > 0
		V.append({})
		newpath = {}
		for s1 in states:
			(prob, state) = max([(V[t-1][s0] + transition_probs[s0][s1] +
				emission_probs[t][s1], s0) for s0 in states])
			V[t][s1] = prob
			newpath[s1] = path[state] + [s1]
		path = newpath  # Don't need to remember the old paths
	(prob, final_state) = max([(V[len(emission_probs)-1][s], s) for s in states])
	# get the optimal sequence of states
	return path[final_state]


def emission_probabilities(points, locations):
	"""
	Given lists of points and locations, estimate the log probabilities of each 
	point having been emitted from one of the locations or from a non-location
	(i.e. travel). Returns a list of lists per point, e.g.:
	[ [travel_prob,loc1_prob,loc2_prob...],       # point1
	  [travel_prob,loc1_prob,loc2_prob...], ... ] # point2, etc.
	Location emission is based on distance and a gaussian decay function.
	The travel emission probability is based on instantaneous travel speed.
	TODO: Unlogged probabilities should be standardized to sum(*)==1.
	"""
	emission_probs_per_point = []
	for i, point in enumerate(points):
		# location probability is based on distance to locations
		loc_probs = [
			gaussian_log_prob(loc.distance(point), 75) for loc in locations ]
		# travel probability is based on estimate of momentary speed
		if 0 < i < len(points)-1:
			avg_mps = (point.mps(points[i-1]) + point.mps(points[i+1])) / 2
			trav_prob = log(1 - exp(-avg_mps/2)) if avg_mps > 0 else -100
		else:
			trav_prob = log(0.25)
		# standardize such that sum(*) = 1
		point_probs = [trav_prob] + loc_probs
		#point_probs = [p / sum(point_probs) for p in point_probs]
		emission_probs_per_point.append(point_probs)
		# store the probabilities with the points for debugging
		point.emit_p.extend(point_probs)
	return emission_probs_per_point


def state_transition_matrix(states=[]):
	"""
	Given a list of potential activity location id's, return a simple
	transition probability matrix for use in the viterbi function.
	Transition probs are currently hardcoded and returned as a list of lists.
	0 is the 'travel' state. E.g.:
	   0   1   2   3 ...
	0  .9  .03 .03 .03
	1  .2  .8  .0  .0
	2  .2  .0  .8  .0
	3  .2  .0  .0  .8
		...
	Returns log probabilities.
	"""
	# define possible transition probabilities
	travel_to_travel_prob = log(0.95)
	travel_to_place_prob = log( 0.05 / len(states) )
	place_to_travel_prob = log(0.5)
	place_to_itself_prob = log(0.5)
	teleport_prob = -100.0  # impossible, in theory at least
	# make sure travel is an option
	if 0 not in states:
		states += [0]
	trans_prob_matrix = []
	for s0 in states:
		assert type(s0) == int
		trans_prob_matrix.append([])
		for s1 in states:
			if s0 + s1 == 0:  # travel -> travel
				trans_prob_matrix[s0].append(travel_to_travel_prob)
			elif s0 == 0:  # travel -> place
				trans_prob_matrix[s0].append(travel_to_place_prob)
			elif s1 == 0:  # place -> travel
				trans_prob_matrix[s0].append(place_to_travel_prob)
			elif s0 == s1:  # place -> same place
				trans_prob_matrix[s0].append(place_to_itself_prob)
			else:  # place -> place (no travel)
				trans_prob_matrix[s0].append(teleport_prob)
	# the rows should sum to one but there's not a fantastic way to assert this
	# because of floating point precision errors
	return trans_prob_matrix
