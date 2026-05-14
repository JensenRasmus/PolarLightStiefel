clear all
close all
clc
rtimes = readNPY('runtimes.npy');
ptimes = readNPY('processtimes.npy');


labs = {'PF','PL','PL Cay','QG St.','QG St. Cay.','QG Gr.','QR','Cayley'};
figure
% Ensure rtimes and ptimes have same number of rows
n = max(size(rtimes,1), size(ptimes,1));
% If one has fewer rows, pad with NaNs
if size(rtimes,1) < n
    rtimes(end+1:n, :) = NaN;
end
if size(ptimes,1) < n
    ptimes(end+1:n, :) = NaN;
end

% Number of columns for each
cr = size(rtimes,2);
cp = size(ptimes,2);

% Choose distinct colors and markers
% colors_r = lines(cr);
% colors_p = lines(cp);
% colors_r = {[1 0 0],[0 0 1],[0.5210    0.0860    0.8190],[0.9290    0.6940    0.1250]}
cs = lines(8);
cs = cs(5:end,:);
colors_r = {[1 0 0],[0 0 1],[0.7520    0.3600    0.9840],cs(1,:),cs(2,:),cs(3,:),cs(4,:),[0 0 0]};

markers = {'o','s','d','^','p','h','x','*','+','*','v','>','<'}; % cycle if more cols than markers
% Provide a list of common MATLAB line styles for reference
linestyles = {'-','--','-','--','-','--','-','--'};

xla = 'p';
yla = 'Runtime (s)';
% Subplot for rtimes
subplot(1,2,1)
hold on
idx = [500 1000 1500 2000];
for k = 1:cr
    m = markers{mod(k-1,numel(markers))+1};
    ls = linestyles{mod(k-1,numel(linestyles))+1};
    plot(idx, rtimes(:,k), [ls m], 'Color', colors_r{k}, 'MarkerFaceColor', colors_r{k},'LineWidth',2);
end
hold off
title('Interpolation')
xlabel(xla)
ylabel(yla)
legend(labs,'Location','northwest')
grid on

% Subplot for ptimes
subplot(1,2,2)
hold on
for k = 1:cp
    m = markers{mod(k-1,numel(markers))+1};
    ls = linestyles{mod(k-1,numel(linestyles))+1};
    plot(idx, ptimes(:,k), [ls m], 'Color', colors_r{k}, 'MarkerFaceColor', colors_r{k},'LineWidth',2);
end
hold off
title('Preprocessing')
xlabel(xla)
ylabel(yla)
legend(labs,'Location','northwest')
grid on
% Set figure size to 1200x600 pixels (width x height)
fig = gcf;
fig.Units = 'pixels';
fig.Position(3:4) = [1200 600];
% Increase font sizes for all axes, legends, and text in the figure
fs = 20; % desired base font size
ax = findall(fig,'Type','axes');
for a = 1:numel(ax)
    ax(a).FontSize = fs;
    ax(a).Title.FontSize = fs + 2;
    ax(a).XLabel.FontSize = fs;
    ax(a).YLabel.FontSize = fs;
    lg = findall(ax(a),'Type','Legend');
    for L = 1:numel(lg)
        lg(L).FontSize = fs;
    end
end
% Also update any standalone text objects
txt = findall(fig,'Type','text');
for t = 1:numel(txt)
    txt(t).FontSize = fs;
end
% Save the figure as a PNG file
saveas(fig, 'runtime_processing_plot.png');