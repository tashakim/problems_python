def insert_sort(array):
	"""Purpose: Sorts the elements of an array using 
	insertion sort.
	Input: array
	Output: sorted array
	"""
	for i in range(1, len(array)):
		key = array[i]

		j = i-1
		while j>= and array[j] > key:
			array[j+1] = array[j]
			j -= 1

		array[j+1] = key

	return array

if __name__ == "__main__":
	array = [2,4,64,1,7]
	print(insert_sort(array))