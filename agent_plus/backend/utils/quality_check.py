import numpy as np
from typing import List, Dict, Any
from ..models.data_model import GeneratedReview, UserBackground
from ..models.check_prompt import PromptTemplate
import openai
from ..config import settings
import json
import logging

logger = logging.getLogger(__name__)

class QualityChecker:
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_API_BASE
        )
        self.prompt_template = PromptTemplate()

    async def _check_quality_dimension(
        self,
        review: GeneratedReview,
        prompt_method: str,
        dimension_name: str
    ) -> Dict[str, Any]:
        """
        通用的质量维度检查方法
        
        Args:
            review: 评价对象
            prompt_method: 提示词模板方法名
            dimension_name: 质量维度名称
            
        Returns:
            包含评分和原因的字典
        """
        try:
            # 获取对应的提示词模板方法
            prompt_method = getattr(self.prompt_template, prompt_method)
            prompt = prompt_method(review.content, review.user_background)
            
            # 调用OpenAI API
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_API_MODEL,
                messages=[
                    {"role": "system", "content": "你是一个专业的评价质量检查助手。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS
            )
            
            # 解析响应
            result = response.choices[0].message.content
            try:
                result_dict = json.loads(result)
                return {
                    "score": result_dict.get("score", 0),
                    "reason": result_dict.get("reason", "")
                }
            except json.JSONDecodeError:
                logger.error(f"Failed to parse {dimension_name} check result: {result}")
                return {
                    "score": 0,
                    "reason": f"Failed to parse {dimension_name} check result"
                }
                
        except Exception as e:
            logger.error(f"Error in {dimension_name} check: {str(e)}")
            return {
                "score": 0,
                "reason": f"Error in {dimension_name} check: {str(e)}"
            }

    async def check_quality(self, review: GeneratedReview) -> Dict[str, Any]:
        """
        检查评价质量
        
        Args:
            review: 评价对象
            
        Returns:
            包含各项质量评分的字典
        """
        try:
            # 并行执行所有质量检查
            authenticity_result = await self._check_quality_dimension(
                review, "check_authenticity_prompt", "真实性"
            )
            consistency_result = await self._check_quality_dimension(
                review, "check_consistency_prompt", "一致性"
            )
            specificity_result = await self._check_quality_dimension(
                review, "check_specificity_prompt", "具体性"
            )
            language_result = await self._check_quality_dimension(
                review, "check_language_naturalness_prompt", "语言自然度"
            )
            
            # 计算总体评分
            scores = {
                "真实性": authenticity_result["score"],
                "一致性": consistency_result["score"],
                "具体性": specificity_result["score"],
                "语言自然度": language_result["score"]
            }
            
            overall_score = sum(scores.values()) / len(scores)
            
            # 生成分析报告
            analysis_prompt = self.prompt_template.generate_analysis_prompt(
                review.content,
                scores
            )
            
            analysis_response = await self.client.chat.completions.create(
                model=settings.OPENAI_API_MODEL,
                messages=[
                    {"role": "system", "content": "你是一个专业的评价质量分析助手。"},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS
            )
            
            try:
                analysis_result = json.loads(analysis_response.choices[0].message.content)
                analysis = analysis_result.get("analysis", [])
            except json.JSONDecodeError:
                logger.error("Failed to parse analysis result")
                analysis = ["无法生成分析报告"]
            
            return {
                "scores": scores,
                "overall_score": overall_score,
                "analysis": analysis
            }
            
        except Exception as e:
            logger.error(f"Error in quality check: {str(e)}")
            raise

    def check_quality_batch(self, reviews: List[GeneratedReview]) -> List[Dict[str, Any]]:
        """批量检查评价质量"""
        results = []
        for review in reviews:
            result = self.check_quality(review)
            results.append(result)
        return results 