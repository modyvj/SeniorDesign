% Created by John Steele 2017

clc;
clf;
clear;

% Input Values

A = sind(45);

% Example path [x y z x-orientation of ee y-orientation of ee]
move = [    1       1       10  0   1;
            -1      -15     0   0   1;
            4       -1      5   0   1;
            -3      11      2   0   1;
            20      0       0   0   1];
        
        
%             20*A    20*A    2.5 -1   0;
%             0       20      5   0   -1;
%             -20*A   20*A    7.5 1   0;
%             -20     0       10  0   1;
%             -20*A   -20*A   7.5 -1  0;
%             0       -20     5   0   -1;
%             20*A    -20*A   2.5 1   0;
%             20      0       0   0   1;
%             15*A    15*A    2.5 -1   0;
%             0       10      5   0   -1;
%             -5*A    5*A     7.5 1   0;
%             -1      0       10  0   1;
%             -5*A    -5*A    7.5 -1  0;
%             0       -10     5   0   -1;
%             15*A    -15*A   2.5 1   0;
%             20      0       0   0   1;
%             1       1       10  0   1   ];

% Function Start

s = size(move);
s = s(1);

for i = 1:s-1
    curPnt = move(i,:);
    newPnt = move(i+1,:);
    scara(curPnt,newPnt);
end