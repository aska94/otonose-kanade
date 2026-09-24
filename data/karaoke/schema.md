# Karaoke Data Schema

## Runtime data

정식 원본 데이터는 방송별 파일입니다.

- `data/karaoke/normalized/broadcasts/<video-id>.json`
- `data/karaoke/normalized/index.json`

배포 시 `build_site_data.py`가 임시 aggregate JSON을 생성합니다.

## Broadcast

방송 레코드는 `id`, `title`, `date`, `youtubeUrl`, `broadcastUrl`, `sources`, `status`를 가집니다.

## Performance

공연 레코드는 `id`, `broadcastId`, `date`, `order`, `title`, `normalizedTitle`, `artist`, `timestamp`, `timestampSeconds`, `sourceUrl`, `sources`, `evidence`, `status`를 가집니다.

`broadcastId`로 방송과 공연을 연결합니다. 한 방송은 여러 공연을 포함할 수 있습니다.

## Provenance

원본 URL과 수집 정보는 `data/karaoke/source-metadata/setlist-index.json`에 저장합니다. 원본 HTML은 로컬 전용입니다.
