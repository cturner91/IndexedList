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
        
        if value is not None:
            i = self.values.index(value)  # should raise error if value not in values
            return self.delete(index=i)

        if index is not None:
            del self.values[index]

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
    
    def __repr__(self):
        return str(self.values)


class IndexedList(BaseList):
    def __init__(self, values=None):
        self.values = []

        # cannot use a list for index - accessing it in a list comprehension corrodes performance
        self._index_values = []
        self._index_indices = []

        if values:
            for value in values:
                self.add(value)

    def __len__(self):
        return len(self.values)

    def __repr__(self):
        print(self.values)
        print(self._index_values)
        print(self._index_indices)
        return ''

    def add(self, value=None):

        if value is None:
            raise ValueError('Must have a value to add')
        
        # update index
        if len(self.values) == 0:
            self._index_values = [value]
            self._index_indices = [0]
        
        # special case - new min/max. Don't insert, just append
        elif value <= self._index_values[0]:
            self._index_values.insert(0, value)
            self._index_indices.insert(0, len(self._index_values)-1)
        elif value >= self._index_values[-1]:
            self._index_values.append(value)
            self._index_indices.append(len(self._index_values)-1)
        else:
            index_idx = bisect.bisect_left(self._index_values, value)
            self._index_values.insert(index_idx, value)
            self._index_indices.insert(index_idx, len(self.values))

        # add value
        super().add(value)

    def delete(self, value=None, index=None):
        
        if value is None and index is None:
            raise ValueError('Must specify value or index')
        
        if len(self._index_values) == 1:
            self._index_values = []
            self._index_indices = []
            index = 0  # necesary for super().delete

        else:
            # contrary to add -> we need to know the value here so we can remove it from the index
            if value is None:
                value = self.values[index]
   
            # index is also required for super().delete
            if index is None:
                index = self.values.index(value)
            
            # handle negative indices - screws up off-by-one adjustment later
            if index < 0:
                index = len(self.values) + index

            index_idx = bisect.bisect_left(self._index_values, value)
            if self._index_values[index_idx] != value:
                raise ValueError(f'Value {value} not in index')
            
            # need to decrement the indices AFTER the index value
            self._index_indices = [i-1 if i > index else i for i in self._index_indices]
            del self._index_values[index_idx]
            del self._index_indices[index_idx]
        
        super().delete(index=index)

    def query(self, eq=None, gt=None, gte=None, lt=None, lte=None):

        idx1, idx2 = 0, len(self.values)
        if eq is not None:
            idx1 = max(idx1, bisect.bisect_left(self._index_values, eq))
            idx2 = min(idx2, bisect.bisect_right(self._index_values, eq))
        if gt is not None:
            idx1 = max(idx1, bisect.bisect_right(self._index_values, gt))
        if gte is not None:
            idx1 = max(idx1, bisect.bisect_left(self._index_values, gte))
        if lt is not None:
            idx2 = min(idx2, bisect.bisect_left(self._index_values, lt))
        if lte is not None:
            idx2 = min(idx2, bisect.bisect_right(self._index_values, lte))
        
        # get indices of source list
        # sorted() maintains order of original list - indices are originally extracted in order of value
        indices = sorted(self._index_indices[idx1:idx2])

        return [self.values[i] for i in indices]
    
    def _validate(self):
        # ensure that every indexed value is where it says it is
        for i in range(len(self._index_indices)):
            assert self._index_values[i] == self.values[self._index_indices[i]]

        # ensure no duplicates in indices
        assert len(set(self._index_indices)) == len(self._index_indices)

        # ensure index_values is sorted
        assert self._index_values == sorted(self._index_values)

        return True
