def range_function(ranges: dict, notes: list):

    """
    ranges - словарь диапазонов клавиш, формат: {key(номер клавиши) : [левая граница, правая граница]}
    notes - список нот в кадре, формат: {[[x1,y1, x2,y2]...]}

    Работает на основе наблюдения, что границы клавиш всегда лежат внутри границ падающих нот
    работает примерно, со скростью nlog(n)

    Возвращает словарь формата: {key(номер клавиши):[[x1,y1, x2,y2]...]] - списки параметров нот соотвествующие клавише}
    """

    notes = sorted(notes, key=lambda x: x[0])
    result = {}
    n = 1
    for note in notes:
        while n <= len(ranges):
            #print(ranges[str(n)][0], ranges[str(n)][1], note[0], note[2])

            if ranges[str(n)][0] > note[0] and ranges[str(n)][1]  < note[2]:
                if not str(n) in result:
                    result[str(n)] = [note]
                else:
                    result[str(n)].append(note)

                break
            n += 1
    return result