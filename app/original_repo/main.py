import logging
from typing import Dict, Any, List
from dataclasses import dataclass
from app.original_repo.helper1 import BasicOperations, compute_percentage
from app.original_repo.helper2 import AdvancedOperations, calculate_percentage_change
from app.original_repo.helper3 import StatisticalOperations, fibonacci_power_sum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CalculationConfig:
    precision: int = 2
    cache_size: int = 128
    enable_advanced_stats: bool = True
    sample_size: int = 5
    base_numbers: List[float] = None

    def __post_init__(self):
        if self.base_numbers is None:
            self.base_numbers = [2.0, 3.0, 4.0, 5.0, 6.0]
        if len(self.base_numbers) != self.sample_size:
            raise ValueError("base_numbers length must match sample_size")

class MathOperationsOrchestrator:
    def __init__(self, config: CalculationConfig):
        self.config = config
        self.basic_ops = BasicOperations(precision=config.precision)
        self.advanced_ops = AdvancedOperations(cache_size=config.cache_size)
        self.stats_ops = StatisticalOperations(precision=config.precision)
        
    def _safe_operation(self, operation, *args, default=None):
        try:
            return operation(*args)
        except Exception as e:
            logger.error(f"Error in {operation.__name__}: {str(e)}")
            return default

    def calculate_basic_operations(self, a: float, b: float) -> Dict[str, Any]:
        logger.info(f"Performing basic operations with {a} and {b}")
        return {
            "add": self._safe_operation(self.basic_ops.add, a, b),
            "multiply": self._safe_operation(self.basic_ops.multiply, a, b),
            "subtract": self._safe_operation(self.advanced_ops.subtract, a, b),
            "power": self._safe_operation(self.stats_ops.power, a, b)
        }

    def calculate_advanced_metrics(self) -> Dict[str, Any]:
        if not self.config.enable_advanced_stats:
            return {}
            
        numbers = self.config.base_numbers
        logger.info(f"Calculating advanced metrics for {numbers}")
        
        try:
            stats = self.stats_ops.calculate_statistics(numbers)
            fib_power = self._safe_operation(
                fibonacci_power_sum, 
                self.config.sample_size, 
                2
            )
            
            return {
                "statistics": stats,
                "fibonacci_power_sum": fib_power,
                "percentage_changes": [
                    calculate_percentage_change(numbers[i], numbers[i+1])
                    for i in range(len(numbers)-1)
                ]
            }
        except Exception as e:
            logger.error(f"Error calculating advanced metrics: {str(e)}")
            return {}

def runner(config: CalculationConfig = None) -> Dict[str, Any]:
    """
    Main entry point for running calculations.
    Returns both basic operations and advanced statistical metrics.
    """
    if config is None:
        config = CalculationConfig()
    
    orchestrator = MathOperationsOrchestrator(config)
    
    # Maintain backward compatibility with original test cases
    basic_results = orchestrator.calculate_basic_operations(5, 3)
    
    if config.enable_advanced_stats:
        advanced_results = orchestrator.calculate_advanced_metrics()
        basic_results.update(advanced_results)
    
    return basic_results

if __name__ == "__main__":
    # Example usage with custom configuration
    custom_config = CalculationConfig(
        precision=3,
        cache_size=256,
        base_numbers=[2.5, 3.5, 4.5, 5.5, 6.5]
    )
    results = runner(custom_config)
    logger.info(f"Calculation results: {results}")
