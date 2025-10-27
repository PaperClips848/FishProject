% script        total_countPerGenus_barGaph
% purpose       Plot a bar graph showing the total quantity of each fish genus 
%               recorded across all sampling sites.
% usage         Run as a standalone script after running plotNotes_h.
% notes         Requires: ../data/seth_genusCountData_june2024.csv
% date          10/21/2025
% programmer    K.L. Brashears

% ========================== INITIALIZATION ================================
programName_c = mfilename;                                   % Get script name
msgl_c = [programName_c, ': ', date];                        % Create label with script name and date
msg3_c = 'K.L. Brashears';                                   % Author name

if ~exist('figNum', 'var')                                   % Check if figure number variable exists
    figNum = 1;                                              % Set default figure number
end

plotNotes_h;                                                 % Load plot formatting definitions

% ======================= READ AND PROCESS DATA =============================
fileName_c = '../data/seth_genusCountData_june2024.csv';     % Path to genus count dataset
gc_t = readtable(fileName_c);                                % Read data table from CSV file

gc_m = gc_t{:, 3:end};                                       % Extract numeric genus count data
gn_v = gc_t.Properties.VariableNames(3:end);                 % Get genus names from column headers

gc_v = sum(gc_m, 1);                                         % Compute total fish count per genus (column sum)

[gc_sv, idx] = sort(gc_v, 'descend');                        % Sort totals from highest to lowest
gn_sv = gn_v(idx);                                           % Reorder genus names accordingly

gn_c = categorical(gn_sv);                                   % Convert genus names to categorical array
gn_rc = reordercats(gn_c, gn_sv);                            % Reorder categories to match sorted order

% ============================= CREATE FIGURE ===============================
if ~exist('fileNameData_c', 'var')                           % Check if fileNameData_c exists
    fileNameData_c = '';                                     % Use blank default
end

figure(figNum); figNum = figNum + 1;                         % Create new figure and increment counter
set(gcf, 'Position', plotPositionWide_v);                    % Set figure size and layout

% =============================== PLOT DATA ================================
bar(gn_rc, gc_sv);                                           % Create bar graph of total counts per genus
title({'Total Quantity of Each Fish Genus', ...              % Multi-line title for readability
       ['(', programName_c, ')']});
xlabel('Genus');                                             % Label x-axis
ylabel('Total Quantity of Fish');                            % Label y-axis
xtickangle(45);                                              % Rotate x-axis labels for readability
grid on;                                                     % Add grid for clarity

% ============================== LABEL METADATA =============================
label_plotEdges(msgl_c, fileNameData_c, msg3_c, '');         % Label figure edges with metadata
