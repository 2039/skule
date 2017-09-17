import numpy as np
import math as m
import matplotlib.pyplot as plt

#N signifies the number of candidates interviewed.
N = range(16,45+1)

#The optimal cutoff point is 11 because the expected value of N is 30, given N is uniformly distributed.
#K = range(1,15+1)

#The computed optimal value for k was 10.
K = range(10,11)




def strategy(candidate_values, k):
    best_candidate_value_among_first_k = max(candidate_values[:k])
    for candidate in candidate_values[k:]:
        if candidate > best_candidate_value_among_first_k:
            return candidate
    # If best among first k candidates, we pick the last candidate.
    else:
        return candidate_values[-1]

Y = [0 for k in K]
for k in K:
    # This variable holds the number of times the strategy gives the correct answer.
    correct_answers = 0

    # This variable holds the number of times the strategy's answer was among the top three candidates.
    answer_in_top_three = 0

    # This variable holds the number of times the strategy resulted in interviewing all candidates.
    all_candidates_interviewed = 0

    for n in N:
        #Run simulation of 1000 realizations.
        realizations = 1000

        for realization in range(realizations):
            #Generate N values representing the
            candidate_values_array = [np.random.uniform() for _ in range(n)]

            # Run strategy
            best_candidate_value_given_strategy = strategy(candidate_values= candidate_values_array, k = k)
            best_candidate_value = max(candidate_values_array)

            if(best_candidate_value_given_strategy == best_candidate_value):
                correct_answers += 1/len(N)

            # Were all candidates interviewed? But the best candidate could also be the last one!!!
            best_candidate_value_index = candidate_values_array.index(best_candidate_value_given_strategy)
            if (best_candidate_value_index == len(candidate_values_array) - 1):
                all_candidates_interviewed += 1/len(N)

            #Did the strategy pick a candidate among the top three candidates?
            #Assume distinct values for
            top_three_candidate_values = set()
            for j in range(3):
                max_value_index = candidate_values_array.index(max(candidate_values_array))
                top_three_candidate_values.add(candidate_values_array.pop(max_value_index))
            if (best_candidate_value_given_strategy in top_three_candidate_values):
                answer_in_top_three += 1/len(N)

    #Y[k-1] = correct_answers
    print(k)

correct_answers_ratio = correct_answers/1000
answer_in_top_three_ratio = answer_in_top_three/1000
all_candidates_interviewed_ratio = all_candidates_interviewed/1000

print("The analytical answer was correct " + str(correct_answers) + " times.")
print("The fraction of P(Z = 1) of the simulation is: " + str(correct_answers_ratio))

print("\nThe analytical answer was in top three " + str(answer_in_top_three) + " times.")
print("That is, the analytical answer was in the top three " +
      str(round((answer_in_top_three_ratio * 100), 2)) + "% of the time")

print("\nThe strategy ends up interviewing all candidates " + str(all_candidates_interviewed) + " times.")
print("In other words, the strategy ended up interviewing all candidates " +
       str(round((all_candidates_interviewed_ratio* 100), 2)) + " % of the time.")

plt.plot(K,Y)
plt.grid(True)
plt.ylabel("Expected number of choosing the best candidate");plt.xlabel("k"); plt.title("Expected Number of Choosing the Best Candidate, Given k")
#plt.savefig('p1p1f2.png', transparent=True, bbox_inches='tight',)
plt.show()