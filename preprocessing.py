#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 17:10:17 2019

@author: lsx
"""

import pandas as pd
import numpy as np


class BaseDrop(object):

    def transform(self, X):
        for index in self.indexes:
            X[index] = None
        if not self.keepdims:
            X = X.dropna()
        if self.reset_index:
            X = X.reset_index(drop=True)
        return X 


class TransformerMixin(object):
    """Mixin class for all transformers in DropOutliers Methods"""
    
    def fit_transform(self, X, y=None, **fit_params):
        """Fit to data, then transform it.

        Fits transformer to X and y with optional parameters fit_params
        and returns a transformed version of X.

        Parameters
        ----------
        X : numpy array of shape [n_samples, n_features]
            Training set.

        y : numpy array of shape [n_samples]
            Target values.

        Returns
        -------
        X_new : numpy array of shape [n_samples, n_features_new]
            Transformed array.

        """
        if y is None:
            # fit method of arity 1 (unsupervised transformation)
            return self.fit(X, **fit_params).transform(X)
        else:
            # fit method of arity 2 (supervised transformation)
            return self.fit(X, y, **fit_params).transform(X)

        
class DropOutliersCI(BaseDrop, TransformerMixin):
    ## TODO: Modifier notation
    """Scale features using statistics that are robust to outliers.

    This Scaler removes the median and scales the data according to
    the quantile range (defaults to IQR: Interquartile Range).
    The IQR is the range between the 1st quartile (25th quantile)
    and the 3rd quartile (75th quantile).

    Centering and scaling happen independently on each feature (or each
    sample, depending on the ``axis`` argument) by computing the relevant
    statistics on the samples in the training set. Median and  interquartile
    range are then stored to be used on later data using the ``transform``
    method.

    Standardization of a dataset is a common requirement for many
    machine learning estimators. Typically this is done by removing the mean
    and scaling to unit variance. However, outliers can often influence the
    sample mean / variance in a negative way. In such cases, the median and
    the interquartile range often give better results.

    .. versionadded:: 0.17

    Read more in the :ref:`User Guide <preprocessing_scaler>`.

    Parameters
    ----------
    with_centering : boolean, True by default
        If True, center the data before scaling.
        This will cause ``transform`` to raise an exception when attempted on
        sparse matrices, because centering them entails building a dense
        matrix which in common use cases is likely to be too large to fit in
        memory.

    with_scaling : boolean, True by default
        If True, scale the data to interquartile range.

    quantile_range : tuple (q_min, q_max), 0.0 < q_min < q_max < 100.0
        Default: (25.0, 75.0) = (1st quantile, 3rd quantile) = IQR
        Quantile range used to calculate ``scale_``.

        .. versionadded:: 0.18

    copy : boolean, optional, default is True
        If False, try to avoid a copy and do inplace scaling instead.
        This is not guaranteed to always work inplace; e.g. if the data is
        not a NumPy array or scipy.sparse CSR matrix, a copy may still be
        returned.

    Attributes
    ----------
    center_ : array of floats
        The median value for each feature in the training set.

    scale_ : array of floats
        The (scaled) interquartile range for each feature in the training set.

        .. versionadded:: 0.17
           *scale_* attribute.

    See also
    --------
    robust_scale: Equivalent function without the estimator API.

    :class:`sklearn.decomposition.PCA`
        Further removes the linear correlation across features with
        'whiten=True'.

    Notes
    -----
    For a comparison of the different scalers, transformers, and normalizers,
    see :ref:`examples/preprocessing/plot_all_scaling.py
    <sphx_glr_auto_examples_preprocessing_plot_all_scaling.py>`.

    https://en.wikipedia.org/wiki/Median_(statistics)
    https://en.wikipedia.org/wiki/Interquartile_range
    """    
    def __init__(self, quantile_range=(5,95), keepdims=True,reset_index=True):
        self.quantile_range = quantile_range
        self.keepdims = True
        self.reset_index = True
        
    def fit(self, X):
        q_min, q_max = np.percentile(X, self.quantile_range)
        index_min = X[X<=q_min].index
        index_max = X[X>=q_max].index
        self.indexes = [index_min,index_max]
        return self

        
class DropOutliersQ(BaseDrop, TransformerMixin):
    ## TODO: Modifier notation
    """Scale features using statistics that are robust to outliers.

    This Scaler removes the median and scales the data according to
    the quantile range (defaults to IQR: Interquartile Range).
    The IQR is the range between the 1st quartile (25th quantile)
    and the 3rd quartile (75th quantile).

    Centering and scaling happen independently on each feature (or each
    sample, depending on the ``axis`` argument) by computing the relevant
    statistics on the samples in the training set. Median and  interquartile
    range are then stored to be used on later data using the ``transform``
    method.

    Standardization of a dataset is a common requirement for many
    machine learning estimators. Typically this is done by removing the mean
    and scaling to unit variance. However, outliers can often influence the
    sample mean / variance in a negative way. In such cases, the median and
    the interquartile range often give better results.

    .. versionadded:: 0.17

    Read more in the :ref:`User Guide <preprocessing_scaler>`.

    Parameters
    ----------
    with_centering : boolean, True by default
        If True, center the data before scaling.
        This will cause ``transform`` to raise an exception when attempted on
        sparse matrices, because centering them entails building a dense
        matrix which in common use cases is likely to be too large to fit in
        memory.

    with_scaling : boolean, True by default
        If True, scale the data to interquartile range.

    quantile_range : tuple (q_min, q_max), 0.0 < q_min < q_max < 100.0
        Default: (25.0, 75.0) = (1st quantile, 3rd quantile) = IQR
        Quantile range used to calculate ``scale_``.

        .. versionadded:: 0.18

    copy : boolean, optional, default is True
        If False, try to avoid a copy and do inplace scaling instead.
        This is not guaranteed to always work inplace; e.g. if the data is
        not a NumPy array or scipy.sparse CSR matrix, a copy may still be
        returned.

    Attributes
    ----------
    center_ : array of floats
        The median value for each feature in the training set.

    scale_ : array of floats
        The (scaled) interquartile range for each feature in the training set.

        .. versionadded:: 0.17
           *scale_* attribute.

    See also
    --------
    robust_scale: Equivalent function without the estimator API.

    :class:`sklearn.decomposition.PCA`
        Further removes the linear correlation across features with
        'whiten=True'.

    Notes
    -----
    For a comparison of the different scalers, transformers, and normalizers,
    see :ref:`examples/preprocessing/plot_all_scaling.py
    <sphx_glr_auto_examples_preprocessing_plot_all_scaling.py>`.

    https://en.wikipedia.org/wiki/Median_(statistics)
    https://en.wikipedia.org/wiki/Interquartile_range
    """    
    def __init__(self, quantile_range=(25,75), keepdims=True,reset_index=True):
        self.quantile_range = quantile_range
        self.keepdims = True
        self.reset_index = True
        
    def fit(self, X):
        q_min, q_max = np.percentile(X, self.quantile_range)
        iqr = q_max - q_min
        outlier_step = 1.5 * iqr
        index_min = X[X<=(q_min-outlier_step)].index
        index_max = X[X>=(q_max+outlier_step)].index
        self.indexes = [index_min,index_max]
        return self        
        

class DropMarkOut(BaseDrop, TransformerMixin):

    def __init__(self, keepdims=True,reset_index=True):
        self.keepdims = True
        self.reset_index = True
    
    def _is_valid(self, X, y):
        if len(X) == len(y):
            return True
        else:
            return False
        
    def fit(self, X, y, mark=1):
        if not self._is_valid():
            raise ValueError('X samples and y samples are mismatch')
        X = X.reset_index(drop=True)
#        y = y.reset_index(drop=True)
        index_seizure = y[y==mark].index
        self.indexes = index_seizure
        return self
