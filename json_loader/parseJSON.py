import json # for parsing json files
import os # to iterate over files in directory

# get data from competition file
competition_file = open('competitions.json')
competitions = json.load(competition_file)

# get unique competitions
unique_comps = []
for competition in competitions:
    is_unique = True
    for unique_comp in unique_comps:
        if competition['competition_id'] == unique_comp['competition_id']:
            is_unique = False

    if is_unique:
        unique_comps.append(competition)

competitions = unique_comps
competition_file.close()


# get data from matches files
match_files = ['matches/2/44.json', 'matches/11/4.json', 'matches/11/42.json', 'matches/11/90.json']
teams = [] # currently all teams are in duplicate as 'home_team' and 'away_team'. Fixed when creating dml later
managers = []
stadiums = []
referees = []
matches = []

for file_path in match_files:
    file = open(file_path)

    data = json.load(file)
    for match in data:
        matches.append(match)

        # get teams
        home_team = {'team_id' : match['home_team']['home_team_id'], 'name' : match['home_team']['home_team_name'], 'gender' : match['home_team']['home_team_gender'], 'country' : match['home_team']['country']['name']}
        if home_team not in teams: # check for new team
            teams.append(home_team)

        away_team = {'team_id' : match['away_team']['away_team_id'], 'name' : match['away_team']['away_team_name'], 'gender' : match['away_team']['away_team_gender'], 'country' : match['away_team']['country']['name']}
        if away_team not in teams:
            teams.append(away_team)


        # get other data
        team_types = ['home_team', 'away_team']
        for team_type in team_types:
            if team_type in match:
                team = match[team_type]


                if 'managers' in team:
                    team_managers = team['managers'] # this returns an array
                    for manager in team_managers:
                        if manager not in managers: # check for new manager
                            managers.append(manager)
                            #managers_by_team.append({'team_id': team[team_type + '_id'], 'manager': manager})
        
        if 'stadium' in match:
            stadium = match['stadium']
            if stadium not in stadiums: # check for new stadiums
                stadiums.append(stadium)

        if 'referee' in match:
            referee = match['referee']
            if referee not in referees: # check for new referees
                referees.append(referee)

    file.close()


# get data from lineups directory
directory = os.fsencode('lineups/')

lineups = []
for file in os.listdir(directory):
    filename = os.fsdecode(directory + file)

    file = open(filename)
    data = json.load(file)
    
    #match id is the file name
    match_id, ext = filename.split('.', 1)
    dir, match_id = match_id.split('/', 1)
    for lineup in data: # 
        lineups.append({'match_id' : match_id, 'lineup' : lineup})

    file.close()

# the list of things we want to track for storing in the database
players = [] # a list of players, independent of teams or matches

for team in lineups:
    match_id = team['match_id']
    #team_id = team['lineup']['team_id']
    lineup = team['lineup']['lineup']
    for player in lineup:
        # extract player specific info
        just_player = {'player_id' : player['player_id'], 'name' : player['player_name'], 'nickname' : player['player_nickname'], 'country' : player['country']['name']}
        if just_player not in players: # check if it's a new player
            players.append(just_player)



### create dml file

# create a dml file to add matches data to soccer database 
dml = open('dml.sql', 'w')


# add referees to dml
to_write = 'INSERT INTO referees (referee_id, name, country) VALUES\n'

for referee in referees:
    to_write += '( ' + str(referee['id']) + ', \'' + referee['name'] + '\', \'' + str(referee['country']['name']) + '\' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)


# add stadiums to dml
to_write = 'INSERT INTO stadiums (stadium_id, name, country) VALUES\n'

for stadium in stadiums:
    to_write += '( ' + str(stadium['id']) + ', \'' + stadium['name'] + '\', \'' + str(stadium['country']['name']) + '\' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)


# add managers to dml
to_write = 'INSERT INTO managers (manager_id, name, nickname, dob, country) VALUES\n'

for manager in managers:
    nickname = str(manager['nickname'])
    if nickname != 'None':
        nickname = '\'' + nickname + '\''
    else:
        nickname = 'null'
    to_write += '( ' + str(manager['id']) + ', \'' + manager['name'] + '\', ' + nickname + ', \'' + manager['dob'] + '\', \'' + str(manager['country']['name']) + '\' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)



# add teams to dml
to_write = 'INSERT INTO teams (team_id, name, gender, country) VALUES\n'

# add home teams
for team in teams:
    
    to_write += '( ' + str(team['team_id']) + ', \'' + team['name'] + '\', \'' + team['gender'] + '\', \'' + str(team['country']) + '\' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)



# add competitions to dml
to_write = 'INSERT INTO competitions (competition_id, country, name, gender, youth, international) VALUES\n'

for competition in competitions:

    to_write += '( ' + str(competition['competition_id']) + ', \'' + competition['country_name'] + '\', \'' + competition['competition_name'] + '\', \'' + competition['competition_gender'] + '\', ' + str(competition['competition_youth']) + ', ' + str(competition['competition_international']) + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)



# add matches to dml
to_write = 'INSERT INTO matches (match_id, match_date, kick_off, competition_id, season, home_team_id, away_team_id, home_score, away_score, match_week, competition_stage_name, stadium_id, referee_id) VALUES\n'

for match in matches:
    stadium_id = 'null'
    if 'stadium' in match: # not an attribute of every match
        stadium_id = str(match['stadium']['id'])
    referee_id = 'null'
    if 'referee' in match: # not an attribute of every match
        referee_id = str(match['referee']['id'])

    to_write += '( ' + str(match['match_id']) + ', \'' + match['match_date'] + '\', \'' + match['kick_off'] + '\', ' + str(match['competition']['competition_id']) + ', \'' + str(match['season']['season_name']) + '\', ' + str(match['home_team']['home_team_id']) + ', ' + str(match['away_team']['away_team_id']) + ', ' + str(match['home_score']) + ', ' + str(match['away_score']) + ', ' + str(match['match_week']) + ', \'' + str(match['competition_stage']['name']) + '\', ' + stadium_id + ', ' + referee_id + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)


# connect managers by team and match
to_write = 'INSERT INTO managers_by_team_and_match (match_id, team_id, manager_id) VALUES\n'

for match in matches:
    # managers from home teams
    managers = []
    if 'managers' in match['home_team']:
        for manager in match['home_team']['managers']:
            managers.append(manager)

    for manager in managers:
        to_write += '( ' + str(match['match_id']) + ', ' + str(match['home_team']['home_team_id']) + ', ' + str(manager['id']) + ' ),\n'

    # managers from away teams
    managers = []
    if 'managers' in match['away_team']:
        for manager in match['away_team']['managers']:
            managers.append(manager)
    
    for manager in managers:
        to_write += '( ' + str(match['match_id']) + ', ' + str(match['away_team']['away_team_id']) + ', ' + str(manager['id']) + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)


# add players to dml
to_write = 'INSERT INTO players (player_id, name, nickname, country) VALUES\n'

for player in players:
    name = player['name']
    if "'" in name:
        parts = name.split("'")
        name = ''
        for p in parts:
            if p != '':
                name += p + '\'\''
        name = name[:-2]

    nickname = 'null'
    if str(player['nickname']) != 'None':
        nickname = player['nickname']
        if "'" in nickname:
            parts = nickname.split("'")
            nickname = ''
            for p in parts:
                if p != '':
                    nickname += p + '\'\''
            nickname = nickname[:-2]

    country = player['country']
    if "'" in country:
        parts = country.split("'")
        country = ''
        for p in parts:
            if p != '':
                country += p + '\'\''
        country = country[:-2]

    to_write += '( ' + str(player['player_id']) + ', \'' + name + '\', \'' + nickname + '\', \'' + country + '\' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)


# add match lineups to dml
to_write = 'INSERT INTO lineups (match_id, team_id, player_id, jersey_number, cards, positions) VALUES\n'

for match in lineups:
    for player in match['lineup']['lineup']:
        if player['cards'] == []:
            cards = 'null'
        else:
            cards = 'ARRAY['
            for c in player['cards']:
                time = '\'' + str(c['time']) + '\''
                type_ = '\'' + c['card_type'] + '\''
                reason = '\'' + str(c['reason']) + '\''
                period = str(c['period'])
                card = '(' + time + ', ' + type_ + ', ' + reason + ', ' + period + ')::card, '

                cards += card

            cards = cards[:-2] + ']'

        if player['positions'] == []:
            positions = 'null'
        else:
            positions = 'ARRAY['
            for p in player['positions']:
                position_name = '\'' + p['position'] + '\''

                from_ = str(p['from'])
                if from_ == 'None':
                    from_ = 'null'
                else:
                    from_ = '\'' + from_ + '\''

                to = str(p['to'])
                if to == 'None':
                    to = 'null'
                else:
                    to = '\'' + to + '\''

                from_period = str(p['from_period'])
                if from_period == 'None':
                    from_period = 'null'
                to_period = str(p['to_period'])
                if to_period == 'None':
                    to_period = 'null'
                start_reason = '\'' + p['start_reason'] + '\''
                if start_reason == 'None':
                    start_reason = 'null'
                end_reason = '\'' + p['end_reason'] + '\''
                if end_reason == 'None':
                    end_reason = 'null'

                position = '(' + position_name + ', ' + from_ + ', ' + to + ', ' + from_period + ', ' + to_period + ', ' + start_reason + ', ' + end_reason + ')::"position", '

                positions += position

            positions = positions[:-2] + ']'

            to_write += '( ' + str(match['match_id']) + ', ' + str(match['lineup']['team_id']) + ', ' + str(player['player_id']) + ', ' + str(player['jersey_number']) + ', ' + cards + ', ' + positions + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)


# close the file
dml.close()


