close all
% Data from the final table
% Columns: Col 2, Col 3, Col 4, Col 6, Col 7, Col 8
data = [
    4.08e-02 4.91e-02 3.32e-02 1.65e-02 2.03e-02 1.41e-02;
    5.21e-02 5.79e-02 3.54e-02 1.53e-02 1.84e-02 1.24e-02;
    4.44e-02 5.38e-02 3.67e-02 1.65e-02 2.03e-02 1.41e-02;
    4.50e-02 5.28e-02 3.42e-02 1.62e-02 1.97e-02 1.32e-02;
    4.37e-02 5.52e-02 3.95e-02 1.65e-02 2.03e-02 1.41e-02;
    3.49e-02 4.09e-02 2.67e-02 1.57e-02 1.91e-02 1.31e-02;
    4.18e-02 4.93e-02 3.23e-02 1.62e-02 1.99e-02 1.37e-02
]';
cs = lines(8);
cs = cs(5:end,:);
% Create grouped bar plot
figure;
b = bar(data, 'grouped');
b(1).FaceColor = [0.2310    0.6660    0.1960];
b(2).FaceColor = [1 0 0];
b(3).FaceColor = [0 0 1];
b(4).FaceColor = [0.7520    0.3600    0.9840];
b(5).FaceColor = cs(3,:);
b(6).FaceColor = cs(4,:);
b(7).FaceColor = [0 0 0];
% Axis labels and title
xlabel('\sigma');
ylabel('Relative error');
title('Relative error');
xticklabels({'0.2','0.3','0.4','0.6','0.7','0.8'})
% Column legend
legend({'Exp','PF','PL','PL. Cay','QG Gr.','QR','Cayley'},...
       'Location','northeast');

grid on;


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

saveas(fig, 'barplot_BS.png');