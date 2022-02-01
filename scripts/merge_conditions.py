import os, json
import pandas as pd

def merge_conditions(path, file_filter = None, write_out = None):
	files = os.listdir(path)
	if file_filter is not None:
		files = [f for f in files if f[0:len(file_filter)] == file_filter]
	df = []
	for file in files:
		df.append(pd.read_json(os.path.join(path, file), encoding = 'utf-8', lines = True, dtype = {'tweet_id': 'str'}))
	df = pd.concat(df)
	df.reset_index(inplace = True, drop = True)
	ans = pd.json_normalize([d[0] for d in df['answer']]).apply(lambda row: row[row == True].index, axis=1)
	ans = pd.DataFrame([list(a) for a in ans])
	ans.rename(columns = {0:'climate_action', 1:'anger', 2:'happiness', 3:'worry'}, inplace = True)
	ans['climate_action'] = [a[15:] for a in ans['climate_action']]
	ans['anger'] = [a[14:] for a in ans['anger']]
	ans['happiness'] = [a[18:] for a in ans['happiness']]
	ans['worry'] = [a[14:] for a in ans['worry']]
	df = df[['tweet_id', 'worker_id', 'gender', 'ethnicity', 'accept_time', 'submit_time']].join(ans)
	df.sort_values(by = ['tweet_id', 'gender', 'ethnicity'], axis = 0, inplace = True)
	if write_out is not None:
		df.to_csv(os.path.join(path, 'merged_conditions.csv'), sep = ',', index = False)
	return df
