from fastapi import FastAPI, HTTPException, BackgroundTasks
from typing import List, Dict, Any
from ..models.data_model import UserBackground, ProductInfo, GeneratedReview, ReviewGenerationRequest, ReviewGenerationResponse
from .category_generators import ReviewGeneratorFactory
from ..models.category_prompts import PromptTemplateFactory
from ..utils.review_saver import ReviewSaver
from ..utils.quality_check import QualityChecker
from .review_enhancer import ReviewEnhancer
import time
import os
import asyncio
from uuid import uuid4

app = FastAPI(
    title="Review Generator API",
    description="API for generating product reviews based on user background and product information",
    version="1.0.0"
)

# 初始化评价保存器
review_saver = ReviewSaver()

# 初始化评价增强器
review_enhancer = ReviewEnhancer(api_key=os.getenv("OPENAI_API_KEY"))

# 初始化质量检查器
quality_checker = QualityChecker()

# 存储异步任务结果
quality_check_results = {}

async def process_quality_check(review: GeneratedReview, task_id: str):
    """异步处理质量检查"""
    try:
        result = quality_checker.check_quality(review)
        quality_check_results[task_id] = {
            "status": "completed",
            "result": result
        }
    except Exception as e:
        quality_check_results[task_id] = {
            "status": "failed",
            "error": str(e)
        }

async def process_batch_quality_check(reviews: List[GeneratedReview], task_id: str):
    """异步处理批量质量检查"""
    try:
        results = []
        for review in reviews:
            result = quality_checker.check_quality(review)
            results.append(result)
        quality_check_results[task_id] = {
            "status": "completed",
            "results": results
        }
    except Exception as e:
        quality_check_results[task_id] = {
            "status": "failed",
            "error": str(e)
        }

def validate_user_background(user_background: UserBackground, category: str) -> bool:
    """验证用户背景是否符合类别要求"""
    template = PromptTemplateFactory.create_template(category)
    prompt = template.generate_review_prompt(user_background, ProductInfo(
        name="test",
        category=category,
        price_range="test",
        features=[]
    ))
    
    # 检查用户背景要求
    if "用户背景要求" in prompt:
        requirements = prompt.split("用户背景要求：")[1].strip()
        # 这里可以添加更详细的验证逻辑
        return True
    return True

@app.post("/generate_reviews", response_model=ReviewGenerationResponse)
async def generate_reviews(request: ReviewGenerationRequest):
    """
    生成产品评价
    
    - **user_background**: 用户背景信息
    - **product_info**: 产品信息
    - **num_reviews**: 需要生成的评价数量（1-10）
    
    返回生成的评价列表
    """
    try:
        # 验证用户背景
        if not validate_user_background(request.user_background, request.product_info.category):
            raise HTTPException(
                status_code=400,
                detail="用户背景信息不符合该产品类别的要求"
            )
        
        # 根据产品类别创建对应的生成器
        generator = ReviewGeneratorFactory.create_generator(request.product_info.category)
        
        # 生成指定数量的评价
        reviews = []
        total_time = 0
        start_time = time.time()
        
        for _ in range(request.num_reviews):
            review = generator.generate_review(request.user_background, request.product_info)
            reviews.append(review)
            
        total_time = time.time() - start_time
        
        # 保存生成的评价
        review_saver.save_reviews(reviews, request.product_info.category)
            
        return ReviewGenerationResponse(
            reviews=reviews,
            generation_time=total_time
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/enhance_reviews", response_model=ReviewGenerationResponse)
async def enhance_reviews(request: ReviewGenerationRequest):
    """
    增强产品评价
    
    - **user_background**: 用户背景信息
    - **product_info**: 产品信息
    - **num_reviews**: 需要生成的评价数量（1-10）
    
    返回增强后的评价列表
    """
    try:
        # 首先生成原始评价
        generator = ReviewGeneratorFactory.create_generator(request.product_info.category)
        reviews = []
        total_time = 0
        start_time = time.time()
        
        for _ in range(request.num_reviews):
            review = generator.generate_review(request.user_background, request.product_info)
            reviews.append(review)
            
        # 对评价进行增强
        enhanced_reviews = review_enhancer.enhance_reviews(reviews)
        
        total_time = time.time() - start_time
        
        # 保存增强后的评价
        review_saver.save_reviews(enhanced_reviews, request.product_info.category)
            
        return ReviewGenerationResponse(
            reviews=enhanced_reviews,
            generation_time=total_time
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/categories")
async def get_categories():
    """
    获取支持的产品类别列表
    """
    return {
        "categories": [
            "electronics",  # 电子产品
            "daily_necessities",  # 日用品
            "food_beverage",  # 食品饮料
            "clothing",  # 服装鞋帽
            "home_appliance",  # 家用电器
            "stationery"  # 教育文具
        ]
    }

@app.get("/review_stats/{category}")
async def get_review_stats(category: str):
    """
    获取指定类别的评价统计信息
    
    - **category**: 产品类别
    """
    try:
        stats = review_saver.get_review_stats(category)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get review stats: {str(e)}")

@app.get("/health")
async def health_check():
    """
    健康检查接口
    """
    return {"status": "healthy"}

@app.post("/check_quality", response_model=Dict[str, Any])
async def check_quality(review: GeneratedReview, background_tasks: BackgroundTasks):
    """
    异步检查评价质量
    
    - **review**: 需要检查的评价对象
    
    返回任务ID，用于查询检查结果
    """
    task_id = str(uuid4())
    quality_check_results[task_id] = {"status": "processing"}
    
    background_tasks.add_task(process_quality_check, review, task_id)
    
    return {
        "task_id": task_id,
        "status": "processing",
        "message": "质量检查任务已提交，请使用task_id查询结果"
    }

@app.post("/check_quality_batch", response_model=Dict[str, Any])
async def check_quality_batch(reviews: List[GeneratedReview], background_tasks: BackgroundTasks):
    """
    异步批量检查评价质量
    
    - **reviews**: 需要检查的评价对象列表
    
    返回任务ID，用于查询检查结果
    """
    task_id = str(uuid4())
    quality_check_results[task_id] = {"status": "processing"}
    
    background_tasks.add_task(process_batch_quality_check, reviews, task_id)
    
    return {
        "task_id": task_id,
        "status": "processing",
        "message": "批量质量检查任务已提交，请使用task_id查询结果"
    }

@app.get("/quality_check_result/{task_id}", response_model=Dict[str, Any])
async def get_quality_check_result(task_id: str):
    """
    获取质量检查结果
    
    - **task_id**: 任务ID
    
    返回质量检查结果或任务状态
    """
    if task_id not in quality_check_results:
        raise HTTPException(status_code=404, detail="任务不存在")
        
    result = quality_check_results[task_id]
    
    if result["status"] == "completed":
        # 任务完成后，从存储中删除结果
        del quality_check_results[task_id]
        return result["result"]
    elif result["status"] == "failed":
        # 任务失败后，从存储中删除结果
        del quality_check_results[task_id]
        raise HTTPException(status_code=500, detail=result["error"])
    else:
        return {
            "status": "processing",
            "message": "质量检查任务正在处理中"
        } 