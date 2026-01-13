import time
import json


def create_research_manager(llm, memory):
    def research_manager_node(state) -> dict:
        history = state["investment_debate_state"].get("history", "")
        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]

        investment_debate_state = state["investment_debate_state"]

        curr_situation = f"{market_research_report}\n\n{sentiment_report}\n\n{news_report}\n\n{fundamentals_report}"
        past_memories = memory.get_memories(curr_situation, n_matches=2)

        past_memory_str = ""
        for i, rec in enumerate(past_memories, 1):
            past_memory_str += rec["recommendation"] + "\n\n"

        prompt = f"""作为投资组合经理和辩论主持人，您的职责是批判性地评估本轮辩论并做出明确决策：支持看跌分析师、看涨分析师，或仅在基于所提出的论点有充分理由时选择持有。

简要总结双方的关键观点，重点关注最具说服力的证据或推理。您的建议——买入、卖出或持有——必须清晰且可执行。避免仅仅因为双方都有有效观点而默认选择持有；要根据辩论中最有力的论点做出明确立场。

此外，为交易员制定详细的投资计划。这应该包括：

您的建议：基于最具说服力的论点做出明确立场。
理由：解释为什么这些论点导致您的结论。
战略行动：实施建议的具体步骤。

考虑您在类似情况下的过去错误。利用这些见解来完善您的决策制定，确保您在学习和改进。请用中文以对话方式呈现您的分析，就像自然说话一样，不使用特殊格式。

以下是您对错误的过去反思：
\"{past_memory_str}\"

以下是辩论：
辩论历史：
{history}

请用中文撰写所有分析内容和建议。"""
        response = llm.invoke(prompt)

        new_investment_debate_state = {
            "judge_decision": response.content,
            "history": investment_debate_state.get("history", ""),
            "bear_history": investment_debate_state.get("bear_history", ""),
            "bull_history": investment_debate_state.get("bull_history", ""),
            "current_response": response.content,
            "count": investment_debate_state["count"],
        }

        return {
            "investment_debate_state": new_investment_debate_state,
            "investment_plan": response.content,
        }

    return research_manager_node
