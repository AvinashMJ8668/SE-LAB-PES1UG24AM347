import pytest
from salon_booking import extra_time_charge, can_book, arrival_status

# Test cases for extra_time_charge
def test_extra_time_charge_within_included():
    # Covers lines 13-14 (extra <= 0 -> returns 0)
    assert extra_time_charge("haircut", 20, "junior", False) == 0

def test_extra_time_charge_unknown_service():
    # Covers lines 5-6 (service not in INCLUDED_MIN)
    with pytest.raises(ValueError, match="unknown service"):
        extra_time_charge("massage", 30, "junior", False)

def test_extra_time_charge_negative_duration():
    # Covers lines 7-8 (duration_min < 0)
    with pytest.raises(ValueError, match="invalid duration"):
        extra_time_charge("haircut", -5, "junior", False)

def test_extra_time_charge_junior_member():
    # Covers lines 10-11 (member included extra time), 15-16 (junior rate), 23 (return)
    # haircut included: 30 + 15 = 45 min. duration: 55 min -> extra = 10 min.
    # junior rate = 10 -> charge = 10 * 10 = 100
    assert extra_time_charge("haircut", 55, "junior", True) == 100

def test_extra_time_charge_senior_overtime():
    # Covers lines 17-18 (else rate=18), 19-20 (extra > 60), 21-22 (senior rate += 4), 23
    # haircut included: 30 min. duration: 100 min -> extra = 70 min (> 60).
    # rate = 18 + 8 + 4 = 30 -> charge = 70 * 30 = 2100
    assert extra_time_charge("haircut", 100, "senior", False) == 2100


# Test cases for can_book
def test_can_book_walk_in_allowed():
    # Covers lines 27-28 (walk-in party <= 2)
    assert can_book(2, 1, is_walk_in=True) is True

def test_can_book_walk_in_rejected():
    # Covers lines 27-28 (walk-in party > 2)
    assert can_book(3, 1, is_walk_in=True) is False

def test_can_book_large_party_rejected():
    # Covers lines 29-30 (party_size > 4)
    assert can_book(5, 1, is_walk_in=False) is False

def test_can_book_services_valid():
    # Covers line 31 (services <= 2 is True)
    assert can_book(4, 2, is_walk_in=False) is True

def test_can_book_services_exceeded():
    # Covers line 31 (services <= 2 is False)
    assert can_book(4, 3, is_walk_in=False) is False


# Test cases for arrival_status
def test_arrival_status_open():
    # Covers lines 35-36 (is_colour True -> cutoff = 10), 41-42 (minutes_early >= cutoff -> "open")
    assert arrival_status(12, is_colour=True, is_weekend=False) == "open"

def test_arrival_status_late():
    # Covers lines 37-38 (cutoff = 5), 39-40 (weekend -> cutoff = 15), 43-44 (late)
    assert arrival_status(2, is_colour=False, is_weekend=True) == "late"

def test_arrival_status_closed():
    # Covers line 45 ("closed")
    # weekday non-colour cutoff = 5. minutes_early = -15 < -10 -> closed
    assert arrival_status(-15, is_colour=False, is_weekend=False) == "closed"
