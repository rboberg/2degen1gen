# coding: utf-8

import nfldb
import json
import pandas as pd
import datetime
import argparse

def player_stats(db, player_args, game_args={}):
    # find potential list of players
    players = nfldb.Query(db).player(**player_args).as_players()
    # get list of player ids
    ids = [getattr(pp,'player_id') for pp in players]
    
    player_data = []
    for player in players:
        pid = getattr(player, 'player_id')
        stats = nfldb.Query(db).game(**game_args).player(player_id=pid).as_aggregate()
        if len(stats) == 0:
            stats = None
        elif len(stats) == 1:
            stats = stats[0]
        else:
            print('something wrong with stats')
        player_data += [{'info':player, 'stats':stats}]
    
    return(player_data)


def player_points(player_stats, point_key):
    rows = []
    
    for player in player_stats:
        stat_key = point_key.keys()
        
        if player['stats'] is None:
            # all stats are 0 if none found
            row = {stat: 0 for stat in stat_key}
        else:
            # otherwise get stats
            row = {stat: getattr(player['stats'], stat) for stat in stat_key}
        
        row['fantasy'] = sum([row[stat] * point_key[stat] for stat in stat_key])
        row['full_name'] = player['info'].full_name
        row['team'] = player['info'].team
        rows += [row]
        
    return(rows)

def team_results(db, teams, point_key):
    results = {}
    for team in teams.keys():
        results[team] = []
        for p in teams[team]:
            ps = player_stats(db, player_args=p, game_args={'season_year':2015, 'season_type':"Postseason"})
            results[team] += player_points(ps, point_key)
    return(results)

def total_points(results):
    return({team_name:sum([player['fantasy'] for player in team]) for team_name, team in results.iteritems()})

def add_points_to_teams(db, teams, point_key):
    results = team_results(db, teams, point_key)
    for team in teams.keys():
        for i in range(len(teams[team])):
            teams[team][i].update({'points':results[team][i]['fantasy']})

def write_teams(teams, write_dir = 'updates_2016', write_current = True):
    if write_current:
        with open(write_dir + '/current.json', 'w') as f:
            json.dump(teams,f)
    
    time_str = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    with open(write_dir + '/' + time_str + '.json', 'w') as f:
        json.dump(teams,f)

def main(season_year):
    db = nfldb.connect()

    q = nfldb.Query(db).game(season_year=season_year, season_type='Postseason')

    team_file = 'playoff_' + str(season_year+1) + '_team_master.json'
    with open(team_file) as f:    
        teams = json.load(f)

    point_file = 'playoff_' + str(season_year+1) + '_point_key.json'
    with open(point_file) as f:    
        point_key = json.load(f)

    add_points_to_teams(db, teams, point_key)

    write_teams(teams, write_dir='updates_'+str(season_year+1))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--year",
        help="postseason year", default=2015,type=int)
    args = parser.parse_args()
    main(season_year=args.year)

