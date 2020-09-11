
class Calculator:
    def __init__(self, match):
        self.match = match
        self.averages = match

    # Appends match data
    def add_data(self, data, index):
        data_array = data[index]
        for datum in data_array:
            try:
                self.match.append(float(datum))
            except:
                self.match.append(datum)

    # Calculates averages for each stat in data
    def calc_averages(self, data, first_index):
        data_size = len(data[0])
        for i in range(first_index, data_size):
            sum = 0
            count = 0
            for data_array in data:
                try:
                    sum += float(data_array[i])
                    count += 1
                except:
                    pass
            if count > 0:
                average = round(sum/count,2)
                self.averages.append(average)
            else:
                self.averages.append("n/a")

    # Returns match array
    def get_match(self):
        return self.match

    # Returns averages array
    def get_averages(self):
        return self.averages
