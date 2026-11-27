# My Custom Illegal Fantasy Teams

This document contains two custom illegal fantasy teams created for Deliverable 2, Part B2.

Both teams were submitted through the `POST /teams` API endpoint and returned HTTP 400 responses as expected.

## 1. Duplicate Player Test

**Team Name:** Duplicate Player Test

**Owner:** Waqar

**Violation:** SPD Smith (P075) appears twice in the player list.

**API Endpoint:** `POST /teams`

**Expected HTTP Status:** 400

**Actual API Response:**

```json
{
  "detail": {
    "message": "Duplicate Player Test is not a legal team: Duplicate player found: SPD Smith (P075)",
    "problems": [
      "Duplicate player found: SPD Smith (P075)"
    ]
  }
}
```

**Result:** PASS — The API correctly detected the duplicate player.

## 2. Same Captain and Vice-Captain Test

**Team Name:** Same Captain Test

**Owner:** Waqar

**Violation:** Captain and vice-captain are both P089 (Babar Azam).

**API Endpoint:** `POST /teams`

**Expected HTTP Status:** 400

**Actual API Response:**

```json
{
  "detail": {
    "message": "Same Captain Test is not a legal team: Captain and vice-captain cannot be the same player",
    "problems": [
      "Captain and vice-captain cannot be the same player"
    ]
  }
}
```

**Result:** PASS — The API correctly detected that captain and vice-captain cannot be the same player.

## Summary

Both custom illegal teams were successfully tested using the Dugout Fantasy Cricket API.

- Duplicate player validation: PASS
- Captain and vice-captain validation: PASS
- Both API responses returned HTTP 400 as expected.