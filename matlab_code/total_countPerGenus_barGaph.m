% script        total_genusCount_barGraph
% purpose       Plot a bar graph showing the total quantity of each genus 
%               of fish recorded across all sampling sites.
% usage         Run as a standalone script after setting plotNotes_h.
% notes         Requires: seth_genusCountData_june2024.csv
% date          10/04/2025
% programmer    K.L. Brashears

% ========================== COMMON INITIALIZATION ========================
programName_c = mfilename;                              % script name
msgl_c = [programName_c, ': ', date];                   % message with script name and date
msg3_c = 'K.L. Brashears';                              % author
if ~exist('figNum', 'var')                              % check if figNum exists
    figNum = 1;                                         % default figure number
end
plotNotes_h;                                            % set plot definitions (custom function)

% ============= GETTING AND SORTING THE GENUS COUNTS ======================
fileName_c = '../data/seth_genusCountData_june2024.csv';        % file name containing data
gc_t = readtable(fileName_c);                           % read the CSV into a table

gc_m = gc_t{:, 3:end};                                  % extract numeric genus count data
gn_v = gc_t.Properties.VariableNames(3:end);            % get genus names from variable headers

gc_v = sum(gc_m, 1);                                    % compute total count per genus (column sum)

[gc_sv, idx] = sort(gc_v, 'descend');                   % sort totals (highest to lowest)
gn_sv = gn_v(idx);                                      % reorder genus names to match sorted totals

gn_c = categorical(gn_sv);                              % convert sorted genus names to categorical
gn_rc = reordercats(gn_c, gn_sv);                       % reorder categorical array to sorted order

% ============================= PLOT RESULTS ==============================
if ~exist('fileNameData_c', 'var')                      % check for data file variable
    fileNameData_c = '';                                % default blank
end

figure(figNum), figNum = figNum + 1; clf                % create figure and increment counter
set(gcf, 'Position', plotPositionWide_v);               % set figure size

bar(gn_rc, gc_sv);                                      % create bar graph of total counts per genus
title({'Total Quantity of Each Fish Genus', ...         % multi-line title for clarity
       ['(', programName_c, ')']}, 'Interpreter', 'none');
xlabel('Genus', 'Interpreter', 'none');                 % label x-axis
ylabel('Quantity of Fish');                             % label y-axis
xtickangle(45);                                         % rotate x-axis labels for readability

label_plotEdges(msgl_c, fileNameData_c, msg3_c, '');    % label figure edges with script metadata
