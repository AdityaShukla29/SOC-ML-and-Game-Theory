import numpy as np
import itertools
from tqdm import tqdm
import matplotlib.pyplot as plt


''' Do not change anything in this function '''
def generate_random_profiles(num_voters, num_candidates):
    '''
        Generates a NumPy array where row i denotes the strict preference order of voter i
        The first value in row i denotes the candidate with the highest preference
        Result is a NumPy array of size (num_voters x num_candidates)
    '''
    return np.array([np.random.permutation(np.arange(1, num_candidates+1)) 
            for _ in range(num_voters)])


def find_winner(profiles, voting_rule):
    '''
        profiles is a NumPy array with each row denoting the strict preference order of a voter
        voting_rule is one of [plurality, borda, stv, copeland]
        In STV, if there is a tie amongst the candidates with minimum plurality score in a round, then eliminate the candidate with the lower index
        For Copeland rule, ties among pairwise competitions lead to half a point for both candidates in their Copeland score

        Return: Index of winning candidate (1-indexed) found using the given voting rule
        If there is a tie amongst the winners, then return the winner with a lower index
    '''

    winner_index = None

    # TODO

    if voting_rule == 'plurality':
        num_voters=profiles.shape[0]
        num_candidates=profiles.shape[1]
        vote_counter=[0]*num_candidates
        for voter in range(num_voters):
            candidate=profiles[voter][0]
            vote_counter[candidate-1] = 1+vote_counter[candidate-1]
        winner_votes=max(vote_counter)
        winner_indice=[i+1 for i,votes in enumerate(vote_counter) if votes == winner_votes]
        winner_index= min(winner_indice)




    elif voting_rule == 'borda':
        num_voters = profiles.shape[0]
        num_candidates = profiles.shape[1]
        vote_score = [0] * num_candidates
        for voter in range(num_voters):
            for rank in range(num_candidates):
                candidate=profiles[voter][rank]
                vote_score[candidate-1]=vote_score[candidate-1]+num_candidates-rank
        winner_votes=max(vote_score)
        winner_indice=[i+1 for i,votes in enumerate(vote_score) if votes == winner_votes]

        winner_index=min(winner_indice)




    elif voting_rule == 'stv':
        num_voters = profiles.shape[0]
        num_candidates = profiles.shape[1]
        candidates_not_eliminated=list(range(1,num_candidates+1))
        while len(candidates_not_eliminated)>1:
            vote_counter={}
            for candidate in candidates_not_eliminated:
                vote_counter[candidate]=0
            for voter in range(num_voters):
                for rank in profiles[voter]:
                    if rank in candidates_not_eliminated:
                        vote_counter[rank]=vote_counter[rank]+1
                        break
            min_votes = min(vote_counter.values())
            candidates_to_eliminate=[]
            for candidate, votes in vote_counter.items():
                if votes == min_votes:
                    candidates_to_eliminate.append(candidate)
            candidate_to_eliminate = min(candidates_to_eliminate)
            candidates_not_eliminated.remove(candidate_to_eliminate)
        winner_index = candidates_not_eliminated[0]


    elif voting_rule == 'copeland':
        num_voters=profiles.shape[0]
        num_candidates=profiles.shape[1]
        copeland_score=[0]*num_candidates
        for candidate_a in range(num_candidates):
            for candidate_b in range(candidate_a+1,num_candidates):
                candidate_a_win_count=0
                candidate_b_win_count=0
                for voter in range(num_voters):
                    for rank in range(num_candidates):
                        if profiles[voter][rank]==candidate_a+1:
                            rank_a=rank
                        elif profiles[voter][rank]==candidate_b+1:
                            rank_b=rank
                    if rank_a<rank_b:
                        candidate_a_win_count=candidate_a_win_count+1
                    elif rank_b<rank_a:
                        candidate_b_win_count=candidate_b_win_count+1
                    else:
                        candidate_a_win_count = candidate_a_win_count + 0.5
                        candidate_b_win_count=candidate_b_win_count+0.5
                if candidate_a_win_count>candidate_b_win_count:
                    copeland_score[candidate_a]=copeland_score[candidate_a]+1
                elif candidate_b_win_count>candidate_a_win_count:
                    copeland_score[candidate_b]=copeland_score[candidate_b]+1
                else:
                    copeland_score[candidate_a]=copeland_score[candidate_a]+0.5
                    copeland_score[candidate_b]=copeland_score[candidate_b]+0.5

        winner_index=copeland_score.index(max(copeland_score))+1





    # END TODO

    return winner_index


def find_winner_average_rank(profiles, winner):
    '''
        profiles is a NumPy array with each row denoting the strict preference order of a voter
        winner is the index of the winning candidate for some voting rule (1-indexed)

        Return: The average rank of the winning candidate (rank wrt a voter can be from 1 to num_candidates)
    '''



    average_rank = None

    # TODO
    rank_list = []
    for voter in profiles:
        for index in range(len(voter)):
            if voter[index] == winner:
                rank = index + 1
                rank_list.append(rank)
                break

    average_rank=np.mean(rank_list)


    # END TODO

    return average_rank


def check_manipulable(profiles, voting_rule, find_winner):
    '''
        profiles is a NumPy array with each row denoting the strict preference order of a voter
        voting_rule is one of [plurality, borda, stv, copeland]
        find_winner is a function that takes profiles and voting_rule as input, and gives the winner index as the output
        It is guaranteed that there will be at most 8 candidates if checking manipulability of a voting rule

        Return: Boolean representing whether the voting rule is manipulable for the given preference profiles
    '''

    manipulable = False

    # TODO
    original_winner = find_winner(profiles, voting_rule)
    num_voters=profiles.shape[0]
    num_candidates=profiles.shape[1]
    for voter in range(num_voters):
        original_preference = profiles[voter].copy()
        for permutations in itertools.permutations(profiles[voter]):
            profiles[voter] = np.array(permutations)
            new_winner = find_winner(profiles, voting_rule)
            if new_winner!=original_winner:
                manipulable=True
                break
        profiles[voter] = original_preference
        if manipulable:
            break

    # END TODO

    return manipulable


if __name__ == '__main__':
    np.random.seed(420)

    num_tests = 200
    voting_rules = ['plurality', 'borda', 'stv', 'copeland']

    average_ranks = [[] for _ in range(len(voting_rules))]
    manipulable = [[] for _ in range(len(voting_rules))]
    for _ in tqdm(range(num_tests)):
        # Check average ranks of winner
        num_voters = np.random.choice(np.arange(80, 150))
        num_candidates = np.random.choice(np.arange(10, 80))
        profiles = generate_random_profiles(num_voters, num_candidates)

        for idx, rule in enumerate(voting_rules):
            winner = find_winner(profiles, rule)
            avg_rank = find_winner_average_rank(profiles, winner)
            average_ranks[idx].append(avg_rank / num_candidates)

        # Check if profile is manipulable or not
        num_voters = np.random.choice(np.arange(10, 20))
        num_candidates = np.random.choice(np.arange(4, 8))
        profiles = generate_random_profiles(num_voters, num_candidates)
        
        for idx, rule in enumerate(voting_rules):
            manipulable[idx].append(check_manipulable(profiles, rule, find_winner))


    # Plot average ranks as a histogram
    for idx, rule in enumerate(voting_rules):
        plt.hist(average_ranks[idx], alpha=0.8, label=rule)

    plt.legend()
    plt.xlabel('Fractional average rank of winner')
    plt.ylabel('Frequency')
    plt.savefig('average_ranks.jpg')
    
    # Plot bar chart for fraction of manipulable profiles
    manipulable = np.sum(np.array(manipulable), axis=1)
    manipulable = np.divide(manipulable, num_tests)
    plt.clf()
    plt.bar(voting_rules, manipulable)
    plt.ylabel('Manipulability fraction')
    plt.savefig('manipulable.jpg')