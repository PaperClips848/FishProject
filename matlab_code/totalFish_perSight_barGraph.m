% script        totalSpecies_perSight_barGraph
% purpose       Plot a bar graph showing the species richness (number of 
%               genera present) at each sampling site.
% usage         Run the script directly after setting the working directory.
% notes         Requires: seth_genusCountData_june2024.csv
% date          10/04/2025
% programmer    K.L. Brashears

% ========================== COMMON INITIALIZATION ========================
programName_c = mfilename;                              % get script name
msgl_c = [programName_c, ': ', date];                   % message with script name and date
msg3_c = 'K.L. Brashears';                              % author
if ~exist('figNum', 'var')                              % check if figNum exists
    figNum = 1;                                         % set default figure number
end
plotNotes_h;                                            % load plot formatting definitions

% ============= GETTING AND COUNTING THE GENUS PRESENCE ===================
fileName_c = '../data/seth_environmentalGenusCountData_nov2024.csv';        % data file name
gc_t = readtable(fileName_c);                           % read CSV into a table

sn_v = (1:46);                                      % site identifiers (first column)
gc_m = gc_t{:, 27:56};                                  % numeric genus count data only

ts_v = gc_t.t_species;                                % number of genera present at each site (species richness)
tf_v = gc_t.t_population;                                % number of genera present at each site (species richness)

[ts_sv, idx] = sort(ts_v, 'descend');                   % sort richness values (high to low)
sns_sv = sn_v(idx);                                      % reorder site names accordingly

[tf_sv, idx] = sort(tf_v, 'descend');                   % sort richness values (high to low)
snf_sv = sn_v(idx);                                      % reorder site names accordingly

sns_c = categorical(sns_sv);                              % convert sorted site names to categorical
sns_rc = reordercats(sns_c, sns_sv);                       % lock category order to sorted order

snf_c = categorical(snf_sv);                              % convert sorted site names to categorical
snf_rc = reordercats(snf_c, snf_sv);                       % lock category order to sorted order

% ============================= PLOT RESULTS ==============================
if ~exist('fileNameData_c', 'var')                      % check if data file name variable exists
    fileNameData_c = '';                                % set default blank value
end

figure(figNum), figNum = figNum + 1; clf;               % create new figure and increment figNum
set(gcf, 'Position', plotPositionWide_v);               % set figure size and layout

subplot(211);
bar(sns_rc, ts_sv);                                      % plot bar graph of species richness per site
title('Total Species per Site', 'Interpreter', 'none'); % title for the figure
xlabel('Site', 'Interpreter', 'none');                  % label x-axis
ylabel('Number of Genera Present', 'Interpreter', 'none'); % label y-axis
xtickangle(45);                                         % rotate x-axis labels for readability

subplot(212);
bar(snf_rc, tf_sv);                                      % plot bar graph of species richness per site
title('Total Fish per Site', 'Interpreter', 'none'); % title for the figure
xlabel('Site', 'Interpreter', 'none');                  % label x-axis
ylabel('Number of Fish Present', 'Interpreter', 'none'); % label y-axis
xtickangle(45);                                         % rotate x-axis labels for readability

label_plotEdges(msgl_c, fileNameData_c, msg3_c, '');    % label figure edges with metadata