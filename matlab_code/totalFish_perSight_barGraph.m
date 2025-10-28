% script        totalFish_perSight_barGraph
% purpose       Plot bar graphs showing (1) species richness (number of genera)
%               and (2) total fish count for each sampling site.
% usage         Run the script directly after setting the working directory.
% notes         Requires: ../data/seth_environmentalGenusCountData_nov2024.csv
% date          10/21/2025
% programmer    K.L. Brashears

% ========================== INITIALIZATION ================================
programName_c = mfilename;                                   % Get script name
msgl_c = [programName_c, ': ', date];                        % Create label with script name and date
msg3_c = 'K.L. Brashears';                                   % Author name

if ~exist('figNum', 'var')                                   % Check if figure number variable exists
    figNum = 1;                                              % Default figure number
end

plotNotes_h;                                                 % Load plot formatting definitions

% ======================= READ AND PREPARE DATA =============================
fileName_c = '../data/seth_environmentalGenusCountData_nov2024.csv';  % Path to dataset
gc_t = readtable(fileName_c);                                % Read data table from CSV

sn_v = (1:height(gc_t));                                     % Generate site numbers (1:N)
gc_m = gc_t{:, 27:56};                                       % Extract numeric genus count data

ts_v = gc_t.t_species;                                       % Species richness (number of genera per site)
tf_v = gc_t.t_population;                                    % Total fish count per site

% ======================== SORT SITES BY METRICS ============================
[ts_sv, idx] = sort(ts_v, 'descend');                        % Sort species richness values (high to low)
sns_sv = sn_v(idx);                                          % Reorder site numbers accordingly

[tf_sv, idx] = sort(tf_v, 'descend');                        % Sort total fish counts (high to low)
snf_sv = sn_v(idx);                                          % Reorder site numbers accordingly

% Convert to categorical for ordered bar plotting
sns_c = categorical(sns_sv);                                 
sns_rc = reordercats(sns_c, sns_sv);                         % Maintain sorted order for species richness

snf_c = categorical(snf_sv);
snf_rc = reordercats(snf_c, snf_sv);                         % Maintain sorted order for total fish count

% ============================= PLOT RESULTS ================================
if ~exist('fileNameData_c', 'var')                           % Check for data file name variable
    fileNameData_c = '';                                     % Default blank
end

figure(figNum); figNum = figNum + 1;                         % Create new figure and increment counter
set(gcf, 'Position', plotPositionWide_v);                    % Set figure size and layout

% --- (A) Species Richness per Site ---
subplot(2,1,1);
bar(sns_rc, ts_sv);                                          % Bar graph of species richness per site
title('Species Richness per Site');                          % Title
xlabel('Site Number');                                       % X-axis label
ylabel('Number of Genera Present');                          % Y-axis label
xtickangle(45);                                              % Rotate x-axis labels
grid on;

% --- (B) Total Fish Count per Site ---
subplot(2,1,2);
bar(snf_rc, tf_sv);                                          % Bar graph of total fish count per site
title('Total Fish Count per Site');                          % Title
xlabel('Site Number');                                       % X-axis label
ylabel('Total Number of Fish');                              % Y-axis label
xtickangle(45);                                              % Rotate x-axis labels
grid on;

% ============================= LABEL METADATA =============================
label_plotEdges(msgl_c, fileName_c, msg3_c, '');         % Add metadata labels to figure edges
