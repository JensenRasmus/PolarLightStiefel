clear all
close all
clc

GradNorms = readNPY("GradNorm.npy");
N_iter = readNPY("N_iter.npy");
TimeStamp =  readNPY("TimeStamp.npy");
fVals = readNPY("fVals.npy");

% N_iter(i) + 1  is the number of iterations we needed in order to reach tol
% At pos 1 (0 in Python) we have recorded the initial values of grad and f
% based on the initial guess. 
N_iter = N_iter + 1;
% Rows: 1 = Exp, 2 = PF, 3 = PL, 4 = PL Cay

% Colors and styles 
labs = {'Exp','PF','PL','PL Cay','Cayley'};
colors = {[0.2310    0.6660    0.1960],[1 0 0],[0 0 1],[0.7520    0.3600    0.9840],[0 0 0]};
linestyles = {'-.','-','--',':','-.','-','--',':'};
markers = {'^','o','s','d','*'};

xla = 'time (s)';
yla = 'Gradient norm';
subplot(1,2,1)
hold on
for i = 1:length(labs)
    semilogy(TimeStamp(i,1:N_iter(i)), GradNorms(i, 1:N_iter(i)), 'Color', colors{i}, 'LineStyle', linestyles{i}, 'Marker', markers{i}, 'DisplayName', labs{i},'LineWidth',2);
end
xlabel(xla);
ylabel(yla);
set(gca, 'YScale', 'log') % But you can explicitly force log
legend(labs, 'Location', 'northeast');
title("Gradient norm vs. time")
legend show;
grid on

xla = 'Iteration';
yla = 'Objective function';


subplot(1,2,2)
hold on
for i = 1:length(labs)
    plot(0:(N_iter(i)-1), fVals(i, 1:N_iter(i)), 'Color', colors{i}, 'LineStyle', linestyles{i}, 'Marker', markers{i}, 'DisplayName', labs{i},'LineWidth',2);
end
xlabel(xla);
ylabel(yla);
legend(labs, 'Location', 'northeast');

legend show;
title("Objective function vs. iteration")
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
% Save the figure as a PNG1 file
saveas(fig, 'timings_RBC.png');