wildcard_constraints:
	project_name = config['project_name']


rule createMSDB:
	input:
		sample_list = "INPUT/sample_list.csv"
	output:
		MSDB = "OUTPUT/{project_name}/tmp/MSDB.RData"
	params:
		project_name = config['project_name']
	conda:
		"dependencies.yaml"
	script:
		"1_createMSDB.R"


rule scoringAndFiltering:
	input:
		sample_list = "INPUT/sample_list.csv",
		MSDB = "OUTPUT/{project_name}/tmp/MSDB.RData"
	output:
		allPSMs = "OUTPUT/{project_name}/tmp/allPSMs.RData"
	params:
		project_name = config['project_name'],
		q_value = config['q_value'],
		ion_score = config['ion_score'],
		delta_score = config['delta_score']
	conda:
		"dependencies.yaml"
	script:
		"2_scoringAndFiltering.R"


rule removeSynErrors:
	input:
		allPSMs = "OUTPUT/{project_name}/tmp/allPSMs.RData"
	output:
		PSMs = "OUTPUT/{project_name}/tmp/extractedPSMs.RData"
	params:
		keep_synErrors = config["keep_synErrors"]
	conda:
		"dependencies.yaml"
	script:
		"3_removeSynErrors.R"


rule mapping:
	input:
		PSMs = "OUTPUT/{project_name}/tmp/extractedPSMs.RData"
	output:
		ProteasomeDB = "OUTPUT/{project_name}/ProteasomeDB.csv"
	conda:
		"dependencies.yaml"
	script:
		"4_mapping.R"


rule output_statistics:
	input:
		ProteasomeDB = "OUTPUT/{project_name}/ProteasomeDB.csv"
	output:
		DB_stats = "OUTPUT/{project_name}/DB_stats.pdf"
	conda:
		"dependencies.yaml"
	script:
		"5_output_statistics.R"

