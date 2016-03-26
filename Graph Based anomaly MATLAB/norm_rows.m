function [ new_data ] = norm_rows( data )
%
%norm_l2:  Normalize the data to have an a mean of 0 and a varaiance of 1.
%          Note that we set rows with zero variance to 0.
%
%[ new_data ] = norm_rows( data )

[ data_rows data_cols ] = size( data );

stds =  std( data, 0, 2 );
z_index = find( stds < 0.01 );
stds( z_index ) = 1;

means = mean( data, 2 );
means( z_index ) = 0;

big_means = repmat( means, 1, data_cols );
big_stds  = repmat( stds, 1, data_cols );

new_data = ( data - big_means ) ./ big_stds;
