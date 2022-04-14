import json
import glob
import numpy

dump_directory = "itl_2022-04-11-08"
score_directory = f"{dump_directory}/song_scores"

difficulties = {n:[] for n in range(7,17)}

def percentile_for_difficulty(difficulty, percentile=50):
    scores = {}
    average_scores = {}

    for song_file in glob.glob(f"{score_directory}/*.json"):
        score_data = json.load(open(song_file))
        meter = score_data['scores'][0]['song_meter']
        if meter == difficulty or difficulty == 0:
            number_title = f"[{meter}] {score_data['scores'][0]['song_title']}" 
            scores[number_title] = score_data['scores']

    for title, scores in scores.items():
        percents = [score['score_ex'] / 100.0 for score in scores]
        average = numpy.percentile(percents, [percentile], method='normal_unbiased')[0]
        average_scores[title] = average
        difficulties[scores[0]['song_meter']].append(percents)

    for title, score in sorted(average_scores.items(), key=lambda item: -item[1]):
        print(title, "({:0.02f})".format(score))

def overall_percentiles():
    for difficulty, score_list in difficulties.items():
        flat_scores = [score for sublist in score_list for score in sublist]
        percents = [50, 75, 90, 95]
        percentiles = numpy.percentile(flat_scores, [percents], method='normal_unbiased')
        print(f"{difficulty}:")
        print("  top 50%: {:0.02f}".format(percentiles[0][0]))
        print("  top 25%: {:0.02f}".format(percentiles[0][1]))
        print("  top 10%: {:0.02f}".format(percentiles[0][2]))
        print("  top 5%: {:0.02f}".format(percentiles[0][3]))

for n in range(7, 17):
    print(f"{n}:")
    percentile_for_difficulty(n)

print("All:")
percentile_for_difficulty(0)
