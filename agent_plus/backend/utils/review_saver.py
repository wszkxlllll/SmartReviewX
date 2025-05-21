import csv
import os
import shutil
import logging
import json
from datetime import datetime
from typing import List, Dict, Optional
from ..models.data_model import GeneratedReview
from pathlib import Path
import msvcrt  # Windows文件锁定
import time

logger = logging.getLogger(__name__)

class ReviewSaver:
    """评价保存工具类"""
    
    def __init__(self, save_dir: str = "data/reviews"):
        """
        初始化评价保存器
        
        Args:
            save_dir: 保存目录，默认为 data/reviews
        """
        self.save_dir = save_dir
        self._ensure_save_dir()
        self._load_schema()
        
    def _ensure_save_dir(self):
        """确保保存目录存在"""
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
            
    def _load_schema(self):
        """加载数据模式"""
        schema_file = os.path.join(self.save_dir, "schema.json")
        if os.path.exists(schema_file):
            with open(schema_file, 'r', encoding='utf-8') as f:
                self.schema = json.load(f)
        else:
            self.schema = {
                "fieldnames": self._get_fieldnames(),
                "version": "1.0",
                "last_updated": datetime.now().isoformat()
            }
            self._save_schema()
            
    def _save_schema(self):
        """保存数据模式"""
        schema_file = os.path.join(self.save_dir, "schema.json")
        with open(schema_file, 'w', encoding='utf-8') as f:
            json.dump(self.schema, f, indent=2, ensure_ascii=False)
            
    def _get_filename(self, category: str) -> str:
        """获取保存文件名"""
        date_str = datetime.now().strftime("%Y%m%d")
        return os.path.join(self.save_dir, f"{category}_reviews_{date_str}.csv")
        
    def _get_fieldnames(self) -> List[str]:
        """获取CSV文件的字段名"""
        return [
            # 用户背景信息
            "user_gender", "user_age", "user_occupation", "user_income_level",
            "user_experience", "user_tech_familiarity", "user_purchase_purpose",
            "user_region", "user_education_level", "user_usage_frequency",
            "user_brand_loyalty",
            
            # 产品信息
            "product_name", "product_category", "product_price_range",
            "product_brand", "product_model_number", "product_specifications",
            "product_warranty_period", "product_expiration_date",
            "product_material", "product_weight", "product_dimensions",
            "product_package_info", "product_energy_efficiency",
            "product_safety_certifications", "product_usage_instructions",
            "product_features",
            
            # 评价信息
            "rating", "content", "sentiment", "experience",
            "pros", "cons", "sentiment_score", "quality_score",
            "generation_time"
        ]
        
    def _validate_review_data(self, review_dict: Dict) -> bool:
        """
        验证评价数据
        
        Args:
            review_dict: 评价数据字典
            
        Returns:
            验证是否通过
        """
        try:
            # 验证必要字段
            required_fields = ["product_name", "product_category", "rating", "content"]
            if not all(field in review_dict and review_dict[field] for field in required_fields):
                logger.error(f"缺少必要字段: {required_fields}")
                return False
                
            # 验证数值字段
            numeric_fields = ["rating", "sentiment_score", "quality_score"]
            for field in numeric_fields:
                if field in review_dict and review_dict[field]:
                    try:
                        value = float(review_dict[field])
                        if field == "rating" and not (1 <= value <= 5):
                            logger.error(f"评分超出范围: {value}")
                            return False
                        if field in ["sentiment_score", "quality_score"] and not (0 <= value <= 1):
                            logger.error(f"分数超出范围: {value}")
                            return False
                    except ValueError:
                        logger.error(f"无效的数值: {review_dict[field]}")
                        return False
                        
            return True
            
        except Exception as e:
            logger.error(f"数据验证失败: {str(e)}")
            return False
            
    def _check_header_consistency(self, filename: str) -> bool:
        """
        检查CSV文件头一致性
        
        Args:
            filename: CSV文件路径
            
        Returns:
            是否一致
        """
        try:
            if not os.path.exists(filename):
                return True
                
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader, None)
                if not header:
                    return True
                    
                return set(header) == set(self.schema["fieldnames"])
                
        except Exception as e:
            logger.error(f"检查文件头一致性失败: {str(e)}")
            return False
            
    def _backup_file(self, filename: str):
        """
        备份文件
        
        Args:
            filename: 要备份的文件路径
        """
        try:
            if not os.path.exists(filename):
                return
                
            backup_dir = os.path.join(self.save_dir, "backups")
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
                
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = os.path.join(
                backup_dir,
                f"{Path(filename).stem}_{timestamp}.csv"
            )
            
            shutil.copy2(filename, backup_filename)
            logger.info(f"文件已备份: {backup_filename}")
            
        except Exception as e:
            logger.error(f"文件备份失败: {str(e)}")
            
    def _review_to_dict(self, review: GeneratedReview) -> dict:
        """将评价对象转换为字典"""
        # 用户背景信息
        user_dict = {
            "user_gender": review.user_background.gender,
            "user_age": review.user_background.age,
            "user_occupation": review.user_background.occupation,
            "user_income_level": review.user_background.income_level,
            "user_experience": review.user_background.experience,
            "user_tech_familiarity": review.user_background.tech_familiarity,
            "user_purchase_purpose": review.user_background.purchase_purpose,
            "user_region": review.user_background.region,
            "user_education_level": review.user_background.education_level,
            "user_usage_frequency": review.user_background.usage_frequency,
            "user_brand_loyalty": review.user_background.brand_loyalty
        }
        
        # 产品信息
        product_dict = {
            "product_name": review.product_info.name,
            "product_category": review.product_info.category,
            "product_price_range": review.product_info.price_range,
            "product_brand": review.product_info.brand,
            "product_model_number": review.product_info.model_number,
            "product_specifications": str(review.product_info.specifications) if review.product_info.specifications else None,
            "product_warranty_period": review.product_info.warranty_period,
            "product_expiration_date": review.product_info.expiration_date,
            "product_material": review.product_info.material,
            "product_weight": review.product_info.weight,
            "product_dimensions": review.product_info.dimensions,
            "product_package_info": review.product_info.package_info,
            "product_energy_efficiency": review.product_info.energy_efficiency,
            "product_safety_certifications": str(review.product_info.safety_certifications) if review.product_info.safety_certifications else None,
            "product_usage_instructions": review.product_info.usage_instructions,
            "product_features": str(review.product_info.features) if review.product_info.features else None
        }
        
        # 评价信息
        review_dict = {
            "rating": review.rating,
            "content": review.content,
            "sentiment": review.sentiment,
            "experience": review.experience,
            "pros": str(review.pros),
            "cons": str(review.cons),
            "sentiment_score": review.sentiment_score,
            "quality_score": review.quality_score,
            "generation_time": datetime.now().isoformat()
        }
        
        return {**user_dict, **product_dict, **review_dict}
        
    def save_reviews(self, reviews: List[GeneratedReview], category: str):
        """
        保存评价到CSV文件
        
        Args:
            reviews: 评价列表
            category: 产品类别
            
        Raises:
            ValueError: 当数据验证失败或文件头不一致时
        """
        filename = self._get_filename(category)
        file_exists = os.path.exists(filename)
        
        # 检查文件头一致性
        if file_exists and not self._check_header_consistency(filename):
            logger.error(f"文件头不一致: {filename}")
            self._backup_file(filename)
            raise ValueError("文件头不一致，已创建备份")
            
        try:
            with open(filename, 'a', newline='', encoding='utf-8') as f:
                # 使用Windows文件锁定
                msvcrt.locking(f.fileno(), msvcrt.LK_LOCK, 1)
                
                writer = csv.DictWriter(f, fieldnames=self.schema["fieldnames"])
                
                # 如果文件不存在，写入表头
                if not file_exists:
                    writer.writeheader()
                    
                # 写入评价数据
                for review in reviews:
                    review_dict = self._review_to_dict(review)
                    if self._validate_review_data(review_dict):
                        writer.writerow(review_dict)
                    else:
                        logger.error(f"评价数据验证失败: {review_dict}")
                        
                # 释放文件锁
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
                
        except Exception as e:
            logger.error(f"保存评价失败: {str(e)}")
            raise
            
    def get_review_stats(self, category: str) -> dict:
        """
        获取评价统计信息
        
        Args:
            category: 产品类别
            
        Returns:
            统计信息字典
        """
        try:
            filename = self._get_filename(category)
            if not os.path.exists(filename):
                return {
                    "total_reviews": 0,
                    "average_rating": 0,
                    "rating_distribution": {},
                    "sentiment_distribution": {}
                }
                
            total_reviews = 0
            total_rating = 0
            rating_dist = {}
            sentiment_dist = {}
            
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    total_reviews += 1
                    rating = float(row['rating'])
                    total_rating += rating
                    
                    # 统计评分分布
                    rating_key = str(int(rating))
                    rating_dist[rating_key] = rating_dist.get(rating_key, 0) + 1
                    
                    # 统计情感分布
                    sentiment = row['sentiment']
                    sentiment_dist[sentiment] = sentiment_dist.get(sentiment, 0) + 1
                    
            return {
                "total_reviews": total_reviews,
                "average_rating": total_rating / total_reviews if total_reviews > 0 else 0,
                "rating_distribution": rating_dist,
                "sentiment_distribution": sentiment_dist
            }
            
        except Exception as e:
            logger.error(f"获取评价统计信息失败: {str(e)}")
            return {
                "total_reviews": 0,
                "average_rating": 0,
                "rating_distribution": {},
                "sentiment_distribution": {}
            } 