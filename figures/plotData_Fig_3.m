close all
timings_p_retracton = readNPY('timings_p_retractions_large.npy')';
timings_p_retracton = timings_p_retracton;

% Color standard
% Red: PF
% Blue: PL
% 

figure
labs = {'PF','PF inv','PL','PL inv.','PL Cay.','PL Cay. inv','Cayley', 'Cayley inv'};
subplot(1,2,1)
% Plot each column with a distinct line style and add legend/labels
styles = {'-','--','-','--','-','--','-','--'};
markers = {'o','o','s','s','*','*'};


colors = {[1 0 0],[1 0 0],[0 0 1],[0 0 1],[0.7520    0.3600    0.9840],[0.7520    0.3600    0.9840], [0 0 0],[0 0 0]};

%colors = lines(size(timings_p_retracton,2));
hold on
%h = gobjects(1,size(timings_p_retracton,2));
x = linspace(500,2000,size(timings_p_retracton,1));
for k = 1:size(timings_p_retracton,2)
    style = styles{mod(k-1,numel(styles))+1};
    mark = markers{mod(k-1,numel(markers))+1};
    h(k) = plot(x, timings_p_retracton(:,k), 'LineStyle', style,'Marker',mark,'Color', colors{k}, 'LineWidth', 2);
end
hold off
xlabel('p');
ylabel('Time (s)');
title('Individual timing results');
legend(labs, 'Location', 'northwest');
grid on


% Add up combinded cost

timings_combinded = zeros(4,4);
timings_combinded(1,:) = timings_p_retracton(:,1)' + timings_p_retracton(:,2)';
timings_combinded(2,:) = timings_p_retracton(:,3)' + timings_p_retracton(:,4)';
timings_combinded(3,:) = timings_p_retracton(:,5)' + timings_p_retracton(:,6)';
timings_combinded(4,:) = timings_p_retracton(:,7)' + timings_p_retracton(:,8)';

timings_combinded = timings_combinded';

subplot(1,2,2)
styles = {'-','--',':','-.'};
markers = {'o','s','*','d'};
colors = {[1 0 0],[0 0 1],[0.7520    0.3600    0.9840],[0 0 0]};

hold on
x = linspace(500,2000,size(timings_p_retracton,1));
for k = 1:size(timings_combinded,2)
    style = styles{mod(k-1,numel(styles))+1};
    mark = markers{mod(k-1,numel(markers))+1};
    h(k) = plot(x, timings_combinded(:,k), 'LineStyle', style,'Marker',mark,'Color', colors{k}, 'LineWidth', 2);
end

labs = {'PF + PF inv','PL + PL inv.','PL Cay. + PL Cay. inv','Cayley + Cayley inv'};
xlabel('p');
ylabel('Time (s)');
title('Forward+inverse timing results');
legend(labs, 'Location', 'northwest');
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
saveas(fig, 'timings.png');