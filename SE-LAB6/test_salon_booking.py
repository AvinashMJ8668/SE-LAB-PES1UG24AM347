import pytest
from salon_booking import extra_time_charge, can_book, arrival_status


# ============================================================================
# Comprehensive Test Suite for salon_booking (100% Code and Branch Coverage)
# ============================================================================

# Tests for extra_time_charge
def test_within_included_time():
    assert extra_time_charge("haircut", 20, "junior", False) == 0


def test_exact_included_time():
    assert extra_time_charge("haircut", 30, "junior", False) == 0


def test_extra_time_charge_unknown_service():
    with pytest.raises(ValueError, match="unknown service"):
        extra_time_charge("invalid_service", 40, "junior", False)


def test_extra_time_charge_negative_duration():
    with pytest.raises(ValueError, match="invalid duration"):
        extra_time_charge("haircut", -10, "junior", False)


def test_extra_time_charge_member_non_spa():
    # Member gets +15 min for non-spa services (haircut: 30 + 15 = 45 min)
    # 55 - 45 = 10 extra min. Junior rate = 10 -> 10 * 10 = 100
    assert extra_time_charge("haircut", 55, "junior", is_member=True) == 100


def test_extra_time_charge_member_spa():
    # Member does not get extra min for spa service (spa = 90 min)
    # 110 - 90 = 20 extra min. Non-junior rate = 18 -> 20 * 18 = 360
    assert extra_time_charge("spa", 110, "senior", is_member=True) == 360


def test_extra_time_charge_non_junior_moderate_extra():
    # Colour included: 60 min. Duration: 80 min -> extra = 20 min (<= 60).
    # Stylist not junior -> rate = 18. Charge = 20 * 18 = 360
    assert extra_time_charge("colour", 80, "intermediate", is_member=False) == 360


def test_extra_time_charge_senior_overtime():
    # Haircut included: 30 min. Duration: 100 min -> extra = 70 min (> 60).
    # Rate: 18 + 8 + 4 (senior) = 30. Charge = 70 * 30 = 2100
    assert extra_time_charge("haircut", 100, "senior", is_member=False) == 2100


def test_extra_time_charge_junior_overtime():
    # Haircut included: 30 min. Duration: 100 min -> extra = 70 min (> 60).
    # Junior rate: 10 + 8 = 18 (not senior). Charge = 70 * 18 = 1260
    assert extra_time_charge("haircut", 100, "junior", is_member=False) == 1260


# Tests for can_book
def test_can_book():
    assert can_book(2, 1, False) is True


def test_can_book_walk_in_allowed():
    assert can_book(2, 1, is_walk_in=True) is True


def test_can_book_walk_in_rejected():
    assert can_book(3, 1, is_walk_in=True) is False


def test_can_book_advance_large_party_rejected():
    assert can_book(5, 1, is_walk_in=False) is False


def test_can_book_advance_services_limit_accepted():
    assert can_book(4, 2, is_walk_in=False) is True


def test_can_book_advance_services_limit_exceeded():
    assert can_book(4, 3, is_walk_in=False) is False


# Tests for arrival_status
def test_arrival_status_colour_weekend_open():
    # Colour (10) + Weekend (10) = 20 cutoff. 20 >= 20 -> "open"
    assert arrival_status(20, is_colour=True, is_weekend=True) == "open"


def test_arrival_status_non_colour_weekday_open():
    # Non-colour (5) + Weekday (0) = 5 cutoff. 5 >= 5 -> "open"
    assert arrival_status(5, is_colour=False, is_weekend=False) == "open"


def test_arrival_status_colour_weekday_late():
    # Colour (10) + Weekday (0) = 10 cutoff. 5 >= -5 and < 10 -> "late"
    assert arrival_status(5, is_colour=True, is_weekend=False) == "late"


def test_arrival_status_non_colour_weekend_late():
    # Non-colour (5) + Weekend (10) = 15 cutoff. 0 >= 0 and < 15 -> "late"
    assert arrival_status(0, is_colour=False, is_weekend=True) == "late"


def test_arrival_status_closed():
    # Non-colour (5) + Weekday (0) = 5 cutoff. -11 < -10 -> "closed"
    assert arrival_status(-11, is_colour=False, is_weekend=False) == "closed"
