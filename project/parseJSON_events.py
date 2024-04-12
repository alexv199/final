import json # for parsing json files
import os # to iterate over files in directory


# get data from events directory
directory = os.fsencode('events/')

events = {'33' : [], '24' : [], '42' : [], '2' : [], '6' : [], '43' : [], '9' : [], '3' : [], '14' : [], '39' : [], '4' : [], '37' : [], '22' : [], '21' : [], '23' : [], '34' : [], '18' : [], '40' : [], '10' : [], '38' : [], '8' : [], '20' : [], '25' : [], '30' : [], '27' : [], '26' : [], '17' : [], '41' : [], '28' : [], '16' : [], '35' : [], '19' : [], '36' : []}

related_events = [] # pairs of related events
related_events_by_match = []
events_by_type = [] # a list of event ids and their type id
duration_count = 0 # for debugging

for file in os.listdir(directory):
    filename = os.fsdecode(directory + file)

    file = open(filename)
    data = json.load(file)

    match_id, ext = filename.split('.', 1)
    dir, match_id = match_id.split('/', 1)

    related_events += related_events_by_match
    related_events_by_match = []
    print(len(related_events))

    for e in data:
        # need event type specific data
        type_id = e['type']['id']
#        if type_id != 36: # for debugging
#            continue

#        events_by_type.append({'event_id' : e['id'], 'type' : type_id})

        if 'related_events' in e:
            for rel_event in e['related_events']:
                event_id0 = {'event_id' : e['id'], 'other_event_id' : rel_event}
                event_id1 = {'event_id' : rel_event, 'other_event_id' : e['id']}
                if event_id1 not in related_events_by_match: # don't track the same pair twice
                    related_events_by_match.append(event_id0)

        continue # for debugging
        if type_id == 33: # 50/50

            if 'player' in e:
                player_id = e['player']['id']
            else:
                player_id = 'null'

            if 'position' in e:
                position = e['position']['name']
            else:
                position = 'null'

            if 'location' in e:
                location = e['location']
            else:
                location = 'null'

            if 'under_pressure' in e:
                under_pressure = e['under_pressure']
            else:
                under_pressure = 'False'

            if 'out' in e:
                out = e['out']
            else:
                out = 'False'

            if 'counterpress' in e:
                counterpress = e['counterpress']
            else:
                counterpress = 'False'

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'period' : e['period'], 'timestamp' : e['timestamp'], 'possession' : e['possession'], 'possession_team_id': e['possession_team']['id'], 'play_pattern' : e['play_pattern']['name'], 'team_id' : e['team']['id'], 'player_id' : player_id, 'position' : position, 'location' : location, 'under_pressure' : under_pressure, 'out' : out, 'outcome' : e['50_50']['outcome']['name'], 'counterpress' : counterpress}
            
            events['33'].append(event)


        elif type_id == 24: # bad behaviour

            if 'player' in e:
                player_id = e['player']['id']
            else:
                player_id = 'null'

            if 'position' in e:
                position = e['position']['name']
            else:
                position = 'null'

            if 'off_camera' in e:
                off_camera = e['off_camera']
            else:
                off_camera = 'False'

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'period' : e['period'], 'timestamp' : e['timestamp'], 'possession' : e['possession'], 'possession_team_id': e['possession_team']['id'], 'play_pattern' : e['play_pattern']['name'], 'team_id' : e['team']['id'], 'player_id' : player_id, 'position' : position, 'off_camera' : off_camera, 'card' : e['bad_behaviour']['card']['name']}
            
            events['24'].append(event)

            
        elif type_id == 42: # ball receipt

            if 'player' in e:
                player_id = e['player']['id']
            else:
                player_id = 'null'

            if 'position' in e:
                position = e['position']['name']
            else:
                position = 'null'

            if 'location' in e:
                location = e['location']
            else:
                location = 'null'

            if 'under_pressure' in e:
                under_pressure = e['under_pressure']
            else:
                under_pressure = 'False'

            if 'ball_receipt' in e:
                outcome = e['ball_receipt']['outcome']['name']
            else:
                outcome = 'null'

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'period' : e['period'], 'timestamp' : e['timestamp'], 'possession' : e['possession'], 'possession_team_id': e['possession_team']['id'], 'play_pattern' : e['play_pattern']['name'], 'team_id' : e['team']['id'], 'player_id' : player_id, 'position' : position, 'location' : location, 'under_pressure' : under_pressure, 'outcome' : outcome}
            
            events['42'].append(event)
            

        elif type_id == 2: # ball recovery

            if 'player' in e:
                player_id = e['player']['id']
            else:
                player_id = 'null'

            if 'position' in e:
                position = e['position']['name']
            else:
                position = 'null'

            if 'location' in e:
                location = e['location']
            else:
                location = 'null'

            if 'under_pressure' in e:
                under_pressure = e['under_pressure']
            else:
                under_pressure = 'False'

            if 'off_camera' in e:
                off_camera = e['off_camera']
            else:
                off_camera = 'False'

            if 'out' in e:
                out = e['out']
            else:
                out = 'False'

            # recovery failure and offensive are  not always recorded
            offensive = 'False'
            recovery_failure = 'False'
            if 'ball_recovery' in e:
                ball_recovery = e['ball_recovery']
                if 'offensive' in ball_recovery:
                    offensive = ball_recovery['offensive']
                if 'recovery_failure' in ball_recovery:
                    recovery_failure = ball_recovery['recovery_failure']

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'period' : e['period'], 'timestamp' : e['timestamp'], 'possession' : e['possession'], 'possession_team_id': e['possession_team']['id'], 'play_pattern' : e['play_pattern']['name'], 'team_id' : e['team']['id'], 'player_id' : player_id, 'position' : position, 'location' : location, 'under_pressure' : under_pressure, 'off_camera' : off_camera, 'out' : out, 'offensive' : offensive, 'recovery_failure' : recovery_failure}
            
            events['2'].append(event)
            

        elif type_id == 6: # block
            if 'player' in e:
                player_id = e['player']['id']
            else:
                player_id = 'null'

            if 'position' in e:
                position = e['position']['name']
            else:
                position = 'null'

            if 'location' in e:
                location = e['location']
            else:
                location = 'null'

            if 'under_pressure' in e:
                under_pressure = e['under_pressure']
            else:
                under_pressure = 'False'

            if 'off_camera' in e:
                off_camera = e['off_camera']
            else:
                off_camera = 'False'

            if 'out' in e:
                out = e['out']
            else:
                out = 'False'

            if 'counterpress' in e:
                counterpress = e['counterpress']
            else:
                counterpress = 'False'

            deflection = 'False'
            save_block = 'False'
            offensive = 'False'
            if 'block' in e:
                block = e['block']
                if 'deflection' in block:
                    deflection = block['deflection']

                if 'save_block' in block:
                    save_block = block['save_block']

                if 'offensive' in block:
                    offensive = block['offensive']
                

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'period' : e['period'], 'timestamp' : e['timestamp'], 'possession' : e['possession'], 'possession_team_id': e['possession_team']['id'], 'play_pattern' : e['play_pattern']['name'], 'team_id' : e['team']['id'], 'player_id' : player_id, 'position' : position, 'location' : location, 'under_pressure' : under_pressure, 'off_camera' : off_camera, 'out' : out, 'counterpress' : counterpress, 'deflection' : deflection, 'save_block' : save_block, 'offensive' : offensive}
            
            events['6'].append(event)


        elif type_id == 43: # carry

            if 'player' in e:
                player_id = e['player']['id']
            else:
                player_id = 'null'

            if 'position' in e:
                position = e['position']['name']
            else:
                position = 'null'

            if 'location' in e:
                location = e['location']
            else:
                location = 'null'

            if 'duration' in e:
                duration = e['duration']
            else:
                duration = 'null'

            if 'under_pressure' in e:
                under_pressure = e['under_pressure']
            else:
                under_pressure = 'False'

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'period' : e['period'], 'timestamp' : e['timestamp'], 'possession' : e['possession'], 'possession_team_id': e['possession_team']['id'], 'play_pattern' : e['play_pattern']['name'], 'team_id' : e['team']['id'], 'player_id' : player_id, 'position' : position, 'location' : location, 'duration' : duration, 'under_pressure' : under_pressure, 'end_location' : e['carry']['end_location']}
            
            events['43'].append(event)

            
        elif type_id == 9: # clearance

            if 'player' in e:
                player_id = e['player']['id']
            else:
                player_id = 'null'

            if 'position' in e:
                position = e['position']['name']
            else:
                position = 'null'

            if 'location' in e:
                location = e['location']
            else:
                location = 'null'

            if 'under_pressure' in e:
                under_pressure = e['under_pressure']
            else:
                under_pressure = 'False'

            if 'off_camera' in e:
                off_camera = e['off_camera']
            else:
                off_camera = 'False'

            if 'out' in e:
                out = e['out']
            else:
                out = 'False'

            clearance = e['clearance']
            if 'aerial_won' in clearance:
                aerial_won = clearance['aerial_won']
            else:
                aerial_won = 'False'

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'period' : e['period'], 'timestamp' : e['timestamp'], 'possession' : e['possession'], 'possession_team_id': e['possession_team']['id'], 'play_pattern' : e['play_pattern']['name'], 'team_id' : e['team']['id'], 'player_id' : player_id, 'position' : position, 'location' : location, 'under_pressure' : under_pressure, 'off_camera' : off_camera, 'out' : out, 'aerial_won' : aerial_won, 'body_part' : clearance['body_part']['name']}
            
            events['9'].append(event)

            
        elif type_id == 3: # dispossessed

            if 'player' in e:
                player_id = e['player']['id']
            else:
                player_id = 'null'

            if 'position' in e:
                position = e['position']['name']
            else:
                position = 'null'

            if 'location' in e:
                location = e['location']
            else:
                location = 'null'

            if 'under_pressure' in e:
                under_pressure = e['under_pressure']
            else:
                under_pressure = 'False'

            if 'off_camera' in e:
                off_camera = e['off_camera']
            else:
                off_camera = 'False'

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'period' : e['period'], 'timestamp' : e['timestamp'], 'possession' : e['possession'], 'possession_team_id': e['possession_team']['id'], 'play_pattern' : e['play_pattern']['name'], 'team_id' : e['team']['id'], 'player_id' : player_id, 'position' : position, 'location' : location, 'under_pressure' : under_pressure, 'off_camera' : off_camera}
            
            events['3'].append(event)


        elif type_id == 14: # dribble

            if 'player' in e:
                player_id = e['player']['id']
            else:
                player_id = 'null'

            if 'position' in e:
                position = e['position']['name']
            else:
                position = 'null'

            if 'location' in e:
                location = e['location']
            else:
                location = 'null'

            if 'under_pressure' in e:
                under_pressure = e['under_pressure']
            else:
                under_pressure = 'False'

            if 'off_camera' in e:
                off_camera = e['off_camera']
            else:
                off_camera = 'False'

            if 'out' in e:
                out = e['out']
            else:
                out = 'False'

            dribble = e['dribble']
            if 'nutmeg' in dribble:
                nutmeg = dribble['nutmeg']
            else:
                nutmeg = 'False'

            if 'overrun' in dribble:
                overrun = dribble['overrun']
            else:
                overrun = 'False'

            if 'no_touch' in dribble:
                no_touch = dribble['no_touch']
            else:
                no_touch = 'False'

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'period' : e['period'], 'timestamp' : e['timestamp'], 'possession' : e['possession'], 'possession_team_id': e['possession_team']['id'], 'play_pattern' : e['play_pattern']['name'], 'team_id' : e['team']['id'], 'player_id' : player_id, 'position' : position, 'location' : location, 'under_pressure' : under_pressure, 'off_camera' : off_camera, 'out' : out, 'outcome' : dribble['outcome']['name'], 'nutmeg' : nutmeg, 'overrun' : overrun, 'no_touch' : no_touch}
            
            events['14'].append(event)


        elif type_id == 39: # dribbled past

            if 'player' in e:
                player_id = e['player']['id']
            else:
                player_id = 'null'

            if 'position' in e:
                position = e['position']['name']
            else:
                position = 'null'

            if 'location' in e:
                location = e['location']
            else:
                location = 'null'

            if 'off_camera' in e:
                off_camera = e['off_camera']
            else:
                off_camera = 'False'

            if 'counterpress' in e:
                counterpress = e['counterpress']
            else:
                counterpress = 'False'

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'period' : e['period'], 'timestamp' : e['timestamp'], 'possession' : e['possession'], 'possession_team_id': e['possession_team']['id'], 'play_pattern' : e['play_pattern']['name'], 'team_id' : e['team']['id'], 'player_id' : player_id, 'position' : position, 'location' : location, 'off_camera' : off_camera, 'counterpress' : counterpress}
            
            events['39'].append(event)


        elif type_id == 4: # duel

            if 'player' in e:
                player_id = e['player']['id']
            else:
                player_id = 'null'

            if 'position' in e:
                position = e['position']['name']
            else:
                position = 'null'

            if 'location' in e:
                location = e['location']
            else:
                location = 'null'

            if 'under_pressure' in e:
                under_pressure = e['under_pressure']
            else:
                under_pressure = 'False'

            if 'off_camera' in e:
                off_camera = e['off_camera']
            else:
                off_camera = 'False'

            if 'counterpress' in e:
                counterpress = e['counterpress']
            else:
                counterpress = 'False'

            duel = e['duel']
            if 'outcome' in duel:
                outcome = duel['outcome']['name']
            else:
                outcome = 'null'

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'period' : e['period'], 'timestamp' : e['timestamp'], 'possession' : e['possession'], 'possession_team_id': e['possession_team']['id'], 'play_pattern' : e['play_pattern']['name'], 'team_id' : e['team']['id'], 'player_id' : player_id, 'position' : position, 'location' : location, 'under_pressure' : under_pressure, 'off_camera' : off_camera, 'counterpress' : counterpress, 'type' : duel['type']['name'], 'outcome' : outcome}
            
            events['4'].append(event)


        elif type_id == 37: # error

            if 'player' in e:
                player_id = e['player']['id']
            else:
                player_id = 'null'

            if 'position' in e:
                position = e['position']['name']
            else:
                position = 'null'

            if 'location' in e:
                location = e['location']
            else:
                location = 'null'

            if 'under_pressure' in e:
                under_pressure = e['under_pressure']
            else:
                under_pressure = 'False'

            if 'off_camera' in e:
                off_camera = e['off_camera']
            else:
                off_camera = 'False'

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'period' : e['period'], 'timestamp' : e['timestamp'], 'possession' : e['possession'], 'possession_team_id': e['possession_team']['id'], 'play_pattern' : e['play_pattern']['name'], 'team_id' : e['team']['id'], 'player_id' : player_id, 'position' : position, 'location' : location, 'under_pressure' : under_pressure, 'off_camera' : off_camera}
            
            events['37'].append(event)


        elif type_id == 22: # foul committed

            if 'player' in e:
                player_id = e['player']['id']
            else:
                player_id = 'null'

            if 'position' in e:
                position = e['position']['name']
            else:
                position = 'null'

            if 'location' in e:
                location = e['location']
            else:
                location = 'null'

            if 'under_pressure' in e:
                under_pressure = e['under_pressure']
            else:
                under_pressure = 'False'

            if 'off_camera' in e:
                off_camera = e['off_camera']
            else:
                off_camera = 'False'

            if 'counterpress' in e:
                counterpress = e['counterpress']
            else:
                counterpress = 'False'

            advantage = 'False'
            offensive = 'False'
            penalty = 'False'
            card = 'null'
            type = 'null'

            if 'foul_committed' in e:
                foul_committed = e['foul_committed']
                if 'advantage' in foul_committed:
                    advantage = foul_committed['advantage']
                if 'offensive' in foul_committed:
                    offensive = foul_committed['offensive']
                if 'penalty' in foul_committed:
                    penalty = foul_committed['penalty']            
                if 'card' in foul_committed:
                    card = foul_committed['card']['name']
                if 'type' in foul_committed:
                    type = foul_committed['type']['name']

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'period' : e['period'], 'timestamp' : e['timestamp'], 'possession' : e['possession'], 'possession_team_id': e['possession_team']['id'], 'play_pattern' : e['play_pattern']['name'], 'team_id' : e['team']['id'], 'player_id' : player_id, 'position' : position, 'location' : location, 'under_pressure' : under_pressure, 'off_camera' : off_camera, 'advantage' : advantage, 'counterpress' : counterpress, 'offensive' : offensive, 'penalty' : penalty, 'card' : card, 'type' : type}
            
            events['22'].append(event)


        elif type_id == 21: # foul won

            if 'player' in e:
                player_id = e['player']['id']
            else:
                player_id = 'null'

            if 'position' in e:
                position = e['position']['name']
            else:
                position = 'null'

            if 'location' in e:
                location = e['location']
            else:
                location = 'null'

            if 'under_pressure' in e:
                under_pressure = e['under_pressure']
            else:
                under_pressure = 'False'

            if 'off_camera' in e:
                off_camera = e['off_camera']
            else:
                off_camera = 'False'

            advantage = 'False'
            defensive = 'False'
            penalty = 'False'

            if 'foul_won' in e:
                foul_won = e['foul_won']
                if 'advantage' in foul_won:
                    advantage = foul_won['advantage']
                if 'defensive' in foul_won:
                    defensive = foul_won['defensive']
                if 'penalty' in foul_won:
                    penalty = foul_won['penalty']            

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'period' : e['period'], 'timestamp' : e['timestamp'], 'possession' : e['possession'], 'possession_team_id': e['possession_team']['id'], 'play_pattern' : e['play_pattern']['name'], 'team_id' : e['team']['id'], 'player_id' : player_id, 'position' : position, 'location' : location, 'under_pressure' : under_pressure, 'off_camera' : off_camera, 'advantage' : advantage, 'defensive' : defensive, 'penalty' : penalty}
            
            events['21'].append(event)


        elif type_id == 23: # goal keeper

            if 'player' in e:
                player_id = e['player']['id']
            else:
                player_id = 'null'

            if 'position' in e:
                position = e['position']['name']
            else:
                position = 'null'

            if 'location' in e:
                location = e['location']
            else:
                location = 'null'

            if 'under_pressure' in e:
                under_pressure = e['under_pressure']
            else:
                under_pressure = 'False'

            if 'off_camera' in e:
                off_camera = e['off_camera']
            else:
                off_camera = 'False'

            if 'out' in e:
                out = e['out']
            else:
                out = 'False'

            goalkeeper = e['goalkeeper']
            if 'position' in goalkeeper:
                goalkeeper_position = goalkeeper['position']['name']
            else:
                goalkeeper_position = 'null'
            if 'technique' in goalkeeper:
                technique = goalkeeper['technique']['name']
            else:
                technique = 'null'
            if 'body_part' in goalkeeper:
                body_part = goalkeeper['body_part']['name']
            else:
                body_part = 'null'
            if 'type' in goalkeeper:
                type_ = goalkeeper['type']['name']
            else:
                type_ = 'null'
            
            if 'outcome' in goalkeeper:
                outcome = goalkeeper['outcome']['name']
            else:
                outcome = 'null'

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'period' : e['period'], 'timestamp' : e['timestamp'], 'possession' : e['possession'], 'possession_team_id': e['possession_team']['id'], 'play_pattern' : e['play_pattern']['name'], 'team_id' : e['team']['id'], 'player_id' : player_id, 'position' : position, 'location' : location, 'under_pressure' : under_pressure, 'off_camera' : off_camera, 'out' : out, 'goalkeeper_position' : goalkeeper_position, 'technique' : technique, 'body_part' : body_part, 'type' : type_, 'outcome' : outcome}
            
            events['23'].append(event)


        elif type_id == 34: # half end

            if 'under_pressure' in e:
                under_pressure = e['under_pressure']
            else:
                under_pressure = 'False'

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'period' : e['period'], 'timestamp' : e['timestamp'], 'possession' : e['possession'], 'possession_team_id': e['possession_team']['id'], 'play_pattern' : e['play_pattern']['name'], 'team_id' : e['team']['id'], 'under_pressure' : under_pressure}
            
            events['34'].append(event)


        elif type_id == 18: # half start

            if 'under_pressure' in e:
                under_pressure = e['under_pressure']
            else:
                under_pressure = 'False'

            if 'half_start' in e:
                late_video_start = e['half_start']
            else:
                late_video_start = 'False'

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'period' : e['period'], 'possession' : e['possession'], 'possession_team_id': e['possession_team']['id'], 'play_pattern' : e['play_pattern']['name'], 'team_id' : e['team']['id'], 'under_pressure' : under_pressure, 'late_video_start' : late_video_start}
            
            events['18'].append(event)


        elif type_id == 40: # injury stoppage

            if 'player' in e:
                player_id = e['player']['id']
            else:
                player_id = 'null'

            if 'position' in e:
                position = e['position']['name']
            else:
                position = 'null'

            if 'under_pressure' in e:
                under_pressure = e['under_pressure']
            else:
                under_pressure = 'False'

            if 'off_camera' in e:
                off_camera = e['off_camera']
            else:
                off_camera = 'False'

            if 'injury_stoppage' in e:
                in_chain = e['injury_stoppage']['in_chain']
            else:
                in_chain = 'False'

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'period' : e['period'], 'timestamp' : e['timestamp'], 'possession' : e['possession'], 'possession_team_id': e['possession_team']['id'], 'play_pattern' : e['play_pattern']['name'], 'team_id' : e['team']['id'], 'player_id' : player_id, 'position' : position, 'under_pressure' : under_pressure, 'off_camera' : off_camera, 'in_chain' : in_chain}
            
            events['40'].append(event)


        elif type_id == 10: # interception

            if 'player' in e:
                player_id = e['player']['id']
            else:
                player_id = 'null'

            if 'position' in e:
                position = e['position']['name']
            else:
                position = 'null'

            if 'location' in e:
                location = e['location']
            else:
                location = 'null'

            if 'under_pressure' in e:
                under_pressure = e['under_pressure']
            else:
                under_pressure = 'False'

            if 'off_camera' in e:
                off_camera = e['off_camera']
            else:
                off_camera = 'False'

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'period' : e['period'], 'timestamp' : e['timestamp'], 'possession' : e['possession'], 'possession_team_id': e['possession_team']['id'], 'play_pattern' : e['play_pattern']['name'], 'team_id' : e['team']['id'], 'player_id' : player_id, 'position' : position, 'location' : location, 'under_pressure' : under_pressure, 'off_camera' : off_camera, 'outcome' : e['interception']['outcome']['name']}
            
            events['10'].append(event)


        elif type_id == 38: # miscontrol

            if 'player' in e:
                player_id = e['player']['id']
            else:
                player_id = 'null'

            if 'position' in e:
                position = e['position']['name']
            else:
                position = 'null'

            if 'location' in e:
                location = e['location']
            else:
                location = 'null'

            if 'under_pressure' in e:
                under_pressure = e['under_pressure']
            else:
                under_pressure = 'False'

            if 'off_camera' in e:
                off_camera = e['off_camera']
            else:
                off_camera = 'False'

            if 'out' in e:
                out = e['out']
            else:
                out = 'False'

            if 'miscontrol' in e:
                aerial_won = e['miscontrol']['aerial_won']
            else:
                aerial_won = 'False'

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'period' : e['period'], 'timestamp' : e['timestamp'], 'possession' : e['possession'], 'possession_team_id': e['possession_team']['id'], 'play_pattern' : e['play_pattern']['name'], 'team_id' : e['team']['id'], 'player_id' : player_id, 'position' : position, 'location' : location, 'under_pressure' : under_pressure, 'off_camera' : off_camera, 'out' :  out, 'aerial_won' : aerial_won}
            
            events['38'].append(event)


        elif type_id == 8: # offside

            if 'player' in e:
                player_id = e['player']['id']
            else:
                player_id = 'null'

            if 'position' in e:
                position = e['position']['name']
            else:
                position = 'null'

            if 'location' in e:
                location = e['location']
            else:
                location = 'null'

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'period' : e['period'], 'timestamp' : e['timestamp'], 'possession' : e['possession'], 'possession_team_id': e['possession_team']['id'], 'play_pattern' : e['play_pattern']['name'], 'team_id' : e['team']['id'], 'player_id' : player_id, 'position' : position, 'location' : location}
            
            events['8'].append(event)


        elif type_id == 20: # own goal against

            if 'player' in e:
                player_id = e['player']['id']
            else:
                player_id = 'null'

            if 'position' in e:
                position = e['position']['name']
            else:
                position = 'null'

            if 'location' in e:
                location = e['location']
            else:
                location = 'null'

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'period' : e['period'], 'timestamp' : e['timestamp'], 'possession' : e['possession'], 'possession_team_id': e['possession_team']['id'], 'play_pattern' : e['play_pattern']['name'], 'team_id' : e['team']['id'], 'player_id' : player_id, 'position' : position, 'location' : location}
            
            events['20'].append(event)


        elif type_id == 25: # own goal for

            if 'player' in e:
                player_id = e['player']['id']
            else:
                player_id = 'null'

            if 'position' in e:
                position = e['position']['name']
            else:
                position = 'null'

            if 'location' in e:
                location = e['location']
            else:
                location = 'null'

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'period' : e['period'], 'timestamp' : e['timestamp'], 'possession' : e['possession'], 'possession_team_id': e['possession_team']['id'], 'play_pattern' : e['play_pattern']['name'], 'team_id' : e['team']['id'], 'player_id' : player_id, 'position' : position, 'location' : location}
            
            events['25'].append(event)


        elif type_id == 30: # pass

            if 'player' in e:
                player_id = e['player']['id']
            else:
                player_id = 'null'

            if 'position' in e:
                position = e['position']['name']
            else:
                position = 'null'

            if 'location' in e:
                location = e['location']
            else:
                location = 'null'

            if 'duration' in e:
                duration = e['duration']
            else:
                duration = 'null'

            if 'under_pressure' in e:
                under_pressure = e['under_pressure']
            else:
                under_pressure = 'False'

            if 'off_camera' in e:
                off_camera = e['off_camera']
            else:
                off_camera = 'False'

            if 'out' in e:
                out = e['out']
            else:
                out = 'False'

            p = e['pass']
            if 'recipient' in p:
                recipient = p['recipient']['id']
            else:
                recipient = 'null'
            length = p['length']
            angle = p['angle']
            height = p['height']['name']
            end_location = p['end_location']
            if 'assisted_shot_id' in p:
                assisted_shot_id = p['assisted_shot_id']
            else:
                assisted_shot_id = 'null'
            if 'backheel' in p:
                backheel = p['backheel']
            else:
                backheel = 'False'
            if 'deflected' in p:
                deflected = p['deflected']
            else:
                deflected = 'False'
            if 'miscommunication' in p:
                miscommunication = p['miscommunication']
            else:
                miscommunication = 'False'
            if 'cross' in p:
                cross = p['cross']
            else:
                cross = 'False'
            if 'cut_back' in p:
                cut_back = p['cut_back']
            else:
                cut_back = 'False'
            if 'switch' in p:
                switch = p['switch']
            else:
                switch = 'False'
            if 'shot_assist' in p:
                shot_assist = p['shot_assist']
            else:
                shot_assist = 'False'
            if 'goal_assist' in p:
                goal_assist = p['goal_assist']
            else:
                goal_assist = 'False'
            if 'body_part' in p:
                body_part = p['body_part']['name']
            else:
                body_part = 'null'
            if 'type' in p:
                type_ = p['type']['name']
            else:
                type_ = 'null'
            if 'outcome' in p:
                outcome = p['outcome']['name']
            else:
                outcome = 'null'
            if 'technique' in p:
                technique = p['technique']['name']
            else:
                technique = 'null'

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'period' : e['period'], 'timestamp' : e['timestamp'], 'possession' : e['possession'], 'possession_team_id': e['possession_team']['id'], 'play_pattern' : e['play_pattern']['name'], 'team_id' : e['team']['id'], 'player_id' : player_id, 'position' : position, 'location' : location, 'duration' : duration, 'under_pressure' : under_pressure, 'off_camera' : off_camera, 'out' : out, 'recipient' :recipient, 'length' : length, 'angle' : angle, 'height' : height, 'end_location' : end_location, 'assisted_shot_id' : assisted_shot_id, 'backheel' : backheel, 'deflected' : deflected, 'miscommunication' : miscommunication, 'cross' : cross, 'cut_back' : cut_back,  'switch' : switch, 'shot_assist' : shot_assist, 'goal_assist' : goal_assist, 'body_part' : body_part, 'type' : type_, 'outcome' : outcome, 'technique' : technique}
            
            events['30'].append(event)


        elif type_id == 27: # player off

            if 'player' in e:
                player_id = e['player']['id']
            else:
                player_id = 'null'

            if 'position' in e:
                position = e['position']['name']
            else:
                position = 'null'

            if 'off_camera' in e:
                off_camera = e['off_camera']
            else:
                off_camera = 'False'

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'period' : e['period'], 'timestamp' : e['timestamp'], 'possession' : e['possession'], 'possession_team_id': e['possession_team']['id'], 'play_pattern' : e['play_pattern']['name'], 'team_id' : e['team']['id'], 'player_id' : player_id, 'position' : position, 'off_camera' : off_camera}
            
            events['27'].append(event)


        elif type_id == 26: # player on

            if 'player' in e:
                player_id = e['player']['id']
            else:
                player_id = 'null'

            if 'position' in e:
                position = e['position']['name']
            else:
                position = 'null'

            if 'off_camera' in e:
                off_camera = e['off_camera']
            else:
                off_camera = 'False'

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'period' : e['period'], 'timestamp' : e['timestamp'], 'possession' : e['possession'], 'possession_team_id': e['possession_team']['id'], 'play_pattern' : e['play_pattern']['name'], 'team_id' : e['team']['id'], 'player_id' : player_id, 'position' : position, 'off_camera' : off_camera}
            
            events['26'].append(event)


        elif type_id == 17: # pressure

            if 'player' in e:
                player_id = e['player']['id']
            else:
                player_id = 'null'

            if 'position' in e:
                position = e['position']['name']
            else:
                position = 'null'

            if 'location' in e:
                location = e['location']
            else:
                location = 'null'

            if 'duration' in e:
                duration = e['duration']
            else:
                duration = 'null'

            if 'under_pressure' in e:
                under_pressure = e['under_pressure']
            else:
                under_pressure = 'False'

            if 'off_camera' in e:
                off_camera = e['off_camera']
            else:
                off_camera = 'False'

            if 'counterpress' in e:
                counterpress = e['counterpress']
            else:
                counterpress = 'False'

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'period' : e['period'], 'timestamp' : e['timestamp'], 'possession' : e['possession'], 'possession_team_id': e['possession_team']['id'], 'play_pattern' : e['play_pattern']['name'], 'team_id' : e['team']['id'], 'player_id' : player_id, 'position' : position, 'location' : location, 'duration' : duration, 'under_pressure' : under_pressure, 'off_camera' : off_camera, 'counterpress' : counterpress}
            
            events['17'].append(event)


        elif type_id == 41: # referee ball drop

            if 'location' in e:
                location = e['location']
            else:
                location = 'null'

            if 'off_camera' in e:
                off_camera = e['off_camera']
            else:
                off_camera = 'False'

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'period' : e['period'], 'timestamp' : e['timestamp'], 'possession' : e['possession'], 'possession_team_id': e['possession_team']['id'], 'play_pattern' : e['play_pattern']['name'], 'team_id' : e['team']['id'], 'location' : location, 'off_camera' : off_camera}
            
            events['41'].append(event)


        elif type_id == 28: # shield

            if 'player' in e:
                player_id = e['player']['id']
            else:
                player_id = 'null'

            if 'position' in e:
                position = e['position']['name']
            else:
                position = 'null'

            if 'location' in e:
                location = e['location']
            else:
                location = 'null'

            if 'under_pressure' in e:
                under_pressure = e['under_pressure']
            else:
                under_pressure = 'False'

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'period' : e['period'], 'timestamp' : e['timestamp'], 'possession' : e['possession'], 'possession_team_id': e['possession_team']['id'], 'play_pattern' : e['play_pattern']['name'], 'team_id' : e['team']['id'], 'player_id' : player_id, 'position' : position, 'location' : location, 'under_pressure' : under_pressure}
            
            events['28'].append(event)


        elif type_id == 16: # shot

            if 'player' in e:
                player_id = e['player']['id']
            else:
                player_id = 'null'

            if 'position' in e:
                position = e['position']['name']
            else:
                position = 'null'

            if 'location' in e:
                location = e['location']
            else:
                location = 'null'

            if 'duration' in e:
                duration = e['duration']
            else:
                duration = 'null'

            if 'under_pressure' in e:
                under_pressure = e['under_pressure']
            else:
                under_pressure = 'False'

            if 'off_camera' in e:
                off_camera = e['off_camera']
            else:
                off_camera = 'False'

            if 'out' in e:
                out = e['out']
            else:
                out = 'False'

            shot = e['shot']
            if 'key_pass_id' in shot:
                key_pass_id = shot['key_pass_id']
            else:
                key_pass_id = 'null'
            if 'aerial_won' in shot:
                aerial_won = shot['aerial_won']
            else:
                aerial_won = 'False'
            if 'follows_dribble' in shot:
                follows_dribble = shot['follows_dribble']
            else:
                follows_dribble = 'False'
            if 'first_time' in shot:
                first_time = shot['first_time']
            else:
                first_time = 'False'
            if 'open_goal' in shot:
                open_goal = shot['open_goal']
            else:
                open_goal = 'False'
            if 'deflected' in shot:
                deflected = shot['deflected']
            else:
                deflected = 'False'

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'period' : e['period'], 'timestamp' : e['timestamp'], 'possession' : e['possession'], 'possession_team_id': e['possession_team']['id'], 'play_pattern' : e['play_pattern']['name'], 'team_id' : e['team']['id'], 'player_id' : player_id, 'position' : position, 'location' : location, 'duration' : duration, 'under_pressure' : under_pressure, 'off_camera' : off_camera, 'out' : out, 'key_pass_id' :key_pass_id, 'end_location' : shot['end_location'], 'aerial_won' : aerial_won, 'follows_dribble' : follows_dribble, 'first_time' : first_time, 'open_goal' : open_goal, 'statsbomb_xg' : shot['statsbomb_xg'], 'deflected' : deflected, 'technique' : shot['technique']['name'], 'body_part' : shot['body_part']['name'], 'type' : shot['type']['name'], 'outcome' : shot['outcome']['name']}
            
            events['16'].append(event)


        elif type_id == 35: # starting xi
            lineup = e['tactics']['lineup']
            players = []
            for p in lineup:
                player = {'player_id' : p['player']['id'], 'position' : p['position']['name'], 'jersey_number' : p['jersey_number']}
                players.append(player)

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'team_id' : e['team']['id'], 'formation' : e['tactics']['formation'], 'lineup' : players}
            
            events['35'].append(event)


        elif type_id == 19: # substitution

            if 'player' in e:
                player_id = e['player']['id']
            else:
                player_id = 'null'

            if 'position' in e:
                position = e['position']['name']
            else:
                position = 'null'

            if 'off_camera' in e:
                off_camera = e['off_camera']
            else:
                off_camera = 'False'         

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'period' : e['period'], 'timestamp' : e['timestamp'], 'possession' : e['possession'], 'possession_team_id': e['possession_team']['id'], 'play_pattern' : e['play_pattern']['name'], 'team_id' : e['team']['id'], 'player_id' : player_id, 'position' : position, 'off_camera' : off_camera, 'replacement' : e['substitution']['replacement']['id'], 'outcome' : e['substitution']['outcome']['name']}
            
            events['19'].append(event)


        elif type_id == 36: # tactical shift

            lineup = e['tactics']['lineup']
            players = []
            for p in lineup:
                player = {'player_id' : p['player']['id'], 'position' : p['position']['name'], 'jersey_number' : p['jersey_number']}
                players.append(player)

            event = {'event_id' : e['id'], 'match_id' : match_id, 'index' : e['index'], 'period' : e['period'], 'timestamp' : e['timestamp'], 'possession' : e['possession'], 'possession_team_id': e['possession_team']['id'], 'play_pattern' : e['play_pattern']['name'], 'team_id' : e['team']['id'], 'formation' : e['tactics']['formation'], 'lineup' : players}
            
            events['36'].append(event)



### create dml files, one for each event type


''' 
# add event 33 to dml first
dml = open('events_dml/33.sql', 'w')
to_write = 'INSERT INTO event_33 (event_id, match_id, index, period, timestamp, possession, possession_team_id, play_pattern, team_id, player_id, position, location, under_pressure, out, outcome, counterpress) VALUES\n'

for e in events['33']:
    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['period']) + ', "' + str(e['timestamp']) + '", ' + str(e['possession']) + ', ' + str(e['possession_team_id']) + ', "' + str(e['play_pattern']) + '", ' + str(e['team_id']) + ', ' + str(e['player_id']) + ', "' + str(e['position']) + '", ' + str(e['location']) + ', ' + str(e['under_pressure']) + ', ' + str(e['out']) + ', "' + str(e['outcome']) + '", ' + str(e['counterpress']) + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()


# add event 24 to dml first (most tables reference countries as foreign key)
dml = open('events_dml/24.sql', 'w')
to_write = 'INSERT INTO event_24 (event_id, match_id, index, period, timestamp, possession, possession_team_id, play_pattern, team_id, player_id, position, off_camera, card) VALUES\n'

for e in events['24']:
    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['period']) + ', "' + str(e['timestamp']) + '", ' + str(e['possession']) + ', ' + str(e['possession_team_id']) + ', "' + str(e['play_pattern']) + '", ' + str(e['team_id']) + ', ' + str(e['player_id']) + ', "' + str(e['position']) + '", ' + str(e['off_camera']) + ', "' + str(e['card']) + '" ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()


# add event 42 to dml first
dml = open('events_dml/42.sql', 'w')
to_write = 'INSERT INTO event_42 (event_id, match_id, index, period, timestamp, possession, possession_team_id, play_pattern, team_id, player_id, position, location, under_pressure, outcome) VALUES\n'

for e in events['42']:
    if e['outcome'] == 'null':
        outcome = 'null'
    else:
        outcome = '"' + str(e['outcome']) + '"'

    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['period']) + ', "' + str(e['timestamp']) + '", ' + str(e['possession']) + ', ' + str(e['possession_team_id']) + ', "' + str(e['play_pattern']) + '", ' + str(e['team_id']) + ', ' + str(e['player_id']) + ', "' + str(e['position']) + '", ' + str(e['location']) + ', ' + str(e['under_pressure']) + ', ' + outcome + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()



# add event 2 to dml first
dml = open('events_dml/2.sql', 'w')
to_write = 'INSERT INTO event_2 (event_id, match_id, index, period, timestamp, possession, possession_team_id, play_pattern, team_id, player_id, position, location, under_pressure, off_camera, out, offensive, recovery_failure) VALUES\n'

for e in events['2']:
    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['period']) + ', "' + str(e['timestamp']) + '", ' + str(e['possession']) + ', ' + str(e['possession_team_id']) + ', "' + str(e['play_pattern']) + '", ' + str(e['team_id']) + ', ' + str(e['player_id']) + ', "' + str(e['position']) + '", ' + str(e['location']) + ', ' + str(e['under_pressure']) + ', '+ str(e['off_camera']) + ', ' + str(e['out']) + ', ' + str(e['offensive']) + ', ' + str(e['recovery_failure']) + ' ),\n'
    
to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()


# add event 6 to dml
dml = open('events_dml/6.sql', 'w')
to_write = 'INSERT INTO event_6 (event_id, match_id, index, period, timestamp, possession, possession_team_id, play_pattern, team_id, player_id, position, location, under_pressure, off_camera, out, counterpress, deflection, offensive, save_block) VALUES\n'

for e in events['6']:
    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['period']) + ', "' + str(e['timestamp']) + '", ' + str(e['possession']) + ', ' + str(e['possession_team_id']) + ', "' + str(e['play_pattern']) + '", ' + str(e['team_id']) + ', ' + str(e['player_id']) + ', "' + str(e['position']) + '", ' + str(e['location']) + ', ' + str(e['under_pressure']) + ', ' + str(e['off_camera']) + ', ' + str(e['out']) + ', ' + str(e['counterpress']) + ', ' + str(e['deflection']) + ', ' + str(e['offensive']) + ', ' + str(e['save_block']) + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()


# add event 43 to dml
dml = open('events_dml/43.sql', 'w')
to_write = 'INSERT INTO event_43 (event_id, match_id, index, period, timestamp, possession, possession_team_id, play_pattern, team_id, player_id, position, location, duration, under_pressure, end_location) VALUES\n'

for e in events['43']:
    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['period']) + ', "' + str(e['timestamp']) + '", ' + str(e['possession']) + ', ' + str(e['possession_team_id']) + ', "' + str(e['play_pattern']) + '", ' + str(e['team_id']) + ', ' + str(e['player_id']) + ', "' + str(e['position']) + '", ' + str(e['location']) + ', ' + str(e['duration']) + ', ' + str(e['under_pressure']) + ', ' + str(e['end_location']) + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()


# add event 9 to dml
dml = open('events_dml/9.sql', 'w')
to_write = 'INSERT INTO event_9 (event_id, match_id, index, period, timestamp, possession, possession_team_id, play_pattern, team_id, player_id, position, location, under_pressure, off_camera, out, aerial_won, body_part) VALUES\n'

for e in events['9']:
    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['period']) + ', "' + str(e['timestamp']) + '", ' + str(e['possession']) + ', ' + str(e['possession_team_id']) + ', "' + str(e['play_pattern']) + '", ' + str(e['team_id']) + ', ' + str(e['player_id']) + ', "' + str(e['position']) + '", ' + str(e['location']) + ', ' + str(e['under_pressure']) + ', ' + str(e['off_camera']) + ', ' + str(e['out']) + ', ' + str(e['aerial_won']) + ', "' + str(e['body_part']) + '" ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()


# add event 3 to dml
dml = open('events_dml/3.sql', 'w')
to_write = 'INSERT INTO event_3 (event_id, match_id, index, period, timestamp, possession, possession_team_id, play_pattern, team_id, player_id, position, location, under_pressure, off_camera) VALUES\n'

for e in events['3']:
    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['period']) + ', "' + str(e['timestamp']) + '", ' + str(e['possession']) + ', ' + str(e['possession_team_id']) + ', "' + str(e['play_pattern']) + '", ' + str(e['team_id']) + ', ' + str(e['player_id']) + ', "' + str(e['position']) + '", ' + str(e['location']) + ', ' + str(e['under_pressure']) + ', ' + str(e['off_camera']) + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()


# add event 14 to dml
dml = open('events_dml/14.sql', 'w')
to_write = 'INSERT INTO event_14 (event_id, match_id, index, period, timestamp, possession, possession_team_id, play_pattern, team_id, player_id, position, location, under_pressure, out, outcome, nutmeg, overrun, no_touch) VALUES\n'

for e in events['14']:
    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['period']) + ', "' + str(e['timestamp']) + '", ' + str(e['possession']) + ', ' + str(e['possession_team_id']) + ', "' + str(e['play_pattern']) + '", ' + str(e['team_id']) + ', ' + str(e['player_id']) + ', "' + str(e['position']) + '", ' + str(e['location']) + ', ' + str(e['under_pressure']) + ', ' + str(e['out']) + ', "' + str(e['outcome']) + '", ' + str(e['nutmeg']) + ', ' + str(e['overrun']) + ', ' + str(e['no_touch']) + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()


# add event 39 to dml
dml = open('events_dml/39.sql', 'w')
to_write = 'INSERT INTO event_39 (event_id, match_id, index, period, timestamp, possession, possession_team_id, play_pattern, team_id, player_id, position, location, off_camera, counterpress) VALUES\n'

for e in events['39']:
    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['period']) + ', "' + str(e['timestamp']) + '", ' + str(e['possession']) + ', ' + str(e['possession_team_id']) + ', "' + str(e['play_pattern']) + '", ' + str(e['team_id']) + ', ' + str(e['player_id']) + ', "' + str(e['position']) + '", ' + str(e['location']) + ', ' + str(e['off_camera']) + ', ' + str(e['counterpress']) + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()


# add event 4 to dml
dml = open('events_dml/4.sql', 'w')
to_write = 'INSERT INTO event_4 (event_id, match_id, index, period, timestamp, possession, possession_team_id, play_pattern, team_id, player_id, position, location, under_pressure, off_camera, counterpress, type, outcome) VALUES\n'

for e in events['4']:
    if e['type'] == 'null':
        type_ = 'null'
    else:
        type_ = '"' + e['type'] + '"'
    if e['outcome'] == 'null':
        outcome = 'null'
    else:
        outcome = '"' + e['outcome'] + '"'
    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['period']) + ', "' + str(e['timestamp']) + '", ' + str(e['possession']) + ', ' + str(e['possession_team_id']) + ', "' + str(e['play_pattern']) + '", ' + str(e['team_id']) + ', ' + str(e['player_id']) + ', "' + str(e['position']) + '", ' + str(e['location']) + ', ' + str(e['under_pressure']) + ', ' + str(e['off_camera']) + ', ' + str(e['counterpress']) + ', ' + type_ + ', ' + outcome + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()


# add event 37 to dml
dml = open('events_dml/37.sql', 'w')
to_write = 'INSERT INTO event_37 (event_id, match_id, index, period, timestamp, possession, possession_team_id, play_pattern, team_id, player_id, position, location, under_pressure, off_camera) VALUES\n'
under_pressure = False
off_camera = False
for e in events['37']:
    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['period']) + ', "' + str(e['timestamp']) + '", ' + str(e['possession']) + ', ' + str(e['possession_team_id']) + ', "' + str(e['play_pattern']) + '", ' + str(e['team_id']) + ', ' + str(e['player_id']) + ', "' + str(e['position']) + '", ' + str(e['location']) + ', ' + str(e['under_pressure']) + ', ' + str(e['off_camera']) + ' ),\n'
    if e['under_pressure'] == True:
        under_pressure = True
    if e['off_camera'] == True:
        off_camera = True
print(under_pressure)
print(off_camera)
to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()


# add event 22 to dml
dml = open('events_dml/22.sql', 'w')
to_write = 'INSERT INTO event_22 (event_id, match_id, index, period, timestamp, possession, possession_team_id, play_pattern, team_id, player_id, position, location, under_pressure, off_camera, advantage, counterpress, offensive, penalty, card, type) VALUES\n'

for e in events['22']:
    if e['card'] == 'null':
        card = 'null'
    else:
        card = '"' + e['card'] + '"'
    if e['type'] == 'null':
        type_ = 'null'
    else:
        type_ = '"' + e['type'] + '"'

    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['period']) + ', "' + str(e['timestamp']) + '", ' + str(e['possession']) + ', ' + str(e['possession_team_id']) + ', "' + str(e['play_pattern']) + '", ' + str(e['team_id']) + ', ' + str(e['player_id']) + ', "' + str(e['position']) + '", ' + str(e['location']) + ', ' + str(e['under_pressure']) + ', ' + str(e['off_camera']) + ', ' + str(e['advantage']) + ', ' + str(e['counterpress']) + ', ' + str(e['offensive']) + ', ' + str(e['penalty']) + ', ' + card + ', ' + type_ + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()


# add event 21 to dml
dml = open('events_dml/21.sql', 'w')
to_write = 'INSERT INTO event_21 (event_id, match_id, index, period, timestamp, possession, possession_team_id, play_pattern, team_id, player_id, position, location, under_pressure, off_camera, advantage, defensive, penalty) VALUES\n'

for e in events['21']:
    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['period']) + ', "' + str(e['timestamp']) + '", ' + str(e['possession']) + ', ' + str(e['possession_team_id']) + ', "' + str(e['play_pattern']) + '", ' + str(e['team_id']) + ', ' + str(e['player_id']) + ', "' + str(e['position']) + '", ' + str(e['location']) + ', ' + str(e['under_pressure']) + ', ' + str(e['off_camera']) + ', ' + str(e['advantage']) + ', ' + str(e['defensive']) + ', ' + str(e['penalty']) + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()


# add event 23 to dml
dml = open('events_dml/23.sql', 'w')
to_write = 'INSERT INTO event_23 (event_id, match_id, index, period, timestamp, possession, possession_team_id, play_pattern, team_id, player_id, position, location, under_pressure, off_camera, out, goalkeeper_position, technique, body_part, type, outcome) VALUES\n'

for e in events['23']:
    if e['goalkeeper_position'] == 'null':
        gkp = 'null'
    else:
        gkp = '"' + e['goalkeeper_position'] + '"'
    if e['technique'] == 'null':
        technique = 'null'
    else:
        technique = '"' + e['technique'] + '"'
    if e['body_part'] == 'null':
        body_part = 'null'
    else:
        body_part = '"' + e['body_part'] + '"'
    if e['type'] == 'null':
        type_ = 'null'
    else:
        type_ = '"' + e['type'] + '"'
    if e['outcome'] == 'null':
        outcome = 'null'
    else:
        outcome = '"' + e['outcome'] + '"'
    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['period']) + ', "' + str(e['timestamp']) + '", ' + str(e['possession']) + ', ' + str(e['possession_team_id']) + ', "' + str(e['play_pattern']) + '", ' + str(e['team_id']) + ', ' + str(e['player_id']) + ', "' + str(e['position']) + '", ' + str(e['location']) + ', ' + str(e['under_pressure']) + ', ' + str(e['off_camera']) + ', ' + str(e['out']) + ', ' + gkp + ', ' + technique + ', ' + body_part + ', ' + type_ + ', ' + outcome + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()

# add event 34 to dml
dml = open('events_dml/34.sql', 'w')
to_write = 'INSERT INTO event_34 (event_id, match_id, index, period, timestamp, possession, possession_team_id, play_pattern, team_id, under_pressure) VALUES\n'

for e in events['34']:
    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['period']) + ', "' + str(e['timestamp']) + '", ' + str(e['possession']) + ', ' + str(e['possession_team_id']) + ', "' + str(e['play_pattern']) + '", ' + str(e['team_id']) + ', ' + str(e['under_pressure']) + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()


# add event 18 to dml
dml = open('events_dml/18.sql', 'w')
to_write = 'INSERT INTO event_18 (event_id, match_id, index, period, possession, possession_team_id, play_pattern, team_id, late_video_start) VALUES\n'

for e in events['18']:
    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['period']) + ', ' + str(e['possession']) + ', ' + str(e['possession_team_id']) + ', "' + str(e['play_pattern']) + '", ' + str(e['team_id']) + ', ' + str(e['late_video_start']) + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()


# add event 40 to dml
dml = open('events_dml/40.sql', 'w')
to_write = 'INSERT INTO event_40 (event_id, match_id, index, period, timestamp, possession, possession_team_id, play_pattern, team_id, player_id, position, under_pressure, off_camera, in_chain) VALUES\n'

for e in events['40']:
    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['period']) + ', "' + str(e['timestamp']) + '", ' + str(e['possession']) + ', ' + str(e['possession_team_id']) + ', "' + str(e['play_pattern']) + '", ' + str(e['team_id']) + ', ' + str(e['player_id']) + ', "' + str(e['position']) + '", ' + str(e['under_pressure']) + ', ' + str(e['off_camera']) + ', ' + str(e['in_chain']) + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()


# add event 10 to dml
dml = open('events_dml/10.sql', 'w')
to_write = 'INSERT INTO event_10 (event_id, match_id, index, period, timestamp, possession, possession_team_id, play_pattern, team_id, player_id, position, location, under_pressure, off_camera, outcome) VALUES\n'

for e in events['10']:
    if e['outcome'] == 'null':
        outcome = 'null'
    else:
        outcome = '"' + e['outcome'] + '"'
    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['period']) + ', "' + str(e['timestamp']) + '", ' + str(e['possession']) + ', ' + str(e['possession_team_id']) + ', "' + str(e['play_pattern']) + '", ' + str(e['team_id']) + ', ' + str(e['player_id']) + ', "' + str(e['position']) + '", ' + str(e['location']) + ', ' + str(e['under_pressure']) + ', ' + str(e['off_camera']) + ', ' + outcome + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()


# add event 38 to dml
dml = open('events_dml/38.sql', 'w')
to_write = 'INSERT INTO event_38 (event_id, match_id, index, period, timestamp, possession, possession_team_id, play_pattern, team_id, player_id, position, location, under_pressure, off_camera, out, aerial_won) VALUES\n'

for e in events['38']:
    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['period']) + ', "' + str(e['timestamp']) + '", ' + str(e['possession']) + ', ' + str(e['possession_team_id']) + ', "' + str(e['play_pattern']) + '", ' + str(e['team_id']) + ', ' + str(e['player_id']) + ', "' + str(e['position']) + '", ' + str(e['location']) + ', ' + str(e['under_pressure']) + ', ' + str(e['off_camera']) + ', ' + str(e['out']) + ', ' + str(e['aerial_won']) + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()


dml = open('events_dml/8.sql', 'w')

# add event 8 to dml
to_write = 'INSERT INTO event_8 (event_id, match_id, index, period, timestamp, possession, possession_team_id, play_pattern, team_id, player_id, position, location) VALUES\n'

for e in events['8']:
    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['period']) + ', "' + str(e['timestamp']) + '", ' + str(e['possession']) + ', ' + str(e['possession_team_id']) + ', "' + str(e['play_pattern']) + '", ' + str(e['team_id']) + ', ' + str(e['player_id']) + ', "' + str(e['position']) + '", ' + str(e['location']) + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()


dml = open('events_dml/20.sql', 'w')

# add event 20 to dml
to_write = 'INSERT INTO event_20 (event_id, match_id, index, period, timestamp, possession, possession_team_id, play_pattern, team_id, player_id, position, location) VALUES\n'

for e in events['20']:
    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['period']) + ', "' + str(e['timestamp']) + '", ' + str(e['possession']) + ', ' + str(e['possession_team_id']) + ', "' + str(e['play_pattern']) + '", ' + str(e['team_id']) + ', ' + str(e['player_id']) + ', "' + str(e['position']) + '", ' + str(e['location']) + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()


dml = open('events_dml/25.sql', 'w')

# add event 25 to dml
to_write = 'INSERT INTO event_25 (event_id, match_id, index, period, timestamp, possession, possession_team_id, play_pattern, team_id, player_id, position, location) VALUES\n'

for e in events['25']:
    if e['position'] == 'null':
        position = 'null'
    else:
        position = '"' + e['position'] + '"'

    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['period']) + ', "' + str(e['timestamp']) + '", ' + str(e['possession']) + ', ' + str(e['possession_team_id']) + ', "' + str(e['play_pattern']) + '", ' + str(e['team_id']) + ', ' + str(e['player_id']) + ', ' + position + ', ' + str(e['location']) + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()


dml = open('events_dml/30.sql', 'w')

# add event 30 to dml
to_write = 'INSERT INTO event_30 (event_id, match_id, index, period, timestamp, possession, possession_team_id, play_pattern, team_id, player_id, position, location, duration, under_pressure, off_camera, out, recipient, length, angle, height, end_location, assisted_shot_id, backheel, deflected, miscommunication, cross, cut_back, switch, shot_assist, goal_assist, body_part, type, outcome, technique) VALUES\n'

for e in events['30']:
    if e['body_part'] == 'null':
        body_part = 'null'
    else:
        body_part = '"' + e['body_part'] + '"'
    if e['type'] == 'null':
        type_ = 'null'
    else:
        type_ = '"' + e['type'] + '"'
    if e['outcome'] == 'null':
        outcome = 'null'
    else:
        outcome = '"' + e['outcome'] + '"'
    if e['technique'] == 'null':
        technique = 'null'
    else:
        technique = '"' + e['technique'] + '"'

    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['period']) + ', "' + str(e['timestamp']) + '", ' + str(e['possession']) + ', ' + str(e['possession_team_id']) + ', "' + str(e['play_pattern']) + '", ' + str(e['team_id']) + ', ' + str(e['player_id']) + ', "' + str(e['position']) + '", ' + str(e['location']) + ', ' + str(e['duration']) + ', ' + str(e['under_pressure']) + ', ' + str(e['off_camera']) + ', ' + str(e['out']) + ', ' + str(e['recipient']) + ', ' + str(e['length']) + ', ' + str(e['angle']) + ', "' + str(e['height']) + '", ' + str(e['end_location']) + ', ' + str(e['assisted_shot_id']) + ', ' + str(e['backheel']) + ', ' + str(e['deflected']) + ', ' + str(e['miscommunication']) + ', ' + str(e['cross']) + ', ' + str(e['cut_back']) + ', ' + str(e['switch']) + ', ' + str(e['shot_assist']) + ', ' + str(e['goal_assist']) + ', ' + body_part + ', ' + type_ + ', ' + outcome + ', ' + technique + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()


dml = open('events_dml/27.sql', 'w')

# add event 27 to dml
to_write = 'INSERT INTO event_27 (event_id, match_id, index, period, timestamp, possession, possession_team_id, play_pattern, team_id, player_id, position, off_camera) VALUES\n'

for e in events['27']:
    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['period']) + ', "' + str(e['timestamp']) + '", ' + str(e['possession']) + ', ' + str(e['possession_team_id']) + ', "' + str(e['play_pattern']) + '", ' + str(e['team_id']) + ', ' + str(e['player_id']) + ', "' + str(e['position']) + '", ' + str(e['off_camera']) + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()


dml = open('events_dml/26.sql', 'w')

# add event 26 to dml
to_write = 'INSERT INTO event_26 (event_id, match_id, index, period, timestamp, possession, possession_team_id, play_pattern, team_id, player_id, position, off_camera) VALUES\n'

for e in events['26']:
    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['period']) + ', "' + str(e['timestamp']) + '", ' + str(e['possession']) + ', ' + str(e['possession_team_id']) + ', "' + str(e['play_pattern']) + '", ' + str(e['team_id']) + ', ' + str(e['player_id']) + ', "' + str(e['position']) + '", ' + str(e['off_camera']) + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()


dml = open('events_dml/17.sql', 'w')

# add event 17 to dml
to_write = 'INSERT INTO event_17 (event_id, match_id, index, period, timestamp, possession, possession_team_id, play_pattern, team_id, player_id, position, location, duration, under_pressure, off_camera, counterpress) VALUES\n'
under_pressure = False
off_camera = False
counterpress = False
for e in events['17']:
    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['period']) + ', "' + str(e['timestamp']) + '", ' + str(e['possession']) + ', ' + str(e['possession_team_id']) + ', "' + str(e['play_pattern']) + '", ' + str(e['team_id']) + ', ' + str(e['player_id']) + ', "' + str(e['position']) + '", ' + str(e['location']) + ', ' + str(e['duration']) + ', ' + str(e['under_pressure']) + ', ' + str(e['off_camera']) + ', ' + str(e['counterpress']) + ' ),\n'
    if e['under_pressure']:
        under_pressure = True
    if e['off_camera']:
        off_camera = True
    if e['counterpress']:
        counterpress = True
print(under_pressure)
print(off_camera)
print(counterpress)
to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()


dml = open('events_dml/41.sql', 'w')

# add event 41 to dml
to_write = 'INSERT INTO event_41 (event_id, match_id, index, period, timestamp, possession, possession_team_id, play_pattern, team_id, location, off_camera) VALUES\n'

for e in events['41']:
    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['period']) + ', "' + str(e['timestamp']) + '", ' + str(e['possession']) + ', ' + str(e['possession_team_id']) + ', "' + str(e['play_pattern']) + '", ' + str(e['team_id']) + ', ' + str(e['location']) + ', ' + str(e['off_camera']) + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()


dml = open('events_dml/28.sql', 'w')

# add event 28 to dml
to_write = 'INSERT INTO event_28 (event_id, match_id, index, period, timestamp, possession, possession_team_id, play_pattern, team_id, player_id, position, location, under_pressure) VALUES\n'

for e in events['28']:
    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['period']) + ', "' + str(e['timestamp']) + '", ' + str(e['possession']) + ', ' + str(e['possession_team_id']) + ', "' + str(e['play_pattern']) + '", ' + str(e['team_id']) + ', ' + str(e['player_id']) + ', "' + str(e['position']) + '", ' + str(e['location']) + ', ' + str(e['under_pressure']) + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()


dml = open('events_dml/16.sql', 'w')

# add event 16 to dml
to_write = 'INSERT INTO event_16 (event_id, match_id, index, period, timestamp, possession, possession_team_id, play_pattern, team_id, player_id, position, location, duration, under_pressure, off_camera, out, key_pass_id, end_location, aerial_won, follows_dribble, first_time, open_goal, statsbomb_xg, deflected, technique, body_part, type, outcome ) VALUES\n'

for e in events['16']:
    if e['technique'] == 'null':
        technique = 'null'
    else:
        technique = '"' + e['technique'] + '"'
    if e['body_part'] == 'null':
        body_part = 'null'
    else:
        body_part = '"' + e['body_part'] + '"'
    if e['type'] == 'null':
        type_ = 'null'
    else:
        type_ = '"' + e['type'] + '"'
    if e['outcome'] == 'null':
        outcome = 'null'
    else:
        outcome = '"' + e['outcome'] + '"'

    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['period']) + ', "' + str(e['timestamp']) + '", ' + str(e['possession']) + ', ' + str(e['possession_team_id']) + ', "' + str(e['play_pattern']) + '", ' + str(e['team_id']) + ', ' + str(e['player_id']) + ', "' + str(e['position']) + '", ' + str(e['location']) + ', ' + str(e['duration']) + ', ' + str(e['under_pressure']) + ', ' + str(e['off_camera']) + ', ' + str(e['out']) + ', ' + str(e['key_pass_id']) + ', ' + str(e['end_location']) + ', ' + str(e['aerial_won']) + ', ' + str(e['follows_dribble']) + ', ' + str(e['first_time']) + ', ' + str(e['open_goal']) + ', ' + str(e['statsbomb_xg']) + ', ' + str(e['deflected']) + ', ' + technique + ', ' + body_part + ', ' + type_ + ', ' + outcome + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()


dml = open('events_dml/35.sql', 'w')

# add event 35 to dml
to_write = 'INSERT INTO event_35 (event_id, match_id, index, team_id, formation, lineup) VALUES\n'

for e in events['35']:
    lineup = 'ARRAY['
    for p in e['lineup']:
        player_id = str(p['player_id'])
        position = '"' + p['position'] + '"'
        jersey_number = str(p['jersey_number'])
        player = '\'(' + player_id + ', ' + position + ', ' + jersey_number + ')\', '

        lineup += player

    lineup = lineup[:-2] + ']'

    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['team_id']) + ', ' + str(e['formation']) + ', ' + lineup + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()


dml = open('events_dml/19.sql', 'w')

# add event 19 to dml
to_write = 'INSERT INTO event_19 (event_id, match_id, index, period, timestamp, possession, possession_team_id, play_pattern, team_id, player_id, position, off_camera, replacement, outcome) VALUES\n'

for e in events['19']:
    if e['outcome'] == 'null':
        outcome = 'null'
    else:
        outcome = '"' + e['outcome'] + '"'

    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['period']) + ', "' + str(e['timestamp']) + '", ' + str(e['possession']) + ', ' + str(e['possession_team_id']) + ', "' + str(e['play_pattern']) + '", ' + str(e['team_id']) + ', ' + str(e['player_id']) + ', "' + str(e['position']) + '", ' + str(e['off_camera']) + ', ' + str(e['replacement']) + ', ' + outcome + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()


dml = open('events_dml/36.sql', 'w')

# add event 36 to dml
to_write = 'INSERT INTO event_36 (event_id, match_id, index, period, timestamp, possession, possession_team_id, play_pattern, team_id, formation, lineup) VALUES\n'

for e in events['36']:
    lineup = 'ARRAY['
    for p in e['lineup']:
        player_id = str(p['player_id'])
        position = '"' + p['position'] + '"'
        jersey_number = str(p['jersey_number'])
        player = '\'(' + player_id + ', ' + position + ', ' + jersey_number + ')\', '

        lineup += player

    lineup = lineup[:-2] + ']'

    to_write += '( "' + str(e['event_id']) + '", ' + str(e['match_id']) + ', ' + str(e['index']) + ', ' + str(e['period']) + ', "' + str(e['timestamp']) + '", ' + str(e['possession']) + ', ' + str(e['possession_team_id']) + ', "' + str(e['play_pattern']) + '", ' + str(e['team_id']) + ', ' + str(e['formation']) + ', ' + lineup + ' ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()
'''
dml = open('events_dml/related_events.sql', 'w')


# add related events to dml
to_write = 'INSERT INTO related_events (event_id_1, event_id_2) VALUES\n'

for e in related_events:
    to_write += '( "' + str(e['event_id']) + '", "' + str(e['other_event_id']) + '" ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)
dml.close()

'''
# add events by type to dml
dml = open('events_dml/events_by_type.sql', 'w')
to_write = 'INSERT INTO events_by_type (event_id, table_name) VALUES\n'

for e in events_by_type:
    to_write += '( "' + str(e['event_id']) + '", "event_' + str(e['type']) + '" ),\n'

to_write = to_write[:-2] + ';\n\n'
dml.write(to_write)

dml.close()
'''
