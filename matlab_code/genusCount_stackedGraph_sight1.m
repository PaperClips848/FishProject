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

% Load your background map
img = imread('tx_eco_lg.png');  

nSites = 2;  % how many sites you want to place
 
% ============================= PLOT RESULTS ==============================
if ~exist('fileNameData_c', 'var')                      % check data file
    fileNameData_c = '';                                % default blank
end

figure(figNum),figNum = figNum+1; clf                   % create figure
set(gcf, 'position', plotPositionWide_v)                % set figure size

imshow(img);   % display the map
hold on;                                       % giving the labels a 45deg angle

[x, y] = ginput(nSites);
scatter(x, y, 'k.');

label_plotEdges(msgl_c, fileNameData_c, msg3_c, '');    % label figure edges