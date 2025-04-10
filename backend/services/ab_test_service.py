from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
import numpy as np
from scipy import stats
from ..models.ab_test import ABTest, ABTestResult, ABTestStatus
from ..schemas.ab_test import ABTestCreate, ABTestUpdate, ABTestResultCreate, ABTestStatistics

class ABTestService:
    def __init__(self, db: Session):
        self.db = db

    async def create_test(self, test: ABTestCreate) -> ABTest:
        """Создание нового A/B теста"""
        db_test = ABTest(
            name=test.name,
            description=test.description,
            type=test.type,
            target_audience=test.target_audience,
            variants=test.variants,
            metrics=test.metrics,
            status=ABTestStatus.DRAFT
        )
        self.db.add(db_test)
        self.db.commit()
        self.db.refresh(db_test)
        return db_test

    async def update_test(
        self,
        test_id: int,
        test_update: ABTestUpdate
    ) -> Optional[ABTest]:
        """Обновление A/B теста"""
        test = self.db.query(ABTest).filter(ABTest.id == test_id).first()
        if not test:
            return None

        for field, value in test_update.dict(exclude_unset=True).items():
            setattr(test, field, value)

        self.db.commit()
        self.db.refresh(test)
        return test

    async def start_test(self, test_id: int) -> Optional[ABTest]:
        """Запуск A/B теста"""
        test = self.db.query(ABTest).filter(ABTest.id == test_id).first()
        if not test or test.status != ABTestStatus.DRAFT:
            return None

        test.status = ABTestStatus.ACTIVE
        test.start_date = datetime.now()
        self.db.commit()
        self.db.refresh(test)
        return test

    async def stop_test(self, test_id: int) -> Optional[ABTest]:
        """Остановка A/B теста"""
        test = self.db.query(ABTest).filter(ABTest.id == test_id).first()
        if not test or test.status != ABTestStatus.ACTIVE:
            return None

        test.status = ABTestStatus.COMPLETED
        test.end_date = datetime.now()
        self.db.commit()
        self.db.refresh(test)
        return test

    async def assign_variant(
        self,
        test_id: int,
        user_id: Optional[int] = None
    ) -> Optional[str]:
        """Назначение варианта теста пользователю"""
        test = self.db.query(ABTest).filter(
            ABTest.id == test_id,
            ABTest.status == ABTestStatus.ACTIVE
        ).first()

        if not test:
            return None

        # Проверяем критерии целевой аудитории
        if test.target_audience and not self._check_target_audience(test.target_audience, user_id):
            return None

        # Получаем текущее распределение по вариантам
        variant_counts = self.db.query(
            ABTestResult.variant,
            func.count(ABTestResult.id).label("count")
        ).filter(
            ABTestResult.test_id == test_id
        ).group_by(
            ABTestResult.variant
        ).all()

        # Создаем словарь с количеством участников по вариантам
        variant_distribution = {variant: 0 for variant in test.variants.keys()}
        for variant, count in variant_counts:
            variant_distribution[variant] = count

        # Выбираем вариант с наименьшим количеством участников
        selected_variant = min(variant_distribution.items(), key=lambda x: x[1])[0]
        return selected_variant

    def _check_target_audience(
        self,
        criteria: Dict[str, Any],
        user_id: Optional[int]
    ) -> bool:
        """Проверка соответствия пользователя критериям целевой аудитории"""
        # TODO: Реализовать проверку критериев целевой аудитории
        return True

    async def record_result(
        self,
        result: ABTestResultCreate
    ) -> ABTestResult:
        """Запись результата A/B теста"""
        db_result = ABTestResult(
            test_id=result.test_id,
            variant=result.variant,
            user_id=result.user_id,
            metrics_data=result.metrics_data
        )
        self.db.add(db_result)
        self.db.commit()
        self.db.refresh(db_result)
        return db_result

    async def get_test_statistics(
        self,
        test_id: int,
        confidence_level: float = 0.95
    ) -> Dict[str, ABTestStatistics]:
        """Получение статистики по A/B тесту"""
        test = self.db.query(ABTest).filter(ABTest.id == test_id).first()
        if not test:
            return {}

        results = self.db.query(ABTestResult).filter(
            ABTestResult.test_id == test_id
        ).all()

        statistics = {}
        for variant in test.variants.keys():
            variant_results = [r for r in results if r.variant == variant]
            if not variant_results:
                continue

            metrics_summary = {}
            for metric in test.metrics:
                values = [r.metrics_data.get(metric, 0) for r in variant_results]
                metrics_summary[metric] = {
                    "mean": np.mean(values),
                    "std": np.std(values),
                    "count": len(values)
                }

            # Проверка статистической значимости
            is_significant = None
            confidence = None
            if len(test.variants) == 2:  # Только для A/B тестов
                other_variant = next(v for v in test.variants.keys() if v != variant)
                other_results = [r for r in results if r.variant == other_variant]
                
                if other_results:
                    for metric in test.metrics:
                        variant_values = [r.metrics_data.get(metric, 0) for r in variant_results]
                        other_values = [r.metrics_data.get(metric, 0) for r in other_results]
                        
                        if len(variant_values) > 1 and len(other_values) > 1:
                            t_stat, p_value = stats.ttest_ind(variant_values, other_values)
                            is_significant = p_value < (1 - confidence_level)
                            confidence = 1 - p_value

            statistics[variant] = ABTestStatistics(
                test_id=test_id,
                variant=variant,
                total_participants=len(variant_results),
                metrics_summary=metrics_summary,
                confidence_level=confidence,
                is_significant=is_significant
            )

        return statistics 