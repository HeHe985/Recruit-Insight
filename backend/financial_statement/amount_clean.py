"""
    DART API를 통해 얻은 amount 값이
    '' 또는 '-' 또는 ' ' 등 숫자로 변환할 수 없는 경우
    None로 변환하는 함수
"""

def amount_clean(value):
    """
    변수 : API의 amount 값 전달
    """
    if not value:
        return None
    
    val_str = str(value).strip()  # 공백 제거
    if val_str == '-' or val_str == '_' or val_str == '':
        return None

    try:
        return int(val_str.replace(',', ''))
    except ValueError:
        return None