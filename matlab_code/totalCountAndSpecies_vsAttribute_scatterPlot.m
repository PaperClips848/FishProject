% function       totalCountAndSpecies_vsAttribute_scatterPlot
% purpose        Plot species richness (number of genera) and total fish count
%                against a selected environmental variable, using a combined
%                dataset that includes both environmental and genus count data.
% usage          Run directly, passing an environmental variable name as input, 
%                   and returning a figNum as output:
%                >> [figNum] = totalCountAndSpecies_vsAttribute_scatterPlot('pH')
% notes          Requires: ../data/seth_environmentalGenusCountData_nov2024.csv
% date           10/21/2025
% programmer     K.L. Brashears

function [figNum] = totalCountAndSpecies_vsAttribute_scatterPlot(figNum, yAttr_c)

    % ========================== INITIALIZATION ================================
    programName_c = mfilename;                                   % Get script name
    msgl_c = [programName_c, ': ', date];                        % Message with script name and date
    msg3_c = 'K.L. Brashears';                                   % Author identifier
    
    if ~exist('figNum', 'var')                                   % If figure number not set
        figNum = 1;                                              % Set default figure number
    end

    plotNotes_h;                                                 % Load plot formatting definitions

    % ============================= READ DATA ==================================
    fileName_c = '../data/seth_environmentalGenusCountData_nov2024.csv';   % Input data file
    tbl = readtable(fileName_c);                                           % Read combined dataset
    
    % ====================== COMPUTE COMMUNITY METRICS =========================
    t_fish  = tbl.t_population;                                   % Total fish count per site
    t_genus = tbl.t_species;                                      % Species richness (number of genera)
    
    % ====================== SELECT ENVIRONMENTAL VARIABLE =====================
    yData_v = tbl.(yAttr_c);                                      % Extract selected environmental variable
    
    % ============================= CREATE FIGURE ==============================
    figure(figNum); figNum = figNum + 1;                          % Create and clear figure
    set(gcf, 'Position', plotPositionWide_v);                     % Set figure position and size
    tiledlayout(2,1, 'TileSpacing','compact', 'Padding','compact'); % Two subplots (stacked vertically)
    
    % ==================== (A) SPECIES RICHNESS VS ATTRIBUTE ===================
    nexttile;                                                     % First subplot
    scatter(yData_v, t_genus, 50, 'b', 'filled');                 % Plot scatter of species richness
    xlabel(strrep(yAttr_c, '_', ' '));                            % Replace underscores for readability
    ylabel('Species Richness (Number of Genera)');                % Y-axis label
    title('Species Richness vs Environmental Attribute');         % Subplot title
    grid on; hold on;
    
    % ----- Add Linear Trend Line -----
    coeffs1 = polyfit(yData_v, t_genus, 1);                       % Linear fit coefficients
    xfit1 = linspace(min(yData_v), max(yData_v), 100);            % Generate fit X values
    yfit1 = polyval(coeffs1, xfit1);                              % Compute fitted Y values
    plot(xfit1, yfit1, 'k--', 'LineWidth', 1.5);                  % Plot trend line
    legend('Data Points', sprintf('Trend Line (y = %.2fx + %.2f)', ...
        coeffs1(1), coeffs1(2)), 'Location', 'best');             % Add legend
    
    % ==================== (B) TOTAL FISH COUNT VS ATTRIBUTE ===================
    nexttile;                                                     % Second subplot
    scatter(yData_v, t_fish, 50, 'r', 'filled');                  % Plot scatter of total fish count
    xlabel(strrep(yAttr_c, '_', ' '));                            % Replace underscores for readability
    ylabel('Total Fish Count');                                   % Y-axis label
    title('Total Fish Count vs Environmental Attribute');         % Subplot title
    grid on; hold on;
    
    % ----- Add Linear Trend Line -----
    coeffs2 = polyfit(yData_v, t_fish, 1);                        % Linear fit coefficients
    xfit2 = linspace(min(yData_v), max(yData_v), 100);            % Generate fit X values
    yfit2 = polyval(coeffs2, xfit2);                              % Compute fitted Y values
    plot(xfit2, yfit2, 'k--', 'LineWidth', 1.5);                  % Plot trend line
    legend('Data Points', sprintf('Trend Line (y = %.2fx + %.2f)', ...
        coeffs2(1), coeffs2(2)), 'Location', 'best');             % Add legend
    
    % ============================ FIGURE LABELING =============================
    sgtitle(sprintf('Fish Community Metrics vs %s', ...
        strrep(yAttr_c, '_', ' ')));                              % Overall figure title
    
    label_plotEdges(msgl_c, fileName_c, msg3_c, '');               % Label figure edges with metadata

end
