import pandas as pd
import numpy as np


def election_program(political_parties=5):
    voting_groups = pd.read_csv('Oregon Districts.csv', index_col='District')
    voting_groups['Left'] = ((voting_groups['Left']/(voting_groups['Left']+voting_groups['Right']))*100).astype(int)
    voting_groups['Right'] = 100-voting_groups['Left']

    def voting():
        parties = []
        for i in range(political_parties):
            parties.append(input("Enter a Political Party: "))
        matrix = []
        for i in range(0, 2):
            preference = []
            for j in range(len(parties)):
                preference.append(int(input(f'{parties[j]}, {voting_groups.columns[i+1]}: ')))
            matrix.append(preference)
        voting_matrix = pd.DataFrame(data=matrix, index=voting_groups.columns[1:], columns=parties)
        return voting_matrix

    voting_preference = voting()

    def party_strength():
        party_matrix = []
        for i in range(len(voting_preference.columns)):
            position = input(f'Is {voting_preference.columns[i]} Left or Right?: ')
            position_dict = {"Major": voting_groups[position].mean(),
                             "Competitive": voting_groups[position].mean() - voting_groups[position].std(),
                             "Minor": voting_groups[position].mean() - 3 * voting_groups[position].std()}
            major = np.random.randint(95, 105)/100
            competitive = np.random.randint(80, 95)/100
            minor = np.random.randint(65, 80)/100
            small = np.random.randint(50, 65)/100
            party_level = [major if j > position_dict['Major'] else
                           (competitive if j <= position_dict['Major'] and j > position_dict['Competitive'] else
                            (minor if j <= position_dict['Competitive'] and j > position_dict['Minor'] else
                             (small))) for j in voting_groups[position]]
            party_level_list = pd.Series(data=party_level)
            left = 0 if (voting_preference.iloc[0, i] + (voting_preference.iloc[0, i] - voting_preference.iloc[0, :].std())) < 0 else (voting_preference.iloc[0, i] + (voting_preference.iloc[0, i] - voting_preference.iloc[0, :].std()))/(voting_preference.iloc[0, :].sum() ** (1 / party_level_list.values)) * party_level_list.values
            right = 0 if (voting_preference.iloc[1, i] + (voting_preference.iloc[1, i] - voting_preference.iloc[1, :].std())) < 0 else (voting_preference.iloc[1, i] + (voting_preference.iloc[1, i] - voting_preference.iloc[1, :].std())) / (voting_preference.iloc[1, :].sum() ** (1 / party_level_list.values)) * party_level_list.values
            party_matrix.append((left+right).round(4))
        party_matrix = pd.DataFrame(data=party_matrix)
        return party_matrix.transpose()

    strength = party_strength()

    def votes():
        votes_matrix = []
        for i in range(len(voting_groups.index)):
            district_votes = []
            for j in range(len(voting_preference.columns)):
                vote_totals = ((strength.iloc[i, j].sum() / strength.iloc[i, :].sum()) *
                               voting_groups.iloc[i, 0]).astype(int)
                district_votes.append(vote_totals)
            votes_matrix.append(district_votes)
        votes_matrix = pd.DataFrame(data=votes_matrix, index=voting_groups.index, columns=voting_preference.columns)
        votes_matrix['Seat Winner'] = votes_matrix.iloc[:, :].idxmax(axis=1)
        return votes_matrix

    election_results = votes()
    return election_results.to_excel()

    election_results

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
