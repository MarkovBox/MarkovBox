import numpy as np

sequence = ['C', 'D', 'E', 'D', 'C', 'G', 'A', 'B', 'C']
notes = {
        'C': 0,
        'D': 1,
        'E': 2,
        'F': 3,
        'G': 4,
        'A': 5,
        'B': 6,
}


def rowindex(lastNotes):
    index = 0
    order = len(notes)
    mult = 1
    for note in lastNotes[::-1]:
        index += mult*notes[note]
        mult *= order
    return index


def generate_matrix(sequence, order=1):
    markov = np.zeros((len(notes)**order, len(notes)))
    lastNotes = []
    for note in sequence:
        if len(lastNotes) < order:
            lastNotes.append(str(note))
            continue
        markov[rowindex(lastNotes)][notes[note]] += 1
        lastNotes.append(note)
        lastNotes.pop(0)
    for r in markov:
        rowsum = sum(r)
        if rowsum > 0:
            r /= sum(r)
    return markov


def nextNote(lastnotes, transitions):
    rowsum = sum(transitions[rowindex(lastnotes)])
    if rowsum == 1:
        return str(np.random.choice(list(notes.keys()),
                                    1,
                                    p=transitions[rowindex(lastnotes)])[0])
    else:
        return str(np.random.choice(list(notes.keys()), 1)[0])


def main():
    transitions = generate_matrix(sequence, 2)
    print(transitions)
    lastnotes = ['C', 'D']
    for _ in range(10):
        nextnote = nextNote(lastnotes, transitions)
        print("Note:", lastnotes, ":", nextnote)
        lastnotes.append(nextnote)
        lastnotes.pop(0)


if __name__ == '__main__':
    main()
