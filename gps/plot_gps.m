clc
clear

%% user set up
trueCoor = [400065308,-1052715937]/1e7; %will define this coordinate as origin (0,0)
coor = table2array(readtable("data.txt"))/1e7;
limit = 100; %x and y limit in plot, meter

%% don't change anything below this

len = size(coor,1);
x = zeros(1,len);
y = x;

for i=1:len
    dist = distanceFromTrue(coor(i,:),trueCoor); %meter
    rad = angleFromTrue(coor(i,:),trueCoor); %from north
    x(i) = dist*sin(rad);
    y(i) = dist*cos(rad);
end

scatter(x,y,'.b')
hold on
scatter(0,0,'xr')
grid on
xlabel("meter")
ylabel("meter")
xlim([-limit,limit])
ylim([-limit,limit])
title("GPS test at ["+trueCoor(1)+","+trueCoor(2)+"]")
hold off

function meter = distanceFromTrue(currCoor,trueCoor)
    deg2rad = pi/180;
    lat = currCoor(1)*deg2rad;
    lon = currCoor(2)*deg2rad;
    truelat = trueCoor(1)*deg2rad;
    truelon = trueCoor(2)*deg2rad;
    radius = 6371000; %m
   
    %haversine
    a = (sin((truelat-lat)/2))^2 + cos(lat)*cos(truelat)*(sin((truelon-lon)/2))^2;
    c = 2*atan2(sqrt(a),sqrt(1-a));
    
    meter = radius * c;
end

function radian = angleFromTrue(currCoor,trueCoor)
    deg2rad = pi/180;
    lat = currCoor(1)*deg2rad;
    lon = currCoor(2)*deg2rad;
    truelat = trueCoor(1)*deg2rad;
    truelon = trueCoor(2)*deg2rad;
    
    a = sin(lon-truelon)*cos(lat);
    b = cos(truelat)*sin(lat)-sin(truelat)*cos(lat)*cos(lon-truelon);
   	radian = atan2(a,b);
end

