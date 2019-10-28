clear;clc;
f = chebfun(@(x) abs(x), [-1,1]);

coeff_absx = {};
for poly_degree = 0:100
    poly_degree
    [p,err] = minimax(f,poly_degree);    
    coeff_absx{end+1,1} = chebcoeffs(p);
end

save('coeff_absx.mat',"coeff_absx")