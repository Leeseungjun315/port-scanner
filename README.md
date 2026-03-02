# Ethical Port Scanner

> 🇺🇸 English \| 🇰🇷 한국어

------------------------------------------------------------------------

# English

## Additional Disclaimer

Any misuse of this software is solely the responsibility of the user.  
The author assumes no liability for any damages, losses, or legal consequences arising from the use or misuse of this tool.

## Overview

Ethical Port Scanner is a minimal TCP connect port scanner built for
**authorized security checks and educational purposes only**.

This project demonstrates how to design security tools responsibly with
built-in ethical guardrails.

------------------------------------------------------------------------

## Legal & Ethical Use

This tool must be used **ONLY** on:

-   Systems you own, or
-   Systems you have **explicit written permission** to test

Unauthorized scanning may violate laws, regulations, or organizational
policies.

### Built-in Safety Features

-   Defaults to localhost (`127.0.0.1`)
-   Requires `--acknowledge` for non-local targets
-   Conservative timeout and concurrency defaults
-   No stealth techniques
-   No exploitation features

------------------------------------------------------------------------

## Installation

Python 3.10+ recommended.

``` bash
git clone https://github.com/yourusername/ethical-port-scanner.git
cd ethical-port-scanner
```

------------------------------------------------------------------------

## Usage Examples

Scan common ports on localhost:

``` bash
python scanner.py --ports 1-1024
```

Scan specific ports and show only open ones:

``` bash
python scanner.py --ports 22,80,443 --open-only
```

Scan a permitted remote host (REQUIRES permission):

``` bash
python scanner.py --host example.com --ports 80,443 --acknowledge
```

------------------------------------------------------------------------

# 한국어

## 추가 면책 조항

본 소프트웨어의 사용 또는 오남용으로 인해 발생하는 모든 책임은 사용자에게 있습니다.  
저자는 이 도구의 사용으로 인해 발생하는 어떠한 손해, 손실, 법적 책임에 대해서도 책임을 지지 않습니다.

## 개요

Ethical Port Scanner는 **허가된 보안 점검 및 학습 목적 전용**으로 제작된
TCP connect 기반 포트 스캐너입니다.

이 프로젝트는 보안 도구를 설계하는 방법과 윤리적 안전장치를 코드에 포함하는 방식을 보여줍니다.

------------------------------------------------------------------------

## 법적 및 윤리적 사용 기준

이 도구는 다음의 경우에만 사용해야 합니다:

-   본인이 소유한 시스템
-   명시적인 서면 허가를 받은 시스템

무단 포트 스캔은 관련 법률, 규정 또는 조직 정책을 위반할 수 있습니다.

### 내장된 안전 장치

-   기본 대상은 localhost (`127.0.0.1`)
-   원격 대상은 `--acknowledge` 옵션 필수
-   보수적인 timeout 및 동시성 기본값
-   스텔스 기능 없음
-   취약점 공격 기능 없음

------------------------------------------------------------------------

## 설치 방법

Python 3.10 이상 권장

``` bash
git clone https://github.com/yourusername/ethical-port-scanner.git
cd ethical-port-scanner
```

------------------------------------------------------------------------

## 사용 예시

로컬호스트 기본 포트 스캔:

``` bash
python scanner.py --ports 1-1024
```

특정 포트만 스캔 후 열린 포트만 출력:

``` bash
python scanner.py --ports 22,80,443 --open-only
```

허가받은 원격 서버 스캔 (반드시 허가 필요):

``` bash
python scanner.py --host example.com --ports 80,443 --acknowledge
```
