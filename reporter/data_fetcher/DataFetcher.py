import abc
import logging
from typing import Any, Dict, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class DataFetcher(abc.ABC):

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        DataFetcher를 초기화합니다.

        Args:
            config (Optional[Dict[str, Any]]): API 키, 기본 URL 등 필요한 설정을 담을 수 있는
                                                 선택적인 설정 딕셔너리입니다.
                                                 하위 클래스에서 특정 설정을 처리합니다.
        """
        # 각 하위 클래스 이름으로 로거를 생성합니다.
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config = config if config else {}
        self.logger.info(f"{self.__class__.__name__} initialized.")
        # 필요하다면 여기에 공통 리소스(예: requests 세션)를 초기화할 수 있습니다.
        # import requests
        # self.session = requests.Session()
        # self.session.headers.update({'User-Agent': 'MyDataFetcherApp/1.0'})

    @abc.abstractmethod
    def fetch_data(self, *args: Any, **kwargs: Any) -> Any:
        """
        특정 소스로부터 데이터를 가져옵니다.

        이 메소드는 반드시 하위 클래스에서 구현되어야 합니다.
        메소드가 받는 파라미터와 반환하는 데이터의 형태는
        각 데이터 소스의 특성에 따라 달라집니다.

        Args:
            *args: 하위 클래스 구현에 필요한 위치 기반 인자들.
            **kwargs: 하위 클래스 구현에 필요한 키워드 기반 인자들
                      (예: query, keywords, region, count 등).

        Returns:
            Any: 가져온 데이터. 보통 dict, list 등의 구조화된 형태이거나,
                 실패 시 None 또는 예외 발생.

        Raises:
            NotImplementedError: 하위 클래스가 이 메소드를 구현하지 않은 경우.
            Exception: 데이터 가져오기 중 발생할 수 있는 다양한 예외 (하위 클래스 구현에 따름).
        """
        # 이 메소드는 하위 클래스에서 반드시 오버라이드(재정의)되어야 함을 나타냅니다.
        raise NotImplementedError("Subclasses must implement the fetch_data() method.")

    def __repr__(self) -> str:
        """객체를 문자열로 표현하여 디버깅 등에 용이하게 합니다."""
        # 설정 값은 민감할 수 있으므로 기본적으로는 표시하지 않거나 일부만 표시하는 것이 좋을 수 있습니다.
        # 여기서는 간단히 클래스 이름만 표시합니다.
        return f"<{self.__class__.__name__}>"
