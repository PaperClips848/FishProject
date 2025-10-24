% function       species_vs_environment_fromCombinedFile_demo
% purpose        Plot species richness and total fish count vs an environmental variable,
%                using a single combined dataset of environment + genus counts.
% usage          Run directly. Change 'yAttr_c' to any environmental variable.
% notes          Requires: ../data/seth_environmentalGenusCountData_nov2024.csv
% date           10/21/2025
% programmer     K.L. Brashears

% ========================== COMMON INITIALIZATION ========================
programName_c = mfilename;                               % get script name
msgl_c = [programName_c, ': ', date];                    % message with script name and date
msg3_c = 'K.L. Brashears';                               % author
if ~exist('figNum', 'var')
    figNum = 1;                                          % default figure number
end
plotNotes_h;                                             % load plot formatting definitions

% ============================= READ DATA =================================
fileName_c = '../data/seth_environmentalGenusCountData_nov2024.csv';
tbl = readtable(fileName_c);

% ==================== DEFINE COLUMN GROUPS ===============================
% Genus columns are everything after the last environmental variable
genusCols_c = tbl.Properties.VariableNames( ...
    find(strcmp(tbl.Properties.VariableNames, 'minMonthFlow_cfs')) + 1 : end );

% =================== COMPUTE COMMUNITY METRICS ===========================
gc_m = tbl{:, genusCols_c};                 % numeric matrix of genus counts
t_fish = tbl.t_fish;                % total individuals per site
t_genus = tbl.t_genus;       % number of genera present

% =================== SELECT ENVIRONMENTAL VARIABLE =======================
yAttr_c = 'pfloat_macrophytes';   % <-- change to any variable in envCols_c
yData_v = tbl.(yAttr_c);

% ============================= CREATE FIGURE =============================
figure(figNum); figNum = figNum + 1; clf;
set(gcf, 'Position', plotPositionWide_v);
tiledlayout(1,2,'TileSpacing','compact','Padding','compact');

% --- (A) Species richness vs environmental variable
subplot(2,1,1);
scatter(yData_v, t_genus, 50, 'b', 'filled');
xlabel(strrep(yAttr_c, '_', ' '));
ylabel('Species Richness (Number of Genera)');
title('Species Richness vs Environmental Attribute');
grid on; hold on;

% ----- ADD TREND LINE -----
coeffs1 = polyfit(yData_v, t_genus, 1); % linear fit (1st-degree polynomial)
xfit1 = linspace(min(yData_v), max(yData_v), 100);
yfit1 = polyval(coeffs1, xfit1);
plot(xfit1, yfit1, 'k--', 'LineWidth', 1.5);
legend('Data Points', sprintf('Trend Line (y = %.2fx + %.2f)', coeffs1(1), coeffs1(2)), 'Location', 'best');

% --- (B) Total fish count vs environmental variable
subplot(2,1,2);
scatter(yData_v, t_fish, 50, 'r', 'filled');
xlabel(strrep(yAttr_c, '_', ' '));
ylabel('Total Fish Count');
title('Total Fish Count vs Environmental Attribute');
grid on; hold on;

% ----- ADD TREND LINE -----
coeffs2 = polyfit(yData_v, t_fish, 1);
xfit2 = linspace(min(yData_v), max(yData_v), 100);
yfit2 = polyval(coeffs2, xfit2);
plot(xfit2, yfit2, 'k--', 'LineWidth', 1.5);
legend('Data Points', sprintf('Trend Line (y = %.2fx + %.2f)', coeffs2(1), coeffs2(2)), 'Location', 'best');

sgtitle(sprintf('Fish Community vs %s', strrep(yAttr_c, '_', ' ')));

label_plotEdges(msgl_c, fileName_c, msg3_c, '');
