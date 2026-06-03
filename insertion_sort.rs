fn insertion_sort<T: Ord>(arr: &mut [T]) {
    for i in 1..arr.len() {
        let mut j = i;
        // Move element at index i to its correct position
        while j > 0 && arr[j - 1] > arr[j] {
            arr.swap(j - 1, j);
            j -= 1;
        }
    }
}

fn main() {
    // Example 1: Sorting integers
    let mut numbers = vec![64, 34, 25, 12, 22, 11, 90];
    println!("Orginalus masyvas: {:?}", numbers);
    insertion_sort(&mut numbers);
    println!("Surūšiuotas masyvas: {:?}", numbers);
    println!();
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_empty_array() {
        let mut arr: Vec<i32> = vec![];
        insertion_sort(&mut arr);
        assert_eq!(arr, vec![]);
    }

    #[test]
    fn test_single_element() {
        let mut arr = vec![5];
        insertion_sort(&mut arr);
        assert_eq!(arr, vec![5]);
    }

    #[test]
    fn test_already_sorted() {
        let mut arr = vec![1, 2, 3, 4, 5];
        insertion_sort(&mut arr);
        assert_eq!(arr, vec![1, 2, 3, 4, 5]);
    }

    #[test]
    fn test_reverse_sorted() {
        let mut arr = vec![5, 4, 3, 2, 1];
        insertion_sort(&mut arr);
        assert_eq!(arr, vec![1, 2, 3, 4, 5]);
    }

    #[test]
    fn test_random_order() {
        let mut arr = vec![3, 1, 4, 1, 5, 9, 2, 6];
        insertion_sort(&mut arr);
        assert_eq!(arr, vec![1, 1, 2, 3, 4, 5, 6, 9]);
    }

    #[test]
    fn test_duplicates() {
        let mut arr = vec![5, 2, 8, 2, 9, 2, 5];
        insertion_sort(&mut arr);
        assert_eq!(arr, vec![2, 2, 2, 5, 5, 8, 9]);
    }
}
