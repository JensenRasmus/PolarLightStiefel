clear all
close all
clc

errs = readNPY('Errors.npy');
%sigs = readNPY('sigma_ps.npy');

labs = {'Exp','PF','PL','QG Gr.','QR','Cayley'};

cs = lines(8);
cs = cs(5:end,:);
colors = {[0.2310    0.6660    0.1960],[1 0 0],[0 0 1],cs(3,:),cs(4,:),[0 0 0]};
linestyles = {'-.','-','--',':'};
markers = {'*','o','s','d','v'};
figure
hold on
xla = '\rho';
yla = 'Error';
idx = linspace(0.1,0.9,size(errs,2));
for k = 1:size(errs,1)
    m = markers{mod(k-1,numel(markers))+1};
    ls = linestyles{mod(k-1,numel(linestyles))+1};
    plot(idx, errs(k,:), ls, 'Color', colors{k}, 'MarkerFaceColor', colors{k},'LineWidth',2);
end
hold off
title('Interpolation')
xlabel(xla)
ylabel(yla)
legend(labs,'Location','northwest')
grid on

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
saveas(fig, 'fisher_experiment.png');



linestyles = {':','--','-.'};
colors = {[0 0 0],[1 0 0],[0 0 1]};
labs = {'\sigma_{p-1}','\sigma_{p}','\sigma_{p+1}'};
xla = 'r';
yla = 'Magnitude';

figure
hold on
for k = 1:size(sigs,1)
    m = markers{mod(k-1,numel(markers))+1};
    ls = linestyles{mod(k-1,numel(linestyles))+1};
    plot(idx, sigs(k,:), ls, 'Color', colors{k}, 'MarkerFaceColor', colors{k},'LineWidth',2);
end
xlim([0.1 0.9])
hold off
title('Singular values')
xlabel(xla)
ylabel(yla)
legend(labs,'Location','northwest')


fig = gcf;
fig.Units = 'pixels';
fig.Position(3:4) = [600 600];
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
saveas(fig, 'fisher_experiment_sigmas.png');
