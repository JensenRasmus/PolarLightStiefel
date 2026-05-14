clear all
close all
clc

str = "err_coord_approx_mode2";
%str = "err_coord_approx_mode1_p400";
errs = readNPY(str+'.npy')';

labs = {'RL','PF','PL Cay'};
colors_r = {[0 0 0],[1 0 0],[0 0 1]};
linestyles = {'-','--',':'};

xla = 't';
yla = 'Error';

idx = linspace(0,1,size(errs,2));
hold on
for k = 1:3
    ls = linestyles{mod(k-1,numel(linestyles))+1};
    plot(idx,errs(k,:),ls,'Color', colors_r{k}, 'MarkerFaceColor', colors_r{k},'LineWidth',2)
end
hold off
xlabel(xla)
ylabel(yla)
ylim([-0.0001,max(errs(:))])
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