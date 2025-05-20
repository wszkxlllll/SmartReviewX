from typing import Dict, Any
from .data_model import UserBackground, ProductInfo

class CategoryPromptTemplate:
    """基础类别提示词模板"""
    @staticmethod
    def generate_review_prompt(user_background: UserBackground, product_info: ProductInfo) -> str:
        # 构建用户背景信息
        user_info = []
        if user_background.gender:
            user_info.append(f"- 性别：{user_background.gender}")
        if user_background.age:
            user_info.append(f"- 年龄：{user_background.age}")
        if user_background.occupation:
            user_info.append(f"- 职业：{user_background.occupation}")
        if user_background.income_level:
            user_info.append(f"- 收入水平：{user_background.income_level}")
        if user_background.experience:
            user_info.append(f"- 使用经验：{user_background.experience}")
        if user_background.tech_familiarity:
            user_info.append(f"- 技术熟悉度：{user_background.tech_familiarity}")
        if user_background.purchase_purpose:
            user_info.append(f"- 购买目的：{user_background.purchase_purpose}")
        if user_background.region:
            user_info.append(f"- 所在地区：{user_background.region}")
        if user_background.education_level:
            user_info.append(f"- 教育水平：{user_background.education_level}")
        if user_background.usage_frequency:
            user_info.append(f"- 使用频率：{user_background.usage_frequency}")
        if user_background.brand_loyalty:
            user_info.append(f"- 品牌忠诚度：{user_background.brand_loyalty}")

        # 构建产品信息
        product_details = []
        product_details.append(f"- 名称：{product_info.name}")
        product_details.append(f"- 类别：{product_info.category}")
        if product_info.price_range:
            product_details.append(f"- 价格区间：{product_info.price_range}")
        if product_info.brand:
            product_details.append(f"- 品牌：{product_info.brand}")
        if product_info.model_number:
            product_details.append(f"- 型号：{product_info.model_number}")
        if product_info.specifications:
            specs = [f"{k}: {v}" for k, v in product_info.specifications.items()]
            product_details.append(f"- 规格：{', '.join(specs)}")
        if product_info.warranty_period:
            product_details.append(f"- 保修期：{product_info.warranty_period}")
        if product_info.expiration_date:
            product_details.append(f"- 有效期：{product_info.expiration_date}")
        if product_info.material:
            product_details.append(f"- 材质：{product_info.material}")
        if product_info.weight:
            product_details.append(f"- 重量：{product_info.weight}")
        if product_info.dimensions:
            product_details.append(f"- 尺寸：{product_info.dimensions}")
        if product_info.package_info:
            product_details.append(f"- 包装信息：{product_info.package_info}")
        if product_info.energy_efficiency:
            product_details.append(f"- 能效等级：{product_info.energy_efficiency}")
        if product_info.safety_certifications:
            product_details.append(f"- 安全认证：{', '.join(product_info.safety_certifications)}")
        if product_info.usage_instructions:
            product_details.append(f"- 使用说明：{product_info.usage_instructions}")
        if product_info.features:
            product_details.append(f"- 特点：{', '.join(product_info.features)}")

        return f"""请根据以下用户背景和产品信息生成一条用户评价：

用户背景：
{chr(10).join(user_info)}

产品信息：
{chr(10).join(product_details)}

【Chain of Thought 推理步骤】
1. 分析用户背景特征：
   - 用户画像分析（年龄、职业、收入等）
   - 使用场景分析（使用频率、购买目的等）
   - 专业程度评估（技术熟悉度、使用经验等）

2. 分析产品特征：
   - 核心功能分析
   - 价格定位分析
   - 目标用户匹配度分析

3. 推导评价重点：
   - 基于用户背景确定评价重点
   - 基于产品特征确定评价维度
   - 确定评价语气和风格

4. 生成评价内容：
   - 根据推理结果组织评价内容
   - 确保评价逻辑性和连贯性
   - 添加具体使用体验和细节

【Self-Consistency 一致性要求】
1. 评价内容必须与用户背景一致：
   - 专业术语使用要符合用户技术水平
   - 评价重点要符合用户使用场景
   - 价格评价要符合用户收入水平

2. 评价内容必须与产品特征一致：
   - 功能描述要准确
   - 使用体验要真实
   - 优缺点分析要合理

3. 评价风格要保持一致：
   - 语气要统一
   - 逻辑要连贯
   - 重点要突出

请生成一条真实的用户评价，包含以下内容：
1. 评分（1-5分）
2. 评价内容（200-300字）
3. 情感倾向（积极/消极/中性）
4. 具体的使用体验和优缺点分析

请你对以下内容打分：
1. 情感倾向置信度：0-1（sentiment_score）
2. 质量置信度：0-1（quality_score）

请以JSON格式返回评价结果。"""

class ElectronicsPromptTemplate(CategoryPromptTemplate):
    """电子产品提示词模板"""
    @staticmethod
    def generate_review_prompt(user_background: UserBackground, product_info: ProductInfo) -> str:
        base_prompt = super().generate_review_prompt(user_background, product_info)
        return base_prompt + """

请特别关注以下方面：
1. 功能性能：运行速度、功能丰富度、稳定性
2. 硬件配置和外观设计
3. 软件体验（系统流畅度、App兼容性）
4. 电池续航、散热表现
5. 售后服务、质保政策

用户背景要求：
- 技术熟悉度应为"精通"或"熟练"
- 使用经验应为"熟练"或"精通"
- 购买目的应包含"工作需要"、"个人使用"或"娱乐需求"
- 收入水平应匹配产品价格区间
- 教育水平建议为"本科"或以上"""

class DailyNecessitiesPromptTemplate(CategoryPromptTemplate):
    """日用品提示词模板"""
    @staticmethod
    def generate_review_prompt(user_background: UserBackground, product_info: ProductInfo) -> str:
        base_prompt = super().generate_review_prompt(user_background, product_info)
        return base_prompt + """

请特别关注以下方面：
1. 使用便捷性和实用性
2. 材质安全、环保
3. 耐用性和质量稳定性
4. 价格合理性
5. 包装设计及物流体验

用户背景要求：
- 使用经验应为"日常使用"或"经常使用"
- 购买目的应包含"家庭使用"、"个人使用"或"生活需求"
- 收入水平应匹配产品价格区间
- 使用频率应为"每天"或"经常"
- 品牌忠诚度可影响评价倾向"""

class FoodBeveragePromptTemplate(CategoryPromptTemplate):
    """食品饮料提示词模板"""
    @staticmethod
    def generate_review_prompt(user_background: UserBackground, product_info: ProductInfo) -> str:
        base_prompt = super().generate_review_prompt(user_background, product_info)
        return base_prompt + """

请特别关注以下方面：
1. 口味与品质
2. 包装安全与方便
3. 保质期和新鲜度
4. 健康成分、营养价值
5. 价格合理性

用户背景要求：
- 使用经验应为"经常购买"或"日常消费"
- 购买目的应包含"个人喜好"、"健康需求"或"日常饮食"
- 收入水平应匹配产品价格区间
- 使用频率应为"每天"或"经常"
- 品牌忠诚度可影响评价倾向
- 地区差异可能影响口味评价"""

class ClothingReviewGenerator(CategoryPromptTemplate):
    """服装鞋帽提示词模板"""
    @staticmethod
    def generate_review_prompt(user_background: UserBackground, product_info: ProductInfo) -> str:
        base_prompt = super().generate_review_prompt(user_background, product_info)
        return base_prompt + """

请特别关注以下方面：
1. 材质舒适度和耐用度
2. 款式设计和时尚度
3. 尺码合适性
4. 透气性和实用性
5. 洗护便捷性

用户背景要求：
- 使用经验应为"经常购买"或"时尚达人"
- 购买目的应包含"个人穿着"、"时尚需求"或"日常搭配"
- 收入水平应匹配产品价格区间
- 使用频率应为"经常"或"日常"
- 品牌忠诚度可影响评价倾向
- 地区差异可能影响尺码选择"""

class HomeAppliancePromptTemplate(CategoryPromptTemplate):
    """家用电器提示词模板"""
    @staticmethod
    def generate_review_prompt(user_background: UserBackground, product_info: ProductInfo) -> str:
        base_prompt = super().generate_review_prompt(user_background, product_info)
        return base_prompt + """

请特别关注以下方面：
1. 功能实用性和技术先进度
2. 能耗表现和环保节能
3. 使用便捷性和维护成本
4. 售后服务和保修政策

用户背景要求：
- 使用经验应为"熟练"或"精通"
- 购买目的应包含"家庭使用"、"生活需求"或"升级换代"
- 收入水平应匹配产品价格区间
- 技术熟悉度应为"熟悉"或"精通"
- 使用频率应为"每天"或"经常"
- 教育水平建议为"高中"或以上"""

class StationeryPromptTemplate(CategoryPromptTemplate):
    """教育文具提示词模板"""
    @staticmethod
    def generate_review_prompt(user_background: UserBackground, product_info: ProductInfo) -> str:
        base_prompt = super().generate_review_prompt(user_background, product_info)
        return base_prompt + """

请特别关注以下方面：
1. 使用安全性和环保性
2. 实用性和耐用性
3. 设计趣味性和创新点
4. 价格合理性

用户背景要求：
- 使用经验应为"经常使用"或"学习需求"
- 购买目的应包含"学习使用"、"办公需求"或"创意需求"
- 收入水平应匹配产品价格区间
- 使用频率应为"每天"或"经常"
- 教育水平可影响使用需求
- 品牌忠诚度可影响评价倾向"""

# 工厂类用于创建不同类型的提示词模板
class PromptTemplateFactory:
    @staticmethod
    def create_template(category: str) -> CategoryPromptTemplate:
        templates = {
            "electronics": ElectronicsPromptTemplate,
            "daily_necessities": DailyNecessitiesPromptTemplate,
            "food_beverage": FoodBeveragePromptTemplate,
            "clothing": ClothingReviewGenerator,
            "home_appliance": HomeAppliancePromptTemplate,
            "stationery": StationeryPromptTemplate
        }
        
        template_class = templates.get(category.lower())
        if not template_class:
            raise ValueError(f"Unsupported category: {category}")
            
        return template_class() 