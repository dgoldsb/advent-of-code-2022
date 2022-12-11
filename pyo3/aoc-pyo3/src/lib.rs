use pyo3::prelude::*;

#[pyfunction]
fn lcm(nums: Vec<usize>) -> PyResult<usize> {
    let max_num = nums.iter().max().unwrap();
    let mut worry_mod = max_mod.clone();
    loop {
        if nums.iter().map(|m| worry_mod % m == 0).min().unwrap() {
            return Ok(worry_mod);
        }
        worry_mod = worry_mod + max_num;
    }
}


#[pymodule]
fn aoc_py03(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(lcm, m)?)?;
    Ok(())
}
