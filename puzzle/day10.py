import sys
import queue
import math

OPEN = "([{<"
MATCH = ["()","[]","{}","<>"]
SCORE_INVALID = {")": 3, "]": 57, "}": 1197, ">": 25137}
SCORE_INCOMPLETE = {")": 1, "]": 2, "}": 3, ">": 4}

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

def get_match(start):
    for match in MATCH:
        if match[0]==start:
            return match[1]

def match(start, stop):
    return (get_match(start)==stop)

def process_line(line):
    active_chunks = queue.LifoQueue()
    for token in line:
        if token in OPEN:
            active_chunks.put(token)
        else:
            if active_chunks.empty() or not match(active_chunks.get(), token):
                return (SCORE_INVALID[token],0)
    incomplete_score = 0
    while not active_chunks.empty():
        incomplete_score = incomplete_score*5
        incomplete_score += SCORE_INCOMPLETE[get_match(active_chunks.get())]
    return (0,incomplete_score)

invalid_score = 0
incomplete_scores = []
with open(sys.argv[1]) as file:
    for line in file:
        scores = process_line(line.rstrip())
        invalid_score += scores[0]
        if scores[1] > 0:
            incomplete_scores.append(scores[1])
incomplete_scores.sort()
print("Invalid score = {}, median incomplete score = {}".format(invalid_score, incomplete_scores[math.floor(len(incomplete_scores)/2)]))

