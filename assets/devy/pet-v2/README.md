# 스피카 G — Codex Pet v2

현재 기본형인 **스피카 G 2.0.0**으로 제작한 펫 자료 모음이다. 제작일은 2026-10-13, 저장소 정리일은 2026-10-20이다.

매끈하게 닫힌 금빛 고리, 얼굴 오른쪽 위의 독립 초승달과 네 갈래 별을 사용하는 **스피카 (개선판)**이다.

![스피카 G 펫 미리보기](previews/all-states.apng)

## 바로 사용하기

- [설치 ZIP](spica-improved-v2.zip): `pet.json`과 최종 `spritesheet.webp`를 담은 패키지.
- [색을 보존한 애니메이션 APNG](previews/all-states.apng): 전체 동작 확인용.
- [MP4](previews/all-states.mp4) · [GIF](previews/all-states.gif) · [16방향 시선 GIF](previews/look-directions.gif)
- [동작 전체 모음 이미지](previews/contact-sheet.png) · [시선 방향 모음 이미지](previews/look-directions.png)

설치 ZIP의 `spica-improved-v2` 폴더를 `~/.codex/pets/` 아래에 놓는다. `pet.json`과 `spritesheet.webp`를 같은 폴더에 유지한다. 제작 당시에는 Codex의 **설정 → Pets → Refresh → 스피카 (개선판)**에서 선택했다. 앱 버전에 따라 메뉴 이름은 달라질 수 있다.

GIF는 색상 수 제한이 있으므로 색 확인에는 APNG나 최종 WebP를 사용한다. 이 패키지의 각 포즈는 **192 × 208 픽셀**이다. 더 크게 표시해도 원본 그림의 세부 정보가 추가되지는 않는다.

## 파일 구성

| 경로 | 내용 |
| --- | --- |
| [pet.json](pet.json) | 펫 ID, 이름, 설명, v2 설정과 시트 경로 |
| [spritesheet.webp](spritesheet.webp) | 실제 설치에 사용한 최종 투명 WebP |
| [spritesheet.png](spritesheet.png) | 최종 WebP와 RGBA 픽셀이 같은 편집용 PNG |
| [animations.json](animations.json) | 행·프레임 좌표, 시선 각도, 저장된 미리보기의 프레임 재생 시간 |
| [frames/](frames/) | 최종 시트에서 원래 크기 그대로 분리한 PNG 73개 |
| [previews/](previews/) | 전체·상태별 동작, 점프 연결, 시선, 정지 이미지 |
| [source/generated/](source/generated/) | 생성 원본 13개와 왼쪽 방향 앵커 1개 |
| [source/generation-request.json](source/generation-request.json) | 당시 외형·동작 요청, 스타일과 시트 규격 |
| [source/recovered-generation-prompts.json](source/recovered-generation-prompts.json) | 생성 기록에서 복구한 작업별 프롬프트 14개 |
| [source/look-mechanics.md](source/look-mechanics.md) | 몸체·표식은 고정하고 눈과 입으로 시선을 표현하는 기준 |
| [source/provenance.json](source/provenance.json) | 사용한 기본 PNG·프롬프트·카드의 저장소 커밋과 해시 |
| [source/generation-provenance.json](source/generation-provenance.json) | 생성 원본 파일, 생성 시각과 당시 검수 기록 |
| [qa/](qa/) | 제작 당시 구조·품질·시각·방향 검수 기록 |
| [archive-validation.json](archive-validation.json) | 이번 정리에서 확인한 파일·픽셀 보존 결과 |
| [checksums.json](checksums.json) | 보관 파일의 SHA-256 목록 |
| [legacy/](legacy/) | G로 바꾸기 전 펫 설치 패키지 보존본 |

기본 캐릭터 자료는 [상위 폴더](../README.md)의 PNG·카드·재사용 프롬프트를 기준으로 한다. 생성 원본은 배경 제거 전 이미지이므로, 바로 사용할 때는 최종 WebP 또는 분리된 프레임을 쓴다.

## 동작과 프레임

시트는 **1536 × 2288**, **8열 × 11행**, 셀은 **192 × 208**이다. 행과 열 번호는 왼쪽 위부터 시작하는 0 기준이다. 사용 프레임은 73개이며 나머지 15개 셀은 투명하다.

| 행 | 상태 | 프레임 | 미리보기 |
| --- | --- | --- | --- |
| 0 | `idle` — 쉬기·숨쉬기·깜빡임 | 6 | [GIF](previews/idle.gif) |
| 1 | `running-right` — 오른쪽 이동 | 8 | [GIF](previews/running-right.gif) |
| 2 | `running-left` — 왼쪽 이동 | 8 | [GIF](previews/running-left.gif) |
| 3 | `waving` — 작은 발로 인사 | 4 | [GIF](previews/waving.gif) |
| 4 | `jumping` — 작은 점프 | 5 | [GIF](previews/jumping.gif) |
| 5 | `failed` — 실패·막힘 반응 | 8 | [GIF](previews/failed.gif) |
| 6 | `waiting` — 입력·도움 대기 | 6 | [GIF](previews/waiting.gif) |
| 7 | `running` — 작업에 집중 | 6 | [GIF](previews/running.gif) |
| 8 | `review` — 결과 확인 | 6 | [GIF](previews/review.gif) |
| 9 | 위쪽부터 아래 오른쪽까지 시선 | 8 | [방향 모음](previews/look-directions.png) |
| 10 | 아래쪽부터 위 왼쪽까지 시선 | 8 | [방향 모음](previews/look-directions.png) |

시선은 화면 기준 시계 방향이다. **0° 위 → 90° 화면 오른쪽 → 180° 아래 → 270° 화면 왼쪽**, 22.5° 간격이다. 0°는 정면이 아니라 위를 보는 포즈이며, 중립 포즈는 행 0·열 0이다. 시선 셀은 각각 정지 포즈다.

[쉬기 → 점프 → 쉬기 연결 GIF](previews/idle-jump-idle.gif)도 보관했다. `animations.json`의 재생 시간은 저장된 GIF에서 읽은 값이며 앱의 현재 재생 속도를 지정하는 설정은 아니다.

## 재제작과 검수 기록

재제작할 때는 상위 기본 PNG와 캐릭터 프롬프트, `source/generation-request.json`의 동작 조건을 함께 사용한다. 원형 고리와 달·별의 위치를 유지하고, 비대칭 표식이 뒤집히지 않도록 좌우 이동을 단순히 반전하지 않는다.

작업별 프롬프트는 완료된 생성 기록의 `revisedPrompt` 원문을 보존했다. 당시 삭제된 `prompts/` 폴더나 호출 인수 전체를 복원한 것은 아니므로, 원래 첨부 이미지 목록이나 도구 설정을 모두 재현한다고 보장하지 않는다.

최종 시트의 SHA-256은 `402c778d07030a6c8a36955548fbad659a9274ad2c9d9e8c0906a37064005637`이다. 제작 당시 구조 검증과 품질 검증, v2 사전 검증을 통과했으며, 일부 중간 시선의 미세한 방향 표현과 프레임 사이 차이는 최종 시각 검수에서 경고를 검토한 뒤 수용했다. 자세한 판단은 `qa/final-visual-qa.json`과 `qa/blind-review-resolution.json`에 남아 있다.

이번 정리에서는 아트워크를 다시 생성하지 않고 최종 파일의 해시, PNG·WebP의 픽셀 일치, 73개 분리 프레임의 픽셀 일치와 미사용 셀의 투명도를 확인했다. 기존 검수 기록은 당시 결과이며, 보고서의 컴퓨터별 절대 경로는 이동 가능한 표기로 정리했다.
