# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**ContentMatch 1.0** — A content-based music recommender using genre, mood, and energy similarity  

---

## 2. Intended Use  

ContentMatch generates personalized music recommendations by matching song attributes to user taste preferences. It is designed for **classroom exploration** to understand how recommendation algorithms work, not for production use. 

It assumes:
- Users can articulate their preferred genre, mood, and target energy level
- Preferences are stable (not mood-dependent or time-varying)
- Content-based matching (song attributes) is sufficient without collaborative filtering (what similar users liked)  

---

## 3. How the Model Works  

ContentMatch scores each song by comparing its attributes to what the user likes:

**Scoring formula:**
- **Genre match**: +2.0 points if song genre exactly matches user's favorite genre
- **Mood match**: +1.0 point if song mood exactly matches user's favorite mood
- **Energy similarity**: 0 to 1.0 points based on how close the song's energy is to the user's target (1.0 when perfect match, 0.0 when 1.0+ away)
- **Total**: Sum all points (max 4.0), then normalize to 0–1.0 scale

After scoring all songs, the system ranks them by score and returns the top 5. It also explains *why* each song matched (which criteria it satisfied).

This approach treats recommendation as a similarity problem: find songs that look like the user's taste profile.

---

## 4. Data  

**Catalog size**: 20 songs

**Genres represented**: pop, lofi, rock, ambient, jazz, indie pop, electronic, hip-hop, synthwave, classical, reggae, folk, country, r&b, indie, metal, techno (17 unique)

**Moods represented**: happy, chill, intense, relaxed, focused, dreamy, melancholic, uplifting, energetic, dark, aggressive, romantic (12 unique)

**Data source**: Provided starter dataset; no changes made.

**Missing dimensions**:
- **Lyrics/language**: Cannot detect themes, storytelling, or cultural context
- **Production style**: Acoustic vs. synthesized is captured but unused
- **Tempo granularity**: Only counts energy, not explicit BPM weighting
- **Artist/cultural representation**: Limited non-English/Western genres
- **Vocal characteristics**: Male/female/group vocals not considered
- **Recency bias**: All songs treated equally regardless of release date  

---

## 5. Strengths  

✓ **Clear preference matches**: When genre + mood + energy all align (e.g., "pop/happy/0.82" → Sunrise City), the system returns perfect 1.000 matches that are intuitively correct.

✓ **Graceful fallback**: When preferences aren't fully met (no matching genre), the system uses mood + energy to find sensible alternatives instead of failing.

✓ **Extreme preference stability**: Energy preferences at 0.1 (very quiet) and 0.99 (very loud) both produce reasonable results without breaking or returning nonsensical songs.

✓ **Transparent reasoning**: Each recommendation includes *why* it matched (Genre match, Mood match, Energy match), making recommendations interpretable rather than opaque.

✓ **Deterministic and reproducible**: Same user input always yields identical rankings—no randomness to confuse testing.  

---

## 6. Limitations and Bias 

I discovered a critical failure: **when a genre has only 1-2 songs in the catalog, requests for that genre are guaranteed a perfect 1.000 match, dominating recommendations regardless of mood/energy fit.** A user asking for classical music received *Nocturne in D Minor* with a 1.000 score even though its melancholic mood (0.25 energy) might not match all classical listeners' preferences. In a real music service, this creates a "diversity desert"—classical users only ever see the same few songs because the genre weight (+2.0) overwhelms all other factors. If the dataset had 3 classical songs, they would *all* tie at 1.000, and users would get arbitrary results. This incentivizes curators to over-represent mainstream genres (pop, hip-hop) and neglect niche ones, perpetuating inequality.

---

## 7. Evaluation  

**Comparison 1: Pop (0.82 energy) vs. Lofi (0.42 energy)**
- **Pop top #1**: Sunrise City (pop/happy/0.82) → 1.000 (perfect match)
- **Lofi top #1**: Midnight Coding (lofi/chill/0.42) → 1.000 (perfect match)
- **What this tests**: Energy preference splitting. Both profiles find perfect matches within their genres, confirming the algorithm correctly identifies high-energy vs. low-energy song pools. Pop's #2 is Gym Hero (0.93 energy, intense mood) showing energy-matching overrides mood mismatch. Lofi's #2 is Library Rain (0.35 energy, almost identical to target 0.42) confirming energy precision matters. ✓ System correctly separates energy bands.

**Comparison 2: Pop (happy/0.82) vs. Rock (intense/0.91)**
- **Pop top 5**: Sunrise City → Gym Hero → Rooftop Lights (indie pop, happy) → Electric Dreams (electronic) → Urban Beats (hip-hop)
- **Rock top 5**: Storm Runner → Gym Hero (pop, intense—mood match!) → Techno Pulse → Raging Inferno (metal, aggressive) → Urban Beats
- **What this tests**: Mood's relative importance vs. genre. Notice both profiles include Gym Hero in top 5 despite genre mismatch (pop → pop/rock users) because mood + energy align perfectly. However, Pop rarely ventures outside pop/indie, while Rock recommendations diversify to metal, techno, and hip-hop. This reveals: **mood matching is weaker than genre matching** (Pop didn't get rock recommendations despite similar energy), but when mood aligns perfectly (Gym Hero's "intense" matches rock user), genre barrier weakens. ✓ Mood provides meaningful but secondary filtering.

**Comparison 3: Rock (intense/0.91) vs. Metal (aggressive/0.95)**
- **Rock top #1**: Storm Runner (rock/intense/0.91) → 1.000
- **Metal top #1**: Raging Inferno (metal/aggressive/0.95) → 0.990 (essentially 1.000)
- **Rock #2**: Gym Hero (pop/intense/0.93 energy) → 0.495 (mood match only, no genre)
- **Metal #2**: Gym Hero (pop/intense/0.93 energy) → 0.245 (energy match only, no mood/genre match)
- **What this tests**: Genre dominance in ranking. Metal user gets a much worse #2 recommendation (0.245 vs 0.495) than Rock user for the same song because rock recommendations fall back on mood matching, while metal recommendations fall back on energy-only. This shows aggressive ≠ intense, so metal users lose both mood *and* genre with non-metal fallbacks. ✓ Confirms genre weight creates isolation for niche listeners.

**Comparison 4: Contradictory Profile (electronic/sad/0.89 energy) vs. Standard Profiles**
- **Contradictory top #1**: Electric Dreams (electronic/uplifting/0.78 energy) → 0.723 (genre + partial energy match, *no mood match*)
- **Pop top #1**: Sunrise City (pop/happy/0.82) → 1.000 (genre + mood + energy match)
- **Rock top #1**: Storm Runner (rock/intense/0.91) → 1.000
- **What this tests**: Preference conflicts and fallback behavior. The contradictory profile (wants "sad" but targets high energy 0.89) cannot find a match because no song is both sad *and* high-energy. The algorithm silently resolves this by prioritizing genre (electronic) and energy (0.89 is close to 0.78), *abandoning the mood entirely*. No explanation tells the user "sad music isn't energetic in this dataset." Compared to standard profiles' perfect 1.000 matches, contradictory gets 0.723—a clear penalty for conflicting preferences, but no transparency about *why*. ✓ Identifies silent failure mode: preferences that don't co-occur get silently downweighted.

**Comparison 5: Sleep/Dance Conflict (lofi + 0.92 energy) vs. Chill Lofi (lofi + 0.42 energy)**
- **Sleep/Dance top 5**: All lofi (Midnight Coding → Focus Flow → Library Rain) with scores 0.625-0.607
- **Chill Lofi top 5**: Mixed (Midnight Coding → Library Rain → Focus Flow → Spacewalk Thoughts [ambient] → Heartbreak Road [country])
- **What this tests**: Preference hierarchy under conflict. Sleep/Dance user *prefers lofi genre* despite mismatch with energy, so they receive lofi-only recommendations. Chill Lofi user has aligned preferences (low energy + low energy songs), so recommendations diversify into ambient and country when lofi runs out. ✓ Confirms: **genre weight (+2.0) wins over energy conflicts**. User gets what they asked for by genre, even if energy preference suggests they'd hate it.

**Comparison 6: Extreme Low Energy (0.1) vs. Extreme High Energy (0.99)**
- **Low-energy top #1**: Nocturne (classical/melancholic/0.25 energy) → 0.963 (all 3 criteria match perfectly)
- **High-energy top #1**: Raging Inferno (metal/aggressive/0.95 energy) → 0.990 (all 3 criteria match)
- **Low-energy #2**: Heartbreak Road (country/melancholic/0.42 energy) → 0.420 (mood match only, energy off)
- **High-energy #2**: Gym Hero (pop/intense/0.93 energy) → 0.235 (energy match only)
- **What this tests**: Boundary stability and fallback diversity. Both extremes find excellent #1 matches (0.96+), but fallbacks differ drastically: low-energy users see diverse genres (country, ambient) when classical/lofi exhaust, while high-energy users narrow to songs matching aggressive/intense moods (metal, rock). This shows: **aggressive moods are rarer than melancholic moods in this dataset**, so high-energy users bottleneck faster. ✓ Energy extremes are stable, but dataset imbalance creates unequal fallbacks.

**Comparison 7: Niche Genre (classical only) vs. Mainstream Profiles (pop, rock)**
- **Classical top #1**: Nocturne (classical/melancholic/0.25 energy) → 1.000 (only song in genre)
- **Classical #2**: Heartbreak Road (country/melancholic/0.42) → 0.458 (no genre, mood+energy)
- **Pop top #1**: Sunrise City (pop/happy/0.82) → 1.000
- **Pop top #2**: Gym Hero (pop/intense/0.93) → 0.722 (genre match, energy match)
- **Rock top #2**: Gym Hero (pop/intense/0.93) → 0.495 (mood match, energy match, no genre)
- **What this tests**: Catalog representation bias. Classical user gets a perfect 1.000, then *plummets* to 0.458 (#2 is country, not classical). Pop user's #2 is 0.722 (still pop, diverse mood/energy). This 0.282-point drop (1.000 → 0.458 vs. 1.000 → 0.722) reveals: **niche genres create recommendation cliffs**. Once the single classical song is exhausted, the algorithm has no backup plan and falls to unrelated genres. Pop users enjoy a smooth decline in relevance, while classical users experience a chasm. ✓ Confirms niche genre dominance weakness.

**Overall Surprises:**
- **Genre cliff**: A single genre match (+2.0) almost always beats multiple partial matches—very high weight concentration.
- **Mood irrelevance**: When mood doesn't exist in dataset, genre + energy still produces decent results. Mood is less critical than expected.
- **Conflict resolution**: Conflicting preferences (lofi + high energy) are resolved by genre dominance, not averaging or negotiation.
- **Diversity illusion**: Mainstream profiles (pop, rock) get diverse recommendations because their genres have multiple songs. Niche profiles get trapped in single-genre loops.

---

## 8. Future Work  

**Short term:**
- **Enable acousticness scoring**: Add +0.5 or +1.0 bonus if user likes acoustic AND song's acousticness > 0.7.
- **Add tempo weighting**: Score songs closer to target BPM, not just energy (energy is rough proxy).
- **Implement fuzzy genre matching**: Allow "indie pop" to partially match "pop" searches (similarity instead of binary).
- **Normalize scores per preference**: Avoid genre cliff by scaling weights based on dataset coverage.

**Medium term:**
- **Diversity re-ranking**: After ranking top K, remove genre duplicates and substitute related genres.
- **Valence separation**: Treat valence (positivity) separately from mood to capture happy metal vs. sad metal.
- **User listening history**: Collaborate with similar users' playlists, not just content features.
- **Explanation richness**: Add "Tempo matched: 118 BPM vs. your target 125 BPM" to justify energy scores.

**Long term:**
- **Hybrid filtering**: Combine content-based + collaborative filtering.
- **Cold-start handling**: Recommend to new users with no history via demographic/preference clustering.
- **Serendipity injection**: Occasionally recommend "unexpectedly good" songs outside user's genre to spark discovery.
- **Context awareness**: Adjust recommendations for time of day, activity (workout vs. sleep), or social context.  

---

## 9. Personal Reflection  

Building ContentMatch revealed that **simple scoring systems have profound biases hidden in their weights**. The genre +2.0 vs. mood +1.0 split seemed arbitrary during implementation, but in testing it completely dominated the recommendation space—songs matching genre but failing mood consistently ranked higher than the reverse. This made me realize that *every design choice is a values choice*: by weighting genre heavily, I was implicitly saying "genre matters most," which may not be true for all listeners.

I was surprised by how much a **single non-existent preference can break a user experience**. When the dataset has no "transcendent" mood songs, the algorithm doesn't *know* to ask the user for clarification or suggest alternatives—it just silently falls back to other factors. Real recommenders must handle this gracefully (e.g., "We don't have any transcendent songs, but here's what we recommend instead").

This experience changed how I listen to music recommendation apps. I now think about:
- **What features matter to the app?** (genre, artist, listener history, time-of-day?)
- **What's invisible?** (Why did Spotify suggest this song? What did I *not* hear?)
- **Who's served well?** (Are metal fans treated differently than pop fans? What about ultra-niche genres?)

Most importantly, I learned that recommender systems are not objective—they encode human decisions and cultural assumptions. Building them is as much about *values* as it is about *code*.  
