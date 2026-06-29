from langchain_core.prompts import ChatPromptTemplate
from schemas.score_schema import MarketScorecard
from prompts.scoring_prompt import SCORING_SYSTEM_PROMPT


class ScoringNode:

    def __init__(self, llm):

        self.chain = (
            ChatPromptTemplate.from_messages(
                [
                    ("system", SCORING_SYSTEM_PROMPT),
                    ("human", "{market_assessment}")
                ]
            )
            | llm.with_structured_output(MarketScorecard)
        )

    def invoke(self, opportunity_analysis):

        return self.chain.invoke(
            {
                "market_assessment": opportunity_analysis
            }
        )