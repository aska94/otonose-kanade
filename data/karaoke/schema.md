# Karaoke Data Schema

## Runtime data

대시보드가 사용하는 정식 데이터는 다음 두 파일입니다.

- `data/karaoke/normalized/broadcasts.json`
- `data/karaoke/normalized/performances.json`

## Broadcast

방송 레코드는 `id`, `title`, `date`, `youtubeUrl`, `broadcastUrl`, `sources`, `status`를 가집니다.

## Performance

공연 레코드는 `id`, `broadcastId`, `date`, `order`, `title`, `normalizedTitle`, `artist`, `timestamp`, `timestampSeconds`, `sourceUrl`, `sources`, `evidence`, `status`를 가집니다.

`broadcastId`로 방송과 공연을 연결합니다. 한 방송은 여러 공연을 포함할 수 있습니다.

## Provenance

원본 URL과 수집 정보는 `data/karaoke/source-metadata/setlist-index.json`에 저장합니다. 원본 HTML은 로컬 전용입니다.
