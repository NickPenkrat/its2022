class MatchPairsData:
    def __init__(self, keypoints0, keypoints1, matches, match_confidence):
        self.keypoints0 = keypoints0
        self.keypoints1 = keypoints1
        self.matches = matches
        self.match_confidence = match_confidence
