pipenv sync
pushd aoc-pyo3 || exit
pipenv run maturin develop --release
popd || exit
pipenv run python -m aoc
