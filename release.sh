set -e

echo "--- 기존 배포 파일 삭제 (dist/) ---"
rm -rf ./dist

echo "--- 버전 올리기 (poetry version patch) ---"
poetry version patch

echo "--- 새로운 버전 빌드 (poetry build) ---"
poetry build

echo "--- PyPI에 업로드 (twine upload) ---"
twine upload --repository pypi dist/*

echo "--- 배포 완료! ---"
