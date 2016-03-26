function [indcnt,score] = getanomaly(data,thres);
%
% [indcnt,score] = getanomaly(data,thres);
%
%    This Matlab code computes the anomaly score of a time series 
%    using moving average and random walk.
%
%  References:
%    1. Haibin Cheng, Pang-Ning Tan, Christopher Potter, Steve Klooster. 
%       Detection and Characterization of Anomalies in Multivariate Time 
%       Series. Proc  of SIAM International Conference on Data Mining Proc of 
%       the SIAM International Conference on Data Mining, 2009.
%
%    2. Haibin Cheng, Pang-Ning Tan, Christopher Potter, Steve Klooster. Data 
%       Mining for Visual Exploration and Detection of Ecosystem Disturbances, 
%       Proc of 16th ACM SIGSPATIAL International Conference on Advances in 
%       Geographic Information Systems (ACM GIS), November, 2008

method = thres(8);
data = double(data);
if (thres(6) == 2)
    data = detrend(data,'linear');
end;
mvd = thres(2);
threshold = thres(1);

if (method == 1) %%% moving average anomaly detection
    mva = 12;
            
    data = mov_avg(mva,data);
    data = norm_rows(data);
    
    adata = zeros(size(data,1),1);
    anomalydl = zeros(size(data,1),1);       
    score = [0 0];
    
    for i = 1:size(data,2)
        sdata = (data(:,i)<threshold);
        adata = adata + sdata;  
        if (sdata == 1 & adata==1)
            score(1) = i;
        end;
        indz = find(sdata==0);
        if (i==size(data,2))
            indz = 1;
        end;
        anomalydl(indz,:) = anomalydl(indz,:) + (adata(indz,:) >= mvd);  
        if (adata(indz,:) >= mvd)
            score(2) = adata(indz,:);
        end;
        adata(indz,:) = 0;      
    end;
    clear adata indz;
end;

if (method == 2) 
    mva = 1;
    %data = mov_avg(mva,data);
    sig = 200;
    sc = [];
    
    for j=1:size(data,1)
        X = [];
        for i=1:(size(data,2)-mva+1)
            X = [X reshape(data(j,i:i+mva-1),[],1)];
        end;
        KXX = exp(-0.5*dist(X).^2/sig);
        KX = zeros(size(KXX,1),size(KXX,2));
        for i = 1:size(KX,1)
            s = -floor((i-1)/12);
            e = 4+s;
            for j=s:e
                ind = i+12*j;
                KX(i,ind) = KXX(i,ind);
            end;
        end;

        %KX = exp(-0.5*dist(data(j,:)).^2/sig);
        S = abs(KX);
		n = size(S,1);
		
		S = S./(repmat(sum(S,1),n,1));
		
		maxinter = 1500;
		
		c = sum(KX,2);
		c = c/sum(c);
		d = 0.1;
        
		cold = 0;
		ep = 10^(-15);
		for i = 1:maxinter
            c = d/n + (1-d)*S*c;
            if (sqrt(sum((c-cold).^2))<ep)
                break;
            end;
            cold = c;
		end;
        sc = [sc;c'];
    end;
    data = (sc - repmat(mean(sc,2),1,size(sc,2)))./repmat(std(sc,[],2),1,size(sc,2));
    
    
    adata = zeros(size(data,1),1);
    anomalydl = zeros(size(data,1),1);       
    score = [0 0];
    
    for i = 1:size(data,2)
        sdata = (data(:,i)<threshold);
        adata = adata + sdata;  
        if (sdata == 1 & adata==1)
            score(1) = i;
        end;
        indz = find(sdata==0);
        if (i==size(data,2))
            indz = 1;
        end;
        anomalydl(indz,:) = anomalydl(indz,:) + (adata(indz,:) >= mvd);  
        if (adata(indz,:) >= mvd)
            score(2) = adata(indz,:);
        end;
        adata(indz,:) = 0;      
    end;
    clear adata indz;
    
end;












