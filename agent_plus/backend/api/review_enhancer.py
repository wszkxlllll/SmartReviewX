from openai import OpenAI
from typing import List, Dict, Optional
from ..models.data_model import GeneratedReview
from ..config import settings
import json
import logging
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

class ReviewEnhancer:
    """评价增强处理类"""
    
    def __init__(self):
        """初始化评价增强器"""
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_API_BASE
        )
        
    def _create_enhancement_prompt(self, review: GeneratedReview) -> str:
        """
        创建增强提示词
        
        Args:
            review: 原始评价对象
            
        Returns:
            增强提示词
        """
        return f"""请基于以下产品评价，使用网络搜索功能补充更多相关信息，使评价更加专业和可信：

产品名称：{review.product_info.name}
产品类别：{review.product_info.category}
产品品牌：{review.product_info.brand}
产品规格：{review.product_info.specifications}

原始评价：
{review.content}

请补充以下方面的信息：
1. 产品的市场定位和竞品对比
2. 最新的用户反馈和评价趋势
3. 相关的技术参数和性能数据
4. 产品的使用场景和适用人群

请保持评价的原有风格和情感倾向，只补充客观事实和数据。

请以JSON格式返回，包含以下字段：
- enhanced_content: 增强后的评价内容
- added_info: 补充的信息列表
- confidence_score: 补充信息的可信度(0-1)
"""

    @retry(
        stop=stop_after_attempt(settings.MAX_RETRIES),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True
    )
    async def _call_enhancement_api(self, prompt: str) -> Dict:
        """
        调用API进行评价增强
        
        Args:
            prompt: 增强提示词
            
        Returns:
            API响应结果
            
        Raises:
            Exception: API调用失败
        """
        try:
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_API_MODEL,
                messages=[
                    {"role": "system", "content": "你是一个专业的评价增强助手。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS
            )
            
            content = response.choices[0].message.content
            if not content:
                raise ValueError("API响应内容为空")
                
            try:
                result = json.loads(content)
                required_fields = ["enhanced_content", "added_info", "confidence_score"]
                if not all(field in result for field in required_fields):
                    raise ValueError("响应缺少必要字段")
                return result
            except json.JSONDecodeError as e:
                logger.error(f"JSON解析错误: {str(e)}")
                raise
                
        except Exception as e:
            logger.error(f"API调用失败: {str(e)}")
            raise

    async def enhance_review(self, review: GeneratedReview) -> GeneratedReview:
        """
        增强评价内容
        
        Args:
            review: 原始评价对象
            
        Returns:
            增强后的评价对象
        """
        try:
            # 创建增强提示词
            prompt = self._create_enhancement_prompt(review)
            
            # 调用API进行增强
            result = await self._call_enhancement_api(prompt)
            
            # 更新评价对象
            review.content = result["enhanced_content"]
            review.quality_score = min(1.0, review.quality_score + 0.1)
            
            # 记录补充的信息
            logger.info(f"评价增强成功，补充信息: {result['added_info']}")
            logger.info(f"补充信息可信度: {result['confidence_score']}")
            
            return review
            
        except Exception as e:
            logger.error(f"评价增强失败: {str(e)}")
            return review
            
    async def enhance_reviews(self, reviews: List[GeneratedReview]) -> List[GeneratedReview]:
        """
        批量增强评价内容
        
        Args:
            reviews: 原始评价列表
            
        Returns:
            增强后的评价列表
        """
        tasks = [self.enhance_review(review) for review in reviews]
        return await asyncio.gather(*tasks) 