def test_status_code(response):
    return response.status_code == 200, "Status code must be 200"

def test_content_type(response):
    return "application/json" in response.headers.get("Content-Type",""), "Content-Type must be JSON"

def test_name_field(data):
    return isinstance(data.get("name"), str), "name must be string"

def test_age_field(data):
    age = data.get("age")
    return (isinstance(age, int) or age is None), "age must be int or null"

def test_count_field(data):
    return isinstance(data.get("count"), int), "count must be int"

def test_invalid_param():
    import requests
    r = requests.get("https://api.agify.io")
    return r.status_code == 200, "API should still return 200 without param"