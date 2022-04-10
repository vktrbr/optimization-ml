import numpy as np
from numbers import Real
from typing import Literal
from MultiDimensionalOptimization.algorithms.gd_optimal_step import gradient_descent_optimal_step


def linear_regression(x: np.ndarray,
                      y: np.ndarray,
                      reg_type: Literal['l1', 'l2', None] = None,
                      epsilon: Real = 1e-4,
                      const_l1: Real = 1e-1,
                      const_l2: Real = 1e-1):
    """
    Make linear regression with tikhonov or lasso regularization or without regularization

    :param x:
    :param y:
    :param reg_type:
    :param epsilon:
    :param const_l1:
    :param const_l2:
    :return:
    """
    x = np.hstack([np.ones((x.shape[0], 1)), x])
    if reg_type is None:
        def loss_function(w):
            return ((x @ w - y) ** 2).sum()

        w0 = np.random.random(size=x.shape[1])
        return gradient_descent_optimal_step(loss_function, w0, epsilon=epsilon)[0]['point']
    if reg_type == 'l2':
        def loss_function(w):
            return ((x @ w - y) ** 2).sum() + const_l2 * (w ** 2).sum()

        w0 = np.random.random(size=x.shape[1])
        return gradient_descent_optimal_step(loss_function, w0, epsilon=epsilon)[0]['point']


if __name__ == '__main__':
    from sklearn.datasets import make_regression
    from sklearn.linear_model import LinearRegression, Ridge

    print('Test without regularization')
    print('--------------------------------')
    x_data, y_data = make_regression(30, 5)
    print('Our method:\t', np.round(linear_regression(x_data, y_data), 2))

    model: LinearRegression = LinearRegression()
    model.fit(x_data, y_data)
    print('Sklearn:\t', np.round([model.intercept_] + list(model.coef_), 2))
    print('--------------------------------')

    print('Test with l2')
    print('--------------------------------')
    x_data, y_data = make_regression(30, 5)
    print('Our method:\t', np.round(linear_regression(x_data, y_data, reg_type='l2', const_l2=.5), 2))

    model: Ridge = Ridge(alpha=.5)
    model.fit(x_data, y_data)
    print('Sklearn:\t', np.round([model.intercept_] + list(model.coef_), 2))
    print('--------------------------------')