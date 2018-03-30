% Created by John Steele 2017


function [] = scara(curPnt,endPnt)
speed = 25;
link = [10 10 10 10 2];
%
% Clarify link lengths and reach functionalities
%

% Debugging: Preset link lengths to ten each - add ability to alter later

% Set base height to min 1 and max 10
if (link(1) < 1 || link(1) > 10)
    if (link(1) < 1)
        link(1) = 1;
    else
        link(1) = 10;
    end
end
% If arms 1 or 2 are shorter than one unit, set them to min of 1
if (link(2) <= 1 || link(3) <= 1)
    if (link(2) <= 1)
        link(2) = 1;
    else
        link(3) = 1;
    end
end
% If arms 1 or 2 are longer than height of base, set them to max or link(0)
if (link(2) > link(1) || link(3) > link(1))
    if (link(2) > link(1))
        link(2) = link(1);
    else
        link(3) = link(1);
    end
end
% Ensure that arm 2 is greater than or equal to arm 3
% May change later after course planning is adapted.  Primarily to prevent
% intersection with base
if (link(3) > link(2))
    link(3) = link(2);
end
% Ensure that the prismatic reach does not exceed [0 link(1)]
if (link(4) < 0 || link(4) > link(1))
    if (link(4) < 0)
        link(4) = 0;
    else
        link(4) = link(1);
    end
end

axisLen  = link(2)+link(3)+1;   % Axis lengths of the plot
linkBase = zeros(10,1);         % Placement array for the z-axis of the arm displays
for i = 1:10
    linkBase(i) = link(1);
end

% Define the angles inherent to the inverse kinematic matrices
curTH = IKM(link,curPnt);   % Angles for the start point
newTH = IKM(link,endPnt);   % Angles for the end point

% Angle ranges for movement from start to end
para1 = linspace(curTH(1),newTH(1),speed);      % th1   (revolute)
para2 = linspace(curTH(2),newTH(2),speed);      % th2   (revolute)
para3 = linspace(curPnt(3),endPnt(3),speed);    % d3    (prismatic)
para4 = linspace(curTH(3),newTH(3),speed);      % th4   (revolute)

% Orientation angle of the end effector
orientAng = linspace(curTH(3),newTH(3),speed);

% Radius of the vertical bars
bar = 0.05;

for i = 1:speed
    
    hold off;
    
    % Denavit-Hartenberg Parameter Table
    DH_Para = [ link(2) link(1)             0       para1(i);       % 1. Link 1
                link(3) 0                   180     para2(i);       % 2. Link 2
                0       link(1)-para3(i)    0       0       ;       % 3. Extension Link
                0       link(5)             0       para4(i)    ];  % 4. End Effector
            
    J1 = DH(DH_Para,1);     % Rotation Matrix of 1.
    J2 = DH(DH_Para,2);     % Rotation Matrix of 2.
    J3 = DH(DH_Para,3);     % Rotation Matrix of 3.
    
    link1_x = linspace(0,J1(1,4),10);           % X parameters of link from origin to point 1
    link1_y = linspace(0,J1(2,4),10);           % Y parameters of link from origin to point 1
    link2_x = linspace(J1(1,4),J2(1,4),10);     % X parameters of link from point 1 to point 2
    link2_y = linspace(J1(2,4),J2(2,4),10);     % Y parameters of link from point 1 to point 2
    
    EffLt = J3*[ -cosd(orientAng(i));  sind(orientAng(i));  0;  1  ]; % Top left corner of end effector
    EffLb = J3*[ -cosd(orientAng(i));  sind(orientAng(i));  1;  1  ]; % Bottom left corner of end effector
    EffRt = J3*[  cosd(orientAng(i)); -sind(orientAng(i));  0;  1  ]; % Top right corner of end effector
    EffRb = J3*[  cosd(orientAng(i)); -sind(orientAng(i));  1;  1  ]; % Bottom right corner of end effector
    orent = J3*[  sind(orientAng(i));  cosd(orientAng(i));  0;  1  ]; % Dot marker for orientation of end effector
    
    effTopX = linspace(EffLt(1),EffRt(1),10);   % X parameters of end effector head
    effTopY = linspace(EffLt(2),EffRt(2),10);   % Y parameters of end effector head
    effTopZ = linspace(EffLt(3),EffRt(3),10);   % Z parameters of end effector head
    
    % Base
    [bX,bY,bZ] = cylinder(bar);
    bX = 10*bX;
    bY = 10*bY;
    bZ = link(1)*bZ;
    
    % Prism Joint
    [pX,pY,pZ] = cylinder(bar);
    pX = pX+J2(1,4);
    pY = pY+J2(2,4);
    pZ = pZ*link(4)+para3(i);
    
    % End Effector (left prong)
    [lX,lY,lZ] = cylinder(bar);
    lX = lX+EffLb(1);
    lY = lY+EffLb(2);
    lZ = lZ+EffLb(3);
    
    % End Effector (right prong)
    [rX,rY,rZ] = cylinder(bar);
    rX = rX+EffRb(1);
    rY = rY+EffRb(2);
    rZ = rZ+EffRb(3);
    
    figure(1);
    plot3(...
        link1_x,link1_y,linkBase,'-k',...       % Link 1 visual
        link2_x,link2_y,linkBase,'-k',...       % Link 2 visual
        effTopX,effTopY,effTopZ,'-k',...        % End Effector top visual
        orent(1),orent(2),orent(3),'-ro'...     % Imaginary Dot orientation of end effector
        );
    hold on;
    surf(bX,bY,bZ);     % Base visual
    surf(pX,pY,pZ);     % Prism arm visual
    surf(lX,lY,lZ);     % Left prong visual
    surf(rX,rY,rZ);     % Right prong visual
        
    axis([-axisLen axisLen -axisLen axisLen 0 axisLen]);
    grid on;
    grid minor;
    xlabel('X');
    ylabel('Y');
    zlabel('Z');
%     view(0,90);
    
    drawnow;
    
end

end