import numpy as np
from scipy import stats


class Distribution:
    def sample(self) -> float:
        raise NotImplementedError

    def get_nth_percentile(self, n: float) -> float:
        raise NotImplementedError


class LogNormalDistribution(Distribution):
    def __init__(self, mu: float, sigma: float):
        self.mu = mu
        self.sigma = sigma
        self._dist = stats.lognorm(s=sigma, scale=np.exp(mu))

    def sample(self) -> float:
        return self._dist.rvs()

    def get_nth_percentile(self, n: float) -> float:
        return self._dist.ppf(n / 100)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(mu={self.mu}, sigma={self.sigma})"
