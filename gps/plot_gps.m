clc
clear

%% user set up
trueCoor1 = [40+0/60+27.95951/3600,-(105+15/60+32.3043/3600)]; %will define this coordinate as origin (0,0)
trueCoor2 = [40+0/60+14.30551/3600,-(105+15/60+38.39176/3600)];
altitude1 = 1619.927; %m
altitude2 = 1624.112; %m

%% call plot functions
plotgps("GPSsurveyData.txt",trueCoor1,altitude1)
plotgps("GPSsurveyData2.txt",trueCoor2,altitude2)

%% call error analysis function
error_analysis("GPSsurveyData.txt",trueCoor1,altitude1)


%% function definitions, don't change anything below this
function error_analysis(file,trueCoor,altitude)
    coor = table2array(readtable(file))/1e7;
    coor = coor(:,1:2);
    
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
    
    avg = mean(dist);
    sigma = std(dist);
    z = 1.96; %for 95% CI
    low_bound = avg-z*sigma/sqrt(len);
    up_bound = avg+z*sigma/sqrt(len);
    fprintf("For testing data at ["+trueCoor(1)+","+trueCoor(2)+"]");
    fprintf("Max distance error: "+max(dist)+" m");
    fprintf("Distance RMS error: "+rms(dist)+" m");
    fprintf("95% confidence interval: ["+low_bound+","+up_bound+"]")
end

function plotgps(file,trueCoor,altitude)
    coor = table2array(readtable(file))/1e7;
    coor = coor(:,1:2);
    
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
    scatter(x,y,'.b')
    hold on
    scatter(0,0,'xr')
    grid on
    xlabel("meter")
    ylabel("meter")
    xlim([-maxdist,maxdist])
    ylim([-maxdist,maxdist])
    legend('Locations read from GPS','True Location')
    title("GPS test for "+len+" points at 1 sec difference at ["+trueCoor(1)+","+trueCoor(2)+"]")
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

