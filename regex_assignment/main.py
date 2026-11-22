"""2026 전주대학교 대동제/해커톤 운영 로그 정규표현식 분석 프로그램."""

from pathlib import Path
import re

# main.py와 같은 폴더에 있는 data.txt를 불러옵니다.
DATA_FILE = Path(__file__).resolve().parent / "data.txt"


def extract_data(text: str) -> dict:
    """로그에서 과제에서 요구하는 다섯 종류의 정보를 추출합니다."""
    # 1. 올바른 이메일: ID@도메인.최상위도메인 구조 (hyunwoo@.ac.kr 제외)
    emails = re.findall(
        r"(?<![\w.@+-])[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+(?![\w.-])",
        text,
    )

    # 2. 휴대전화: 010 + 중간 네 자리 + 마지막 네 자리.
    #    하이픈, 점, 공백으로 구분 가능하며, 010-123-4567은 제외됩니다.
    phones = re.findall(
        r"(?<!\d)010[-. ]\d{4}[-. ]\d{4}(?!\d)", text
    )

    # 3. 재학생 학번/학과: 대괄호 안의 202로 시작하는 9자리 학번만 인정.
    students = re.findall(
        r"\[(202\d{6})\s*/\s*([^\]\n/]+?)\s*\]", text
    )
    students = [(number, department.strip()) for number, department in students]

    # 4. GitHub(gitlab 제외) URL과 2026년도 쿠폰 코드
    github_urls = re.findall(
        r"https?://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", text
    )
    coupons = re.findall(r"\bFEST-2026-[A-Za-z0-9]+\b", text)

    # 5. 부스별 '매출:' 뒤에 바로 나오는 금액만 추출.
    #    괄호 내부 카드/현금 상세 및 쿠폰 5,000원은 합산하지 않습니다.
    sales_matches = re.findall(
        r"^-\s*(.+?)\s+매출:\s*([\d,]+)원", text, flags=re.MULTILINE
    )
    sales = [(booth, int(amount.replace(",", ""))) for booth, amount in sales_matches]

    return {
        "emails": emails,
        "phones": phones,
        "students": students,
        "github_urls": github_urls,
        "coupons": coupons,
        "sales": sales,
        "total_sales": sum(amount for _, amount in sales),
    }


def main() -> None:
    try:
        text = DATA_FILE.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"데이터 파일을 찾을 수 없습니다: {DATA_FILE}")
        return

    result = extract_data(text)

    print("=" * 55)
    print("2026 전주대학교 대동제 및 해커톤 데이터 분석")
    print("=" * 55)

    print("\n[1] 유효한 이메일")
    for email in result["emails"]:
        print(" -", email)
    print(f"총 {len(result['emails'])}개")

    print("\n[2] 휴대전화 번호")
    for phone in result["phones"]:
        print(" -", phone)
    print(f"총 {len(result['phones'])}개")

    print("\n[3] 재학생 학번 / 학과")
    for number, department in result["students"]:
        print(f" - 학번: {number} / 학과: {department}")
    print(f"총 {len(result['students'])}명")

    print("\n[4] GitHub 저장소 URL")
    for url in result["github_urls"]:
        print(" -", url)
    print(f"총 {len(result['github_urls'])}개")

    print("\n[4] 2026년도 유효 쿠폰 코드")
    for coupon in result["coupons"]:
        print(" -", coupon)
    print(f"총 {len(result['coupons'])}개")

    print("\n[5] 부스별 매출액")
    for booth, amount in result["sales"]:
        print(f" - {booth}: {amount:,}원")
    print(f"전체 매출 합계: {result['total_sales']:,}원")


if __name__ == "__main__":
    main()
