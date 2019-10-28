clear;clc;
f2 = chebfun2(@(x,y) max(sqrt(y)-sqrt(x),0) ,[0 1 0 1], [60 60]);
f1 = chebfun2(@(x,y) sqrt(y)+sqrt(x) ,[0 1 0 1], [60, 60]);
coeff1 = chebcoeffs2(f1);
coeff2 = chebcoeffs2(f2);


save('coeff_hk.mat',"coeff2")

save('coeff_vk.mat',"coeff1")