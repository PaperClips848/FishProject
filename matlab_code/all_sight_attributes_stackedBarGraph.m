% script        genusCount_barGaph
% purpose       Plot a bar graph of the total quantity of each genus of fish
%               recorderd
% usage         script
% notes         
% date          9/13/2025
% programmer    K.L. Brashears

% ========================== COMMON INITIALIZATION ========================
programName_c = mfilename;                              % script name
msgl_c = [programName_c,': ', date];                    % message with script name + date
msg3_c = 'K.L. Brashears';                              % author
if ~exist('figNum', 'var')                              % check figNum exists
    figNum = 1;                                         % default figure number
end
plotNotes_h                                             % set plot definitions

% ============= GETTING AND SORTING THE GENUS COUNTS ======================

fileName_c = '../data/seth_environmentalGenusCountData_nov2024.csv';    % file name containing data
ed_t = readtable(fileName_c);                           % reading the csv into a table

sight = 1;

ed_m = gc_t{:, 3:end};                                  % converting the table into a matrix

ed_v = ed_m(sight, :);

edl_v = ed_t.Properties.VariableNames(3:end);

edl_c = categorical(edl_v);

% ============================= PLOT RESULTS ==============================
if ~exist('fileNameData_c', 'var')                      % check data file
    fileNameData_c = '';                                % default blank
end

figure(figNum),figNum = figNum+1; clf                   % create figure
set(gcf, 'position', plotPositionWide_v)                % set figure size

bar(ed_m, "stacked");                            % bar graph of the number of fish in each genus
title('Sight Attributes');
xlabel('Sight')                                         % labeling the x-axis
ylabel('Value')                              % labeling the y-axis
xtickangle(45);                                         % giving the labels a 45deg angle

legend(edl_v);

label_plotEdges(msgl_c, fileNameData_c, msg3_c, '');    % label figure edges