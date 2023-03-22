import os

directory = 'Scripts'

for filename in os.listdir(directory):
	filepath = os.path.join(directory, filename)
	if filepath.endswith(".py"):
		print('---------------------------')
		print(f'Run {filepath} - Start')
		print('---------------------------')
		
		os.system(f'python {filepath}')

		print('---------------------------')
		print(f'Run {filepath} - End')
		print('---------------------------')