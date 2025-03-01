# Sirodrop - 직관적인 파일 전송 도구

<div align="center">
  <img src="docs/images/logo.png" alt="Sirodrop 로고" width="150">
  <p>모던하고 직관적인 croc-cli의 GUI 인터페이스</p>
</div>

## 소개

Sirodrop은 [croc](https://github.com/schollz/croc)을 위한 모던한 GUI 인터페이스입니다. croc은 쉽고 안전하게 파일을 컴퓨터 간에 전송할 수 있는 도구이며, Sirodrop은 직관적인 사용자 인터페이스를 통해 이 기능을 한층 더 사용하기 쉽게 만들었습니다.

### 주요 기능

✨ **직관적인 UI**: 깔끔하고 현대적인 인터페이스로 누구나 쉽게 사용 가능  
🔒 **안전한 전송**: 종단간 암호화로 파일을 안전하게 전송  
📁 **드래그 앤 드롭**: 파일과 폴더를 쉽게 끌어다 놓기 가능  
🌙 **다크 모드**: 라이트/다크 테마 지원  
📱 **크로스 플랫폼**: Windows, macOS, Linux 지원  

## 스크린샷

<div align="center">
  <img src="docs/images/screenshot_light.png" alt="Sirodrop 라이트 모드" width="48%">
  <img src="docs/images/screenshot_dark.png" alt="Sirodrop 다크 모드" width="48%">
</div>

## 설치

### 사전 요구사항

- Python 3.10 이상
- [croc](https://github.com/schollz/croc) 설치

### 설치 방법

```bash
# 저장소 클론
git clone https://github.com/sioaeko/croc-cli.git
cd croc-cli

# 의존성 설치
pip install -r requirements.txt

# 실행
python main.py
```

## 사용 방법

### 파일 보내기

1. "Send" 탭으로 이동
2. 파일을 드래그 앤 드롭하거나 "찾아보기" 버튼 사용
3. 선택적으로 암호화 및 압축 옵션 설정
4. "전송 시작" 버튼 클릭
5. 생성된 코드를 수신자와 공유

### 파일 받기

1. "Receive" 탭으로 이동
2. 보낸 사람으로부터 받은 코드 입력
3. 저장 위치 선택(선택 사항)
4. "수신 시작" 버튼 클릭

## 커스터마이징

설정 탭에서 다음과 같은 옵션을 조정할 수 있습니다:

- UI 테마(라이트/다크)
- 기본 저장 위치
- 전송 옵션 기본값

## 기술 스택

- Python
- PyQt6
- croc CLI

## 기여하기

기여는 언제나 환영합니다! 다음과 같은 방법으로 기여할 수 있습니다:

1. 저장소 포크
2. 기능 브랜치 생성 (`git checkout -b feature/amazing-feature`)
3. 변경사항 커밋 (`git commit -m 'Add some amazing feature'`)
4. 브랜치에 푸시 (`git push origin feature/amazing-feature`)
5. Pull Request 생성

## 라이선스

[MIT License](LICENSE) © [sioaeko](https://github.com/sioaeko)

## 감사의 말

- [croc](https://github.com/schollz/croc) - Christian Muehlhaeuser 및 기여자들
- PyQt 팀
- 피드백과 지원을 제공해준 모든 사용자들 