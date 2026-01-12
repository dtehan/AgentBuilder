--
name: dba_databaseHealthAssessment
allowed-tools: 
description: Builds a database health assessment dashboard
--

# dba_databaseHealthAssessment

Generate a comprehensive Teradata system health dashboard for the last 30 days, structured as an executive summary followed by detailed technical analysis. Create a visual dashboard using tables, charts, and color-coded indicators to highlight critical metrics and resource constraints.

## Instructions
	- Use color coding: Red (critical/>85%), Yellow (warning/70-85%), Green (healthy/<70%) 
	- Include bar charts for space utilization and usage patterns 
	- Present data in sortable tables with key metrics highlighted 
	- Add trend indicators (arrows/percentages) for changing metrics 
	- Target audience: DBA management and Teradata system owners 
	- Focus on informational assessment rather than actionable recommendation
	- Ensure that dashboard is mobile friendly and scales easily

## Workflow
	- Executive Summary Section: 
		* System overview with key performance indicators  (number of databases, number of tables, number of views, number of macros, number of user defined views, number of users and space utilization percentages) 
		* Critical alerts highlighting databases/tables approaching space limits (use red for >85% utilization, yellow for >70%) 
		* Top 5 resource consumption trends and usage patterns 

	- Detailed Technical Analysis: 
		* Current database version and system configuration 
		* Complete space utilization breakdown across all databases with visual charts 
		* Top 10 space-consuming tables with growth trends and utilization percentages 
		* CPU Resource usage heatmaps showing patterns by weekday and hour of day 
		* IO Resource usage heatmaps showing patterns by weekday and hour of day 
		* Memory Resource usage heatmaps showing patterns by weekday and hour of day 
		* Flow control metrics and user delay analysis with performance bottleneck identification 
		* Database and table activity rankings showing most frequently accessed objects 
		* User activity patterns and resource impact analysis 

## Report
    - A professional database health assessment dashboard that is easily navigable.
    - At the beginning of the dashboard identify the system
	- Use color to highlight points of interest

Think through the problem.