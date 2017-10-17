function [S] = walk(N)

clf;                                % clear the entire figure

t = (0:1:N);                       % t is the column vector [0 1 2 3 ... N]

S = [0; cumsum(2*(rand(N,1)>0.5)-1)];  % S is the running sum of +/-1 variables

M = max(abs(S))+1;
plot(t,S);          % plot the path
axis([0 N -M M])
title([int2str(N) '-step random walk'])
