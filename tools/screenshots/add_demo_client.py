"""Adds a demo client ("Leo") with ten backdated sessions to the FUNunciation app's saved data,
for the History screenshot on the Home page (src/assets/captures/history.png).

Usage (quit the app in the simulator first, so it can't overwrite clients.json from memory):
    D=<simulator udid>
    C=$(xcrun simctl get_app_container $D com.bananastandard.speechtherapy data)
    python3 -I tools/screenshots/add_demo_client.py "$C/Library/Application Support"

Writes the same compact, sorted-key JSON the app's encoders write (ClientStore/clients.json and
SessionHistory/<clientID>.json). Leaves every existing client and history untouched, and refuses to
run twice. Back up "Application Support" before running it on a simulator you care about; Leo can be
removed in the app from History → Remove from this iPad → Delete client.
"""
import json, os, sys, uuid
from datetime import datetime, timedelta, timezone

root = sys.argv[1]
clients_path = os.path.join(root, 'ClientStore', 'clients.json')
history_dir = os.path.join(root, 'SessionHistory')

CLIENT_ID = '7C1E5A0B-3F64-4D2B-9A8E-5B2C1D4E6F70'
NAME = 'Leo'

def iso(dt):
    return dt.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def local(y, m, d, hh, mm):
    # Simulator clock is US Eastern (EDT, UTC-4) for these dates.
    return datetime(y, m, d, hh, mm, tzinfo=timezone(timedelta(hours=-4)))

def tally(phoneme, context, trials, tc, ta, ti, replays=(0, 0)):
    """One (phoneme, context) cell. `replays` = (cards replayed after a close, after an incorrect);
    a replayed card's second try is correct, so it counts once at word level, as correct."""
    tries = tc + ta + ti
    unmarked = trials - tries
    r_a, r_i = replays
    return {
        'approximation': ta - r_a,
        'contextCode': context,
        'correct': tc,
        'incorrect': ti - r_i,
        'phonemeID': phoneme,
        'trials': trials,
        'triesApproximation': ta,
        'triesCorrect': tc,
        'triesIncorrect': ti,
        'unjudged': unmarked,
    }

def words(t):
    return t['correct'] + t['approximation'] + t['incorrect'] + t['unjudged']

# (local start, level, support, [(gameID, trials, seconds)], [tallies])
PLAN = [
    (local(2026, 9, 22, 9, 40), 'word', 'maximalCues', [('basketball', 20, 172)],
     [tally('k', 'initial', 20, 9, 5, 6, (1, 1))]),
    (local(2026, 9, 24, 9, 35), 'word', 'maximalCues', [('food-truck', 40, 318)],
     [tally('k', 'initial', 40, 20, 8, 10, (2, 1))]),
    (local(2026, 9, 29, 9, 45), 'word', 'someCues', [('firefly-pond', 40, 301)],
     [tally('k', 'initial', 40, 26, 7, 7, (1, 1))]),
    (local(2026, 10, 1, 9, 30), 'word', 'someCues', [('runway', 40, 296)],
     [tally('k', 'final', 20, 11, 4, 5, (1, 0)), tally('k', 'initial', 20, 14, 3, 3, (1, 0))]),
    (local(2026, 10, 6, 9, 40), 'word', 'independent', [('balloon-friends', 20, 141), ('pizza', 40, 287)],
     [tally('k', 'final', 40, 26, 6, 7, (1, 1)), tally('k', 'initial', 20, 16, 2, 2)]),
    (local(2026, 10, 8, 9, 35), 'word', 'someCues', [('photo-booth', 60, 436)],
     [tally('g', 'initial', 20, 9, 6, 5, (1, 1)), tally('k', 'final', 40, 29, 5, 5, (1, 0))]),
    (local(2026, 10, 13, 9, 50), 'phrase', 'someCues', [('toy-train', 40, 322)],
     [tally('k', 'initial', 40, 23, 9, 8, (2, 1))]),
    (local(2026, 10, 15, 9, 30), 'phrase', 'someCues', [('feed', 40, 298), ('basketball', 20, 151)],
     [tally('g', 'initial', 20, 12, 4, 4, (1, 0)), tally('k', 'final', 20, 13, 4, 3, (1, 0)),
      tally('k', 'initial', 20, 14, 3, 3, (1, 0))]),
    (local(2026, 10, 20, 9, 40), 'phrase', 'independent', [('skyline', 60, 447)],
     [tally('g', 'initial', 20, 13, 3, 4, (1, 0)), tally('k', 'initial', 40, 28, 6, 5, (1, 1))]),
    (local(2026, 10, 22, 9, 35), 'phrase', 'independent', [('food-truck', 40, 289), ('rain-garden', 40, 305)],
     [tally('g', 'initial', 20, 14, 3, 3, (1, 0)), tally('k', 'final', 20, 15, 3, 2, (1, 0)),
      tally('k', 'initial', 40, 30, 5, 4, (1, 1))]),
]

def session(start, level, support, games, targets):
    targets = sorted(targets, key=lambda t: (t['phonemeID'], t['contextCode']))
    total_trials = sum(t['trials'] for t in targets)
    assert total_trials == sum(g[1] for g in games), start
    total_words = sum(words(t) for t in targets)
    app_seconds = float(sum(g[2] for g in games))
    game_rows, words_left = [], total_words
    for i, (game_id, trials, seconds) in enumerate(games):
        w = words_left if i == len(games) - 1 else round(total_words * trials / total_trials)
        words_left -= w
        game_rows.append({'gameID': game_id, 'roundsCompleted': trials // 20, 'seconds': float(seconds),
                          'trials': trials, 'wordsPresented': w})
    return {
        'clientID': CLIENT_ID,
        'id': str(uuid.uuid5(uuid.UUID(CLIENT_ID), iso(start))).upper(),
        'summary': {
            'appSeconds': app_seconds,
            'approximationEnabled': True,
            'completedRounds': total_trials // 20,
            'correctnessCriterion': '',
            'endedAt': iso(start + timedelta(seconds=app_seconds + 95)),
            'endedCleanly': True,
            'games': game_rows,
            'isProbe': False,
            'linguisticLevel': level,
            'markingEnabled': True,
            'roundTarget': 10,
            'startedAt': iso(start),
            'supportLevel': support,
            'targets': targets,
        },
    }

sessions = [session(*p) for p in PLAN]
last = PLAN[-1]

clients = json.load(open(clients_path))
if any(p['id'] == CLIENT_ID for p in clients['presets']):
    sys.exit('Leo is already saved; nothing written.')
clients['presets'].append({
    'createdAt': iso(local(2026, 9, 22, 9, 31)),
    'displayName': NAME,
    'id': CLIENT_ID,
    'lastUsed': {
        'approximationEnabled': True,
        'gameID': 'rain-garden',
        'linguisticLevel': last[1],
        'markSet': 'clinical',
        'markingEnabled': True,
        'mode': 'imageAndText',
        'roundTarget': 10,
        'selection': {'contexts': ['initial', 'final'], 'phonemeID': 'k'},
        'supportLevel': last[2],
        'wordAudioEnabled': False,
    },
    'lastUsedAt': iso(last[0]),
    'pictureID': 'fox',
    'suppressedWords': [],
})

def dump(obj, path):
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(obj, f, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    os.replace(tmp, path)

dump({'schemaVersion': 1, 'sessions': sessions}, os.path.join(history_dir, CLIENT_ID + '.json'))
dump(clients, clients_path)

for s in sessions:
    t = s['summary']['targets']
    tries = sum(x['triesCorrect'] + x['triesApproximation'] + x['triesIncorrect'] for x in t)
    correct = sum(x['triesCorrect'] for x in t)
    trials = sum(x['trials'] for x in t)
    print(s['summary']['startedAt'][:10], s['summary']['linguisticLevel'], s['summary']['supportLevel'],
          f'{trials} trials', f'{correct} of {tries} ({round(100 * correct / tries)}%)')
