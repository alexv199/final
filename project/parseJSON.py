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
        team_types = ['home_team', 'away_team']
        for team_type in team_types:
            if team_type in match:
                team = match[team_type]
                if team not in teams: # check for new team
                    teams.append(team)


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
        just_player = {'player_id' : player['player_id'], 'name' : player['player_name'], 'nickname' : player['player_nickname'], 'country_id' : player['country']['id']}
        if just_player not in players: # check if it's a new player
            players.append(just_player)



### create dml file

# create a dml file to add matches data to soccer database 
dml = open('dml.sql', 'w')


# add referees to dml
to_write = 'INSERT INTO referees (referee_id, name, country_id) VALUES\n'

for referee in referees:
    to_write += '( ' + str(referee['id']) + ', "' + referee['name'] + '", "' + str(referee['country']['name']) + '" ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)


# add stadiums to dml
to_write = 'INSERT INTO stadiums (stadium_id, name, country_id) VALUES\n'

for stadium in stadiums:
    to_write += '( ' + str(stadium['id']) + ', "' + stadium['name'] + '", "' + str(stadium['country']['name']) + '" ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)


# add managers to dml
to_write = 'INSERT INTO managers (manager_id, name, nickname, dob, country_id) VALUES\n'

for manager in managers:
    nickname = str(manager['nickname'])
    if nickname != 'None':
        nickname = '"' + nickname + '"'
    else:
        nickname = 'null'
    to_write += '( ' + str(manager['id']) + ', "' + manager['name'] + '", ' + nickname + ', "' + manager['dob'] + '", "' + str(manager['country']['name']) + '" ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)



# teams are duplicated, need to remove duplicates
home_teams = []
away_teams = []

for team in teams: # split them into home and away
    if 'home_team_id' in team:
        home_teams.append(team)
    elif 'away_team_id' in team:
        away_teams.append(team)

teams = home_teams # remake teams list
unique_away_teams = []

# it's possible that some away teams never appeared as home teams, so check
for team in away_teams:
    away_id = team['away_team_id']
    in_home = [home_team for home_team in teams if home_team['home_team_id'] == away_id]
    #in_home = filter(lambda home_team : home_team['home_team_id'] == away_id, teams)
    if len(in_home) == 0:
        unique_away_teams.append(team)


# add teams to dml
to_write = 'INSERT INTO teams (team_id, name, gender, group, country_id) VALUES\n'

# add home teams
for team in teams:
    group = str(team['home_team_group'])
    if group != 'None':
        group = '"' + group + '"'
    else:
        group = 'null'
    to_write += '( ' + str(team['home_team_id']) + ', "' + team['home_team_name'] + '", "' + team['home_team_gender'] + '", ' + group + ', "' + str(team['country']['name']) + '" ),\n'

# add the away teams that did not appear in the home teams list
for team in unique_away_teams:
    group = str(team['away_team_group'])
    if group != 'None':
        group = '"' + group + '"'
    else:
        group = 'null'
    to_write += '( ' + str(team['away_team_id']) + ', "' + team['away_team_name'] + '", "' + team['away_team_gender'] + '", ' + group + ', "' + str(team['country']['name']) + '" ),\n'


to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)



# add competitions to dml
to_write = 'INSERT INTO competitions (competition_id, country_id, competition_name, competition_gender, competition_youth, competition_international) VALUES\n'

for competition in competitions:

    to_write += '( ' + str(competition['competition_id']) + ', "' + competition['country_name'] + '", "' + competition['competition_name'] + '", "' + competition['competition_gender'] + '", ' + str(competition['competition_youth']) + ', ' + str(competition['competition_international']) + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)



# add matches to dml
to_write = 'INSERT INTO matches (match_id, match_date, kick_off, competition_id, season_id, home_team_id, away_team_id, home_score, away_score, match_week, competition_stage_id, stadium_id, referee_id) VALUES\n'

for match in matches:
    stadium_id = 'null'
    if 'stadium' in match: # not an attribute of every match
        stadium_id = str(match['stadium']['id'])
    referee_id = 'null'
    if 'referee' in match: # not an attribute of every match
        referee_id = str(match['referee']['id'])

    to_write += '( ' + str(match['match_id']) + ', "' + match['match_date'] + '", "' + match['kick_off'] + '", ' + str(match['competition']['competition_id']) + ', "' + str(match['season']['season_name']) + '", ' + str(match['home_team']['home_team_id']) + ', ' + str(match['away_team']['away_team_id']) + ', ' + str(match['home_score']) + ', ' + str(match['away_score']) + ', ' + str(match['match_week']) + ', "' + str(match['competition_stage']['name']) + '", ' + stadium_id + ', ' + referee_id + ' ),\n'

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
to_write = 'INSERT INTO players (player_id, name, nickname, country_id) VALUES\n'

for player in players:
    nickname = 'null'
    if str(player['nickname']) != 'None':
        nickname = '"' + player['nickname'] +'"'
    to_write += '( ' + str(player['player_id']) + ', "' + player['name'] + '", ' + nickname + ', ' + str(player['country_id']) + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)


# add match lineups to dml
to_write = 'INSERT INTO lineups (match_id, team_id, player_id, cards, positions, jersey_number) VALUES\n'

for lineup in lineups:
    if lineup['cards'] == []:
        cards = 'null'
    else:
        cards = 'ARRAY['
        for c in lineup['cards']:
            time = '"' + str(c['time']) + '"'
            type_ = '"' + c['card_type'] + '"'
            reason = '"' + str(c['reason']) + '"'
            period = str(c['period'])
            card = '\'(' + time + ', ' + type_ + ', ' + reason + ', ' + period + ')\', '

            cards += player

        cards = cards[:-2] + ']'

    if lineup['positions'] == []:
        positions = 'null'
    else:
        positions = 'ARRAY['
        for p in lineup['positions']:
            position_name = '"' + p['position'] + '"'
            from_ = '"' + str(p['from']) + '"'
            to = '"' + str(p['to']) + '"'
            from_period = str(p['from_period'])
            to_period = str(p['to_period'])
            start_reason = '"' + p['start_reason'] + '"'
            end_reason = '"' + p['end_reason'] + '"'
            position = '\'(' + position_name + ', ' + from_ + ', ' + to + ', ' + from_period + ', ' + to_period + ', ' + start_reason + ', ' + end_reason + ')\', '

            cards += player

        cards = cards[:-2] + ']'

    to_write += '( ' + str(lineup['match_id']) + ', ' + str(player['team_id']) + ', ' + str(player['player_id']) + ', ' + str(player['jersey_number']) + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)

'''CREATE TABLE lineups (
    match_id            integer REFERENCES matches,
    team_id             integer REFERENCES teams,
    player_id           integer REFERENCES players,
    cards               card[],
    positions           position[],
    jersey_number       integer
);'''

# close the file
dml.close()


