def range_function(ranges: dict, boxes : list):

    """
    ranges - словарь диапазонов клавиш, формат: {key(номер клавиши) : [левая граница, правая граница]}
    notes - список нот в кадре, формат: {[[x1,y1, x2,y2]...]}

    Работает на основе наблюдения, что границы клавиш всегда лежат внутри границ падающих нот
    работает примерно, со скростью nlog(n)

    Возвращает словарь формата: {key(номер клавиши):[[x1,y1, x2,y2]...]] - списки параметров нот соотвествующие клавише}
    """

    notes = sorted(boxes, key=lambda x: x[0])
    result = {}
    n = 1
    for note in notes:
        while n <= len(ranges):
            #print(ranges[str(n)][0], ranges[str(n)][1], note[0], note[2])

            if ranges[str(n)][0] > note[0] and ranges[str(n)][1]  < note[2]:
                result[boxes.index(note)] = n

                break
            n += 1
    return result
