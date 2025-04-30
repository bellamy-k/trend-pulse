import pandas as pd
from pytrends.request import TrendReq
import logging

# 로깅 설정 (간단하게 INFO 레벨 및 메시지 형식 지정)
# 터미널에 바로 결과가 보이도록 print도 사용할 예정이므로, 로깅은 정보/오류 표시에 활용
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def fetch_and_print_kr_daily_trends():
    """
    간단하게 한국(KR)의 일일 인기 급상승 검색어를 가져와서 출력하는 테스트 함수.
    """
    logging.info("Google Trends 접속 시도...")
    try:
        # pytrends 객체 초기화. 한국어(hl)와 한국 시간대(tz=540, UTC+9) 설정
        pytrends = TrendReq(hl='ko-KR', tz=540)
    except Exception as e:
        logging.error(f"pytrends 초기화 중 오류 발생: {e}")
        return # 객체 생성 실패 시 함수 종료

    logging.info("한국(KR) 일일 인기 급상승 검색어 요청...")
    try:
        # trending_searches 함수를 사용하여 한국('kr')의 데일리 트렌드 가져오기
        # 국가 코드는 'pn' 파라미터를 사용하며 소문자로 전달
        daily_trends_df = pytrends.realtime_trending_searches(pn='us')

        # 결과가 DataFrame 형태로 제대로 왔는지 확인
        if isinstance(daily_trends_df, pd.DataFrame) and not daily_trends_df.empty:
            logging.info("데이터 수신 성공!")
            print("\n✅ === 한국(KR) 일일 인기 급상승 검색어 === ✅")
            # DataFrame 전체를 문자열로 변환하여 출력 (인덱스 번호 제외)
            print(daily_trends_df.to_string(index=False))
            print("============================================")
        elif daily_trends_df is not None:
            # 비어있는 DataFrame이나 다른 형태일 경우
            logging.warning("데이터를 가져왔으나 비어있거나 예상 형식이 아닙니다.")
            print(f"수신된 데이터: {daily_trends_df}") # 실제 내용 확인용
        else:
            # None이 반환된 경우
            logging.warning("데이터를 가져오지 못했습니다 (결과가 None입니다).")

    # 오류 처리
    except Exception as e:
        logging.error(f"트렌드 데이터 요청 또는 처리 중 오류 발생: {e}")
        # Rate Limit 에러 (429) 가능성 확인
        if hasattr(e, 'response') and e.response.status_code == 429:
            logging.error("-> 요청 한도 초과(429) 오류일 수 있습니다. 잠시 후 다시 시도해 보세요.")
        elif "response 429" in str(e).lower():
            logging.error("-> 요청 한도 초과(429) 오류일 수 있습니다 (오류 메시지 확인).")


# 메인 코드 실행 부분
if __name__ == "__main__":
    print("\n--- Google Trends 한국 일일 트렌드 가져오기 테스트 ---")
    fetch_and_print_kr_daily_trends()
    print("\n--- 테스트 완료 ---")
