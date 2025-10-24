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
fileName_d = '../data/seth_environmentalGenusCountData_nov2024.csv';        % data file name
table = readtable(fileName_d);                             % read CSV into a table

% for Texas Sights --------------------------------------------------------

fileName_i = '../figures/tx_eco_lg (1).png';

sightPos = [table.Long(1:34), table.Lat(1:34)];

longLim = [-108.1250, -92.2394];

latLim = [37.1957, 24.7451];

% -------------------------------------------------------------------------

img = imread(fileName_i);

coords = get_sight_pos_func('../figures/tx_eco_lg.png', latLim, longLim, sightPos);

% ============================= PLOT RESULTS ==============================
if ~exist('fileNameData_c', 'var')                      % check if data file name variable exists
    fileNameData_c = '';                                % set default blank value
end

figure(figNum), figNum = figNum + 1; clf;               % create new figure and increment figNum
set(gcf, 'Position', plotPositionWide_v);               % set figure size and layout

imshow(img);                                      % plot bar graph of species richness per site
hold on
plot(coords(:,1), coords(:,2), 'r.');

label_plotEdges(msgl_c, fileNameData_c, msg3_c, '');    % label figure edges with metadata