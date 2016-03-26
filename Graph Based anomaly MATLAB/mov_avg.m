function [ moving_avg ] = mov_avg( window_len, data )
%mov_avg:  Given a matrix whose rows indicate values at succesive time intervals return
%          a matrix whose rows are the moving averages.
%
%[ moving_avg ] = mov_avg( window_len, data )
% 1---24  moving average to 1----13
temp = data';

[rows cols ] = size( data );
moving_avg = zeros( cols - window_len + 1, rows ); 

moving_avg( 1, : ) = sum ( temp(1:window_len, : )); 

for col = 2:(cols - window_len + 1)
   moving_avg( col, : ) = moving_avg( col-1, :) + temp( col+window_len-1, :) - temp( col-1, : );
end
moving_avg = moving_avg / window_len;
moving_avg = moving_avg';
