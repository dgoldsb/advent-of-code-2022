use pyo3::prelude::*;

fn gcd(a: usize, b: usize) -> usize {
    if b == 0 {
        return a;
    }
    gcd(b, a % b)
}

fn multi_gcd(nums: &Vec<usize>, idx: usize) -> usize {
    if idx == nums.len() - 1 {
        return nums[idx];
    }
    let a = nums[idx];
    let b = multi_gcd(nums, idx + 1);
    return gcd(a, b);
}

#[pyfunction]
fn lcm(nums: Vec<usize>) -> PyResult<usize> {
    let lcm = nums.iter().product::<usize>() / multi_gcd(&nums, 0);
    return Ok(lcm);
}

#[pymodule]
fn aoc_py03(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(lcm, m)?)?;
    Ok(())
}
