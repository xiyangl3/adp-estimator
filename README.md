# Minimax Optimal Estimation of Approximate Differential Privacy on Neighboring Databases

This repo contains the code for the paper
[Minimax Optimal Estimation of Approximate Differential Privacy on Neighboring Databases](https://arxiv.org/abs/1905.10335)


## Dependencies

* To run the experiments, you need to have the following libraries installed:
    
1. python = 3.6
2. numpy
3. scipy

* The coefficient of best polynomial approximation are pre-computed and stored as ".mat" file. The coefficient of Chebyshev polynomials of the first kind are stored as ".npy" file. 

* To get the coefficient of best polynomial approximation, you need to install Chebfun in Matlab through http://www.chebfun.org/

* To get the coefficient of Chebyshev polynomials, you need to install:

1. sympy


## Citing this work

You are encouraged to cite following paper for acedamic research:

```bibtex
@article{liu2019minimax,
  title={Minimax Rates of Estimating Approximate Differential Privacy},
  author={Liu, Xiyang and Oh, Sewoong},
  journal={arXiv preprint arXiv:1905.10335},
  year={2019}
}
```

## License
[MIT](https://github.com/xiyangl3/adp-estimator/blob/master/LICENSE).