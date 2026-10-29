import pytest
from salon_booking import extra_time_charge, can_book, arrival_status


# ============================================================================
# Branch Coverage Tests for extra_time_charge
# ============================================================================

def test_extra_time_charge_unknown_service():
    # Branch: service not in INCLUDED_MIN is True
    with pytest.raises(ValueError, match="unknown service"):
        extra_time_charge("invalid_service", 30, "junior", False)


def test_extra_time_charge_negative_duration():
    # Branch: duration_min < 0 is True
    with pytest.raises(ValueError, match="invalid duration"):
        extra_time_charge("haircut", -5, "junior", False)


def test_extra_time_charge_within_included_time():
    # Branch: extra <= 0 is True (returns 0)
    # haircut included: 30 min, duration: 25 min -> extra = -5 <= 0
    assert extra_time_charge("haircut", 25, "junior", False) == 0


def test_extra_time_charge_exact_included_time():
    # Boundary case: extra == 0 -> returns 0
    # haircut included: 30 min, duration: 30 min -> extra = 0 <= 0
    assert extra_time_charge("haircut", 30, "junior", False) == 0


def test_extra_time_charge_junior_member_not_spa():
    # Branches:
    # - is_member and service != "spa" is True (included = 30 + 15 = 45)
    # - stylist_level == "junior" is True (rate = 10)
    # - extra > 60 is False (extra = 10 <= 60)
    # Result: 10 * 10 = 100
    assert extra_time_charge("haircut", 55, "junior", is_member=True) == 100


def test_extra_time_charge_member_with_spa():
    # Branch: is_member is True BUT service == "spa" (so service != "spa" is False)
    # spa included: 90 min (no member bonus). duration: 110 -> extra = 20
    # stylist_level != "junior" (rate = 18), extra <= 60
    # Result: 20 * 18 = 360
    assert extra_time_charge("spa", 110, "senior", is_member=True) == 360


def test_extra_time_charge_non_junior_extra_under_60():
    # Branches:
    # - stylist_level == "junior" is False (rate = 18)
    # - extra > 60 is False (extra = 20 <= 60)
    # colour included: 60 min. duration: 80 -> extra = 20. rate = 18 -> charge = 360
    assert extra_time_charge("colour", 80, "intermediate", is_member=False) == 360


def test_extra_time_charge_senior_extra_over_60():
    # Branches:
    # - stylist_level == "junior" is False (rate = 18)
    # - extra > 60 is True (rate = 18 + 8 = 26)
    # - stylist_level == "senior" is True (rate = 26 + 4 = 30)
    # haircut included: 30 min. duration: 100 -> extra = 70.
    # Result: 70 * 30 = 2100
    assert extra_time_charge("haircut", 100, "senior", is_member=False) == 2100


def test_extra_time_charge_junior_extra_over_60():
    # Critical Branch for 100% Branch Coverage:
    # - stylist_level == "junior" is True (rate = 10)
    # - extra > 60 is True (rate = 10 + 8 = 18)
    # - stylist_level == "senior" is False (line 21 -> line 23 branch!)
    # haircut included: 30 min. duration: 100 -> extra = 70.
    # Result: 70 * 18 = 1260
    assert extra_time_charge("haircut", 100, "junior", is_member=False) == 1260


# ============================================================================
# Branch Coverage Tests for can_book
# ============================================================================

def test_can_book_walk_in_allowed():
    # Branch: is_walk_in is True, party_size <= 2 is True
    assert can_book(party_size=2, services=1, is_walk_in=True) is True


def test_can_book_walk_in_rejected():
    # Branch: is_walk_in is True, party_size <= 2 is False (party_size > 2)
    assert can_book(party_size=3, services=1, is_walk_in=True) is False


def test_can_book_advance_large_party_rejected():
    # Branches:
    # - is_walk_in is False
    # - party_size > 4 is True (returns False)
    assert can_book(party_size=5, services=1, is_walk_in=False) is False


def test_can_book_advance_services_allowed():
    # Branches:
    # - is_walk_in is False
    # - party_size > 4 is False
    # - services <= 2 is True (returns True)
    assert can_book(party_size=4, services=2, is_walk_in=False) is True


def test_can_book_advance_services_exceeded():
    # Branches:
    # - is_walk_in is False
    # - party_size > 4 is False
    # - services <= 2 is False (returns False)
    assert can_book(party_size=3, services=3, is_walk_in=False) is False


# ============================================================================
# Branch Coverage Tests for arrival_status
# ============================================================================

def test_arrival_status_colour_weekend_open():
    # Branches:
    # - is_colour is True (cutoff = 10)
    # - is_weekend is True (cutoff = 10 + 10 = 20)
    # - minutes_early >= cutoff is True (20 >= 20 -> "open")
    assert arrival_status(minutes_early=20, is_colour=True, is_weekend=True) == "open"


def test_arrival_status_non_colour_weekday_open():
    # Branches:
    # - is_colour is False (cutoff = 5)
    # - is_weekend is False (cutoff = 5)
    # - minutes_early >= cutoff is True (6 >= 5 -> "open")
    assert arrival_status(minutes_early=6, is_colour=False, is_weekend=False) == "open"


def test_arrival_status_colour_weekday_late():
    # Branches:
    # - is_colour is True (cutoff = 10)
    # - is_weekend is False (cutoff = 10)
    # - minutes_early >= cutoff is False (5 < 10)
    # - minutes_early >= cutoff - 15 is True (5 >= 10 - 15 = -5 -> "late")
    assert arrival_status(minutes_early=5, is_colour=True, is_weekend=False) == "late"


def test_arrival_status_non_colour_weekend_late():
    # Branches:
    # - is_colour is False (cutoff = 5)
    # - is_weekend is True (cutoff = 5 + 10 = 15)
    # - minutes_early >= cutoff is False (0 < 15)
    # - minutes_early >= cutoff - 15 is True (0 >= 15 - 15 = 0 -> "late")
    assert arrival_status(minutes_early=0, is_colour=False, is_weekend=True) == "late"


def test_arrival_status_closed():
    # Branches:
    # - is_colour is False (cutoff = 5)
    # - is_weekend is False (cutoff = 5)
    # - minutes_early >= cutoff is False (-11 < 5)
    # - minutes_early >= cutoff - 15 is False (-11 < 5 - 15 = -10 -> "closed")
    assert arrival_status(minutes_early=-11, is_colour=False, is_weekend=False) == "closed"
