import matplotlib.pyplot as plt
from typing import Dict, List, Tuple

def Gale_Shapley(suitor_prefs, reviewer_prefs) -> Dict[str, str]:
    '''
        Gale-Shapley Algorithm for Stable Matching

        Parameters:

        suitor_prefs: dict - Dictionary of suitor preferences
        reviewer_prefs: dict - Dictionary of reviewer preferences

        Returns:

        matching: dict - Dictionary of suitor matching with reviewer
    '''

    matching = {}

    ## TODO: Implement the Gale-Shapley Algorithm
    free_suitors=[]
    for suitors in suitor_prefs:
        free_suitors.append(suitors)
    next_prop = {}
    for suitors in suitor_prefs:
        next_prop[suitors] = 0
    current_reviewer ={}
    for reviewer in reviewer_prefs:
        current_reviewer[reviewer]=None
    while free_suitors:
        suitors =free_suitors.pop(0)
        prop=suitor_prefs[suitors]
        reviewer=prop[next_prop[suitors]]
        next_prop[suitors]=next_prop[suitors]+1
        current_suitor = current_reviewer[reviewer]
        if current_suitor is None:
            matching[suitors]=reviewer
            current_reviewer[reviewer]=suitors
        else:
            reviewer_ranking = reviewer_prefs[reviewer]
            current_suitor_rank = reviewer_ranking.index(current_suitor)
            new_suitor_rank = reviewer_ranking.index(suitors)
            if new_suitor_rank<current_suitor_rank:
                matching[suitors] = reviewer
                current_reviewer[reviewer] = suitors
                free_suitors.append(current_suitor)
                del matching[current_suitor]
            else:
                free_suitors.append(suitors)

    ## END TODO

    return matching

def avg_suitor_ranking(suitor_prefs: Dict[str, List[str]], matching: Dict[str, str]) -> float:
    '''
        Calculate the average ranking of suitor in the matching
        
        Parameters:
        
        suitor_prefs: dict - Dictionary of suitor preferences
        matching: dict - Dictionary of matching
        
        Returns:
        
        avg_suitor_ranking: float - Average ranking of suitor
    '''

    avg_suitor_ranking = 0

    ## TODO: Implement the average suitor ranking calculation
    total_ranking=0
    for suitor in matching:
        reviewer=matching[suitor]
        pref_list=suitor_prefs[suitor]
        rank = 0
        for i in range(len(pref_list)):
            if pref_list[i]==reviewer:
                rank=i + 1
                break
        total_ranking+=rank

    avg_suitor_ranking= total_ranking / len(suitor_prefs)

    ## END TODO

    assert type(avg_suitor_ranking) == float

    return avg_suitor_ranking

def avg_reviewer_ranking(reviewer_prefs: Dict[str, List[str]], matching: Dict[str, str]) -> float:
    '''
        Calculate the average ranking of reviewer in the matching
        
        Parameters:
        
        reviewer_prefs: dict - Dictionary of reviewer preferences
        matching: dict - Dictionary of matching
        
        Returns:
        
        avg_reviewer_ranking: float - Average ranking of reviewer
    '''

    avg_reviewer_ranking = 0

    ## TODO: Implement the average reviewer ranking calculation
    total_ranking=0
    for suitor in matching:
        reviewer=matching[suitor]
        reviewer_prefs_list=reviewer_prefs[reviewer]
        rank = 0
        for i in range(len(reviewer_prefs_list)):
            if reviewer_prefs_list[i]==suitor:
                rank=i + 1
                break
        total_ranking=rank+total_ranking
    avg_reviewer_ranking =total_ranking / len(reviewer_prefs)
    ## END TODO

    assert type(avg_reviewer_ranking) == float

    return avg_reviewer_ranking

def get_preferences(file) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    '''
        Get the preferences from the file
        
        Parameters:
        
        file: file - File containing the preferences
        
        Returns:
        
        suitor_prefs: dict - Dictionary of suitor preferences
        reviewer_prefs: dict - Dictionary of reviewer preferences
    '''
    suitor_prefs = {}
    reviewer_prefs = {}

    for line in file:
        if line[0].islower():
            reviewer, prefs = line.strip().split(' : ')
            reviewer_prefs[reviewer] = prefs.split()

        else:
            suitor, prefs = line.strip().split(' : ')
            suitor_prefs[suitor] = prefs.split()
        
    return suitor_prefs, reviewer_prefs


if __name__ == '__main__':

    avg_suitor_ranking_list = []
    avg_reviewer_ranking_list = []

    for i in range(100):
        with open('data/data_'+str(i)+'.txt', 'r') as f:
            suitor_prefs, reviewer_prefs = get_preferences(f)

            # suitor_prefs = {
            #     'A': ['a', 'b', 'c'],
            #     'B': ['c', 'b', 'a'],
            #     'C': ['c', 'a', 'b']
            # }

            # reviewer_prefs = {
            #     'a': ['A', 'C', 'B'],
            #     'b': ['B', 'A', 'C'],
            #     'c': ['B', 'A', 'C']
            # }

            matching = Gale_Shapley(suitor_prefs, reviewer_prefs)

            avg_suitor_ranking_list.append(avg_suitor_ranking(suitor_prefs, matching))
            avg_reviewer_ranking_list.append(avg_reviewer_ranking(reviewer_prefs, matching))

    plt.hist(avg_suitor_ranking_list, bins=10, label='Suitor', alpha=0.5, color='r')
    plt.hist(avg_reviewer_ranking_list, bins=10, label='Reviewer', alpha=0.5, color='g')

    plt.xlabel('Average Ranking')
    plt.ylabel('Frequency')

    plt.legend()
    plt.savefig('q2.png')


    

