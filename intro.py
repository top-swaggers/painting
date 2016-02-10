def read_input():
    f = open('input.txt', 'r')
    r, c = map(int, f.readline().split(' '))
    data = f.readlines()
    data = map(
        lambda row: map(
            lambda x: 0 if x == '.' else 1,
            row[:-1],
        ),
        data,
    )
    return data

def find_lines(data):
    result = list()
    for i in xrange(len(data)):
        result.append([])
        for j in xrange(len(data[0])):
            result[i].append([0,0])
            if i == 0:
                result[i][j][1] = data[i][j]
            elif data[i][j] == 1:
                result[i][j][1] = result[i-1][j][1] + 1
            else:
                result[i][j][1] = 0
            if j == 0:
                result[i][j][0] = data[i][j]
            elif data[i][j] ==1:
                result[i][j][0] = result[i][j-1][0] + 1
            else:
                result[i][j][0] = 0
    return result

def get_cells_priority(lines_data):
    priority_queue = []
    for i in xrange(len(lines_data)):
        for j in xrange(len(lines_data[0])):
            for direction in [0, 1]:
                priority_queue.append({
                    'row': i,
                    'column': j,
                    'direction': direction,  # 0 - to left, 1 - to right
                    'value': lines_data[i][j][direction]
                })
    priority_queue = sorted(priority_queue, key=lambda x: x['value'])
    return priority_queue

def draw_lines(lines_data, priority_queue):
    log = []
    while priority_queue:
        cell = priority_queue.pop()
        column, row, direction, value = cell['column'], cell['row'], cell['direction'], cell['value']
        if lines_data[row][column] == [0, 0]:
            continue
        if direction == 0:
            log.append("PAINT_LINE %d %d %d %d" % (row, column-value+1, row, column))
            for i in xrange(column-value+1, column+1):
                lines_data[row][i] = [0, 0]
        if direction == 1:
            log.append("PAINT_LINE %d %d %d %d" % (row-value+1, column, row, column))
            for i in xrange(row-value+1, row+1):
                lines_data[i][column] = [0, 0]
    return log

# Rectangles

def find_rectangles(data):
    result = list()
    for i in xrange(len(data)):
        result.append([])
        for j in xrange(len(data[0])):
            result[i].append([0,0])
            if i == 0:
                result[i][j][1] = 0
            if j == 0:
                result[i][j][0] = 0
            if data[i][j] == 1:
                result[i][j] = [result[i][j-1][0] + 1, result[i-1][j][1] + 1]
            else:
                result[i][j] = [0, 0]
    return result

def get_squares_priority(squares_data, min_square_size):
    priority_queue = []
    for i in xrange(len(squares_data)):
        for j in xrange(len(squares_data[0])):
            square_size = min(squares_data[i][j])
            if square_size >= min_square_size and square_size % 2:
                priority_queue.append({
                    'row': i,
                    'column': j,
                    'value': square_size,
                })
    priority_queue = sorted(priority_queue, key=lambda x: x['value'])
    return priority_queue

def draw_squares(squares_data, priority_queue, also_clear=None):
    log = []
    while priority_queue:
        cell = priority_queue.pop()
        column, row, value = cell['column'], cell['row'], cell['value']
        if squares_data[row][column] == [0, 0]:
            continue
        log.append("PAINT_SQUARE %d %d %d" % (row - (value/2), column - (value/2), (value-1)/2))
        for i in xrange(row-value+1, row+1):
            for j in xrange(column-value+1, column+1):
                squares_data[i][j] = [0, 0]
                if also_clear is not None:
                    also_clear[i][j] = [0, 0]
    return log


def get_result(square_size):
    data = read_input()
    cells_total = reduce(lambda x, y: x + sum(y), data, 0)

    lines_data = find_lines(data)
    priority_queue = get_cells_priority(lines_data)

    rectangles = find_rectangles(data)
    squares_priority = get_squares_priority(rectangles, square_size)
    squares_log = draw_squares(rectangles, squares_priority, also_clear=lines_data)

    lines_log = draw_lines(lines_data, priority_queue)

    scores = cells_total - len(lines_log) - len(squares_log)
    return scores, squares_log + lines_log

def main():

    best_scores = {
        'scores': 0,
        'square_size': 0,
    }

    for i in xrange(100):
        scores, log = get_result(i)
        if scores > best_scores['scores']:
            best_scores['scores'] = scores
            best_scores['square_size'] = i

    scores, log = get_result(best_scores['square_size'])
    f = open('output.txt', 'w+')
    f.write(str(len(log)) + '\n')
    f.write('\n'.join(log))
    print "Scores: %d" % scores

if __name__ == '__main__':
    main()
