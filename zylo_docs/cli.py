import uvicorn
import click 

@click.command()
@click.option('--host', default='127.0.0.1', help='서버를 바인딩할 호스트 주소입니다. 기본값은 127.0.0.1 (localhost) 입니다.')
@click.option('--port', default=8001, type=int, help='서버를 바인딩할 포트 번호입니다. 기본값은 8001입니다.')
@click.option('--reload', is_flag=True, help='코드 변경 시 서버를 자동으로 재시작할지 여부입니다 (개발용).')
def main(host: str, port: int, reload: bool):
    print(f"OpenAPI Fetcher 앱을 http://{host}:{port} 에서 시작합니다.")
    print(f"8000번 포트의 OpenAPI JSON을 가져오려 시도합니다.")
    
    # 현재 실행해야하는 파일 경로 지정
    app_import_string = "zylo_docs.main:app"
    uvicorn.run(app_import_string, host=host, port=port, reload=reload, log_level="info")

if __name__ == "__main__":
    main()