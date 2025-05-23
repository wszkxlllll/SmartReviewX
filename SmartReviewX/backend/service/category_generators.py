from typing import List, Dict, Any
import time
import json
import openai
from ..models.data_model import UserBackground, ProductInfo, GeneratedReview, ReviewGenerationResponse
from ..models.category_prompts import PromptTemplateFactory
from ..config import settings
import logging
import random

logger = logging.getLogger(__name__)

class BaseReviewGenerator:
    """评价生成器基类"""
    
    category: str = None  # 类属性，子类必须定义
    
    def __init__(self):
        """初始化生成器"""
        if not self.category:
            raise NotImplementedError("子类必须定义 category 属性")
            
        try:
            self.client = openai.OpenAI(
                api_key=settings.OPENAI_API_KEY3,
                base_url=settings.OPENAI_API_BASE3
            )
            self.prompt_template = PromptTemplateFactory.create_template(self.category)
        except Exception as e:
            logger.error(f"初始化生成器失败: {str(e)}")
            raise ValueError(f"初始化生成器失败: {str(e)}")

    def generate_review(
        self,
        user_background: UserBackground,
        product_info: ProductInfo
    ) -> GeneratedReview:
        """
        生成产品评价
        
        Args:
            user_background: 用户背景信息
            product_info: 产品信息
            
        Returns:
            生成的评价对象
            
        Raises:
            ValueError: 当生成失败且无法降级时
        """
        max_retries = settings.MAX_RETRIES
        fallback_strategies = [
            self._generate_with_reduced_context,
            self._generate_with_template,
            self._generate_with_fallback
        ]
        
        for attempt in range(max_retries):
            try:
                # 构建提示词
                prompt = self.prompt_template.generate_review_prompt(
                    user_background,
                    product_info
                )
                
                # 调用OpenAI API
                try:
                    response = self.client.chat.completions.create(
                        model=settings.OPENAI_API_MODEL3,
                        messages=[
                            {"role": "system", "content": "你是一个专业的评价生成助手。"},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=settings.LLM_TEMPERATURE,
                        max_tokens=settings.LLM_MAX_TOKENS,
                        response_format={"type": "json_object"}
                    )
                except Exception as e:
                    logger.error(f"OpenAI API调用失败: {str(e)}")
                    raise ValueError(f"OpenAI API调用失败: {str(e)}")
                
                # 解析响应
                content = response.choices[0].message.content
                if not content:
                    logger.warning(f"第{attempt + 1}次尝试：API响应内容为空")
                    continue
                    
                try:
                    result = json.loads(content)
                    #print(result)
                    # 验证必要字段
                    required_fields = ["content", "rating", "sentiment", "sentiment_score", "quality_score"]
                    if not all(field in result for field in required_fields):
                        logger.warning(f"第{attempt + 1}次尝试：响应缺少必要字段")
                        continue
                        
                    # 创建评价对象
                    review = GeneratedReview(
                        user_background=user_background,
                        product_info=product_info,
                        content=result["content"],
                        rating=float(result["rating"]),
                        sentiment=result["sentiment"],
                        experience=result.get("experience", ""),  # 可选字段
                        pros=result.get("pros", []),  # 可选字段
                        cons=result.get("cons", []),  # 可选字段
                        sentiment_score=float(result["sentiment_score"]),
                        quality_score=float(result["quality_score"])
                    )
                    
                    return review
                    
                except json.JSONDecodeError as e:
                    logger.error(f"第{attempt + 1}次尝试：JSON解析错误 - {str(e)}")
                    continue
                except ValueError as e:
                    logger.error(f"第{attempt + 1}次尝试：数值转换错误 - {str(e)}")
                    continue
                    
            except Exception as e:
                logger.error(f"第{attempt + 1}次尝试出错: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(1)  # 添加延迟避免过快重试
                    continue
                    
        # 如果所有重试都失败，尝试降级策略
        for strategy in fallback_strategies:
            try:
                review = strategy(user_background, product_info)
                if review:
                    logger.info("使用降级策略成功生成评价")
                    return review
            except Exception as e:
                logger.error(f"降级策略 {strategy.__name__} 失败: {str(e)}")
                continue
                
        raise ValueError("无法生成评价，所有策略均失败")

    def _generate_with_reduced_context(
        self,
        user_background: UserBackground,
        product_info: ProductInfo
    ) -> GeneratedReview:
        """使用简化的上下文生成评价"""
        simplified_prompt = f"""请生成一条关于{product_info.name}的评价。
用户背景：{user_background.occupation}，{user_background.age}岁
产品特点：{', '.join(product_info.features[:3])}

请以JSON格式返回，包含以下字段：
- content: 评价内容
- rating: 评分(1-5)
- sentiment: 情感倾向
- experience: 使用体验
- pros: 优点列表
- cons: 缺点列表
"""
        try:
            response = self.client.chat.completions.create(
                model=settings.OPENAI_API_MODEL3,
                messages=[
                    {"role": "system", "content": "你是一个专业的评价生成助手。"},
                    {"role": "user", "content": simplified_prompt}
                ],
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS
            )
            
            result = json.loads(response.choices[0].message.content)
            return GeneratedReview(
                user_background=user_background,
                product_info=product_info,
                content=result["content"],
                rating=float(result["rating"]),
                sentiment=result["sentiment"],
                experience=result["experience"],
                pros=result["pros"],
                cons=result["cons"],
                sentiment_score=0.7,
                quality_score=0.7
            )
        except Exception as e:
            logger.error(f"简化上下文生成失败: {str(e)}")
            return None

    def _generate_with_template(
        self,
        user_background: UserBackground,
        product_info: ProductInfo
    ) -> GeneratedReview:
        """使用模板生成评价"""
        template = f"""作为一位{user_background.occupation}，我对{product_info.name}的评价如下：

[使用体验]
{random.choice(["非常好用", "使用体验不错", "基本满足需求"])}

[优点]
- {random.choice(product_info.features)}
- 性价比高
- 质量可靠

[缺点]
- 有待改进
- 可以更好

[总体评价]
{random.choice(["推荐购买", "值得考虑", "可以考虑"])}

评分：{random.randint(3, 5)}分
"""
        try:
            return GeneratedReview(
                user_background=user_background,
                product_info=product_info,
                content=template,
                rating=random.uniform(3.5, 5.0),
                sentiment="positive",
                experience="使用体验良好",
                pros=["优点1", "优点2"],
                cons=["缺点1"],
                sentiment_score=0.6,
                quality_score=0.6
            )
        except Exception as e:
            logger.error(f"模板生成失败: {str(e)}")
            return None

    def _generate_with_fallback(
        self,
        user_background: UserBackground,
        product_info: ProductInfo
    ) -> GeneratedReview:
        """使用最基本的降级策略生成评价"""
        try:
            return GeneratedReview(
                user_background=user_background,
                product_info=product_info,
                content=f"这是一条关于{product_info.name}的评价。",
                rating=3.0,
                sentiment="neutral",
                experience="基本可用",
                pros=["基本功能完整"],
                cons=["有待改进"],
                sentiment_score=0.5,
                quality_score=0.5
            )
        except Exception as e:
            logger.error(f"降级生成失败: {str(e)}")
            return None

class ElectronicsReviewGenerator(BaseReviewGenerator):
    """电子产品评价生成器"""
    category = "electronics"

class DailyNecessitiesReviewGenerator(BaseReviewGenerator):
    """日用品评价生成器"""
    category = "daily_necessities"

class FoodBeverageReviewGenerator(BaseReviewGenerator):
    """食品饮料评价生成器"""
    category = "food_beverage"

class ClothingReviewGenerator(BaseReviewGenerator):
    """服装鞋帽评价生成器"""
    category = "clothing"

class HomeApplianceReviewGenerator(BaseReviewGenerator):
    """家用电器评价生成器"""
    category = "home_appliance"

class StationeryReviewGenerator(BaseReviewGenerator):
    """教育文具评价生成器"""
    category = "stationery"

class ReviewGeneratorFactory:
    """评价生成器工厂类"""
    
    # 注册所有生成器
    _generators = {
        "electronics": ElectronicsReviewGenerator,
        "daily_necessities": DailyNecessitiesReviewGenerator,
        "food_beverage": FoodBeverageReviewGenerator,
        "clothing": ClothingReviewGenerator,
        "home_appliance": HomeApplianceReviewGenerator,
        "stationery": StationeryReviewGenerator
    }
    
    @classmethod
    def create_generator(cls, category: str) -> BaseReviewGenerator:
        """创建指定类别的评价生成器"""
        if category not in cls._generators:
            raise ValueError(f"不支持的类别: {category}")
        generator_class = cls._generators[category]
        instance = generator_class()
        if not isinstance(instance, BaseReviewGenerator):
            raise TypeError(f"生成器实例必须是 BaseReviewGenerator 的子类")
        return instance

# 验证必填字段
def validate_product_info(product_info: ProductInfo):
    if not product_info.model_number:
        raise ValueError("电子产品必须提供型号信息")
    if not product_info.specifications:
        raise ValueError("电子产品必须提供规格信息")
    if not product_info.warranty_period:
        raise ValueError("电子产品必须提供保修期信息")
        
# 添加电子产品特定的评价要点
def extend_product_info_features(product_info: ProductInfo):
    if not product_info.features:
        product_info.features = []
    product_info.features.extend([
        "功能性能评估",
        "硬件配置分析",
        "软件体验评价",
        "电池续航表现",
        "散热性能",
        "售后服务评价"
    ])

# 验证必填字段
def validate_daily_necessities_info(product_info: ProductInfo):
    if not product_info.material:
        raise ValueError("日用品必须提供材质信息")
    if not product_info.package_info:
        raise ValueError("日用品必须提供包装信息")
        
# 添加日用品特定的评价要点
def extend_daily_necessities_features(product_info: ProductInfo):
    if not product_info.features:
        product_info.features = []
    product_info.features.extend([
        "使用便捷性",
        "材质安全性",
        "耐用性评估",
        "价格合理性",
        "包装设计评价"
    ])

# 验证必填字段
def validate_food_beverage_info(product_info: ProductInfo):
    if not product_info.expiration_date:
        raise ValueError("食品饮料必须提供有效期信息")
    if not product_info.package_info:
        raise ValueError("食品饮料必须提供包装信息")
        
# 添加食品饮料特定的评价要点
def extend_food_beverage_features(product_info: ProductInfo):
    if not product_info.features:
        product_info.features = []
    product_info.features.extend([
        "口味评价",
        "包装安全性",
        "保质期评估",
        "营养价值分析",
        "价格合理性"
    ])

# 验证必填字段
def validate_clothing_info(product_info: ProductInfo):
    if not product_info.material:
        raise ValueError("服装鞋帽必须提供材质信息")
    if not product_info.dimensions:
        raise ValueError("服装鞋帽必须提供尺寸信息")
        
# 添加服装鞋帽特定的评价要点
def extend_clothing_features(product_info: ProductInfo):
    if not product_info.features:
        product_info.features = []
    product_info.features.extend([
        "材质舒适度",
        "款式设计评价",
        "尺码合适性",
        "透气性评估",
        "洗护便捷性"
    ])

# 验证必填字段
def validate_home_appliance_info(product_info: ProductInfo):
    if not product_info.energy_efficiency:
        raise ValueError("家用电器必须提供能效等级信息")
    if not product_info.warranty_period:
        raise ValueError("家用电器必须提供保修期信息")
        
# 添加家用电器特定的评价要点
def extend_home_appliance_features(product_info: ProductInfo):
    if not product_info.features:
        product_info.features = []
    product_info.features.extend([
        "功能实用性",
        "能耗表现",
        "使用便捷性",
        "维护成本",
        "售后服务评价"
    ])

# 验证必填字段
def validate_stationery_info(product_info: ProductInfo):
    if not product_info.material:
        raise ValueError("教育文具必须提供材质信息")
    if not product_info.safety_certifications:
        raise ValueError("教育文具必须提供安全认证信息")
        
# 添加教育文具特定的评价要点
def extend_stationery_features(product_info: ProductInfo):
    if not product_info.features:
        product_info.features = []
    product_info.features.extend([
        "使用安全性",
        "环保性评估",
        "实用性分析",
        "设计创新性",
        "价格合理性"
    ]) 