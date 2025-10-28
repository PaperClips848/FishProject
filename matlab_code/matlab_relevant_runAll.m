% script        matlab_relevant_runAll
% purpose       Run all relevant MATLAB scripts and generate corresponding figures.
% usage         Run this script directly after setting the working directory.
% notes         Requires:
%                   Scripts:
%                       total_countPerGenus_barGraph.m
%                       totalSpecies_perSight_barGraph.m
%                       sightN_attributes_barGraph.m
%                       totalCountAndSpecies_vsAttribute_scatterPlot.m
%                   Data:
%                       ../data/seth_environmentalGenusCountData_nov2024.csv
%                       ../data/seth_environmentalData_march2023.csv
%
% date          10/27/2025
% programmer    K.L. Brashears

% =========================== RUNNING SCRIPTS ==============================

if ~exist('figNum', 'var')                                   % If figure number not set
    figNum = 1;                                              % Set default figure number
end

% --- Run scatter plots comparing community metrics to an environmental variable ---
figNum = totalCountAndSpecies_vsAttribute_scatterPlot(figNum, "upstreamCumDA_km2");     % Example attribute: upstreamCumDA_km2

% --- Run attribute visualization for a specific sites ---

% --- Sites with high Total Population AND Species Richness ---

figNum = siteN_attributes_barGraph(figNum, 4);                                          % Plots environmental attributes for a given site (example: site 4)

figNum = siteN_attributes_barGraph(figNum, 29);

figNum = siteN_attributes_barGraph(figNum, 33);

% --- Sites with low Total Population AND Species Richness ---

figNum = siteN_attributes_barGraph(figNum, 17);                     

figNum = siteN_attributes_barGraph(figNum, 2);

figNum = siteN_attributes_barGraph(figNum, 18);

% --- Run per-site richness and population plots ---
run("totalFish_perSight_barGraph.m");                                                   % Generates per-site species richness and fish count plots

% --- Run genus-level total counts ---
run("total_countPerGenus_barGaph.m");                                                   % Generates total fish count per genus bar chart
