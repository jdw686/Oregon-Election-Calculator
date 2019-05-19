import pandas as pd
import numpy as np

voting_groups = pd.read_csv('Oregon Districts.csv', index_col = 'District')
voting_groups['Left'] = ((voting_groups['Left']/(voting_groups['Left'] + voting_groups['Right']))*100).astype(int)
voting_groups['Right'] = 100 - voting_groups['Left']

def election_program(political_parties = 5):
    def voting():
        parties = []
        for i in range(political_parties):
            parties.append(input("Enter a Political Party: "))
        matrix = []
        for i in range(len(voting_groups.columns)):
            a = []
            for j in range(len(parties)):
                a.append(int(input(f'{parties[j]}, {voting_groups.columns[i]}: ')))
            matrix.append(a)
        voting_matrix = pd.DataFrame(data = matrix, index = voting_groups.columns, columns = parties)
        return voting_matrix

    voting_preference = voting()

    def party_level():
        party_matrix = []
        for i in range(len(voting_preference.columns)):
            level = int(input(f'Set Major Party Threshold for {voting_preference.columns[i]}: '))
            party_level = [np.random.randint(95, 105) / 100 if j > level else
             (np.random.randint(75, 90) / 100 if j <= level and j > level*(2/3) else
              (np.random.randint(60, 70) / 100 if j <= level*(2/3) and j > level*(1/3) else
               (np.random.randint(50, 60) / 100 if j <= level*(1/3) and j > (level/4) else 0.01)))
                           for j in voting_groups[input("Left or Right: ")]]
            party_level_list = pd.Series(data = party_level)
            left_wing = 0 if (voting_preference.iloc[0, i] + (voting_preference.iloc[0, i] - voting_preference.iloc[0, :].std())) < 0  \
                    else (voting_preference.iloc[0, i] + (voting_preference.iloc[0, i] - voting_preference.iloc[0, :].std())) \
                         / (voting_preference.iloc[0, :].sum() ** (1/party_level_list)) * party_level_list
            right_wing = 0 if (voting_preference.iloc[1, i] + (voting_preference.iloc[1, i] - voting_preference.iloc[1, :].std())) < 0  \
                    else (voting_preference.iloc[1, i] + (voting_preference.iloc[1, i] - voting_preference.iloc[1, :].std())) \
                         / (voting_preference.iloc[1, :].sum() ** (1/party_level_list)) * party_level_list
            party_base = (left_wing + right_wing).round(4)
            party_matrix.append(party_base)
        party_matrix = pd.DataFrame(data = party_matrix)
        return party_matrix.transpose()

    testing = party_level()

    def votes():
        votes_matrix = []
        for i in range(len(voting_groups.index)):
            district_votes = []
            for j in range(len(voting_preference.columns)):
                votes = ((testing.iloc[i, j].sum()/testing.iloc[i, :].sum())*170000).astype(int)
                district_votes.append(votes)
            votes_matrix.append(district_votes)
        votes_matrix = pd.DataFrame(data = votes_matrix, index = voting_groups.index, columns = voting_preference.columns)
        votes_matrix['Seat Winner'] = votes_matrix.iloc[:, :].idxmax(axis = 1)
        return votes_matrix

    election_results = votes()
    return election_results

# here are some sample variables you can determine to run the program
# elections = election_program(political_parties = 3)
# seat_count = elections.groupby('Seat Winner')['Seat Winner'].count()
# vote_count = elections.iloc[:, 0:-1].sum()
# vote_share = (elections.iloc[:, 0:-1].sum()/elections.iloc[:, 0:-1].sum().sum())*100
#
# print(seat_count)
# print('='*20)
# print(vote_count)
# print('='*20)
# print(vote_share)