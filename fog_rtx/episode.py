import logging
import time
from typing import Any, Dict, List, Optional

from fog_rtx.database import DatabaseManager
from fog_rtx.feature import FeatureType

logger = logging.getLogger(__name__)


class Episode:
    def __init__(
        self,
        db_manager: DatabaseManager,
        description: Optional[str] = None,
        features: Dict[str, FeatureType] = {},
        enable_feature_inferrence=True,  # whether additional FeatureTypes can be inferred
    ):
        self.description = description
        self.features = features
        self.enable_feature_inferrence = enable_feature_inferrence
        self.db_manager = db_manager
        self.db_manager.initialize_episode(
            metadata={"description": self.description}
        )

    def add(
        self,
        feature: str,
        value: Any,
        timestamp: Optional[int] = None,
    ) -> None:
        if timestamp is None:
            timestamp = time.time_ns()

        logger.info(
            f"Adding {feature} with value {value} at timestamp {timestamp}"
        )
        if self.db_manager:
            self.db_manager.add(feature, value, timestamp)
        else:
            logger.warning(
                "No database manager provided, data will not be saved"
            )

    def add_by_dict(
        self, data: Dict[str, Any], timestamp: Optional[int] = None
    ) -> None:
        """
        add the same timestamp for all features
        """
        if timestamp is None:
            timestamp = time.time_ns()
        for feature, value in data.items():
            self.add(feature, value, timestamp)

    def compact(self) -> None:
        self.db_manager.compact()

    def close(self) -> None:
        self.db_manager.close()
