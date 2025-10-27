function coords = get_sight_pos_func(imgFile, latLim, longLim, sightPos)
    % Open image
    img = imread(imgFile);
    
    [imgHeight, imgWidth, ~] = size(img);

    coor2pix = @(coord) [(imgWidth).*((coord(2)-longLim(1))/(longLim(2)-longLim(1))) (imgHeight).*((coord(1)-latLim(1))/(latLim(2)-latLim(1)))];
    
    coords = ones(length(sightPos), 2);

    for k=11:11

        coords(k,:) = coor2pix(sightPos(k,:));

    end

end
