import pytest
from time import perf_counter
from functools import wraps
from fastapi.testclient import TestClient

def benchmark(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        end = perf_counter()
        print(f"{func.__name__} took {end - start} seconds")
        return result
    return wrapper

@pytest.fixture
def client():
    from src.main import app
    return TestClient(app)


@benchmark
def test_benchmark(client):
    for _ in range(100):
        response = client.get("/health")
        assert response.status_code == 200      

    
    