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

        # index is a list of pairs - (value, index) in the .values list
        # value is ordered in the index
        self.index = []

        if values:
            for value in values:
                self.add(value)

    def add(self, value):
        
        # update index
        if len(self.values) == 0:
            self.index = [[value, 0]]
        
        # special case - new max. Don't insert, just append
        elif value >= self.index[-1][0]:
            self.index.append([value, len(self.index)])
        else:
            sorted_values = [x[0] for x in self.index]
            index_idx = bisect.bisect_left(sorted_values, value)

            temp_index = self.index[:index_idx]
            temp_index.append([value, len(self.values)])

            if index_idx != len(self.values):
                temp_index.extend(self.index[index_idx:])
            self.index = temp_index

        # add value
        super().add(value)

    def delete(self, value=None, index=None):
        
        if value is None and index is None:
            raise KeyError('Must specify value or index')

        if value is not None:
            sorted_values = [x[0] for x in self.index]
            index_idx = bisect.bisect_left(sorted_values, value)
            if self.index[index_idx][0] != value:
                raise ValueError(f'Value {value} not in index')
        else:
            index_idx = index
        
        temp_index = self.index[:index_idx]

        later_index = [[x[0], x[1]-1] for x in self.index[index_idx+1:]]
        temp_index.extend(later_index)
        self.index = temp_index
        
        super().delete(index=index_idx)


    def query(self, eq=None, gt=None, gte=None, lt=None, lte=None):

        idx1, idx2 = 0, len(self.values)
        sorted_values = [x[0] for x in self.index]

        if eq is not None:
            idx1 = max(idx1, bisect.bisect_left(sorted_values, eq))
            idx2 = min(idx2, bisect.bisect_right(sorted_values, eq))
        if gt is not None:
            idx1 = max(idx1, bisect.bisect_right(sorted_values, gt))
        if gte is not None:
            idx1 = max(idx1, bisect.bisect_left(sorted_values, gte))
        if lt is not None:
            idx2 = min(idx2, bisect.bisect_left(sorted_values, lt))
        if lte is not None:
            idx2 = min(idx2, bisect.bisect_right(sorted_values, lte))
        
        # get indices of source list
        # sorted() maintains order of original list - indices are originally extracted in order of value
        indices = sorted([x[1] for x in self.index[idx1:idx2]])

        result = []
        for index in indices:
            result.append(self.values[index])

        return result
