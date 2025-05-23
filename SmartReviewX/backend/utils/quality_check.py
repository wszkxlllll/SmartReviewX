import numpy as np
from typing import List, Dict, Any
from ..models.data_model import GeneratedReview, UserBackground
from ..models.check_prompt import CheckPromptTemplate
from openai import AsyncOpenAI
from ..config import settings
import json
import logging
import asyncio

logger = logging.getLogger(__name__)

class QualityChecker:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY3,
            base_url=settings.OPENAI_API_BASE3
        )
        self.prompt_template = CheckPromptTemplate()

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
            
            # 根据不同的检查维度使用不同的参数
            if dimension_name == "真实性":
                prompt = prompt_method(review.content, review.user_background)
            else:
                prompt = prompt_method(review.content)
            
            # 调用OpenAI API
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_API_MODEL3,
                messages=[
                    {"role": "system", "content": "你是一个专业的评价质量检查助手。请根据评价内容的质量给出1-5分的评分，5分表示最高质量。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,  # 降低温度以获得更稳定的结果
                max_tokens=500,  # 增加token限制以确保完整响应
                response_format={"type": "json_object"}
            )
            
            # 解析响应
            result = response.choices[0].message.content
            try:
                result_dict = json.loads(result)
                score = result_dict.get("score", 0)
                # 确保评分在1-5之间
                if score < 1:
                    score = 1
                elif score > 5:
                    score = 5
                return {
                    "score": score,
                    "reason": result_dict.get("reason", "")
                }
            except json.JSONDecodeError:
                logger.error(f"Failed to parse {dimension_name} check result: {result}")
                return {
                    "score": 1,  # 最低分而不是0分
                    "reason": f"Failed to parse {dimension_name} check result"
                }
                
        except Exception as e:
            logger.error(f"Error in {dimension_name} check: {str(e)}")
            return {
                "score": 1,  # 最低分而不是0分
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
            tasks = [
                self._check_quality_dimension(review, "check_authenticity_prompt", "真实性"),
                self._check_quality_dimension(review, "check_consistency_prompt", "一致性"),
                self._check_quality_dimension(review, "check_specificity_prompt", "具体性"),
                self._check_quality_dimension(review, "check_language_naturalness_prompt", "语言自然度")
            ]
            
            results = await asyncio.gather(*tasks)
            
            # 计算总体评分
            scores = {
                "真实性": results[0]["score"],
                "一致性": results[1]["score"],
                "具体性": results[2]["score"],
                "语言自然度": results[3]["score"]
            }
            
            # 确保所有评分都在1-5之间
            for key in scores:
                if scores[key] < 1:
                    scores[key] = 1
                elif scores[key] > 5:
                    scores[key] = 5
            
            overall_score = sum(scores.values()) / len(scores)
            
            # 生成分析报告
            analysis_prompt = self.prompt_template.generate_analysis_prompt(
                review.content,
                scores
            )
            
            analysis_response = await self.client.chat.completions.create(
                model=settings.OPENAI_API_MODEL3,
                messages=[
                    {"role": "system", "content": "你是一个专业的评价质量分析助手。"},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.1,  # 降低温度以获得更稳定的结果
                max_tokens=1000,  # 增加token限制以确保完整响应
                response_format={"type": "json_object"}
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

    async def check_quality_batch(self, reviews: List[GeneratedReview]) -> List[Dict[str, Any]]:
        """批量检查评价质量"""
        results = []
        for review in reviews:
            result = await self.check_quality(review)
            results.append(result)
        return results 