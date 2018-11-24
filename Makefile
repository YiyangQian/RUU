clean:
	find . -name '*.pyc' -delete
	rm -rf __pycache__
	rm -rf .pytest_cache

test: 
	pytest *_test.py
