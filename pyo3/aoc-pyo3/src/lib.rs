use pyo3::prelude::*;

#[pyfunction]
fn count_char(string: String, target: char) -> PyResult<usize> {
    Ok(string.chars().filter(|&c| c == target).count())
}


#[pymodule]
fn aoc_py03(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(count_char, m)?)?;
    Ok(())
}
