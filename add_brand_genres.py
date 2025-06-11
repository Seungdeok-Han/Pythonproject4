from app import create_app, db
from app.models import BrandInfo, GenreTag

def main():
    app = create_app()
    with app.app_context():
        genres = {
            'Fender': '록, 블루스, 재즈',
            'Gibson': '록, 재즈, 컨트리',
            'Ibanez': '메탈, 록, 퓨전',
            'PRS': '록, 재즈, 팝',
            'Yamaha': '팝, 재즈, 클래식',
            'Epiphone': '록, 블루스, 팝',
            'Squier': '록, 팝',
            'Cort': '록, 팝, 재즈',
            'ESP': '메탈, 록',
            'Music Man': '록, 펑크, 재즈',
            'Gretsch': '록, 컨트리, 재즈',
            'Martin': '포크, 컨트리, 팝',
            'Taylor': '포크, 팝, 컨트리',
            'Takamine': '포크, 팝, 재즈',
            'Godin': '재즈, 팝, 록',
            'Schecter': '메탈, 록, 하드록',
            'Suhr': '록, 재즈, 퓨전',
            'Danelectro': '록, 블루스, 팝',
            'Jackson': '메탈, 록',
            'Washburn': '록, 블루스, 포크',
            'Samick': '팝, 포크, 록',
            'Aria': '포크, 팝, 록',
            '기타': '록, 팝, 재즈',
        }
        descriptions = {
            'Fender': '미국의 대표적인 일렉기타 브랜드. 밝고 선명한 싱글코일 사운드, 스트라토캐스터/텔레캐스터로 유명.',
            'Gibson': '깊고 따뜻한 험버커 사운드, 레스폴/SG 등 클래식 록에 최적화된 미국 브랜드.',
            'Ibanez': '일본 브랜드, 빠른 연주와 메탈/퓨전에 강한 슈퍼스트랫 스타일, 다양한 시그니처 모델.',
            'PRS': '미국 하이엔드 브랜드, 깔끔하고 밸런스 좋은 사운드, 아름다운 마감과 현대적 디자인.',
            'Yamaha': '일본의 종합 악기 브랜드, 합리적 가격과 안정적 품질, 다양한 장르에 적합.',
            'Epiphone': 'Gibson의 세컨드 브랜드, 합리적 가격에 Gibson 스타일을 제공.',
            'Squier': 'Fender의 세컨드 브랜드, 입문자용으로 인기, Fender 스타일을 저렴하게 경험.',
            'Cort': '한국 브랜드, 가성비와 품질 모두 우수, 다양한 장르와 스타일 지원.',
            'ESP': '메탈/하드록 특화, 강렬한 디자인과 파워풀한 사운드, 시그니처 모델 다수.',
            'Music Man': '미국 하이엔드 브랜드, 뛰어난 연주감과 펑키한 사운드, 스팅레이 베이스로 유명.',
            'Gretsch': '빈티지 감성의 미국 브랜드, 컨트리/재즈/록어빌리 등에 강점.',
            'Martin': '어쿠스틱 기타의 대명사, 깊고 풍부한 울림, 포크/컨트리 필수 브랜드.',
            'Taylor': '현대적 감성의 어쿠스틱 기타, 밝고 선명한 사운드, 뛰어난 플레이어빌리티.',
            'Takamine': '일본 어쿠스틱 전문, 무대용 픽업 시스템 강점, 안정적 사운드.',
            'Godin': '캐나다 브랜드, 일렉/어쿠스틱 하이브리드, 다양한 실험적 모델.',
            'Schecter': '메탈/하드록 특화, 공격적 디자인과 강한 사운드, 합리적 가격.',
            'Suhr': '미국 하이엔드 커스텀, 현대적 슈퍼스트랫, 정교한 마감과 사운드.',
            'Danelectro': '빈티지/개성파 브랜드, 독특한 디자인과 사운드, 블루스/인디에 적합.',
            'Jackson': '메탈/스래시 특화, 빠른 넥과 강렬한 픽업, 익스트림 연주에 최적.',
            'Washburn': '미국 브랜드, 포크/블루스/록 등 다양한 스타일, 합리적 가격.',
            'Samick': '한국 브랜드, 다양한 입문용 모델, 합리적 가격과 무난한 품질.',
            'Aria': '일본 브랜드, 포크/팝/록 등 다양한 장르, 입문자와 중급자 모두에 적합.',
            '기타': '기타 브랜드 또는 직접 입력. 다양한 스타일과 특징.',
        }
        famous_users = {
            'Fender': 'Eric Clapton, Jimi Hendrix, Jeff Beck, John Mayer',
            'Gibson': 'Slash, Jimmy Page, B.B. King, Joe Bonamassa',
            'Ibanez': 'Steve Vai, Joe Satriani, Paul Gilbert',
            'PRS': 'Carlos Santana, Mark Tremonti, John Mayer',
            'Yamaha': 'Mike Stern, Nathan East',
            'Epiphone': 'Noel Gallagher, Gary Clark Jr.',
            'Squier': 'Jack White',
            'Cort': 'Jeff Berlin',
            'ESP': 'Kirk Hammett, James Hetfield',
            'Music Man': 'John Petrucci, Steve Lukather',
            'Gretsch': 'George Harrison, Brian Setzer',
            'Martin': 'Ed Sheeran, John Mayer',
            'Taylor': 'Jason Mraz, Taylor Swift',
            'Takamine': 'Bruce Springsteen',
            'Godin': 'Steve Stevens',
            'Schecter': 'Synyster Gates',
            'Suhr': 'Mateus Asato',
            'Danelectro': 'Jimmy Page',
            'Jackson': 'Marty Friedman',
            'Washburn': 'Nuno Bettencourt',
            'Samick': '',
            'Aria': '',
            '기타': '',
        }
        # BrandInfo에 브랜드가 없으면 추가 및 설명/유명사용자도 함께 저장
        for brand_name in genres.keys():
            brand = BrandInfo.query.filter_by(name=brand_name).first()
            if not brand:
                brand = BrandInfo(
                    name=brand_name,
                    description=descriptions.get(brand_name, ''),
                    famous_users=famous_users.get(brand_name, '')
                )
                db.session.add(brand)
                print(f'브랜드 추가: {brand_name}')
            else:
                updated = False
                if not brand.description:
                    brand.description = descriptions.get(brand_name, '')
                    updated = True
                # famous_users가 None이거나 빈 문자열일 때도 업데이트
                if not brand.famous_users or brand.famous_users.strip() == '':
                    brand.famous_users = famous_users.get(brand_name, '')
                    updated = True
                if updated:
                    print(f'브랜드 정보 보완: {brand_name}')
        db.session.commit()
        brands = BrandInfo.query.all()
        for brand in brands:
            if not GenreTag.query.filter_by(brand=brand.name, model_name="").first():
                g = genres.get(brand.name, '록, 팝, 재즈')
                db.session.add(GenreTag(brand=brand.name, model_name="", genres=g))
                db.session.commit()
                print(f'장르 추가: {brand.name} -> {g}')
            else:
                print(f'이미 존재: {brand.name}')

if __name__ == "__main__":
    main()
