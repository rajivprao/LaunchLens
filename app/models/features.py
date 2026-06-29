from dataclasses import dataclass


@dataclass
class DemandFeatures:

    interest_level: str

    market_growth: str

    confidence: float

    keyword_count: int


@dataclass
class CompetitionFeatures:

    competition_level: str

    confidence: float

    brand_count: int


@dataclass
class PricingFeatures:

    market_price_range: str

    confidence: float


@dataclass
class CustomerFeatures:

    confidence: float

    pain_point_count: int

    desired_feature_count: int

    expectation_count: int


@dataclass
class MaturityFeatures:

    maturity_level: str

    confidence: float


@dataclass
class OpportunityFeatures:

    opportunity_count: int


@dataclass
class RiskFeatures:

    risk_count: int