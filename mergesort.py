def mergeSortAscend(array):
	# sorts array in ascending order.
	if len(array) > 1:
		left = array[:len(array)//2]
		right  = array[len(array)//2:]

		mergeSortAscend(left)
		mergeSortAscend(right)

		iter1 = iter2 = k = 0

		while iter1 < len(left) and iter2 < len(right):
			if left[iter1] < right[iter2]:
				array[k] = left[iter1]
				iter1 += 1

			else:
				array[k] = right[iter2]
				iter2 += 1
			k += 1

		while iter1 < len(left):
			array[k] = left[iter1]
			iter1 += 1
			k += 1

		while iter2 < len(right):
			iter2 += 1
			k += 1
		return array


def mergeSortDescend(array):
	# sorts array in descending order.
	if len(array) > 1:
		right = array[: len(array)//2]
		left = array[len(array)//2 :]

		mergeSortDescend(left)
		mergeSortDescend(right)

		iter1 = iter2 = k = 0

		while iter1 < len(left) and iter2 < len(right):
			if left[iter1] > right[iter2]:
				array[k] = left[iter1]
				iter1 += 1
			else:
				array[k] = right[iter2]
				iter2 += 1
			k += 1

		while iter1 < len(left):
			array[k] = left[iter1]
			iter1 += 1
			k += 1

		while iter2 < len(right):
			iter2 += 1
			k += 1
		return array 


if __name__ == "__main__":
	array = [4,3,6,2,2,1,10]
	print("Ascending order: ", mergeSortAscend(array))
	print("Descending order: ", mergeSortDescend(array))
