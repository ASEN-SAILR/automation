clc
clear

%% user set up
trueCoor1 = [40+0/60+14.30551/3600,-(105+15/60+38.39176/3600)]; %will define this coordinate as origin (0,0)
trueCoor2 = [40+0/60+27.95951/3600,-(105+15/60+32.3043/3600)]; 
altitude1 = 1619.927; %m
altitude2 = 1624.112; %m

%% call plot functions and error analysis function
%plotgps("data_loc1/test1.txt",trueCoor1,altitude1)
%error_analysis("data_loc1/test1.txt",trueCoor1,altitude1)

%plotgps("data_loc1/test2.txt",trueCoor1,altitude2)
%error_analysis("data_loc1/test2.txt",trueCoor1,altitude1)

%plotgps("data_loc2/test1.txt",trueCoor2,altitude2)
%error_analysis("data_loc2/test1.txt",trueCoor2,altitude2)

plotgps("data_loc2/test2.txt",trueCoor2,altitude2)
error_analysis("data_loc2/test2.txt",trueCoor2,altitude2)

%plotgps("data_loc2/test3.txt",trueCoor2,altitude2)
%error_analysis("data_loc2/test3.txt",trueCoor2,altitude2)



%% function definitions, don't change anything below this
function result = rms(data)
    result = sqrt(mean((data).^2));
end

function error_analysis(file,trueCoor,altitude)
    coor = table2array(readtable(file));
    SIV = coor(:,4);
    coor = coor(SIV>=4,1:2)/1e7;
    %coor = coor(:,1:2)/1e7;
    
    len = size(coor,1);
    x = zeros(1,len);
    y = x;
    maxdist = 0;

    for i=1:len
        dist(i) = distanceFromTrue(coor(i,:),trueCoor,altitude); %meter
        rad = angleFromTrue(coor(i,:),trueCoor); %from north
        x(i) = dist(i)*sin(rad);
        y(i) = dist(i)*cos(rad);
        if maxdist<dist
            maxdist = dist;
        end
    end
    
    avg = mean(dist);
    sigma = std(dist);
    precision = max(sqrt((mean(x)-x).^2+(mean(y)-y).^2));
    fprintf("For testing data at [%.6f,%.6f]",trueCoor(1),trueCoor(2));
    fprintf("\nMax distance error: "+max(dist)+" m\n");
    fprintf("Distance error mean: "+avg+" m\n");
    fprintf("Standard deviation: %.2f m\n", sigma);
    fprintf("Precision: +/- %.2f m\n",precision);
    
end

function plotgps(file,trueCoor,altitude)
    coor = table2array(readtable(file));
    SIV = coor(:,4);
    coor = coor(SIV>=10,1:2)/1e7;
    %coor = coor(:,1:2)/1e7;
    
    len = size(coor,1);
    x = zeros(1,len);
    y = x;
    maxdist = 0;

    for i=1:len
        dist = distanceFromTrue(coor(i,:),trueCoor,altitude); %meter
        rad = angleFromTrue(coor(i,:),trueCoor); %from north
        x(i) = dist*sin(rad);
        y(i) = dist*cos(rad);
        if maxdist<dist
            maxdist = dist;
        end
    end

    figure
    scatter(x,y,50,'.b')
    hold on
    scatter(0,0,150,'*r')
    grid on
    xlabel("East(meter)")
    ylabel("North(meter)")
    xlim([-maxdist,maxdist])
    ylim([-maxdist,maxdist])
    legend('Locations read from GPS','True Location','location','best')
    title("GPS test for "+len+" points at 2s difference at ["+trueCoor(1)+","+trueCoor(2)+"]")
    set(gca,'FontSize',18)
    hold off
end

function meter = distanceFromTrue(currCoor,trueCoor,alti)
    deg2rad = pi/180;
    lat = currCoor(1)*deg2rad;
    lon = currCoor(2)*deg2rad;
    truelat = trueCoor(1)*deg2rad;
    truelon = trueCoor(2)*deg2rad;
    radius = 6371000+alti; %m
   
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

