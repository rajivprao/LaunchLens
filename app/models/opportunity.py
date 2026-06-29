from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class MarketSignal:
    level: str
    reasoning: str
    evidence: str
    confidence: float


@dataclass
class MarketSummary:
    overall_market: str
    market_stage: str
    reasoning: str
    evidence: str
    confidence: float


@dataclass
class Competition:
    level: str
    reasoning: str
    evidence: str
    confidence: float
    major_brands: List[str] = field(default_factory=list)


@dataclass
class Pricing:
    market_price_range: str
    reasoning: str
    evidence: str
    confidence: float


@dataclass
class CustomerVoice:
    pain_points: List[str]
    desired_features: List[str]
    common_expectations: List[str]
    evidence: str
    confidence: float


@dataclass
class MarketMaturity:
    level: str
    reasoning: str
    evidence: str
    confidence: float


@dataclass
class OpportunityAnalysis:

    market_interest: MarketSignal

    market_summary: MarketSummary

    competition: Competition

    pricing: Pricing

    customer_voice: CustomerVoice

    market_maturity: MarketMaturity

    opportunities: List[str]

    risks: List[str]

    positioning_opportunities: List[str]