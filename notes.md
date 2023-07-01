Publish on PyPI

- [ ] Check that the version incrementation is correct

```bash
	rm -rf dist
	python setup.py sdist
	# python -m pip install twine
	twine upload dist/*
```
