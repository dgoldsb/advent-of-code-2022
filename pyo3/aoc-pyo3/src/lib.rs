use pyo3::prelude::*;
use std::cmp::Reverse;
use std::collections::BinaryHeap;
use std::collections::HashMap;

fn reconstruct_path(came_from: &HashMap<isize, isize>, goal: &isize) -> Vec<isize> {
    let mut path: Vec<isize> = vec![*goal];
    let mut current = goal;
    while came_from.contains_key(current) {
        current = came_from.get(current).unwrap();
        path.push(*current);
    }
    path.reverse();
    path
}

#[pyfunction]
fn dijkstra(
    start: isize,
    goal: isize,
    successors: HashMap<isize, Vec<(usize, isize)>>,
) -> PyResult<Vec<isize>> {
    let mut open_set = BinaryHeap::new();
    let mut came_from: HashMap<isize, isize> = HashMap::new();
    let mut distance: HashMap<isize, usize> = HashMap::new();

    distance.insert(start, 0);
    open_set.push(Reverse((0, start)));

    while !open_set.is_empty() {
        let empty_vec = Vec::new();
        if let Some(Reverse(heap_top)) = open_set.pop() {
            let current = heap_top.1;

            if current == goal {
                return Ok(reconstruct_path(&came_from, &goal));
            }

            let candidates = successors.get(&current).unwrap_or(&empty_vec);
            for candidate in candidates {
                let candidate_node = candidate.1;
                let candidate_distance = candidate.0;
                let distance_through_current = distance.get(&current).unwrap() + candidate_distance;

                if distance_through_current
                    < *distance
                    .get(&candidate_node)
                    .unwrap_or(&(10000000 as usize))
                {
                    came_from.insert(candidate_node, current);
                    distance.insert(candidate_node, distance_through_current);
                    open_set.push(Reverse((distance_through_current, candidate.1)));
                }
            }
        }
    }

    panic!("No solution found")
}

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
    m.add_function(wrap_pyfunction!(dijkstra, m)?)?;
    Ok(())
}
