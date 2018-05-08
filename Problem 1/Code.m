  %% m = 11,7
clc; clear;

n = 11;
m = 7;
combos = nchoosek(1:n+m,n);

for i = 1:size(combos,1)
    temp = zeros(n+m,1);
    temp(combos(i,:)) = 1;
    coord = zeros(2,n+m);
    for j = 1:n+m
        coord(1,j) = sum(temp(1:j) == 0);
        coord(2,j) = sum(temp(1:j) == 1);
    end
    D(i) = max(abs(coord(1,:)/m - coord(2,:)/n));
end

mean(D)
std(D)
length(D(D>0.6))/length(D(D>0.2))

%% m = 31, 23
clc; clear;

N = 3e6;
n = 31;
m = 23;

Path = zeros(n+m,N);

for i = 1:N
    id = randperm(n+m,n);
    temp = zeros(n+m,1);
    temp(id) = 1;
    coord = zeros(2,n+m);
    for j = 1:n+m
        coord(1,j) = sum(temp(1:j) == 0);
        coord(2,j) = sum(temp(1:j) == 1);
    end
    D(i) = max(abs(coord(1,:)/m - coord(2,:)/n));
end

mean(D)
std(D)
length(D(D>0.6))/length(D(D>0.2))
