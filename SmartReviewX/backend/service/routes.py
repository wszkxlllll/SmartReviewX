from fastapi import FastAPI, HTTPException, BackgroundTasks, Response
from fastapi.responses import RedirectResponse
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
import logging
import json
from pathlib import Path

# 配置日志
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Review Generator API",
    description="API for generating product reviews based on user background and product information\n目前支持的类别：\n" + "electronics, daily_necessities, food_beverage, clothing, home_appliance, stationery",
    version="1.0.0"
)

# 初始化评价保存器
review_saver = ReviewSaver()

# 初始化评价增强器
review_enhancer = ReviewEnhancer()

# 初始化质量检查器
quality_checker = QualityChecker()

# 创建存储目录
STORAGE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) / "storage"
logger.info(f"存储目录路径: {STORAGE_DIR}")
STORAGE_DIR.mkdir(exist_ok=True)
QUALITY_CHECK_FILE = STORAGE_DIR / "quality_check_results.json"
logger.info(f"存储文件路径: {QUALITY_CHECK_FILE}")

# 初始化存储
def init_storage():
    try:
        if QUALITY_CHECK_FILE.exists():
            logger.info(f"从文件加载任务结果: {QUALITY_CHECK_FILE}")
            with open(QUALITY_CHECK_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info(f"加载的任务结果: {data}")
                return data
        else:
            logger.info("存储文件不存在，创建新的存储")
            return {}
    except Exception as e:
        logger.error(f"初始化存储时发生错误: {str(e)}")
        return {}

def save_storage(data):
    try:
        logger.info(f"保存任务结果到文件: {QUALITY_CHECK_FILE}")
        logger.info(f"保存的数据: {data}")
        with open(QUALITY_CHECK_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info("任务结果保存成功")
    except Exception as e:
        logger.error(f"保存任务结果时发生错误: {str(e)}")

# 初始化存储
quality_check_results = init_storage()
logger.info(f"初始化后的任务结果: {quality_check_results}")

@app.get("/")
async def root():
    """重定向到API文档页面"""
    return RedirectResponse(url="/docs")

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
        logger.info(f"开始处理批量质量检查任务 {task_id}")
        results = []
        for i, review in enumerate(reviews, 1):
            logger.info(f"正在检查第 {i}/{len(reviews)} 条评价")
            result = await quality_checker.check_quality(review)
            results.append(result)
        logger.info(f"批量质量检查任务 {task_id} 完成")
        
        # 更新任务结果
        quality_check_results[task_id] = {
            "status": "completed",
            "results": results
        }
        save_storage(quality_check_results)
    except Exception as e:
        logger.error(f"批量质量检查任务 {task_id} 失败: {str(e)}")
        quality_check_results[task_id] = {
            "status": "failed",
            "error": str(e)
        }
        save_storage(quality_check_results)

def validate_user_background(user_background: UserBackground, category: str) -> bool:
    """验证用户背景是否符合类别要求"""
    try:
        template = PromptTemplateFactory.create_template(category)
        test_product = ProductInfo(
            name="test",
            category=category,
            price_range="test",
            features=[]
        )
        prompt = template.generate_review_prompt(user_background, test_product)
        return True
    except Exception as e:
        logger.error(f"用户背景验证失败: {str(e)}")
        return False

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
        # 验证请求参数
        if not request.user_background:
            raise HTTPException(status_code=400, detail="用户背景信息不能为空")
        if not request.product_info:
            raise HTTPException(status_code=400, detail="产品信息不能为空")
        if not request.num_reviews or request.num_reviews < 1 or request.num_reviews > 10:
            raise HTTPException(status_code=400, detail="评价数量必须在1-10之间")
            
        logger.info(f"开始生成评价 - 类别: {request.product_info.category}, 数量: {request.num_reviews}")
        
        # 验证用户背景
        if not validate_user_background(request.user_background, request.product_info.category):
            logger.warning(f"用户背景验证失败 - 类别: {request.product_info.category}")
            raise HTTPException(
                status_code=400,
                detail="用户背景信息不符合该产品类别的要求"
            )
        
        # 根据产品类别创建对应的生成器
        try:
            generator = ReviewGeneratorFactory.create_generator(request.product_info.category)
        except ValueError as e:
            logger.error(f"创建生成器失败: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.error(f"创建生成器时发生未知错误: {str(e)}")
            raise HTTPException(status_code=500, detail="创建评价生成器失败")
        
        # 生成指定数量的评价
        reviews = []
        total_time = 0
        start_time = time.time()
        
        for i in range(request.num_reviews):
            try:
                logger.info(f"正在生成第 {i+1}/{request.num_reviews} 条评价")
                # 使用同步方式调用生成器
                review = await asyncio.to_thread(
                    generator.generate_review,
                    request.user_background,
                    request.product_info
                )
                reviews.append(review)
            except Exception as e:
                logger.error(f"生成第 {i+1} 条评价时发生错误: {str(e)}")
                raise HTTPException(status_code=500, detail=f"生成评价失败: {str(e)}")
            
        total_time = time.time() - start_time
        logger.info(f"评价生成完成 - 总耗时: {total_time:.2f}秒")
        
        # 保存生成的评价
        try:
            # 使用同步方式保存评价
            await asyncio.to_thread(
                review_saver.save_reviews,
                reviews,
                request.product_info.category
            )
        except Exception as e:
            logger.error(f"保存评价失败: {str(e)}")
            # 这里我们不抛出异常，因为评价已经生成成功
            
        return ReviewGenerationResponse(
            reviews=reviews,
            generation_time=total_time
        )
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"参数验证错误: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"生成评价时发生未知错误: {str(e)}")
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
        
        for i in range(request.num_reviews):
            # 使用同步方式调用生成器
            review = await asyncio.to_thread(
                generator.generate_review,
                request.user_background,
                request.product_info
            )
            reviews.append(review)
            
        # 对评价进行增强
        enhanced_reviews = await review_enhancer.enhance_reviews(reviews)
        
        total_time = time.time() - start_time
        
        # 保存增强后的评价
        await asyncio.to_thread(
            review_saver.save_reviews,
            enhanced_reviews,
            request.product_info.category
        )
            
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
async def check_quality(request: ReviewGenerationResponse, background_tasks: BackgroundTasks):
    """
    检查评价质量
    
    - **request**: 包含评价列表的请求对象
    
    返回质量检查结果
    """
    try:
        if not request.reviews or len(request.reviews) == 0:
            raise HTTPException(status_code=400, detail="评价列表不能为空")
            
        # 获取第一个评价进行检查
        review = request.reviews[0]
        
        # 验证评价对象的必需字段
        required_fields = ["content", "rating", "sentiment", "sentiment_score", "quality_score"]
        for field in required_fields:
            if not getattr(review, field):
                raise HTTPException(status_code=400, detail=f"{field} 不能为空")
                
        if review.rating < 1 or review.rating > 5:
            raise HTTPException(status_code=400, detail="评分必须在1-5之间")
        if review.sentiment_score < 0 or review.sentiment_score > 1:
            raise HTTPException(status_code=400, detail="情感置信评分必须在0-1之间")
        if review.quality_score < 0 or review.quality_score > 1:
            raise HTTPException(status_code=400, detail="质量置信评分必须在0-1之间")
            
        # 执行质量检查
        result = await quality_checker.check_quality(review)
        
        return {
            "status": "completed",
            "result": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"质量检查失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/check_quality_batch", response_model=Dict[str, Any])
async def check_quality_batch(request: ReviewGenerationResponse, background_tasks: BackgroundTasks):
    """
    批量检查评价质量
    
    - **reviews**: 评价列表
    - **generation_time**: 生成时间
    
    返回质量检查结果
    """
    try:
        # 验证请求参数
        if not request.reviews:
            raise HTTPException(status_code=400, detail="评价列表不能为空")
            
        logger.info(f"开始批量质量检查 - 评价数量: {len(request.reviews)}")
        
        # 创建任务ID
        task_id = str(uuid4())
        logger.info(f"创建新任务: {task_id}")
        
        # 初始化任务状态
        quality_check_results[task_id] = {
            "status": "processing",
            "message": "质量检查任务已启动"
        }
        save_storage(quality_check_results)
        
        # 启动异步任务
        background_tasks.add_task(
            process_batch_quality_check,
            request.reviews,
            task_id
        )
        
        return {
            "status": "processing",
            "task_id": task_id,
            "message": "质量检查任务已启动"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"启动批量质量检查任务时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

