import abc
import bisect


class BaseList:

    def __init__(self, values=None):
        self.values = []
        if values:
            for value in values:
                self.add(value)

    def add(self, value):
        self.values.append(value)

    def delete(self, value=None, index=None):
        
        if value is None and index is None:
            raise KeyError('Must specify value or index')
        
        if index is not None:
            if index < 0 or index >= len(self.values):
                raise IndexError('0 < index < len()')
            value = self.values[index]
            self.values = self.values[:index] + self.values[index+1:]
            return value
        
        if value is not None:
            # loop through, find first element that matches and remove it
            for i in range(len(self.values)):
                if self.values[i] == value:
                    return self.delete(index=i)
            raise ValueError(f'Value {value} not found in values')
        
    def query(self, eq=None, gt=None, gte=None, lt=None, lte=None):
        filtered_list = self.values[:]
        if eq is not None:
            filtered_list = [x for x in filtered_list if x == eq]
        if gt is not None:
            filtered_list = [x for x in filtered_list if x > gt]
        if gte is not None:
            filtered_list = [x for x in filtered_list if x >= gte]
        if lt is not None:
            filtered_list = [x for x in filtered_list if x < lt]
        if lte is not None:
            filtered_list = [x for x in filtered_list if x <= lte]
        return filtered_list


class IndexedList(BaseList):
    def __init__(self, values=None):
        self.values = []

        # cannot use a list for index - accessing it in a list comprehension corrodes performance
        self.index_values = []
        self.index_indices = []

        if values:
            for value in values:
                self.add(value)

    def add(self, value):
        
        # update index
        if len(self.values) == 0:
            self.index_values = [value]
            self.index_indices = [0]
        
        # special case - new min/max. Don't insert, just append
        elif value <= self.index_values[0]:
            self.index_values.insert(0, value)
            self.index_indices.insert(0, len(self.index_values)-1)
        elif value >= self.index_values[-1]:
            self.index_values.append(value)
            self.index_indices.append(len(self.index_values)-1)
        else:
            index_idx = bisect.bisect_left(self.index_values, value)

            temp_index_values = self.index_values[:index_idx]
            temp_index_indices = self.index_indices[:index_idx]
            temp_index_values.append(value)
            temp_index_indices.append(len(self.values))

            if index_idx != len(self.values):
                temp_index_values.extend(self.index_values[index_idx:])
                temp_index_indices.extend(self.index_indices[index_idx:])
            self.index_values = temp_index_values
            self.index_indices = temp_index_indices

        # add value
        super().add(value)

    def delete(self, value=None, index=None):
        
        if value is None and index is None:
            raise KeyError('Must specify value or index')
        
        if len(self.index_values) == 1:
            self.index_values = []
            self.index_indices = []

        else:
            if value is not None:
                index_idx = bisect.bisect_left(self.index_values, value)
                if self.index_values[index_idx] != value:
                    raise ValueError(f'Value {value} not in index')
            else:
                index_idx = index

            if index == 0:
                self.index_values = self.index_values[1:]
                self.index_indices = self.index_indices[1:]
            elif index == len(self.values)-1:
                self.index_values = self.index_values[:-1]
                self.index_indices = self.index_indices[:-1]
            else:
                temp_index_values = self.index_values[:index_idx]
                temp_index_indices = self.index_indices[:index_idx]

                later_index_values = [x for x in self.index_values[index_idx+1:]]
                later_index_indices = [x-1 for x in self.index_indices[index_idx+1:]]
                temp_index_values.extend(later_index_values)
                temp_index_indices.extend(later_index_indices)
                self.index_values = temp_index_values
                self.index_indices = temp_index_indices
        
                super().delete(index=index_idx)


    def query(self, eq=None, gt=None, gte=None, lt=None, lte=None):

        idx1, idx2 = 0, len(self.values)
        if eq is not None:
            idx1 = max(idx1, bisect.bisect_left(self.index_values, eq))
            idx2 = min(idx2, bisect.bisect_right(self.index_values, eq))
        if gt is not None:
            idx1 = max(idx1, bisect.bisect_right(self.index_values, gt))
        if gte is not None:
            idx1 = max(idx1, bisect.bisect_left(self.index_values, gte))
        if lt is not None:
            idx2 = min(idx2, bisect.bisect_left(self.index_values, lt))
        if lte is not None:
            idx2 = min(idx2, bisect.bisect_right(self.index_values, lte))
        
        # get indices of source list
        # sorted() maintains order of original list - indices are originally extracted in order of value
        indices = sorted(self.index_indices[idx1:idx2])

        result = []
        for index in indices:
            result.append(self.values[index])

        return result
