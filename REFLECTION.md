# Reflection

I fixed the playlist classification, search, statistics, and Lucky Pick behavior.

One issue I observed was that songs did not always go into the playlist I expected. For example, songs with rock or party genres should be Hype, low-energy songs should be Chill, and songs that do not clearly match either rule should be Mixed. I looked in `playlist_logic.py` because that file controlled the main logic. The problem was connected to inconsistent text handling and unclear classification rules.

I used the AI coding assistant to understand what the existing code was doing before changing it. I treated the AI response as a hypothesis, then checked whether it matched the app behavior. After that, I updated the classification logic so it follows the required rules. I also normalized user input by trimming whitespace and lowercasing artist and genre values so comparisons are more consistent.

Another issue was search. Search now uses case-insensitive partial matching, so searching `ac` can find `AC/DC`. I also fixed Lucky Pick so choosing Hype only picks from the Hype playlist, choosing Chill only picks from the Chill playlist, and choosing Any picks from all playlists.

For the refactor, I added helper functions such as `normalize_text`, `normalize_song`, and `get_unique_songs`. This made the code easier to read and reduced repeated logic. I tested the app again after refactoring to make sure the behavior stayed the same.

My main insight is that AI is useful for explaining code and suggesting fixes, but I still need to test the app myself. The best debugging process was to start with one clear expected behavior, observe what actually happened, trace the issue to the code, make a small fix, and test again.
