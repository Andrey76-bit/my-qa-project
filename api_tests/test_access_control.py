import pytest
from access_control_demo import get_user_profile_safe, get_user_profile_vulnerable

def test_vulnerable_allows_access_to_other_profile():
    """Уязвимая функция должна вернуть чужой профиль (демонстрация проблемы)"""
    result = get_user_profile_vulnerable(124)
    assert result is not None
    assert result["name"] == "Злоумышленник"

def test_safe_blocks_access_to_other_profile():
    """Безопасная функция не должна отдавать чужие данные"""
    result = get_user_profile_safe(current_user_id=123, requested_user_id=124)
    assert result is None, "Безопасная функция пропустила чужой доступ!"

def test_safe_allows_access_to_own_profile():
    """Безопасная функция должна отдавать свой профиль"""
    result = get_user_profile_safe(current_user_id=123, requested_user_id=123)
    assert result is not None
    assert result["name"] == "Андрей"
