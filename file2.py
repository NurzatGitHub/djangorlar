# Data processing and analysis utilities
import json
import csv
import statistics
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

class DataProcessor:
    def __init__(self):
        self.data = []
        self.processed_data = []
        self.metrics = {}
    
    def load_json_data(self, file_path: str) -> List[Dict]:
        """Load data from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
            return self.data
        except FileNotFoundError:
            raise FileNotFoundError(f"File {file_path} not found")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
    
    def load_csv_data(self, file_path: str) -> List[Dict]:
        """Load data from CSV file"""
        self.data = []
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    self.data.append(row)
            return self.data
        except FileNotFoundError:
            raise FileNotFoundError(f"File {file_path} not found")
    
    def filter_data(self, condition_func) -> List[Dict]:
        """Filter data based on condition function"""
        self.processed_data = [item for item in self.data if condition_func(item)]
        return self.processed_data
    
    def sort_data(self, key_func, reverse: bool = False) -> List[Dict]:
        """Sort data based on key function"""
        self.processed_data = sorted(self.data, key=key_func, reverse=reverse)
        return self.processed_data
    
    def calculate_numeric_stats(self, field_name: str) -> Dict[str, float]:
        """Calculate statistics for numeric field"""
        values = []
        for item in self.data:
            try:
                value = float(item.get(field_name, 0))
                values.append(value)
            except (ValueError, TypeError):
                continue
        
        if not values:
            return {}
        
        self.metrics[field_name] = {
            'mean': statistics.mean(values),
            'median': statistics.median(values),
            'mode': statistics.mode(values) if len(values) > 1 else values[0],
            'stdev': statistics.stdev(values) if len(values) > 1 else 0,
            'min': min(values),
            'max': max(values),
            'count': len(values)
        }
        return self.metrics[field_name]
    
    def group_by_field(self, field_name: str) -> Dict[Any, List]:
        """Group data by specified field"""
        grouped = {}
        for item in self.data:
            key = item.get(field_name)
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(item)
        return grouped
    
    def transform_field(self, field_name: str, transform_func) -> List[Dict]:
        """Transform field values using provided function"""
        for item in self.data:
            if field_name in item:
                item[field_name] = transform_func(item[field_name])
        return self.data
    
    def export_to_json(self, file_path: str, data: Optional[List] = None) -> bool:
        """Export data to JSON file"""
        export_data = data if data is not None else self.processed_data
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(export_data, file, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Export failed: {e}")
            return False
    
    def export_to_csv(self, file_path: str, data: Optional[List] = None) -> bool:
        """Export data to CSV file"""
        export_data = data if data is not None else self.processed_data
        if not export_data:
            return False
        
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                fieldnames = export_data[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(export_data)
            return True
        except Exception as e:
            print(f"Export failed: {e}")
            return False
    
    def find_duplicates(self, key_fields: List[str]) -> List[Dict]:
        """Find duplicate entries based on key fields"""
        seen = set()
        duplicates = []
        
        for item in self.data:
            key = tuple(item.get(field) for field in key_fields)
            if key in seen:
                duplicates.append(item)
            else:
                seen.add(key)
        
        return duplicates
    
    def clean_data(self, required_fields: List[str]) -> List[Dict]:
        """Remove entries missing required fields"""
        self.processed_data = [
            item for item in self.data 
            if all(field in item and item[field] is not None for field in required_fields)
        ]
        return self.processed_data
    
    def merge_datasets(self, other_data: List[Dict], key_field: str) -> List[Dict]:
        """Merge two datasets based on key field"""
        merged = []
        lookup = {item[key_field]: item for item in other_data}
        
        for item in self.data:
            key_value = item.get(key_field)
            if key_value in lookup:
                merged_item = {**item, **lookup[key_value]}
                merged.append(merged_item)
        
        return merged

class TimeSeriesAnalyzer(DataProcessor):
    def __init__(self):
        super().__init__()
        self.timestamps = []
        self.values = []
    
    def parse_timeseries(self, timestamp_field: str, value_field: str):
        """Parse timestamp and value fields from data"""
        self.timestamps = []
        self.values = []
        
        for item in self.data:
            try:
                timestamp = datetime.fromisoformat(item[timestamp_field])
                value = float(item[value_field])
                self.timestamps.append(timestamp)
                self.values.append(value)
            except (KeyError, ValueError, TypeError):
                continue
    
    def calculate_moving_average(self, window: int = 5) -> List[float]:
        """Calculate moving average"""
        if len(self.values) < window:
            return self.values
        
        moving_avg = []
        for i in range(len(self.values) - window + 1):
            window_values = self.values[i:i + window]
            avg = sum(window_values) / window
            moving_avg.append(avg)
        
        return moving_avg
    
    def detect_anomalies(self, threshold: float = 2.0) -> List[Dict]:
        """Detect anomalies based on standard deviation"""
        if not self.values:
            return []
        
        mean = statistics.mean(self.values)
        stdev = statistics.stdev(self.values) if len(self.values) > 1 else 0
        
        anomalies = []
        for i, (timestamp, value) in enumerate(zip(self.timestamps, self.values)):
            if abs(value - mean) > threshold * stdev:
                anomalies.append({
                    'timestamp': timestamp,
                    'value': value,
                    'deviation': value - mean,
                    'index': i
                })
        
        return anomalies

# Demonstration
if __name__ == "__main__":
    # Sample data for demonstration
    sample_data = [
        {"id": 1, "name": "Alice", "age": 25, "salary": 50000, "department": "IT"},
        {"id": 2, "name": "Bob", "age": 30, "salary": 60000, "department": "HR"},
        {"id": 3, "name": "Charlie", "age": 35, "salary": 70000, "department": "IT"},
        {"id": 4, "name": "Diana", "age": 28, "salary": 55000, "department": "Finance"},
        {"id": 5, "name": "Eve", "age": 32, "salary": 65000, "department": "IT"}
    ]
    
    processor = DataProcessor()
    processor.data = sample_data
    
    print("Data Processing Demo:")
    print(f"Original data count: {len(processor.data)}")
    
    # Filter IT department
    it_employees = processor.filter_data(lambda x: x['department'] == 'IT')
    print(f"IT employees: {len(it_employees)}")
    
    # Calculate salary statistics
    salary_stats = processor.calculate_numeric_stats('salary')
    print(f"Salary statistics: {salary_stats}")
    
    # Group by department
    grouped = processor.group_by_field('department')
    print(f"Departments: {list(grouped.keys())}")
    
    # Time series analysis demo
    timeseries_data = [
        {"timestamp": "2024-01-01T10:00:00", "value": 100},
        {"timestamp": "2024-01-01T11:00:00", "value": 150},
        {"timestamp": "2024-01-01T12:00:00", "value": 200},
        {"timestamp": "2024-01-01T13:00:00", "value": 50},  # anomaly
        {"timestamp": "2024-01-01T14:00:00", "value": 180},
    ]
    
    ts_analyzer = TimeSeriesAnalyzer()
    ts_analyzer.data = timeseries_data
    ts_analyzer.parse_timeseries('timestamp', 'value')
    
    anomalies = ts_analyzer.detect_anomalies()
    print(f"Detected anomalies: {len(anomalies)}")