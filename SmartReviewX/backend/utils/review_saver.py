import pandas as pd
import os
import shutil
import logging
import json
from datetime import datetime
from typing import List, Dict, Optional
from ..models.data_model import GeneratedReview
from pathlib import Path
import platform

logger = logging.getLogger(__name__)

class ReviewSaver:
    """评价保存工具类"""
    
    def __init__(self):
        self.base_path = Path("data/reviews")
        self.base_path.mkdir(parents=True, exist_ok=True)
        self._load_schema()
        
    def _load_schema(self):
        """加载数据模式"""
        schema_file = self.base_path / "schema.json"
        if schema_file.exists():
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
        schema_file = self.base_path / "schema.json"
        with open(schema_file, 'w', encoding='utf-8') as f:
            json.dump(self.schema, f, indent=2, ensure_ascii=False)
            
    def _get_filename(self, category: str) -> str:
        """获取保存文件名"""
        date_str = datetime.now().strftime("%Y%m%d")
        return self.base_path / f"{category}_reviews_{date_str}.csv"
        
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
            if not filename.exists():
                return True
                
            with open(filename, 'r', encoding='utf-8') as f:
                reader = pd.read_csv(f)
                header = reader.columns.tolist()
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
            if not filename.exists():
                return
                
            backup_dir = self.base_path / "backups"
            backup_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = backup_dir / f"{filename.stem}_{timestamp}.csv"
            
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
        
    def _get_lock_file(self, file_path):
        """获取锁文件路径"""
        return str(file_path) + ".lock"
        
    def _acquire_lock(self, file_path):
        """获取文件锁"""
        lock_file = self._get_lock_file(file_path)
        try:
            if platform.system() == 'Windows':
                import msvcrt
                file_handle = open(lock_file, 'w')
                msvcrt.locking(file_handle.fileno(), msvcrt.LK_NBLCK, 1)
                return file_handle
            else:
                import fcntl
                file_handle = open(lock_file, 'w')
                fcntl.flock(file_handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                return file_handle
        except (IOError, OSError):
            if 'file_handle' in locals():
                file_handle.close()
            return None
            
    def _release_lock(self, file_handle):
        """释放文件锁"""
        if file_handle:
            if platform.system() == 'Windows':
                import msvcrt
                msvcrt.locking(file_handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(file_handle.fileno(), fcntl.LOCK_UN)
            file_handle.close()
            try:
                os.remove(self._get_lock_file(file_handle.name))
            except:
                pass

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
        file_exists = filename.exists()
        
        # 检查文件头一致性
        if file_exists and not self._check_header_consistency(filename):
            logger.error(f"文件头不一致: {filename}")
            self._backup_file(filename)
            raise ValueError("文件头不一致，已创建备份")
            
        try:
            # 获取文件锁
            lock_handle = self._acquire_lock(filename)
            if not lock_handle:
                logger.warning(f"无法获取文件锁: {filename}")
                return
                
            try:
                # 转换评价为DataFrame
                df = pd.DataFrame([self._review_to_dict(review) for review in reviews])
                
                # 保存到CSV
                df.to_csv(filename, index=False, encoding='utf-8')
                logger.info(f"评价已保存到: {filename}")
                
            finally:
                # 释放文件锁
                self._release_lock(lock_handle)
                
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
            if not filename.exists():
                return {
                    "total_reviews": 0,
                    "average_rating": 0,
                    "rating_distribution": {},
                    "sentiment_distribution": {}
                }
                
            # 读取所有CSV文件
            all_reviews = []
            for file in self.base_path.glob(f"{category}_reviews_*.csv"):
                df = pd.read_csv(file)
                all_reviews.append(df)
            
            if not all_reviews:
                return {
                    "total_reviews": 0,
                    "average_rating": 0,
                    "rating_distribution": {},
                    "sentiment_distribution": {}
                }
            
            # 合并所有评价
            combined_df = pd.concat(all_reviews, ignore_index=True)
            
            # 计算统计信息
            stats = {
                "total_reviews": len(combined_df),
                "average_rating": combined_df["rating"].mean(),
                "rating_distribution": combined_df["rating"].value_counts().to_dict(),
                "sentiment_distribution": combined_df["sentiment"].value_counts().to_dict()
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"获取评价统计信息失败: {str(e)}")
            return {
                "total_reviews": 0,
                "average_rating": 0,
                "rating_distribution": {},
                "sentiment_distribution": {}
            } 