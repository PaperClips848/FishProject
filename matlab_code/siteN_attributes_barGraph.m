% function       siteN_attributes_barGraph
% purpose        Plot the environmental attribute values for a specific sampling site.
%                Displays a bar chart of all recorded environmental variables
%                for the selected site number.
% usage          Run directly by passing a site number, 
%                   and returning a figNum as output:
%                >> [figNum] = siteN_attributes_barGraph(5)
% notes          Requires: ../data/seth_environmentalData_march2023.csv
% date           10/21/2025
% programmer     K.L. Brashears

function [figNum] = siteN_attributes_barGraph(figNum, siteN)

    % ========================== INITIALIZATION ================================
    programName_c = mfilename;                                   % Get script name
    msgl_c = [programName_c, ': ', date];                        % Message with script name and date
    msg3_c = 'K.L. Brashears';                                   % Author identifier
    
    if ~exist('figNum', 'var')                                   % If figure number not set
        figNum = 1;                                              % Set default figure number
    end

    plotNotes_h;                                                 % Load plot formatting definitions

    % ============================ READ DATA ===================================
    fileName_c = '../data/seth_environmentalData_march2023.csv'; % Input data file
    ed_t = readtable(fileName_c);                                % Read table from CSV file
    
    % ======================= EXTRACT SITE DATA ================================
    ed_m = ed_t{:, 3:end};                                       % Convert numeric columns to matrix
    ed_v = ed_m(siteN, :);                                       % Select values for the specified site
    edl_v = ed_t.Properties.VariableNames(3:end);                % Get attribute labels from table headers
    edl_c = categorical(edl_v);                                  % Convert labels to categorical for plotting

    % ============================= CREATE FIGURE ==============================
    if ~exist('fileNameData_c', 'var')                           % If file name variable not defined
        fileNameData_c = '';                                     % Use blank as default
    end

    figure(figNum); figNum = figNum + 1;                         % Create and clear figure
    set(gcf, 'Position', plotPositionWide_v);                    % Set figure size and layout

    % ============================== PLOT DATA =================================
    bar(edl_c, ed_v);                                            % Plot bar chart of site attributes
    title(['Site #', num2str(siteN, '%d')]);                    % Title showing the site number
    xlabel('Environmental Attribute');                           % Label x-axis
    ylabel('Measured Value');                                    % Label y-axis
    xtickangle(45);                                              % Rotate x-axis labels for readability
    grid on;                                                     % Add background grid for clarity

    % =========================== LABEL METADATA ===============================
    label_plotEdges(msgl_c, fileNameData_c, msg3_c, '');         % Add metadata around figure edges

end
