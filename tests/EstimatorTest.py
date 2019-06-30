# -*- coding: utf-8 -*-

from sys import version_info as PYTHON_VERSION
from typing import Tuple

import pytest

import random as rd
import numpy as np

import sklearn

from sklearn.tree.tree import DecisionTreeClassifier
from sklearn.ensemble.weight_boosting import AdaBoostClassifier
from sklearn.ensemble.forest import RandomForestClassifier
from sklearn.ensemble.forest import ExtraTreesClassifier
from sklearn.svm.classes import LinearSVC
from sklearn.svm.classes import SVC
from sklearn.svm.classes import NuSVC
from sklearn.neighbors.classification import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB

from sklearn_porter.exceptions import InvalidTemplateError, \
    InvalidMethodError, InvalidLanguageError, NotFittedEstimatorError

try:
    from sklearn.neural_network.multilayer_perceptron import MLPClassifier
except ImportError:
    MLPClassifier = None

try:
    from sklearn.neural_network.multilayer_perceptron import MLPRegressor
except ImportError:
    MLPRegressor = None

try:
    from sklearn.model_selection import GridSearchCV
except ImportError:
    GridSearchCV = None

try:
    from sklearn.model_selection import RandomizedSearchCV
except ImportError:
    RandomizedSearchCV = None

from sklearn_porter.Estimator import Estimator


# Force deterministic number generation:
np.random.seed(0)
rd.seed(0)

# Check python version:
if PYTHON_VERSION[:2] < (3, 5):
    pytest.skip('tests requires python >= 3.5', allow_module_level=True)

# Parse and prepare scikit-learn version:
SKLEARN_VERSION = tuple(map(int, str(sklearn.__version__).split('.')))


@pytest.mark.parametrize('Class', [
    DecisionTreeClassifier,
    AdaBoostClassifier,
    RandomForestClassifier,
    ExtraTreesClassifier,
    LinearSVC,
    SVC,
    NuSVC,
    KNeighborsClassifier,
    GaussianNB,
    BernoulliNB,
    MLPClassifier,
    MLPRegressor,
], ids=[
    'DecisionTreeClassifier',
    'AdaBoostClassifier',
    'RandomForestClassifier',
    'ExtraTreesClassifier',
    'LinearSVC',
    'SVC',
    'NuSVC',
    'KNeighborsClassifier',
    'GaussianNB',
    'BernoulliNB',
    'MLPClassifier',
    'MLPRegressor',
])
def test_valid_base_estimator_since_0_14(Class):
    """Test initialization with valid base estimator."""
    if Class:
        est = Estimator(Class().fit(X=[[1, 1], [1, 1], [2, 2]], y=[1, 1, 2]))
        assert isinstance(est.estimator, Class)



@pytest.mark.skipif(
    SKLEARN_VERSION[:2] < (0, 18),
    reason='requires scikit-learn >= v0.18'
)
def test_list_of_regressors():
    """Test and compare list of regressors."""
    regressors = [
        MLPRegressor
    ]
    regressors = sorted([r.__class__.__name__ for r in regressors])
    candidates = sorted([r.__class__.__name__ for r in Estimator.regressors()])
    assert regressors == candidates


@pytest.mark.skipif(
    SKLEARN_VERSION[:2] < (0, 18),
    reason='requires scikit-learn >= v0.18'
)
def test_list_of_classifiers():
    """Test and compare list of classifiers."""
    classifiers = [
        AdaBoostClassifier,
        BernoulliNB,
        DecisionTreeClassifier,
        ExtraTreesClassifier,
        GaussianNB,
        KNeighborsClassifier,
        LinearSVC,
        NuSVC,
        RandomForestClassifier,
        SVC,
        MLPClassifier,
    ]
    classifiers = sorted([c.__class__.__name__ for c in classifiers])
    candidates = sorted([c.__class__.__name__ for c in Estimator.classifiers()])
    assert classifiers == candidates


@pytest.mark.parametrize('Class', [
    DecisionTreeClassifier,
    AdaBoostClassifier,
    RandomForestClassifier,
    ExtraTreesClassifier,
    LinearSVC,
    SVC,
    NuSVC,
    KNeighborsClassifier,
    GaussianNB,
    BernoulliNB,
    MLPClassifier,
    MLPRegressor,
], ids=[
    'DecisionTreeClassifier',
    'AdaBoostClassifier',
    'RandomForestClassifier',
    'ExtraTreesClassifier',
    'LinearSVC',
    'SVC',
    'NuSVC',
    'KNeighborsClassifier',
    'GaussianNB',
    'BernoulliNB',
    'MLPClassifier',
    'MLPRegressor',
])
def test_unfitted_est(Class):
    """Test unfitted estimators."""
    if Class:
        with pytest.raises(NotFittedEstimatorError):
            Estimator(Class())


@pytest.mark.parametrize('obj', [None, object, 0, 'string'])
def test_invalid_base_estimator(obj):
    """Test initialization with invalid base estimator."""
    with pytest.raises(ValueError):
        Estimator(obj)


@pytest.mark.skipif(
    SKLEARN_VERSION[:2] < (0, 15),
    reason='requires scikit-learn >= v0.15'
)
def test_extraction_from_pipeline():
    """Test the extraction of an estimator from a pipeline."""
    from sklearn.pipeline import Pipeline
    pipeline = Pipeline([('SVM', SVC())])
    pipeline.fit(X=[[1, 1], [1, 1], [2, 2]], y=[1, 1, 2])
    est = Estimator(pipeline)
    assert isinstance(est.estimator, SVC)


@pytest.mark.skipif(
    SKLEARN_VERSION[:2] < (0, 15),
    reason='requires scikit-learn >= v0.15'
)
def test_unfitted_est_in_pipeline():
    """Test the extraction of an estimator from a pipeline."""
    from sklearn.pipeline import Pipeline
    pipeline = Pipeline([('SVM', SVC())])
    with pytest.raises(NotFittedEstimatorError):
        Estimator(pipeline)


@pytest.mark.parametrize('Class', [
    DecisionTreeClassifier,
    AdaBoostClassifier,
    RandomForestClassifier,
    ExtraTreesClassifier,
    LinearSVC,
    SVC,
    NuSVC,
    KNeighborsClassifier,
    GaussianNB,
    BernoulliNB,
    MLPClassifier,
    MLPRegressor,
], ids=[
    'DecisionTreeClassifier',
    'AdaBoostClassifier',
    'RandomForestClassifier',
    'ExtraTreesClassifier',
    'LinearSVC',
    'SVC',
    'NuSVC',
    'KNeighborsClassifier',
    'GaussianNB',
    'BernoulliNB',
    'MLPClassifier',
    'MLPRegressor',
])
@pytest.mark.parametrize('params', [
    (InvalidMethodError, dict(method='i_n_v_a_l_i_d')),
    (InvalidLanguageError, dict(language='i_n_v_a_l_i_d')),
    (InvalidTemplateError, dict(template='i_n_v_a_l_i_d')),
], ids=[
    'InvalidMethodError',
    'InvalidLanguageError',
    'InvalidTemplateError',
])
def test_invalid_params_on_port_method(Class, params: Tuple):
    """Test initialization with valid base estimator."""
    if Class:
        est = Class().fit(X=[[1, 1], [1, 1], [2, 2]], y=[1, 1, 2])
        with pytest.raises(params[0]):
            Estimator(est).port(**params[1])


@pytest.mark.parametrize('Class', [
    DecisionTreeClassifier,
    AdaBoostClassifier,
    RandomForestClassifier,
    ExtraTreesClassifier,
    LinearSVC,
    SVC,
    NuSVC,
    KNeighborsClassifier,
    GaussianNB,
    BernoulliNB,
    MLPClassifier,
    MLPRegressor,
], ids=[
    'DecisionTreeClassifier',
    'AdaBoostClassifier',
    'RandomForestClassifier',
    'ExtraTreesClassifier',
    'LinearSVC',
    'SVC',
    'NuSVC',
    'KNeighborsClassifier',
    'GaussianNB',
    'BernoulliNB',
    'MLPClassifier',
    'MLPRegressor',
])
@pytest.mark.parametrize('params', [
    (InvalidMethodError, dict(method='i_n_v_a_l_i_d')),
    (InvalidLanguageError, dict(language='i_n_v_a_l_i_d')),
    (InvalidTemplateError, dict(template='i_n_v_a_l_i_d')),
], ids=[
    'InvalidMethodError',
    'InvalidLanguageError',
    'InvalidTemplateError',
])
def test_invalid_params_on_dump_method(Class, params: Tuple):
    """Test initialization with valid base estimator."""
    if Class:
        est = Class().fit(X=[[1, 1], [1, 1], [2, 2]], y=[1, 1, 2])
        with pytest.raises(params[0]):
            Estimator(est).dump(**params[1])


@pytest.mark.skipif(
    SKLEARN_VERSION[:2] < (0, 19),
    reason='requires scikit-learn >= v0.19'
)
@pytest.mark.parametrize('Class', [
    GridSearchCV,
    RandomizedSearchCV
], ids=[
    'GridSearchCV',
    'RandomizedSearchCV',
])
def test_extraction_from_optimizer(Class):
    """Test the extraction from an optimizer."""
    params = {'kernel': ('linear', 'rbf'), 'C': [1, 10]}
    search = Class(SVC(gamma='scale'), params, cv=2)

    # Test unfitted optimizer:
    with pytest.raises(ValueError):
        est = Estimator(search)
        assert isinstance(est.estimator, SVC)

    # Test fitted optimizer:
    search.fit(X=[[1, 1], [2, 2], [3, 3], [1, 1], [2, 2], [3, 3]],
               y=[1, 2, 3, 1, 2, 3])
    est = Estimator(search)
    assert isinstance(est.estimator, SVC)
