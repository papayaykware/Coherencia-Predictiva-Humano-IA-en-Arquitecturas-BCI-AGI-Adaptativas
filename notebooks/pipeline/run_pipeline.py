"""
Pipeline for executing trials and calculating simplified ICP.
"""

import json
import random
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import numpy as np

# Add parent directory to path to import modules
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from models.dummy_agi import DummyAGI, Task, TaskType


@dataclass
class TrialResult:
    """Represents the result of a single trial."""
    trial_id: int
    task: Task
    agi_response: Dict[str, Any]
    success: bool
    execution_time: float
    performance_metrics: Dict[str, float]
    icp_component: float  # Component contribution to ICP
    timestamp: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        data['task'] = {
            'task_id': self.task.task_id,
            'task_type': self.task.task_type.value,
            'complexity': self.task.complexity,
            'data_size': self.task.data_size,
            'features': self.task.features,
            'description': self.task.description
        }
        return data


class ICPCalculator:
    """
    Calculates simplified ICP (Index of Complexity of Problem) based on trial results.
    ICP = α * Complexity_Score + β * Performance_Score + γ * Resource_Score
    """
    
    def __init__(self, weights: Optional[Dict[str, float]] = None):
        """
        Initialize ICP calculator with custom weights.
        
        Args:
            weights: Dictionary with weights for different components
                    Default: {'complexity': 0.4, 'performance': 0.4, 'resources': 0.2}
        """
        self.weights = weights or {
            'complexity': 0.4,
            'performance': 0.4,
            'resources': 0.2
        }
        
        # Normalize weights to sum to 1
        total = sum(self.weights.values())
        self.weights = {k: v/total for k, v in self.weights.items()}
        
    def calculate_complexity_score(self, task: Task) -> float:
        """
        Calculate complexity score based on task characteristics.
        Score ranges from 0 (simple) to 1 (very complex).
        """
        # Normalize complexity (already 0-1)
        complexity_score = task.complexity
        
        # Data size factor (normalized to 0-1, assuming max 10000)
        data_size_score = min(1.0, task.data_size / 10000)
        
        # Feature count factor (normalized to 0-1, assuming max 100 features)
        feature_score = min(1.0, len(task.features) / 100)
        
        # Combine factors with weights
        combined = (complexity_score * 0.5 + 
                   data_size_score * 0.3 + 
                   feature_score * 0.2)
        
        return min(1.0, combined)
    
    def calculate_performance_score(self, agi_response: Dict[str, Any]) -> float:
        """
        Calculate performance score based on AGI response.
        Higher score indicates better performance (lower complexity impact).
        """
        if not agi_response.get('success', False):
            return 1.0  # Failed tasks contribute max complexity
        
        performance = agi_response.get('performance', {})
        
        # Extract primary metric based on task type
        primary_metric = None
        if 'accuracy' in performance:
            primary_metric = performance['accuracy']
        elif 'r2_score' in performance:
            primary_metric = performance['r2_score']
        elif 'silhouette_score' in performance:
            primary_metric = performance['silhouette_score']
        elif 'optimal_value' in performance:
            primary_metric = performance['optimal_value']
        
        if primary_metric is None:
            return 0.5  # Default if no metric found
        
        # Convert to complexity score (inverse of performance)
        # High performance -> low complexity contribution
        complexity_contribution = 1.0 - primary_metric
        
        return max(0.0, min(1.0, complexity_contribution))
    
    def calculate_resource_score(self, agi_response: Dict[str, Any]) -> float:
        """
        Calculate resource usage score.
        Higher score indicates higher resource usage (more complexity).
        """
        if not agi_response.get('success', False):
            return 1.0
        
        # Get resource estimates from analysis
        analysis = agi_response.get('analysis', {})
        resources = analysis.get('resource_requirements', {})
        
        if not resources:
            return 0.5
        
        # Combine resource factors
        cpu_score = resources.get('cpu_usage', 0.5)
        memory_score = min(1.0, resources.get('memory_mb', 0) / 1000)  # Normalize to 1GB max
        
        # GPU factor: if GPU required, add penalty
        gpu_penalty = 0.3 if resources.get('gpu_required', False) else 0
        
        combined = (cpu_score * 0.4 + memory_score * 0.3 + gpu_penalty)
        
        return min(1.0, combined)
    
    def calculate_icp(self, trial_result: TrialResult) -> float:
        """
        Calculate ICP for a single trial.
        
        ICP = w1 * Complexity_Score + w2 * Performance_Score + w3 * Resource_Score
        """
        complexity_score = self.calculate_complexity_score(trial_result.task)
        performance_score = self.calculate_performance_score(trial_result.agi_response)
        resource_score = self.calculate_resource_score(trial_result.agi_response)
        
        icp = (self.weights['complexity'] * complexity_score +
               self.weights['performance'] * performance_score +
               self.weights['resources'] * resource_score)
        
        # Store component scores for analysis
        trial_result.icp_component = icp
        trial_result.performance_metrics = {
            'complexity_score': complexity_score,
            'performance_score': performance_score,
            'resource_score': resource_score,
            'icp': icp
        }
        
        return icp


class TrialRunner:
    """Manages execution of multiple trials."""
    
    def __init__(self, agi: DummyAGI, icp_calculator: ICPCalculator):
        """
        Initialize trial runner.
        
        Args:
            agi: AGI instance to test
            icp_calculator: ICP calculator instance
        """
        self.agi = agi
        self.icp_calculator = icp_calculator
        self.trials: List[TrialResult] = []
        
    def generate_task(self, task_id: int) -> Task:
        """Generate a random task for testing."""
        task_types = list(TaskType)
        task_type = random.choice(task_types)
        
        # Generate random features
        n_features = random.randint(5, 50)
        features = [f"feature_{i}" for i in range(n_features)]
        
        # Generate complexity (biased towards medium complexity)
        complexity = random.betavariate(2, 2)  # Beta distribution centered around 0.5
        
        # Generate data size
        data_size = random.randint(100, 10000)
        
        descriptions = [
            f"Classify {data_size} samples with {n_features} features",
            f"Predict continuous values from {n_features} variables",
            f"Cluster {data_size} data points into natural groups",
            f"Find optimal parameters for given constraints"
        ]
        
        return Task(
            task_id=f"task_{task_id:04d}",
            task_type=task_type,
            complexity=complexity,
            data_size=data_size,
            features=features,
            description=random.choice(descriptions)
        )
    
    def run_trial(self, trial_id: int, task: Optional[Task] = None) -> TrialResult:
        """
        Run a single trial.
        
        Args:
            trial_id: ID for this trial
            task: Task to execute (generates random if None)
            
        Returns:
            TrialResult object
        """
        if task is None:
            task = self.generate_task(trial_id)
        
        start_time = time.time()
        response = self.agi.execute_task(task)
        execution_time = time.time() - start_time
        
        # Extract success status
        success = response.get('success', False)
        
        # Create trial result
        trial_result = TrialResult(
            trial_id=trial_id,
            task=task,
            agi_response=response,
            success=success,
            execution_time=execution_time,
            performance_metrics={},
            icp_component=0.0,
            timestamp=datetime.now().isoformat()
        )
        
        # Calculate ICP
        icp = self.icp_calculator.calculate_icp(trial_result)
        
        self.trials.append(trial_result)
        
        return trial_result
    
    def run_batch(self, n_trials: int, verbose: bool = True) -> List[TrialResult]:
        """
        Run a batch of trials.
        
        Args:
            n_trials: Number of trials to run
            verbose: Print progress information
            
        Returns:
            List of trial results
        """
        results = []
        
        for i in range(n_trials):
            if verbose:
                print(f"Running trial {i+1}/{n_trials}...", end=' ', flush=True)
            
            result = self.run_trial(i)
            results.append(result)
            
            if verbose:
                icp = result.performance_metrics.get('icp', 0)
                print(f"ICP={icp:.3f}, Time={result.execution_time:.2f}s, "
                      f"Success={result.success}")
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Calculate statistics from all trials."""
        if not self.trials:
            return {"error": "No trials executed"}
        
        n_trials = len(self.trials)
        successful_trials = sum(1 for t in self.trials if t.success)
        success_rate = successful_trials / n_trials
        
        icp_values = [t.performance_metrics.get('icp', 0) for t in self.trials]
        complexity_scores = [t.performance_metrics.get('complexity_score', 0) 
                            for t in self.trials]
        performance_scores = [t.performance_metrics.get('performance_score', 0) 
                             for t in self.trials]
        resource_scores = [t.performance_metrics.get('resource_score', 0) 
                          for t in self.trials]
        
        execution_times = [t.execution_time for t in self.trials]
        
        # Group by task type
        task_type_stats = {}
        for trial in self.trials:
            task_type = trial.task.task_type.value
            if task_type not in task_type_stats:
                task_type_stats[task_type] = []
            task_type_stats[task_type].append(trial.performance_metrics.get('icp', 0))
        
        avg_icp_by_type = {
            tt: np.mean(icps) for tt, icps in task_type_stats.items()
        }
        
        return {
            "total_trials": n_trials,
            "successful_trials": successful_trials,
            "success_rate": success_rate,
            "icp_statistics": {
                "mean": np.mean(icp_values),
                "median": np.median(icp_values),
                "std": np.std(icp_values),
                "min": np.min(icp_values),
                "max": np.max(icp_values)
            },
            "component_scores": {
                "complexity_mean": np.mean(complexity_scores),
                "performance_mean": np.mean(performance_scores),
                "resource_mean": np.mean(resource_scores)
            },
            "execution_time": {
                "mean": np.mean(execution_times),
                "total": np.sum(execution_times)
            },
            "average_icp_by_task_type": avg_icp_by_type
        }


def save_results(results: List[TrialResult], filename: str = "trial_results.json"):
    """Save trial results to a JSON file."""
    output = {
        "timestamp": datetime.now().isoformat(),
        "total_trials": len(results),
        "trials": [t.to_dict() for t in results]
    }
    
    with open(filename, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Results saved to {filename}")


def main():
    """Main function to run the pipeline."""
    print("=" * 60)
    print("AGI Pipeline - Trial Execution and ICP Calculation")
    print("=" * 60)
    
    # Initialize AGI
    print("\n1. Initializing Dummy AGI...")
    agi_config = {
        "name": "DummyAGI_V1",
        "version": "1.0.0",
        "learning_rate": 0.01,
        "accuracy_base": 0.85
    }
    agi = DummyAGI(agi_config)
    print(f"   AGI: {agi.name} v{agi.version}")
    print(f"   Capabilities: {agi.get_capabilities()}")
    
    # Initialize ICP calculator
    print("\n2. Initializing ICP Calculator...")
    icp_weights = {
        'complexity': 0.4,
        'performance': 0.4,
        'resources': 0.2
    }
    icp_calculator = ICPCalculator(icp_weights)
    print(f"   Weights: {icp_weights}")
    
    # Initialize trial runner
    print("\n3. Initializing Trial Runner...")
    runner = TrialRunner(agi, icp_calculator)
    
    # Run trials
    n_trials = 10
    print(f"\n4. Running {n_trials} trials...")
    print("-" * 60)
    results = runner.run_batch(n_trials, verbose=True)
    print("-" * 60)
    
    # Calculate and display statistics
    print("\n5. Calculating Statistics...")
    stats = runner.get_statistics()
    
    print("\n" + "=" * 60)
    print("PIPELINE RESULTS")
    print("=" * 60)
    print(f"\nOverall Statistics:")
    print(f"  Total Trials: {stats['total_trials']}")
    print(f"  Success Rate: {stats['success_rate']:.2%}")
    print(f"\nICP Statistics (0=simple, 1=complex):")
    print(f"  Mean ICP: {stats['icp_statistics']['mean']:.3f}")
    print(f"  Median ICP: {stats['icp_statistics']['median']:.3f}")
    print(f"  Std Dev: {stats['icp_statistics']['std']:.3f}")
    print(f"  Range: [{stats['icp_statistics']['min']:.3f}, {stats['icp_statistics']['max']:.3f}]")
    
    print(f"\nComponent Scores (mean):")
    print(f"  Complexity Score: {stats['component_scores']['complexity_mean']:.3f}")
    print(f"  Performance Score: {stats['component_scores']['performance_mean']:.3f}")
    print(f"  Resource Score: {stats['component_scores']['resource_mean']:.3f}")
    
    print(f"\nAverage ICP by Task Type:")
    for task_type, avg_icp in stats['average_icp_by_task_type'].items():
        print(f"  {task_type}: {avg_icp:.3f}")
    
    print(f"\nExecution Time:")
    print(f"  Mean per trial: {stats['execution_time']['mean']:.2f}s")
    print(f"  Total: {stats['execution_time']['total']:.2f}s")
    
    # Save results
    print("\n6. Saving Results...")
    save_results(results, "pipeline_results.json")
    
    # Show AGI performance summary
    print("\n7. AGI Performance Summary:")
    agi_summary = agi.get_performance_summary()
    print(f"  Total tasks processed: {agi_summary['total_tasks']}")
    print(f"  Average performance: {agi_summary['average_performance']:.3f}")
    
    print("\n" + "=" * 60)
    print("Pipeline execution completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
