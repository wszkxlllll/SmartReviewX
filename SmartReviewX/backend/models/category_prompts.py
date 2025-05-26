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
        base_prompt = CategoryPromptTemplate.generate_review_prompt(user_background, product_info)
        
        # 添加电子产品特定的Few-shot examples
        electronics_examples = """
【电子产品评价示例】
示例1:
用户背景：
- 性别：男
- 年龄：32
- 职业：软件开发工程师
- 收入水平：高
- 使用经验：精通
- 技术熟悉度：精通
- 购买目的：工作需要

产品信息：
- 名称：ProBook X5
- 类别：笔记本电脑
- 价格区间：8000-12000元
- 品牌：TechMaster
- 规格：处理器: i7-13代, 内存: 16GB, 存储: 1TB SSD

评价结果：
{
  "rating": 4,
  "content": "作为软件开发工程师，我对这款ProBook X5的性能相当满意。搭载13代i7处理器和16GB内存，运行多个开发环境和虚拟机时流畅无卡顿。SSD读写速度优秀，大型项目编译速度提升明显。键盘手感舒适，适合长时间编码工作。散热系统表现中规中矩，高负载下风扇噪音较大，但温度控制得当。续航方面，中等亮度下能维持约6小时，满足一般办公需求。系统预装软件较少，没有明显的性能拖累。整体而言是一款性价比不错的开发用机。",
  "sentiment": "积极",
  "sentiment_score": 0.8,
  "quality_score": 0.9,
  "pros": [
    "性能强劲，运行多个开发环境流畅",
    "SSD读写速度快，编译效率高",
    "键盘手感舒适，适合长时间编码",
    "系统预装软件少，性能无拖累",
    "性价比高"
  ],
  "cons": [
    "高负载下风扇噪音较大",
    "续航时间一般，仅6小时左右"
  ]
}

示例2:
用户背景：
- 性别：女
- 年龄：26
- 职业：设计师
- 收入水平：中高
- 使用经验：熟练
- 技术熟悉度：精通
- 购买目的：工作需要

产品信息：
- 名称：DesignPad Pro
- 类别：平板电脑
- 价格区间：5000-7000元
- 品牌：CreativeTouch
- 规格：屏幕: 12.9英寸, 分辨率: 2732×2048, 存储: 256GB

评价结果：
{
  "rating": 5,
  "content": "身为专业设计师，这款DesignPad Pro彻底改变了我的工作流程。12.9英寸的高分辨率屏幕色彩准确度极高，P3广色域覆盖让设计作品呈现更为精准。触控笔响应灵敏，压感级别丰富，手绘效果接近真实纸笔体验。搭配专业绘图软件运行流畅，没有明显卡顿。续航表现出色，中等亮度下能持续工作8小时以上。机身轻薄，携带方便，经常需要客户现场修改设计方案的我非常依赖这一点。唯一遗憾是256GB存储对大型设计文件略显不足，建议设计师考虑更大容量版本。",
  "sentiment": "积极",
  "sentiment_score": 0.95,
  "quality_score": 0.95,
  "pros": [
    "高分辨率屏幕，色彩准确度高",
    "触控笔响应灵敏，压感级别丰富",
    "专业绘图软件运行流畅",
    "续航时间长，可达8小时以上",
    "机身轻薄，携带方便"
  ],
  "cons": [
    "256GB存储对大型设计文件略显不足"
  ]
}
"""
        return base_prompt + """

请特别关注以下方面：
1. 功能性能：运行速度、功能丰富度、稳定性
2. 硬件配置和外观设计
3. 软件体验（系统流畅度、App兼容性）
4. 电池续航、散热表现
5. 售后服务、质保政策

""" + electronics_examples

class DailyNecessitiesPromptTemplate(CategoryPromptTemplate):
    """日用品提示词模板"""
    @staticmethod
    def generate_review_prompt(user_background: UserBackground, product_info: ProductInfo) -> str:
        base_prompt = CategoryPromptTemplate.generate_review_prompt(user_background, product_info)
        
        # 添加日用品特定的Few-shot examples
        daily_examples = """
【日用品评价示例】
示例1:
用户背景：
- 性别：女
- 年龄：30
- 职业：白领
- 收入水平：中等
- 使用经验：日常使用
- 购买目的：个人使用
- 使用频率：每天

产品信息：
- 名称：轻奢保温杯
- 类别：日用品
- 价格区间：200-300元
- 品牌：LifeStyle
- 材质：304不锈钢
- 容量：500ml

评价结果：
{
  "rating": 5,
  "content": "作为一名办公室白领，这款LifeStyle保温杯已经成为我日常生活的必备品。304不锈钢材质让我对饮水安全很放心，500ml的容量刚好满足上午的饮水需求。保温效果出众，早上装入的热茶，午饭时仍然温热适宜。杯盖设计严密不漏水，单手开启也很方便，放在电脑旁也不担心。外观简约时尚，拿在手里有质感，同事都很羡慕。清洗方便，杯口大小适中，洗杯刷能轻松伸入内部。唯一的小缺点是稍微偏重，但考虑到保温效果，完全可以接受。",
  "sentiment": "积极",
  "sentiment_score": 0.9,
  "quality_score": 0.95,
  "pros": [
    "304不锈钢材质，饮水安全",
    "500ml容量适中，满足日常需求",
    "保温效果出众，热茶保持温热",
    "杯盖设计严密，单手开启方便",
    "外观简约时尚，质感好",
    "清洗方便，杯口大小适中"
  ],
  "cons": [
    "稍微偏重"
  ]
}

示例2:
用户背景：
- 性别：男
- 年龄：45
- 职业：教师
- 收入水平：中等
- 使用经验：经常使用
- 购买目的：家庭使用
- 使用频率：每天

产品信息：
- 名称：超细纤维抹布套装
- 类别：日用品
- 价格区间：40-60元
- 品牌：CleanHome
- 材质：超细纤维
- 规格：30x30cm，5片装

评价结果：
{
  "rating": 4,
  "content": "家里打扫卫生主要靠我，这套CleanHome超细纤维抹布确实提高了清洁效率。吸水性强，一片抹布就能擦干一张餐桌溢出的水，不会留下水痕。对灰尘的吸附力也很好，清洁电视柜和书架特别方便。材质柔软，清洁玻璃和镜面不会留下划痕。使用一个月后进行机洗，没有明显变形或掉毛现象，品质不错。唯一美中不足的是颜色较浅，容易显脏，建议厂家推出深色系列。性价比很高，比普通抹布贵不了多少，但使用体验提升明显。",
  "sentiment": "积极",
  "sentiment_score": 0.8,
  "quality_score": 0.85,
  "pros": [
    "吸水性强，不留水痕",
    "灰尘吸附力好",
    "材质柔软，不伤表面",
    "耐用性好，机洗不变形",
    "性价比高"
  ],
  "cons": [
    "颜色较浅，容易显脏"
  ]
}
"""
        return base_prompt + """

请特别关注以下方面：
1. 使用便捷性和实用性
2. 材质安全、环保
3. 耐用性和质量稳定性
4. 价格合理性
5. 包装设计及物流体验

""" + daily_examples

class FoodBeveragePromptTemplate(CategoryPromptTemplate):
    """食品饮料提示词模板"""
    @staticmethod
    def generate_review_prompt(user_background: UserBackground, product_info: ProductInfo) -> str:
        base_prompt = CategoryPromptTemplate.generate_review_prompt(user_background, product_info)
        
        # 添加食品饮料特定的Few-shot examples
        food_examples = """
【食品饮料评价示例】
示例1:
用户背景：
- 性别：女
- 年龄：28
- 职业：健身教练
- 收入水平：中等
- 使用经验：经常购买
- 购买目的：健康需求
- 使用频率：每天

产品信息：
- 名称：有机蛋白粉
- 类别：食品补充剂
- 价格区间：200-300元/罐
- 品牌：HealthyFit
- 规格：500g/罐
- 保质期：18个月

评价结果：
{
  "rating": 4,
  "content": "作为健身教练，我对蛋白粉的要求很高。这款HealthyFit有机蛋白粉的蛋白质含量达到85%，氨基酸配比合理，运动后恢复效果明显。溶解度好，用摇摇杯冷水即可完全融化，没有明显颗粒感。原味口感清淡不腻，适合长期食用。包装设计有密封条和量勺，使用方便。唯一不足是价格略高，但考虑到有机认证和品质，还是值得的。对乳糖不耐受的朋友需注意，虽然含量低但仍有少量乳糖成分。总体来说是一款适合日常健身人士的优质蛋白粉。",
  "sentiment": "积极",
  "sentiment_score": 0.8,
  "quality_score": 0.85,
  "pros": [
    "蛋白质含量高，达到85%",
    "氨基酸配比合理，恢复效果好",
    "溶解度好，无颗粒感",
    "口感清淡，适合长期食用",
    "包装设计合理，使用方便"
  ],
  "cons": [
    "价格略高",
    "含有少量乳糖，乳糖不耐受者需注意"
  ]
}

示例2:
用户背景：
- 性别：男
- 年龄：35
- 职业：办公室职员
- 收入水平：中等
- 使用经验：日常消费
- 购买目的：日常饮食
- 使用频率：经常
- 所在地区：北方城市

产品信息：
- 名称：即食燕麦片
- 类别：早餐食品
- 价格区间：30-50元/盒
- 品牌：GrainLife
- 规格：30g*15包
- 保质期：12个月

评价结果：
{
  "rating": 5,
  "content": "北方冬天早上匆忙，这款GrainLife即食燕麦片成了我的救星。冲泡极其方便，热水冲泡一分钟就能食用，口感醇厚不黏牙。每包独立包装，带着去公司也很方便。原味中加入了少量坚果和干果，增加了饱腹感和口感层次。原料表显示无添加蔗糖，用的是天然水果甜度，血糖反应温和，能量持续释放，不会上午工作犯困。包装结实，收到后没有破损情况。15包的分量刚好够两周工作日早餐。价格虽然比普通燕麦片贵一些，但考虑到配料和便捷性，非常值得。",
  "sentiment": "积极",
  "sentiment_score": 0.95,
  "quality_score": 0.9,
  "pros": [
    "冲泡方便，一分钟即可食用",
    "独立包装，携带方便",
    "添加坚果干果，口感丰富",
    "无添加蔗糖，血糖反应温和",
    "包装结实，不易破损",
    "分量适中，适合工作日早餐"
  ],
  "cons": [
    "价格比普通燕麦片贵"
  ]
}
"""
        return base_prompt + """

请特别关注以下方面：
1. 口味与品质
2. 包装安全与方便
3. 保质期和新鲜度
4. 健康成分、营养价值
5. 价格合理性

用户背景要求：
- 品牌忠诚度可影响评价倾向
- 地区差异可能影响口味评价""" + food_examples

class ClothingPromptTemplate(CategoryPromptTemplate):
    """服装鞋帽提示词模板"""
    @staticmethod
    def generate_review_prompt(user_background: UserBackground, product_info: ProductInfo) -> str:
        base_prompt = CategoryPromptTemplate.generate_review_prompt(user_background, product_info)
        
        # 添加服装鞋帽特定的Few-shot examples
        clothing_examples = """
【服装鞋帽评价示例】
示例1:
用户背景：
- 性别：女
- 年龄：25
- 职业：白领
- 收入水平：中等
- 使用经验：时尚达人
- 购买目的：个人穿着
- 使用频率：经常
- 所在地区：南方城市

产品信息：
- 名称：轻薄羊毛针织衫
- 类别：女装
- 价格区间：400-600元
- 品牌：StyleLife
- 材质：80%羊毛，20%聚酯纤维
- 尺寸：S/M/L

评价结果：
{
  "rating": 5,
  "content": "身为南方人，这款StyleLife轻薄羊毛针织衫简直是秋冬季节的完美单品。80%的羊毛含量保证了足够的保暖性，而20%的聚酯纤维提供了良好的弹性和抗皱性。面料亲肤不扎，敏感肌也能直接穿着。M码完美贴合我165cm、52kg的身材，廓形简约但有设计感，搭配西装裤通勤，配牛仔裤休闲都很适合。洗过一次后没有明显起球或变形，但还是建议手洗或干洗为佳。颜色与网页展示一致，质感超出这个价位的预期。唯一需要注意的是初次穿着会有轻微掉毛现象，建议先单独洗一次。",
  "sentiment": "积极",
  "sentiment_score": 0.9,
  "quality_score": 0.95,
  "pros": [
    "羊毛含量高，保暖性好",
    "聚酯纤维提供良好弹性",
    "面料亲肤，不扎皮肤",
    "版型合身，搭配百搭",
    "洗后不易变形起球",
    "颜色与展示一致，质感好"
  ],
  "cons": [
    "初次穿着有轻微掉毛",
    "建议手洗或干洗"
  ]
}

示例2:
用户背景：
- 性别：男
- 年龄：32
- 职业：销售经理
- 收入水平：中高
- 使用经验：经常购买
- 购买目的：工作需求
- 使用频率：经常
- 所在地区：北方城市

产品信息：
- 名称：商务正装皮鞋
- 类别：男鞋
- 价格区间：800-1200元
- 品牌：GentlemanStep
- 材质：头层牛皮
- 尺码：38-44码

评价结果：
{
  "rating": 4,
  "content": "作为销售经理，体面的皮鞋是必不可少的。这双GentlemanStep商务皮鞋使用了真正的头层牛皮，皮质柔软有光泽，做工精细，鞋底车缝线整齐无断线。脚感舒适，内里软皮包裹，即使站立一整天也不会有明显不适。鞋楦形状中规中矩，不夸张但也不老气，与各式西装都能很好搭配。尺码偏大半码，我平时穿42码，这款选41码刚好。耐用度方面，穿了两个月，鞋面保养得当依然挺括有型。最大缺点是鞋底略硬，需要一周左右磨合期。总体来说，这个价位能买到这样品质的皮鞋已经很超值了。",
  "sentiment": "积极",
  "sentiment_score": 0.8,
  "quality_score": 0.85,
  "pros": [
    "头层牛皮，皮质柔软有光泽",
    "做工精细，车缝线整齐",
    "脚感舒适，内里软皮包裹",
    "鞋楦形状适中，百搭",
    "耐用度好，保养得当"
  ],
  "cons": [
    "鞋底略硬，需要磨合期",
    "尺码偏大半码"
  ]
}
"""
        return base_prompt + """

请特别关注以下方面：
1. 材质舒适度和耐用度
2. 款式设计和时尚度
3. 尺码合适性
4. 透气性和实用性
5. 洗护便捷性

用户背景要求：
- 品牌忠诚度可影响评价倾向
- 地区差异可能影响尺码选择""" + clothing_examples

class HomeAppliancePromptTemplate(CategoryPromptTemplate):
    """家用电器提示词模板"""
    @staticmethod
    def generate_review_prompt(user_background: UserBackground, product_info: ProductInfo) -> str:
        base_prompt = CategoryPromptTemplate.generate_review_prompt(user_background, product_info)
        
        # 添加家用电器特定的Few-shot examples
        home_appliance_examples = """
【家用电器评价示例】
示例1:
用户背景：
- 性别：女
- 年龄：35
- 职业：会计师
- 收入水平：中等
- 使用经验：熟练
- 购买目的：家庭使用，旧机更换
- 使用频率：经常
- 所在地区：南方城市

产品信息：
- 名称：静音变频空调E6
- 类别：空调
- 价格区间：3000-4000元
- 品牌：CoolBreeze
- 功能：节能静音、智能温控、除湿
- 能效等级：一级能效

评价结果：
{
  "rating": 5,
  "content": "身处南方湿热环境，CoolBreeze静音变频空调E6真的是夏天必备。开机几乎听不到声音，睡眠模式下夜晚特别安静。智能温控很灵敏，温度上下浮动极小，体感特别舒服。开机5分钟内房间就能迅速降温，且节能效果明显，一个月电费比原来的老空调节省了近30%。安装师傅专业负责，安装位置合理。外观设计简洁，和家里的简约风客厅很搭。唯一建议是附带的遥控器按键字体偏小，家里老人用起来稍不方便。",
  "sentiment": "积极",
  "sentiment_score": 0.92,
  "quality_score": 0.96,
  "pros": [
    "静音效果好，睡眠模式特别安静",
    "智能温控灵敏，温度稳定",
    "制冷速度快，5分钟即可降温",
    "节能效果明显，省电30%",
    "安装专业，位置合理",
    "外观设计简洁美观"
  ],
  "cons": [
    "遥控器按键字体偏小，老人使用不便"
  ]
}

示例2:
用户背景：
- 性别：男
- 年龄：40
- 职业：产品经理
- 收入水平：中高
- 使用经验：丰富
- 购买目的：家中新房配备
- 使用频率：每日
- 所在地区：北方城市

产品信息：
- 名称：超滤净水器X8
- 类别：净水器
- 价格区间：2500-3500元
- 品牌：AquaPure
- 功能：五级过滤、直饮、滤芯更换提醒
- 安装方式：厨下式

评价结果：
{
  "rating": 4,
  "content": "家里刚装修完就入手了这款AquaPure超滤净水器X8，外观简洁，安装在橱柜下方完全不占空间。五级过滤效果不错，水质清澈口感改善明显，泡茶、煮饭都能感觉出来差别。配有滤芯更换提醒功能，维护省心。出水速度略微偏慢，特别是夏天用水量大的时候，稍显不足。滤芯价格略高，但胜在品质和服务可靠，厂家包安装且态度很好。综合来看是值得推荐的一款厨下净水器。",
  "sentiment": "积极",
  "sentiment_score": 0.85,
  "quality_score": 0.9,
  "pros": [
    "外观简洁，安装不占空间",
    "五级过滤，水质清澈",
    "口感改善明显",
    "配有滤芯更换提醒功能",
    "厂家包安装，服务好"
  ],
  "cons": [
    "出水速度偏慢",
    "滤芯价格略高"
  ]
}
"""
        return base_prompt + """

请特别关注以下方面：
1. 功能实用性和技术先进度
2. 能耗表现和环保节能
3. 使用便捷性和维护成本
4. 售后服务和保修政策

""" + home_appliance_examples

class StationeryPromptTemplate(CategoryPromptTemplate):
    """教育文具提示词模板"""
    @staticmethod
    def generate_review_prompt(user_background: UserBackground, product_info: ProductInfo) -> str:
        base_prompt = CategoryPromptTemplate.generate_review_prompt(user_background, product_info)
        # 添加教育文具特定的Few-shot examples
        stationery_examples = """
【教育文具评价示例】
示例1:
用户背景：
- 性别：女
- 年龄：22
- 职业：大学生
- 收入水平：一般
- 使用经验：频繁
- 购买目的：学习记录
- 使用频率：每日
- 所在地区：南方城市

产品信息：
- 名称：晨光中性笔G7
- 类别：书写工具
- 价格区间：5-8元/支
- 品牌：晨光
- 笔芯规格：0.5mm
- 墨水颜色：黑色

评价结果：
{
  "rating": 5,
  "content": "作为资深笔控，这款晨光G7中性笔一直是我的学习必备。书写顺滑，不断墨不卡纸，0.5mm笔尖粗细适中，做笔记、写作业都很适合。握感舒适，长时间写字手也不会酸。墨水颜色饱和，晕染情况极少，搭配A4打印纸和笔记本都非常协调。价格实惠，常备一打随时更换。唯一小缺点是笔帽容易丢，但基本不影响使用体验。",
  "sentiment": "积极",
  "sentiment_score": 0.9,
  "quality_score": 0.95,
  "pros": [
    "书写顺滑，不断墨不卡纸",
    "笔尖粗细适中，适合笔记",
    "握感舒适，长时间使用不累",
    "墨水颜色饱和，不晕染",
    "价格实惠"
  ],
  "cons": [
    "笔帽容易丢"
  ]
}

示例2:
用户背景：
- 性别：男
- 年龄：28
- 职业：小学教师
- 收入水平：中等
- 使用经验：经常
- 购买目的：课堂教学
- 使用频率：每周5次
- 所在地区：北方城市

产品信息：
- 名称：儿童环保橡皮擦
- 类别：文具用品
- 价格区间：3-5元/块
- 品牌：GreenNote
- 材质：无毒环保PVC
- 尺寸：4cm*2cm*1cm

评价结果：
{
  "rating": 4,
  "content": "我在课堂上为学生准备了这款GreenNote环保橡皮，材质柔软，无异味，擦拭干净，不易留下残渣。小巧尺寸方便儿童手握使用，孩子们很喜欢。价格便宜，适合大批量采购。唯一不足是颜色略单调，只有白色和粉蓝，希望以后能出更多款式。总体性价比很高，教学专用首选。",
  "sentiment": "积极",
  "sentiment_score": 0.82,
  "quality_score": 0.88,
  "pros": [
    "材质柔软，无异味",
    "擦拭干净，不留残渣",
    "尺寸小巧，适合儿童使用",
    "价格便宜，适合批量采购",
    "性价比高"
  ],
  "cons": [
    "颜色单调，只有白色和粉蓝"
  ]
}
"""
        return base_prompt + """

请特别关注以下方面：
1. 使用安全性和环保性
2. 实用性和耐用性
3. 设计趣味性和创新点
4. 价格合理性

用户背景要求：
- 教育水平可影响使用需求
- 品牌忠诚度可影响评价倾向""" + stationery_examples 

# 工厂类用于创建不同类型的提示词模板
class PromptTemplateFactory:
    @classmethod
    def create_template(cls, category: str) -> CategoryPromptTemplate:
        templates = {
            "electronics": ElectronicsPromptTemplate,
            "daily_necessities": DailyNecessitiesPromptTemplate,
            "food_beverage": FoodBeveragePromptTemplate,
            "clothing": ClothingPromptTemplate,
            "home_appliance": HomeAppliancePromptTemplate,
            "stationery": StationeryPromptTemplate
        }
        
        template_class = templates.get(category.lower())
        if not template_class:
            raise ValueError(f"Unsupported category: {category}")
            
        instance = template_class()
        if not isinstance(instance, CategoryPromptTemplate):
            raise TypeError(f"Template instance must be a subclass of CategoryPromptTemplate")
        return instance 
