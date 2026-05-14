clear all
close all
clc

str = "errs_n_1000_p_400";
errs = readNPY(str+'.npy');

labs = {'PF','PL'};
colors_r = {[1 0 0],[0 0 1]};
linestyles = {'-','--'};

xla = 't';
yla = 'Error';

idx = linspace(0,1,size(errs,2));
hold on
for k = 1:2
    ls = linestyles{mod(k-1,numel(linestyles))+1};
    plot(idx,errs(k,:),ls,'Color', colors_r{k}, 'MarkerFaceColor', colors_r{k},'LineWidth',2)
end
hold off
xlabel(xla)
ylabel(yla)
legend(labs,'Location','northwest')
grid on
fig = gcf;
fig.Units = 'pixels';
fig.Position(3:4) = [800 400];
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
saveas(fig, str+'.png');