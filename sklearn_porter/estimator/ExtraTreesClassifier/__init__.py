# scikit-learn
from sklearn.ensemble import ExtraTreesClassifier as ExtraTreesClassifierClass

# sklearn-porter
from sklearn_porter.estimator.EstimatorBase import EstimatorBase
from sklearn_porter.estimator.RandomForestClassifier import (
    RandomForestClassifier
)


class ExtraTreesClassifier(RandomForestClassifier, EstimatorBase):
    """Extract model data and port an ExtraTreesClassifier classifier."""

    SKLEARN_URL = 'sklearn.ensemble.ExtraTreesClassifier.html'

    estimator = None  # type: ExtraTreesClassifierClass

    def __init__(self, estimator: ExtraTreesClassifierClass):
        super().__init__(estimator)
