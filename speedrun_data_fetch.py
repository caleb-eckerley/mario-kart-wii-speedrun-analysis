import pandas as pd
import srcomapi
import srcomapi.datatypes as dt

api = srcomapi.SpeedrunCom()


def getMarioKart():
  game = api.search(dt.Game, {"name": "mario kart wii"})[0]
  return game


def getAllCategoryRuns(game):
  sms_runs = {}
  for category in game.categories:
    if not category.name in sms_runs:
      sms_runs[category.name] = {}
    if category.type == 'per-level':
      for level in game.levels:
        sms_runs[category.name][level.name] = dt.Leaderboard(api, data=api.get("leaderboards/{}/level/{}/{}?embed=variables".format(game.id, level.id, category.id)))
    else:
      sms_runs[category.name] = dt.Leaderboard(api, data=api.get("leaderboards/{}/category/{}?embed=variables".format(game.id, category.id)))
  return sms_runs


def getCharacterData(game, metadata_dict):
  character_dict = game.variables[22].values['choices']
  character_id = game.variables[22].id
  metadata_dict[character_id] = character_dict
  return metadata_dict


def getVehicleData(game, metadata_dict):
  vehicle_dict = game.variables[23].values['choices']
  vehicle_id = game.variables[23].id
  metadata_dict[vehicle_id] = vehicle_dict
  return metadata_dict


def getSkipData(game, metadata_dict):
  tracks32_skip_id = game.categories[0].variables[0].id
  tracks32_skip_option_dict = game.categories[0].variables[0].values['choices']
  metadata_dict[tracks32_skip_id] = tracks32_skip_option_dict
  return metadata_dict


def getItemData(game, metadata_dict):
  tracks32_item_id = game.categories[0].variables[1].id
  tracks32_item_dict = game.categories[0].data['variables'][1].values['choices']
  metadata_dict[tracks32_item_id] = tracks32_item_dict
  return metadata_dict


def getRunData(runs):
  run_list = []
  for run in runs:
    if run['run'].status['status'] == 'verified':
      values_dict = run['run'].values
      time_seconds = run['run'].times['ingame_t']
      run_list.append([time_seconds, values_dict])
  return run_list


def matchValues(runs, metadata_dict):
  modified_data = []
  for run in runs:
    new_values = []
    value = run[1]
    
    new_values.append(run[0])
    for v in value:
      if v in metadata_dict:
        v_value = value[v]
        true_value = metadata_dict[v][v_value]
        new_values.append(true_value)
      else:
        print(f'Something went wrong.\n{v} not found in dictionary')
    
    modified_data.append(new_values)
  return modified_data


def doubleCheckLen(data):
  count = 0
  checked_data = []
  for run in data:
    if len(run) != 5:
      count = count + 1
    else:
      checked_data.append(run)
  print(f'{count} records removed for insufficient data length')
  return checked_data
  
  
def main():
  game = getMarioKart()
  runs = getAllCategoryRuns(game)
  runs = runs['32 Tracks'].runs
  metadata_dict = {}
  metadata_dict = getCharacterData(game, metadata_dict)
  metadata_dict = getVehicleData(game, metadata_dict)
  metadata_dict = getSkipData(game, metadata_dict)
  metadata_dict = getItemData(game, metadata_dict)
  runs_data = getRunData(runs)
  modified_data = matchValues(runs_data, metadata_dict)
  checked_data = doubleCheckLen(modified_data)
  df = pd.DataFrame(data=checked_data, columns=['time', 'skips', 'items', 'character', 'vehicle'])
  filtered_df = df[df['time'] != 0]
  filtered_df.to_csv('./data/speedrun_data', index=False)
  #print(filtered_df['vehicle'].unique())
  return 1

main()