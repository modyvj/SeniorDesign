% Created by John Steele 2017

function [ikm] = IKM(arms, pos)
%
% Objective:
%
% Generate the inverse kinematic information, relating to a four-joint
% SCARA design.  Initially generate and return the necessary angles to
% achieve the position of the end-effector without orienting the
% end-effector.  
%
% Potentially, determine and return the shortest angle to travel, but get
% it working first.
% _________________________________________________________________________
%
% Input:
%
% arms: An array of size n by 1, containing the lengths of each respective
%       link
% endPos: The end position of the end-effector on the p_0 axis
%
% Output:
%
% angles: The angles needed for each joint to reach the desired end point
% _________________________________________________________________________
% 
% Define:
%
% x: endPos(1): The x position of the desired end point
% y: endPos(2): The y position of the desired end point
% a1: arms(1): The length of the link from J_0 to J_1
% a2: arms(2): The length of the link from J_1 to J_2
%
% s_arms: Size of the array containing the incoming arm lengths
% s_end: Size of the array containing the incoming end points
% _________________________________________________________________________
%
% Assume/State:
% 
% - Part 1 should recieve two link lengths, and two angle values.  Revise
%   as section is developed.
% - Assume that the links of the arm will always form a scalene triangle.
% - All sides of the triangle are either known or acheivable.  Therefore,
%   the Law of Cosines is useable.
% - 
% _________________________________________________________________________

% Confirm inputs are accurate
s_arms = size(arms);
s_end = size(pos);

if (max(s_arms) ~= 5 || min(s_arms) ~= 1)
    error('Link Array has incorrect dimensions.');
elseif (max(s_end) ~= 5 || min(s_end) ~= 1)
    error('Target Array has incorrect dimensions.');
end

% Extract provided information
x = pos(1);
y = pos(2);
% z-position not needed
ox = pos(4);
oy = pos(5);

% base height not needed
r1 = arms(2);
r2 = arms(3);
% prismatic length not needed


% Generate cosine of th2, according to the inverse of the law of cosines
c_th2 = (x^2+y^2-(r1^2+r2^2))/(2*r1*r2);
% Use atan2d to project th2 onto the x_0-y_0 plane
th2 = atan2d(sqrt(1-c_th2^2),c_th2);
% Use th2 to generate the sine of th2
s_th2 = sind(th2);
% Generate th1
th1 = atan2d(y,x)-atan2d(r2*s_th2,r1+r2*c_th2);

th3 = atan2d(oy,ox);

ikm = [th1 th2 th3];

end