from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class UserBackground(BaseModel):
    gender: Optional[str] = Field(None, description="用户性别，适用所有类别")
    age: Optional[int] = Field(None, description="用户年龄，适用所有类别")
    occupation: Optional[str] = Field(None, description="用户职业，适用所有类别")
    income_level: Optional[str] = Field(None, description="用户收入水平，适用所有类别")
    experience: Optional[str] = Field(None, description="使用经验水平，如'新手'、'中级'、'专家'，适用技术类产品尤为重要")
    tech_familiarity: Optional[str] = Field(None, description="技术熟练度，适用于电子产品、软件等技术密集型产品")
    purchase_purpose: Optional[str] = Field(None, description="购买主要目的，如'自用'、'送礼'、'办公'，适用所有类别")
    region: Optional[str] = Field(None, description="用户所在地区，适用所有类别")
    education_level: Optional[str] = Field(None, description="教育水平，部分高技术产品或专业产品时参考")
    usage_frequency: Optional[str] = Field(None, description="使用频率，如'每天'、'偶尔'，适用所有类别")
    brand_loyalty: Optional[str] = Field(None, description="品牌忠诚度，适用所有类别")

class ProductInfo(BaseModel):
    name: str = Field(..., description="产品名称，适用所有类别")
    category: str = Field(..., description="产品类别，如'电子产品'、'日用品'、'食品饮料'等")
    price_range: Optional[str] = Field(None, description="价格区间，适用所有类别")
    features: Optional[List[str]] = Field(None, description="产品特点，适用所有类别")
    
    # 下面字段针对部分类别，非必填
    brand: Optional[str] = Field(None, description="品牌，电子产品、服装、食品等类别重要")
    model_number: Optional[str] = Field(None, description="型号，电子产品必填")
    specifications: Optional[Dict[str, str]] = Field(
        None,
        description="产品具体规格信息（键值对），如电子产品CPU、屏幕尺寸，服装尺码，食品成分等"
    )
    warranty_period: Optional[str] = Field(None, description="保修期，电子产品、家电类产品重要")
    expiration_date: Optional[str] = Field(None, description="有效期，食品饮料类产品必须")
    material: Optional[str] = Field(None, description="材质，服装、家居用品等类目重要")
    weight: Optional[str] = Field(None, description="重量，物流及使用体验相关，适用大部分实物产品")
    dimensions: Optional[str] = Field(None, description="尺寸，适用于家具、家电、服装等")
    package_info: Optional[str] = Field(None, description="包装信息，适用食品、日用品等")
    energy_efficiency: Optional[str] = Field(None, description="能效等级，家电类产品重要")
    safety_certifications: Optional[List[str]] = Field(None, description="安全认证，如3C、FDA等，适用于食品、电子产品、玩具等")
    usage_instructions: Optional[str] = Field(None, description="使用说明，适用所有类别")
    additional_info: Optional[Dict[str, str]] = Field(None, description="其他补充信息，灵活扩展")


class QualityCheckResult(BaseModel):
    authenticity_score: float = Field(..., ge=1, le=5, description="真实性评分")
    consistency_score: float = Field(..., ge=1, le=5, description="一致性评分")
    specificity_score: float = Field(..., ge=1, le=5, description="具体性评分")
    language_score: float = Field(..., ge=1, le=5, description="语言自然度评分")
    overall_score: float = Field(..., ge=1, le=5, description="总体评分")
    analysis: List[str] = Field(..., description="分析意见列表")
    suggestions: Optional[List[str]] = Field(None, description="改进建议列表")


class GeneratedReview(BaseModel):
    id: Optional[int] = None
    user_background: UserBackground
    product_info: ProductInfo
    rating: float = Field(..., ge=1, le=5, description="评分(1-5)")
    content: str = Field(..., description="评价内容")
    sentiment: str = Field(..., description="情感倾向")
    experience: str = Field(..., description="使用体验")
    pros: List[str] = Field(..., description="优点列表")
    cons: List[str] = Field(..., description="缺点列表")
    sentiment_score: float = Field(..., description="情感置信评分")
    quality_score: float = Field(..., description="质量置信评分")
    timeliness_analysis: Optional[Dict] = None

class ReviewGenerationRequest(BaseModel):
    user_background: UserBackground
    product_info: ProductInfo
    num_reviews: int = Field(default=1, ge=1, le=10, description="生成评价数量")

class ReviewGenerationResponse(BaseModel):
    reviews: List[GeneratedReview]
    generation_time: float 
    
class AsyncTask(BaseModel):
    task_id: str
    status: TaskStatus
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    result: Optional[Any] = None
    error: Optional[str] = None