import numpy as np
import matplotlib.pyplot as plt
import os


BUFFER_LENGTH = 3000.0
MS_IN_S = 1000.0
KB_IN_MB = 1000.0
TRANS_BL = str(int(BUFFER_LENGTH/MS_IN_S))
ALL_RESULTS_DIR = './all_results_old/'
SAVING_DIR = './metrics_old/'
# SHOW_LIST = ['naive', 'PI', 'MPCs' , 'MPC_iLQR_SEG_', 'MPC\'' , 'MPC_iLQR_CHUNK_','RLs', 'RL\'', 'MPCl', 'RL_speed']
# SHOW_LIST = ['RL\'', 'RL_speed']
SHOW_LIST = ['naive', 'PI', 'MPCs' , 'MPC_iLQR_SEG_', 'MPC\'' , 'MPC_iLQR_CHUNK_','RLs', 'RL\'']

palette = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
                  '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
                  '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
                  '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']
new_palette = ['#1f77b4',  '#ff7f0e',  '#2ca02c',
                  '#d62728', '#9467bd',
                  '#8c564b', '#e377c2', '#7f7f7f',
                  '#bcbd22', '#17becf']
line_t = ['--','-']

def name_change(curr_name):
	if curr_name == 'naive':
		return r"Naive"
	elif curr_name == "PI":
		return r"PI"
	elif curr_name == "MPCs":
		return r"MPC$^{(s)}$"
	elif curr_name == "MPC_iLQR_SEG_":
		return r"iMPC$^{(s)}$"
	elif curr_name == "MPC\'":
		return r"MPC$^{(c)}$"
	elif curr_name == "MPC_iLQR_CHUNK_":
		return r"iMPC$^{(c)}$"
	elif curr_name == "RLs":
		return r"DRL$^{(s)}$"
	elif curr_name == "RL\'":
		return r"DRL$^{(c)}$"
	# elif curr_name == "MPCl":
	# 	return r"MPC$^{(p)}$"
	# elif curr_name == "RL_speed":
	# 	return r"RL$^{(p)}$"

def qoe_cdf_plot(qoe_records):
	qoe_lower = np.amin(qoe_records)
	qoe_upper = np.amax(qoe_records)
	qoe_values = range(int(np.ceil(qoe_lower)), int(np.ceil(qoe_upper)), 2)
	X_GAP = 100
	cdf = []
	# print qoe_lower
	# print qoe_upper
	p = plt.figure(figsize=(7,5.5))
	# print len(qoe_records)
	for i in range(len(SHOW_LIST)):
		curr_name = SHOW_LIST[i]
		# if curr_name == 'MPCs':
		# 	curr_name = 'MPC'
		# elif curr_name == 'RLs':
		# 	curr_name = 'RL'
		# elif curr_name == 'naive':
		# 	curr_name = 'Navie'
		# elif curr_name == 'MPCl':
		# 	curr_name = 'MPC\'\''
		curr_name = name_change(curr_name)
		curr_record = qoe_records[i]
		# print curr_record
		sorted(curr_record)
		curr_cdf = []
		for qoe in qoe_values:
			curr_cdf.append(len([x for x in curr_record if x <= qoe])/float(len(curr_record)))

		plt.plot(qoe_values, curr_cdf, line_t[i%len(line_t)], color=new_palette[i], label=curr_name, linewidth = 2)
	plt.legend(loc='lower right',fontsize = 22, ncol=1, frameon=False, labelspacing=0.)
	plt.xlabel('Accumulate QoE', fontweight='bold', fontsize=22)
	if BUFFER_LENGTH == 2000.0:
		plt.xticks([0, 100, 200, 300],  fontsize=22)
	elif BUFFER_LENGTH == 3000.0:
		plt.xticks([0, 100, 200, 300],  fontsize=22)
	else:
		plt.xticks([-100, 0,  100, 200],  fontsize=22)
	plt.yticks(np.arange(0, 1.001, 0.2), fontsize=22)
	plt.ylabel('CDF', fontweight='bold', fontsize=22)
	if BUFFER_LENGTH == 2000.0:
		plt.axis([0, 300, 0.001, 1])
	elif BUFFER_LENGTH == 3000.0:
		plt.axis([0, 300, 0.001, 1])	
	else:
		plt.axis([-100, 250, 0.001, 1])	
	p.set_tight_layout(True)
	# p.show()
	# raw_input()
	return p

def freeze_cdf_plot(freeze_records):
	freeze_lower = np.amin(freeze_records)
	freeze_upper = np.amax(freeze_records)
	freeze_values = range(int(np.ceil(freeze_lower)), int(np.ceil(freeze_upper)), 5)
	cdf = []
	# print freeze_lower
	# print freeze_upper
	X_GAP = 1000
	p = plt.figure(figsize=(7,5.5))
	for i in range(len(SHOW_LIST)):
		curr_name = SHOW_LIST[i]
		# if curr_name == 'MPCs':
		# 	curr_name = 'MPC'
		# elif curr_name == 'RLs':
		# 	curr_name = 'RL'
		# elif curr_name == 'naive':
		# 	curr_name = 'Navie'
		# elif curr_name == 'MPCl':
		# 	curr_name = 'MPC\'\''
		curr_name = name_change(curr_name)
		curr_record = freeze_records[i]
		# print curr_record
		sorted(curr_record)
		curr_cdf = []
		for freeze in freeze_values:
			curr_cdf.append(len([x for x in curr_record if x <= freeze])/float(len(curr_record)))

		plt.plot(freeze_values, curr_cdf, line_t[i%len(line_t)], color=new_palette[i], label=curr_name, linewidth = 2)
	plt.legend(loc='lower right',fontsize = 22, ncol=1, frameon=False, labelspacing=0.)
	plt.xlabel('Total Freeze (s)', fontweight='bold', fontsize=22)
	plt.xticks(np.arange(int(freeze_lower/X_GAP)*X_GAP, int(freeze_upper/X_GAP)*X_GAP+0.01, X_GAP),  \
			np.arange(int(freeze_lower/X_GAP)*X_GAP/MS_IN_S, int(freeze_upper/X_GAP)*X_GAP/MS_IN_S+0.001, X_GAP/MS_IN_S), fontsize=22)
	plt.yticks(np.arange(0, 1.001, 0.2), fontsize=22)
	plt.ylabel('CDF', fontweight='bold', fontsize=22)
	plt.axis([int(freeze_lower/X_GAP)*X_GAP, int(freeze_upper/X_GAP)*X_GAP, 0, 1])
	p.set_tight_layout(True)
	# p.show()
	# raw_input()
	return p

def bit_rate_cdf_plot(bit_rate_records):
	bit_rate_lower = np.amin(bit_rate_records)
	bit_rate_upper = np.amax(bit_rate_records)
	bit_rate_values = range(int(np.ceil(bit_rate_lower)), int(np.ceil(bit_rate_upper)), 1)
	cdf = []
	# print bit_rate_lower
	# print bit_rate_upper
	X_GAP = 2000
	p = plt.figure(figsize=(7,5.5))
	for i in range(len(SHOW_LIST)):
		curr_name = SHOW_LIST[i]
		# if curr_name == 'MPCs':
		# 	curr_name = 'MPC'
		# elif curr_name == 'RLs':
		# 	curr_name = 'RL'
		# elif curr_name == 'naive':
		# 	curr_name = 'Navie'
		# elif curr_name == 'MPCl':
		# 	curr_name = 'MPC\'\''
		curr_name = name_change(curr_name)
		curr_record = bit_rate_records[i]
		# print curr_record
		sorted(curr_record)
		curr_cdf = []
		for bit_rate in bit_rate_values:
			curr_cdf.append(len([x for x in curr_record if x <= bit_rate])/float(len(curr_record)))

		plt.plot(bit_rate_values, curr_cdf, line_t[i%len(line_t)], color=new_palette[i], label=curr_name, linewidth = 2)
	plt.legend(loc='lower right',fontsize = 22, ncol=1, frameon=False, labelspacing=0.)
	plt.xlabel('Average Bitrate (Mbps)', fontweight='bold', fontsize=22)
	plt.xticks([300, 2000, 4000, 6000],[0.3, 2, 4, 6],  fontsize=22)
	plt.yticks(np.arange(0, 1.001, 0.2), fontsize=22)
	plt.ylabel('CDF', fontweight='bold', fontsize=22)
	plt.axis([300.0, 6000.0, 0, 1])
	p.set_tight_layout(True)
	# p.show()
	# raw_input()
	return p

def change_cdf_plot(change_records):
	change_lower = np.amin(change_records)
	change_upper = np.minimum(np.amax(change_records), 800.0)
	change_values = np.arange(int(np.ceil(change_lower)), int(np.ceil(change_upper)), 2)
	cdf = []
	# print change_lower
	# print change_upper
	X_GAP = 200
	p = plt.figure(figsize=(7,5.5))
	for i in range(len(SHOW_LIST)):
		curr_name = SHOW_LIST[i]
		# if curr_name == 'MPCs':
		# 	curr_name = 'MPC'
		# elif curr_name == 'RLs':
		# 	curr_name = 'RL'
		# elif curr_name == 'naive':
		# 	curr_name = 'Navie'
		# elif curr_name == 'MPCl':
		# 	curr_name = 'MPC\'\''
		curr_name = name_change(curr_name)
		curr_record = change_records[i]
		# print curr_record
		sorted(curr_record)
		curr_cdf = []
		for change in change_values:
			curr_cdf.append(len([x for x in curr_record if x <= change])/float(len(curr_record)))

		plt.plot(change_values, curr_cdf, line_t[i%len(line_t)], color=new_palette[i], label=curr_name, linewidth = 2)
	plt.legend(loc='lower right',fontsize = 22, ncol=1, frameon=False, labelspacing=0.)
	plt.xlabel('Average Bitrate Change (Kbps)', fontweight='bold', fontsize=22)
	
	plt.xticks(np.arange(int(change_lower/X_GAP)*X_GAP, int(change_upper/X_GAP)*X_GAP+X_GAP+1, X_GAP), \
	np.arange(int(int(change_lower/X_GAP)*X_GAP), int(change_upper/X_GAP)*X_GAP+X_GAP+1, X_GAP),  fontsize=22)
	# else:
	# 	plt.xticks(np.arange(int(change_lower/X_GAP)*X_GAP, int(change_upper/X_GAP)*X_GAP+1, X_GAP), \
	# 	np.arange(int(change_lower/X_GAP)*X_GAP, int(change_upper/X_GAP)*X_GAP+1, X_GAP),  fontsize=22)
	plt.yticks(np.arange(0, 1.001, 0.2), fontsize=22)
	plt.ylabel('CDF', fontweight='bold', fontsize=22)
	# if BUFFER_LENGTH == 3000.0 or BUFFER_LENGTH == 4000.0:
	# 	plt.axis([50.0, int(change_upper/X_GAP)*X_GAP+1, 0, 1])
	# else:
	plt.axis([0.0, np.minimum(int(change_upper/X_GAP)*X_GAP+X_GAP,800), 0, 1])
	p.set_tight_layout(True)
	# p.show()
	# raw_input()
	return p

def latency_cdf_plot(latency_records):
	# print(latency_records)
	latency_lower = np.amin(latency_records)
	latency_upper = np.amax(latency_records)
	latency_values = range(int(np.ceil(latency_lower)), int(np.ceil(latency_upper)), 1)
	cdf = []
	# print latency_lower
	# print latency_upper
	X_GAP = 1000.0
	p = plt.figure(figsize=(7,5.5))
	for i in range(len(SHOW_LIST)):
		curr_name = SHOW_LIST[i]
		# if curr_name == 'MPCs':
		# 	curr_name = 'MPC'
		# elif curr_name == 'RLs':
		# 	curr_name = 'RL'
		# elif curr_name == 'naive':
		# 	curr_name = 'Navie'
		# elif curr_name == 'MPCl':
		# 	curr_name = 'MPC\'\''
		curr_name = name_change(curr_name)
		curr_record = latency_records[i]
		sorted(curr_record)
		curr_cdf = []
		for latency in latency_values:
			curr_cdf.append(len([x for x in curr_record if x <= latency])/float(len(curr_record)))

		plt.plot(latency_values, curr_cdf, line_t[i%len(line_t)], color=new_palette[i], label=curr_name, linewidth = 2)
	if BUFFER_LENGTH == 4000:
		plt.legend(loc='upper left',fontsize = 22, ncol=1, frameon=False, labelspacing=0.)
	else:
		plt.legend(loc='lower right',fontsize = 22, ncol=1, frameon=False, labelspacing=0.)
	plt.xlabel('Average Latency (s)', fontweight='bold', fontsize=22)
	plt.xticks(np.arange(int(latency_lower/X_GAP)*X_GAP, int(latency_upper/X_GAP)*X_GAP+X_GAP+0.01, X_GAP),  \
			np.arange(int(latency_lower/X_GAP)*X_GAP/MS_IN_S, (int(latency_upper/X_GAP)+1)*X_GAP/MS_IN_S+0.001, X_GAP/MS_IN_S), fontsize=22)
	plt.yticks(np.arange(0, 1.001, 0.2), fontsize=22)
	plt.ylabel('CDF', fontweight='bold', fontsize=22)
	if BUFFER_LENGTH == 4000.0:
		plt.axis([int(latency_lower/X_GAP)*X_GAP, int(latency_upper/X_GAP)*X_GAP, 0, 1])
	else:
		plt.axis([int(latency_lower/X_GAP)*X_GAP + X_GAP, int(latency_upper/X_GAP)*X_GAP, 0, 1])
	# else:
	# 	plt.axis([int(latency_lower/X_GAP)*X_GAP, int(latency_upper/X_GAP)*X_GAP, 0, 1])
	p.set_tight_layout(True)
	# p.show()
	# raw_input()
	return p

def main():
	results = os.listdir(ALL_RESULTS_DIR)
	file_records = []
	qoe_records = []
	bit_rate_records = []
	freeze_records = []
	change_records = []
	latency_records = []
	name_records = []
	for name in SHOW_LIST:
		for data in results:
			if name in data and TRANS_BL in data:
				# print name
				file_info = []
				qoe_record = []
				bit_rate_record = []
				freeze_record = []
				change_record = []
				latency_record = []
				name_record = []
				file_path = ALL_RESULTS_DIR + data
				with open(file_path, 'r') as f:
					for line in f:
						parse = line.strip('\n')
						parse = parse.split('\t')
						name_record.append(parse[0])
						qoe_record.append(float(parse[1]))
						bit_rate_record.append(float(parse[2]))
						freeze_record.append(float(parse[3]))
						change_record.append(float(parse[4]))
						latency_record.append(float(parse[5]))
						file_info.append(parse)
				file_records.append(file_info)
				qoe_records.append(qoe_record)
				bit_rate_records.append(bit_rate_record)
				freeze_records.append(freeze_record)
				change_records.append(change_record)
				latency_records.append(latency_record)
				name_records.append(name_record)

	# Show results

	qoe_fig = qoe_cdf_plot(qoe_records)
	freeze_fig = freeze_cdf_plot(freeze_records)
	bit_rate_fig = bit_rate_cdf_plot(bit_rate_records)
	change_fig = change_cdf_plot(change_records)
	latency_fig = latency_cdf_plot(latency_records)

	#
	save_buff = str(int(BUFFER_LENGTH/MS_IN_S))
	qoe_fig.savefig(SAVING_DIR + 'buff_'+save_buff+'_qoe_0.eps', format='eps', dpi=1000, figsize=(7, 5.5))
	freeze_fig.savefig(SAVING_DIR + 'buff_'+save_buff+'_freeze_0.eps', format='eps', dpi=1000, figsize=(7, 5.5))
	bit_rate_fig.savefig(SAVING_DIR + 'buff_'+save_buff+'_br_0.eps', format='eps', dpi=1000, figsize=(7, 5.5))
	change_fig.savefig(SAVING_DIR + 'buff_'+save_buff+'_change_0.eps', format='eps', dpi=1000, figsize=(7, 5.5))
	latency_fig.savefig(SAVING_DIR + 'buff_'+save_buff+'_latency_0.eps', format='eps', dpi=1000, figsize=(7, 5.5))



if __name__ == '__main__':
	main()